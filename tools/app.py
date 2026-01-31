from fastapi import FastAPI, HTTPException
import requests

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
try:
    from tools.converter import convert_code
except ImportError:
    from converter import convert_code


app = FastAPI(title="Selenium to Playwright Converter")

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Models
class ConvertRequest(BaseModel):
    java_source_code: str
    target_flavor: str = "typescript"
    model: str = "llama3"

class ConvertResponse(BaseModel):
    playwright_code: str
    status: str
    error_message: str = None

@app.get("/models")
async def get_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        data = response.json()
        models = [m["name"] for m in data.get("models", [])]
        return {"models": models}
    except Exception as e:
        # Fallback if Ollama is down or error
        return {"models": ["llama3", "mistral", "codellama"], "error": str(e)}

@app.post("/convert", response_model=ConvertResponse)
async def convert(request: ConvertRequest):
    try:
        result = convert_code(request.java_source_code, request.model)
        if result.startswith("Error:"):
            return ConvertResponse(
                playwright_code="",
                status="error",
                error_message=result
            )
        return ConvertResponse(playwright_code=result, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve UI
# Assumes app.py is in /tools/, so ui is in ../ui/
ui_path = os.path.join(os.path.dirname(__file__), "../ui")
if os.path.exists(ui_path):
    app.mount("/", StaticFiles(directory=ui_path, html=True), name="ui")
else:
    print(f"Warning: UI path {ui_path} does not exist.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
