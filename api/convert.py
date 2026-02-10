import json

def get_mock_conversion(java_code: str) -> str:
    return '''import { test, expect } from '@playwright/test';

test('converted test', async ({ page }) => {
    await page.goto('https://example.com');
    await page.locator('#username').fill('user');
    await page.locator('#password').fill('pass');
    await page.locator('#submit').click();
    await expect(page).toHaveTitle('Dashboard');
});

// NOTE: DEMO conversion. Add API key for real conversions.'''

def Handler(request):
    """Vercel Python Serverless Function Handler"""
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    # Handle OPTIONS (CORS preflight)
    if request.get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    # Handle POST
    try:
        body_str = request.get('body', '{}')
        if isinstance(body_str, str):
            body = json.loads(body_str)
        else:
            body = body_str
        
        java_code = body.get('java_source_code', '')
        
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

# Backwards compatibility
handler = Handler
