"""
Vercel Serverless Function - GET /models
Returns available AI models
"""
import json

AVAILABLE_MODELS = ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
DEFAULT_MODEL = "moonshot-v1-8k"

def handler(event, context):
    """AWS Lambda / Vercel serverless handler"""
    method = event.get('httpMethod', 'GET')
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {**headers, 'Access-Control-Allow-Methods': 'GET, OPTIONS'},
            'body': json.dumps({'message': 'OK'})
        }
    
    if method == 'GET':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'models': AVAILABLE_MODELS,
                'default': DEFAULT_MODEL
            })
        }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed'})
    }
