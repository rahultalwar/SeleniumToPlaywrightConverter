import json
from http.server import BaseHTTPRequestHandler

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

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
            java_code = data.get('java_source_code', '')
            
            if not java_code:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'playwright_code': '',
                    'status': 'error',
                    'error_message': 'No Java code provided'
                }).encode())
                return
            
            result = get_mock_conversion(java_code)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'playwright_code': result,
                'status': 'success',
                'error_message': None
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'playwright_code': '',
                'status': 'error',
                'error_message': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
