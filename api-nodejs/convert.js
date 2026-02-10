// Node.js Serverless Function - POST /convert
// Converts Java Selenium code to Playwright TypeScript

const getMockConversion = (javaCode) => {
  return `import { test, expect } from '@playwright/test';

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
// To get real AI-powered conversions, configure a valid API key in Vercel Environment Variables.`;
};

module.exports = (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    const { java_source_code, model } = req.body;

    if (!java_source_code) {
      res.status(400).json({
        playwright_code: '',
        status: 'error',
        error_message: 'No Java code provided'
      });
      return;
    }

    const result = getMockConversion(java_source_code);

    res.status(200).json({
      playwright_code: result,
      status: 'success',
      error_message: null
    });
  } catch (error) {
    console.error('Conversion error:', error);
    res.status(500).json({
      playwright_code: '',
      status: 'error',
      error_message: error.message
    });
  }
};
