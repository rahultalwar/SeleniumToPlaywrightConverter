# Project Constitution

## Data Schemas

### Conversion Payload
```json
{
  "input": {
    "java_source_code": "string",
    "target_flavor": "typescript" 
  },
  "output": {
    "playwright_code": "string",
    "status": "success | error",
    "conversion_notes": [
      {
        "line_number": "integer",
        "severity": "info | warning | error",
        "message": "string"
      }
    ]
  }
}
```

## Behavioral Rules
- **Maintainability First**: Generated code should use readable selectors and Page Object Model where possible.
- **Equivalence**: TestNG assertions must map to Playwright `expect` assertions.
- **UI & File Output**: The system must display the result and save it to disk.

## Architectural Invariants
- 3-Layer Architecture (SOPs, Navigation, Tools)
- Data-First Rule
- Python-based Logic (`tools/`)
- Web-based Interface (HTML/JS)
- **AI Backend**: Local LLM (Ollama) prior to fallback logic.
