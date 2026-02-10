# Findings & Discoveries

## Constraints
- **North Star**: Develop a Selenium (Java) to Playwright (JS/TS) converter.
- **Integrations**: specific focus on TestNG/Selenium Java -> Playwright JS/TS.
- **Source of Truth**: User input via a Web UI (Java code snippet).
- **Delivery Payload**: Display on UI and save to a new directory.
- **Behavioral Rules**: Convert everything, Prioritize maintainability over speed.
- **Model**: Use Moonshot AI (Kimi) API (cloud-based LLM).

## Migration from Ollama to Moonshot AI

### Changes Made:
1. **Backend (`tools/converter.py`)**:
   - Replaced Ollama local API calls with Moonshot AI cloud API
   - Uses OpenAI-compatible API format
   - Reads API key from environment variable `K2_API_KEY`
   - Default endpoint: `https://api.moonshot.cn/v1/chat/completions`
   - Default model: `moonshot-v1-8k`
   - Added `AVAILABLE_MODELS` list for UI consumption

2. **Backend (`tools/app.py`)**:
   - Added `AVAILABLE_MODELS` constant with all Moonshot models
   - `/models` endpoint returns available models and default model
   - Removed Ollama-specific model discovery

3. **Backend (`tools/verify_env.py`)**:
   - Replaced Ollama connectivity check with API key verification
   - Creates `.env` template file if not exists

4. **Frontend (`ui/index.html`)**:
   - Added Moonshot AI branding badge
   - Replaced static model info with dynamic dropdown selector
   - Added model selection with all 3 Moonshot variants

5. **Frontend (`ui/script.js`)**:
   - `fetchModels()` fetches available models from `/models` endpoint
   - Dynamically populates dropdown with server-provided models
   - Sends selected model to backend during conversion
   - Shows model context info in status messages
   - Added `MODEL_INFO` object for display names and descriptions

6. **Frontend (`ui/style.css`)**:
   - Added styling for Moonshot badge (blue gradient)
   - Enhanced model selector styling with hover effects
   - Added `.model-help` class for context window hints

7. **Configuration (`.env.example`)**:
   - Created template for Moonshot API configuration

## API Configuration
- Endpoint: `https://api.moonshot.cn/v1/chat/completions`
- Authentication: Bearer token via `Authorization` header
- Models Available:
  - `moonshot-v1-8k` - 8K context window (default)
  - `moonshot-v1-32k` - 32K context window
  - `moonshot-v1-128k` - 128K context window
- Format: OpenAI-compatible chat completions API

## UI Model Selection Feature
Users can now select from available models via a dropdown in the control center:
- Dropdown is populated dynamically from `/models` endpoint
- Each option shows model name and context window size
- Selected model is passed to backend during conversion
- Status messages reflect the currently selected model
