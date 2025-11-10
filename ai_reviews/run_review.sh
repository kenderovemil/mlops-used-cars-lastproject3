#!/bin/bash
#
# Script to run the Azure ML jobs review
# This will install dependencies and execute the review script
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Installing dependencies..."
pip install -q -r "$SCRIPT_DIR/requirements.txt"

echo ""
echo "🚀 Running Azure ML jobs review..."
python3 "$SCRIPT_DIR/review_jobs.py"

echo ""
echo "✅ Done! Check jobs_review.md for results."
