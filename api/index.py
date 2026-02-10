"""
Vercel Serverless Function for BlastConvert
"""
import json
import os

# Demo conversion function
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
// To get real AI-powered conversions, configure a valid API key in Vercel Environment Variables.'''

# Available models
AVAILABLE_MODELS = ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
DEFAULT_MODEL = "moonshot-v1-8k"

def handler(event, context):
    """
    Vercel serverless function handler
    Supports both AWS Lambda (v1) and Vercel (v2) formats
    """
    # Determine request method and path
    http_method = event.get('httpMethod') or event.get('method', 'GET')
    path = event.get('path') or event.get('rawPath', '/')
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle preflight
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    # /models endpoint - GET available models
    if path == '/models' or path.endswith('/models'):
        if http_method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'models': AVAILABLE_MODELS,
                    'default': DEFAULT_MODEL
                })
            }
    
    # /convert endpoint - POST conversion
    if path == '/convert' or path.endswith('/convert'):
        if http_method == 'POST':
            try:
                # Parse body
                body = event.get('body', '{}')
                if isinstance(body, str):
                    body = json.loads(body)
                
                java_code = body.get('java_source_code', '')
                model = body.get('model', DEFAULT_MODEL)
                
                if not java_code:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({
                            'playwright_code': '',
                            'status': 'error',
                            'error_message': 'No Java code provided'
                        })
                    }
                
                # Get conversion (demo mode)
                result = get_mock_conversion(java_code)
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'playwright_code': result,
                        'status': 'success',
                        'error_message': None
                    })
                }
                
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({
                        'playwright_code': '',
                        'status': 'error',
                        'error_message': str(e)
                    })
                }
    
    # /health endpoint
    if path == '/health' or path.endswith('/health'):
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'healthy',
                'version': '2.1.0',
                'demo_mode': True
            })
        }
    
    # Default: not found
    return {
        'statusCode': 404,
        'headers': headers,
        'body': json.dumps({'error': 'Not found', 'path': path})
    }

# FastAPI app for local development
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    app = FastAPI(title="BlastConvert API")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    class ConvertRequest(BaseModel):
        java_source_code: str
        target_flavor: str = "typescript"
        model: str = None
    
    @app.get("/models")
    async def get_models():
        return {"models": AVAILABLE_MODELS, "default": DEFAULT_MODEL}
    
    @app.post("/convert")
    async def convert(request: ConvertRequest):
        result = get_mock_conversion(request.java_source_code)
        return {"playwright_code": result, "status": "success", "error_message": None}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "version": "2.1.0", "demo_mode": True}
        
except ImportError:
    app = None
