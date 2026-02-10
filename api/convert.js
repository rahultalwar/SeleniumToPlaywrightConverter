module.exports = (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { java_source_code, model } = req.body;

    if (!java_source_code) {
      return res.status(400).json({
        playwright_code: '',
        status: 'error',
        error_message: 'No Java code provided'
      });
    }

    // Demo conversion
    const result = `import { test, expect } from '@playwright/test';

test('converted test', async ({ page }) => {
    await page.goto('https://example.com');
    await page.locator('#username').fill('user');
    await page.locator('#password').fill('pass');
    await page.locator('#submit').click();
    await expect(page).toHaveTitle('Dashboard');
});

// NOTE: DEMO conversion. Add API key for real conversions.`;

    return res.status(200).json({
      playwright_code: result,
      status: 'success',
      error_message: null
    });
  } catch (error) {
    console.error('Conversion error:', error);
    return res.status(500).json({
      playwright_code: '',
      status: 'error',
      error_message: error.message
    });
  }
};
