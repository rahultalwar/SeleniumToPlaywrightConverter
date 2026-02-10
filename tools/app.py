from fastapi import FastAPI, HTTPException
import requests

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
try:
    from tools.converter import convert_code, K2_MODEL
except ImportError:
    from converter import convert_code, K2_MODEL


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
    model: str = None  # Optional, uses K2_MODEL by default

class ConvertResponse(BaseModel):
    playwright_code: str
    status: str
    error_message: str = None

# Available Moonshot models
AVAILABLE_MODELS = [
    "moonshot-v1-8k",
    "moonshot-v1-32k", 
    "moonshot-v1-128k"
]

@app.get("/models")
async def get_models():
    """Returns available Moonshot models."""
    return {"models": AVAILABLE_MODELS, "default": K2_MODEL}

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
