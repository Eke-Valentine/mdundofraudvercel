#!/bin/bash

# Mdundo Fraud Detection - Setup Script
# Helps with local development setup

set -e

echo "🚀 Mdundo Fraud Detection - Local Setup"
echo "========================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo ""
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
    echo "  Virtual environment created"
fi

# Activate venv
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate
echo "  Virtual environment activated"

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "  Dependencies installed"

# Check for .env.local
echo ""
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found"
    cp .env.example .env.local
    echo "  Created .env.local from template"
    echo "  ⚠️  IMPORTANT: Edit .env.local with your API credentials:"
    echo "     - SPOTIFY_TOKEN: Get from https://developer.spotify.com/dashboard"
    echo "     - SLACK_WEBHOOK: Create at https://api.slack.com/apps"
else
    echo "✓ .env.local found"
fi

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.local with your API credentials"
echo "2. Run: python api/functions/fraud_daily.py"
echo "3. Test: python -c \"from lib.fraud_detector import MdundoFraudDetector; print('OK')\""
echo ""
echo "To activate venv in future: source venv/bin/activate"
echo ""
