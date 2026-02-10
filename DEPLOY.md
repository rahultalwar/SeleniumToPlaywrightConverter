# Deploy to Vercel

## Option 1: Deploy via Vercel CLI (Recommended)

### Step 1: Install Vercel CLI
```bash
npm i -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
cd /path/to/SeleniumToPlaywrightConverter
vercel --prod
```

### Step 4: Set Environment Variables (Optional)
If you have a valid API key:
```bash
vercel env add K2_API_KEY
vercel env add DEMO_MODE false
```

## Option 2: Deploy via Git Integration

1. Push this code to a GitHub repository
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. Click "Deploy"

## Option 3: Manual Upload

1. Go to https://vercel.com/new
2. Select "Upload" option
3. Zip the project folder (excluding .git and node_modules)
4. Upload the zip file
5. Deploy

## Project Structure for Vercel

```
SeleniumToPlaywrightConverter/
├── api/
│   └── index.py          # Serverless API functions
├── public/
│   ├── index.html        # Static UI
│   ├── script.js         # Frontend JavaScript
│   └── style.css         # Styles
├── requirements.txt      # Python dependencies
└── vercel.json          # Vercel configuration
```

## API Endpoints

After deployment, your app will have these endpoints:

- `GET /models` - List available models
- `POST /convert` - Convert Java code to Playwright
- `GET /health` - Health check

## Demo Mode

By default, the app runs in DEMO MODE (no API calls).
To enable real AI conversions:

1. Get an API key from https://platform.moonshot.cn/
2. Add it to Vercel Environment Variables:
   - Name: `K2_API_KEY`
   - Value: `your_api_key_here`
3. Set `DEMO_MODE` to `false`
4. Redeploy

## Troubleshooting

### 404 Errors
- Make sure `vercel.json` routes are configured correctly
- Check that files are in the correct folders (`api/` and `public/`)

### API Not Working
- Check Vercel Function Logs in the dashboard
- Ensure `requirements.txt` has all dependencies

### CORS Errors
- The API includes CORS headers by default
- If issues persist, check browser console for details
