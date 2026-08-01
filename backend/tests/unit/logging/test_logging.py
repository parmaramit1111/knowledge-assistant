import logging
from unittest.mock import MagicMock, patch
from app.core.logging import (
    request_id_context,
    RequestIdFilter,
    setup_logging,
    get_logger,
)

def test_filter_injects_request_id_when_present():
    """Ensure the filter grabs a valid string ID from ContextVar."""
    log_filter = RequestIdFilter()
    mock_record = MagicMock(spec=logging.LogRecord)

    # Simulate an active context ID
    token = request_id_context.set("test-12345")
    try:
        result = log_filter.filter(mock_record)
        assert result is True
        assert mock_record.request_id == "test-12345"
    finally:
        request_id_context.reset(token)

# --- 1. Test the Logging Filter Behavior ---

def test_filter_injects_request_id_when_present():
    """Ensure the filter grabs a valid string ID from ContextVar."""
    log_filter = RequestIdFilter()
    mock_record = MagicMock(spec=logging.LogRecord)

    # Simulate an active context ID
    token = request_id_context.set("test-12345")
    try:
        result = log_filter.filter(mock_record)
        assert result is True
        assert mock_record.request_id == "test-12345"
    finally:
        request_id_context.reset(token)

def test_filter_injects_dash_when_request_id_missing():
    """Ensure the filter gracefully falls back to a dash placeholder if empty."""
    log_filter = RequestIdFilter()
    mock_record = MagicMock(spec=logging.LogRecord)

    # Explicitly verify the default fallback state
    request_id_context.set(None)

    result = log_filter.filter(mock_record)
    assert result is True
    assert mock_record.request_id == "-"

def test_get_logging():
    """Ensure we get a proper Logger instance back from the helper."""
    logger = get_logger("test_application_scope")

    assert isinstance(logger, logging.Logger)

# --- 2. Test the Setup Configuration and Formatting ---

def test_setup_logging_configures_formatter_and_handlers(capsys):
    """Ensure setup properly binds handlers and implements the log format."""
    # Run setup explicitly targeting standard DEBUG/INFO output
    setup_logging(level="INFO")

    logger = get_logger("test_application_scope")

    # Set context ID to track it inside the intercepted string output
    token = request_id_context.set("log-track-id")
    try:
        logger.info("Hello world validation message")
    finally:
        request_id_context.reset(token)

    # Read the captured stdout stream
    captured = capsys.readouterr()

    # Verify the structure matches: %(asctime)s | %(levelname)s | %(request_id)s | %(name)s | %(message)s
    assert "INFO" in captured.out
    assert "log-track-id" in captured.out
    assert "test_application_scope" in captured.out
    assert "Hello world validation message" in captured.out
    assert " | " in captured.out


# --- 3. Test Library Suppression ---

@patch("app.core.config.settings")
def test_setup_logging_quiets_noisy_libraries(mock_settings):
    """Ensure standard ecosystem dependencies are actively muted to clean logs."""
    mock_settings.log_level = "INFO"

    setup_logging()

    # Verify that targeted noisy library instances reflect custom levels
    assert logging.getLogger("uvicorn.access").level == logging.WARNING
    assert logging.getLogger("httpx").level == logging.WARNING
    assert logging.getLogger("httpcore").level == logging.WARNING
    assert logging.getLogger("uvicorn.error").level == logging.INFO
