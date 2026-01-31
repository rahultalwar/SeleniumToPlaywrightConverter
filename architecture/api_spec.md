# API Specification

## `POST /convert`

**Description**: Accepts Java source code and returns converted Playwright code.

**Request Body** (`application/json`):
```json
{
  "java_source_code": "string (The raw Java Selenium code)",
  "target_flavor": "typescript" (Optional, defaults to typescript)
}
```

**Response Body** (`application/json`):
```json
{
  "playwright_code": "string (The converted TypeScript code)",
  "status": "success" | "error",
  "error_message": "string" (Optional, if status is error)
}
```
