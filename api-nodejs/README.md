# Node.js API for Vercel

This is an alternative Node.js implementation of the API endpoints.
Node.js functions on Vercel are more reliable and have better cold-start performance than Python.

## Switching to Node.js API

To use the Node.js version instead of Python:

```bash
# Replace vercel.json with the Node.js version
cp vercel-nodejs.json vercel.json

# Commit and push
git add vercel.json api-nodejs/
git commit -m "Switch to Node.js API"
git push
```

Then redeploy on Vercel.

## Files

- `convert.js` - POST /convert endpoint
- `models.js` - GET /models endpoint
- `health.js` - GET /health endpoint

## Why Node.js?

1. **Better Cold Start**: Node.js functions start faster on Vercel
2. **Native Support**: Vercel is optimized for Node.js
3. **Simpler**: No Python runtime to configure
4. **Better Debugging**: More straightforward error messages
