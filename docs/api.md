# API Guidelines

## Base URL

/api/v1

## Authentication

(Currently Not Implemented)

## Standard Response

{
"code": "...",
"success": true,
"message": "...",
"result": {}
}

## Error Response

...

## Upload API

POST /documents/upload

Supported Types

- PDF
- DOCX
- TXT
- HTML
- Markdown

## Health API

GET /health
