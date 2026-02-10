export const config = {
  runtime: 'edge',
};

const SYSTEM_PROMPT = `You are a code converter expert. Convert Java Selenium WebDriver code to Playwright TypeScript.

Rules:
1. Convert TestNG @Test annotations to Playwright test()
2. Replace WebDriver with Playwright page object
3. Use Playwright's locator() instead of findElement()
4. Use async/await for all Playwright operations
5. Import { test, expect } from '@playwright/test'
6. Remove WebDriver setup/teardown - use Playwright's built-in fixtures
7. Convert Assert.assertEquals() to expect().toBe() or expect().toEqual()

Output only the TypeScript code, no explanations.`;

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

    // Call Groq API
    const apiKey = process.env.GROQ_API_KEY;
    
    if (!apiKey) {
      return new Response(
        JSON.stringify({
          playwright_code: '',
          status: 'error',
          error_message: 'API key not configured',
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

    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'llama-3.1-8b-instant',
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          { role: 'user', content: `Convert this Java Selenium code to Playwright TypeScript:\n\n${java_code}` }
        ],
        temperature: 0.2,
        max_tokens: 4096,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('Groq API error:', error);
      return new Response(
        JSON.stringify({
          playwright_code: '',
          status: 'error',
          error_message: `AI service error: ${response.status}`,
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

    const data = await response.json();
    const convertedCode = data.choices?.[0]?.message?.content || '';

    return new Response(
      JSON.stringify({
        playwright_code: convertedCode,
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
    console.error('Conversion error:', error);
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
