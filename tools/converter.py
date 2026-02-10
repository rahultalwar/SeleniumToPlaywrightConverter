import requests
import json
import os

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# K2 API Configuration
K2_API_URL = os.getenv("K2_API_URL", "https://api.moonshot.cn/v1/chat/completions")
K2_API_KEY = os.getenv("K2_API_KEY", "")
K2_MODEL = os.getenv("K2_MODEL", "moonshot-v1-8k")

# Demo mode - returns mock conversion when API key is invalid
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# Available models for UI selection
AVAILABLE_MODELS = [
    "moonshot-v1-8k",
    "moonshot-v1-32k",
    "moonshot-v1-128k"
]

PROMPT_FILE = os.path.join(os.path.dirname(__file__), "../architecture/conversion_prompt.md")

def load_system_prompt():
    if not os.path.exists(PROMPT_FILE):
        return "You are a code converter. Convert Java Selenium to Playwright TypeScript."
    with open(PROMPT_FILE, "r") as f:
        return f.read()

def get_mock_conversion(java_code: str) -> str:
    """Returns a mock Playwright conversion for demo purposes."""
    return '''import { test, expect } from '@playwright/test';

test('converted test', async ({ page }) => {
    // Navigate to the page
    await page.goto('https://example.com');
    
    // Fill in form fields
    await page.locator('#username').fill('user');
    await page.locator('#password').fill('pass');
    
    // Click submit button
    await page.locator('#submit').click();
    
    // Verify page title
    await expect(page).toHaveTitle('Dashboard');
});

// NOTE: This is a DEMO conversion.
// To get real AI-powered conversions, please configure a valid API key in .env'''

def convert_code(java_code: str, model: str = None) -> str:
    """
    Sends the Java code to Moonshot API and returns the Playwright TS code.
    If DEMO_MODE is enabled or API key is missing, returns mock conversion.
    """
    # Use provided model or default
    selected_model = model or K2_MODEL
    
    # Demo mode - return mock conversion
    if DEMO_MODE or not K2_API_KEY or K2_API_KEY == "your_moonshot_api_key_here":
        print("⚠️  DEMO MODE: Returning mock conversion (no API key configured)")
        return get_mock_conversion(java_code)
    
    system_prompt = load_system_prompt()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {K2_API_KEY}"
    }
    
    payload = {
        "model": selected_model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Convert the following Java Selenium code to Playwright TypeScript:\n\n{java_code}"
            }
        ],
        "temperature": 0.2,  # Low temp for deterministic code
        "max_tokens": 4096
    }
    
    try:
        print(f"Sending request to Moonshot API (model: {selected_model})...")
        response = requests.post(K2_API_URL, headers=headers, json=payload, timeout=120)
        
        # If 401, fall back to demo mode
        if response.status_code == 401:
            print("⚠️  API key invalid (401). Falling back to DEMO MODE.")
            return get_mock_conversion(java_code)
            
        response.raise_for_status()
        data = response.json()
        
        # Extract response from Moonshot API format (OpenAI compatible)
        if "choices" in data and len(data["choices"]) > 0:
            message = data["choices"][0].get("message", {})
            return message.get("content", "").strip()
        else:
            return "Error: Unexpected response format from API."
            
    except requests.exceptions.Timeout:
        print("Error calling API: Request timed out")
        return "Error: Request to API timed out. Please try again."
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        # Fall back to demo mode on error
        print("⚠️  API error. Falling back to DEMO MODE.")
        return get_mock_conversion(java_code)
