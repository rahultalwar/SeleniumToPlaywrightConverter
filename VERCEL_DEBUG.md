# Vercel Deployment Debugging Guide

## 🔍 How to Check Vercel Logs

### Method 1: Vercel Dashboard (Easiest)

1. Go to https://vercel.com/dashboard
2. Click on your project: `selenium-to-playwright-converter`
3. Click on the latest deployment
4. Click **"View Logs"** button
5. Filter by:
   - **Functions** - See API endpoint logs
   - **Static** - See static file requests
   - **Errors** - See only error messages

### Method 2: Vercel CLI

```bash
# Install Vercel CLI if not already
npm i -g vercel

# Login
vercel login

# View logs in real-time
vercel logs selenium-to-playwright-converter --all

# View only error logs
vercel logs selenium-to-playwright-converter --errors
```

### Method 3: Browser DevTools

1. Open your deployed URL in browser
2. Press **F12** to open DevTools
3. Go to **Network** tab
4. Try to convert some code
5. Look for failed requests (red)
6. Click on failed request to see details

## 🚨 Common Errors & Solutions

### Error: "404 Not Found" on API endpoints

**Cause**: Routes not configured correctly

**Solution**:
- Check `vercel.json` has correct routes
- Make sure API files exist in `api/` or `api-nodejs/` folder
- Redeploy after fixing

### Error: "502 Bad Gateway"

**Cause**: Serverless function crashed

**Solution**:
- Check function logs in Vercel dashboard
- Look for Python/Node.js syntax errors
- Make sure handler function is exported correctly

### Error: "CORS policy" error in browser

**Cause**: Missing CORS headers

**Solution**:
- Check `vercel.json` has headers configuration
- Make sure API returns CORS headers in response

### Error: "Function invocation failed"

**Cause**: Runtime error in function

**Solution**:
- Check function logs for stack trace
- Test locally with `vercel dev`

## 🔧 Quick Fixes to Try

### 1. Redeploy

Sometimes a fresh deploy fixes issues:
```bash
vercel --prod
```

Or use Vercel Dashboard → Redeploy

### 2. Switch Between Python and Node.js

**To use Node.js (Recommended):**
```bash
cp vercel-nodejs.json vercel.json
git add vercel.json
git commit -m "Switch to Node.js"
git push
```

**To use Python:**
```bash
git checkout HEAD -- vercel.json  # Restore Python vercel.json
git commit -m "Switch to Python"
git push
```

### 3. Check Environment Variables

In Vercel Dashboard:
1. Go to Project Settings
2. Click **Environment Variables**
3. Make sure these are set:
   - `K2_API_URL` = `https://api.moonshot.cn/v1/chat/completions`
   - `K2_MODEL` = `moonshot-v1-8k`
   - `DEMO_MODE` = `true`

### 4. Test Locally First

```bash
# Install Vercel CLI
npm i -g vercel

# Run local dev server
vercel dev

# This simulates Vercel environment locally
```

## 📊 Current Deployment Status

**Repository**: https://github.com/rahultalwar/SeleniumToPlaywrightConverter

**Current Configuration**:
- ✅ Using Node.js API (more reliable)
- ✅ CORS headers configured
- ✅ Retry mechanism in frontend
- ✅ Demo mode enabled

**To Deploy**:
```bash
# Push latest changes
git push origin main

# Or deploy via CLI
vercel --prod
```

## 🆘 Getting Help

If issues persist:

1. **Check Vercel Status**: https://www.vercel-status.com/
2. **Vercel Docs**: https://vercel.com/docs
3. **Serverless Functions**: https://vercel.com/docs/concepts/functions/serverless-functions
4. **Open an Issue**: Create GitHub issue with logs

## 📋 Debug Checklist

- [ ] Checked Vercel function logs
- [ ] Checked browser console for errors
- [ ] Verified environment variables are set
- [ ] Tested locally with `vercel dev`
- [ ] Tried redeploying
- [ ] Checked CORS headers in response
- [ ] Verified API files exist in correct folder
