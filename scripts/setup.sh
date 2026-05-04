#!/usr/bin/env bash
set -euo pipefail

echo "=== Brand Studio Forge — Setup ==="

# Check Python
python3 --version || { echo "ERROR: python3 not found"; exit 1; }

# Install Python deps
pip install -r "$(dirname "$0")/../requirements.txt"

# Install Playwright browsers
playwright install chromium

echo "=== Setup complete ==="
