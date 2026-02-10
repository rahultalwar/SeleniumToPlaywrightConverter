"""
Vercel Serverless Function - GET /health
Health check endpoint
"""
import json

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
                'status': 'healthy',
                'version': '2.1.0',
                'demo_mode': True
            })
        }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed'})
    }
