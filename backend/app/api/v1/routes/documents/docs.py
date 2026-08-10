"""
OpenAPI documentation constants for Document endpoints.
"""

# Tags
DOCUMENTS_TAG = "Documents"

# Upload
UPLOAD_SUMMARY = "Upload a PDF document"

UPLOAD_DESCRIPTION = """
Upload a PDF document to the Knowledge Assistant.

The uploaded document is validated and stored locally.

Document parsing, chunking, embedding generation, and indexing
are performed in later processing stages.
"""

UPLOAD_SUCCESS_DESCRIPTION = "Document uploaded successfully."