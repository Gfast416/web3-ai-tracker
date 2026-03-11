#!/bin/bash
# =============================================
# Web3 AI Tracker — Runner Script
# Usage: bash scripts/run.sh
# =============================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "🤖 Web3 AI Tracker"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Load .env if exists
if [ -f "config/.env" ]; then
  echo "✅ Loading config/.env"
  export $(grep -v '^#' config/.env | xargs)
else
  echo "⚠️  config/.env not found — copy from config/.env.example first"
  echo "   cp config/.env.example config/.env"
  exit 1
fi

# Check required env vars
REQUIRED_VARS=("ETHERSCAN_API_KEY" "ANTHROPIC_API_KEY" "TELEGRAM_BOT_TOKEN" "TELEGRAM_CHAT_ID")
MISSING=0
for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR}" ]; then
    echo "❌ Missing: $VAR"
    MISSING=1
  fi
done

if [ "$MISSING" -eq 1 ]; then
  echo ""
  echo "Fill in all required keys in config/.env and try again."
  exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
  echo "❌ Python3 not found. Please install Python 3.11+"
  exit 1
fi

# Install dependencies if needed
if [ ! -d ".venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting tracker..."
echo ""

python3 src/main.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Done."