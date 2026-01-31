import requests
import json
import os

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # Default, can be overridden
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "../architecture/conversion_prompt.md")

def load_system_prompt():
    if not os.path.exists(PROMPT_FILE):
        return "You are a code converter. Convert Java Selenium to Playwright TypeScript."
    with open(PROMPT_FILE, "r") as f:
        return f.read()

def convert_code(java_code: str, model: str = "llama3") -> str:
    """
    Sends the Java code to Ollama and returns the Playwright TS code.
    """
    system_prompt = load_system_prompt()
    full_prompt = f"{system_prompt}\n\nINPUT:\n{java_code}\n\nOUTPUT:"
    
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.2 # Low temp for deterministic code
        }
    }
    
    try:
        print(f"Sending request to Ollama ({model})...")
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return f"Error: Failed to communicate with Ollama. {e}"
