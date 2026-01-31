#!/bin/bash

# Configuration
PORT=8000
HOST="0.0.0.0"

echo "🚀 Starting BlastConvert Server..."
echo "📍 Access UI at http://localhost:$PORT"

# Ensure dependencies are available (in case they were installed with --user)
export PATH=$PATH:$HOME/.local/bin

python3 tools/app.py
