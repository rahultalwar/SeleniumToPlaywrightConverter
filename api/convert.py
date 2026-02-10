"""
Vercel Serverless Function - POST /convert
Converts Java Selenium code to Playwright TypeScript
"""
import json

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

def handler(event, context):
    """AWS Lambda / Vercel serverless handler"""
    method = event.get('httpMethod', 'POST')
    
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {**headers, 'Access-Control-Allow-Methods': 'POST, OPTIONS'},
            'body': json.dumps({'message': 'OK'})
        }
    
    if method == 'POST':
        try:
            body_str = event.get('body', '{}')
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
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed'})
    }
