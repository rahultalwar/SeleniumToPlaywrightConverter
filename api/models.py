import json

AVAILABLE_MODELS = ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
DEFAULT_MODEL = "moonshot-v1-8k"

def Handler(request):
    """Vercel Python Serverless Function Handler"""
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS (CORS preflight)
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    # Handle GET
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'models': AVAILABLE_MODELS,
            'default': DEFAULT_MODEL
        })
    }

# Backwards compatibility - Vercel looks for 'handler' or 'Handler'
handler = Handler
