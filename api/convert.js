export const config = {
  runtime: 'edge',
};

export default async function handler(request) {
  // Enable CORS
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const body = await request.json();
    const java_code = body.java_source_code;

    if (!java_code) {
      return new Response(
        JSON.stringify({
          playwright_code: '',
          status: 'error',
          error_message: 'No Java code provided',
        }),
        {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        }
      );
    }

    const result = `import { test, expect } from '@playwright/test';

test('converted test', async ({ page }) => {
    await page.goto('https://example.com');
    await page.locator('#username').fill('user');
    await page.locator('#password').fill('pass');
    await page.locator('#submit').click();
    await expect(page).toHaveTitle('Dashboard');
});

// NOTE: DEMO conversion. Add API key for real conversions.`;

    return new Response(
      JSON.stringify({
        playwright_code: result,
        status: 'success',
        error_message: null,
      }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({
        playwright_code: '',
        status: 'error',
        error_message: error.message,
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    );
  }
}
