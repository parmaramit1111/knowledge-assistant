import logging
import sys
from typing import Optional
from contextvars import ContextVar
from app.core.config import settings

# Context variable so every log can automatically carry the request_id
request_id_context: ContextVar[Optional[str]] = ContextVar("request_id", default=None)

class RequestIdFilter(logging.Filter):
    """Injects request_id into every log record if it exists."""

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add request_id to every log record.

        Args:
            record: The log record to filter.

        Returns:
            True
        """

        record.request_id = request_id_context.get() or "-"
        return True


def setup_logging(level: str | None = None) -> None:
    """
    Configure the logging module.

    This should be called once at application startup.
    It's important that this is called *after* the settings are initialized,
    and *before* any logging occurs.

    Args:
        level: The log level to use for the root logger.
    """
    level = level or settings.log_level

    log_level = getattr(logging, level.upper(), logging.INFO)

    # Clear any existing handlers (important when running under uvicorn --reload)
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(request_id)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(RequestIdFilter())

    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Quiet noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.
    Convenience helper – use this everywhere instead of logging.getLogger.

    Args:
        name: The name of the logger to get.

    Returns:
        A logger with the given name.
    """
    return logging.getLogger(name)