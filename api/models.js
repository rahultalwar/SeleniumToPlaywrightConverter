// Node.js Serverless Function - GET /models
// Returns available AI models

const AVAILABLE_MODELS = ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"];
const DEFAULT_MODEL = "moonshot-v1-8k";

module.exports = (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow GET
  if (req.method !== 'GET') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  res.status(200).json({
    models: AVAILABLE_MODELS,
    default: DEFAULT_MODEL
  });
};
