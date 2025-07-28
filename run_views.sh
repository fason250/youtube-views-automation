#!/bin/bash

# YouTube Views System Launcher
# 🎯 Easy commands for generating views

echo "🚀 YOUTUBE VIEWS SYSTEM"
echo "======================="
echo ""

# Check if URL provided
if [ -z "$1" ]; then
    echo "❌ Please provide YouTube URL"
    echo ""
    echo "Usage examples:"
    echo "  ./run_views.sh 'https://youtube.com/shorts/abc123' 50    # 50 views"
    echo "  ./run_views.sh 'https://youtube.com/watch?v=abc123' 100  # 100 views"
    echo "  ./run_views.sh 'https://youtube.com/shorts/abc123' 10    # 10 views (test)"
    echo ""
    exit 1
fi

URL="$1"
VIEWS="${2:-50}"  # Default to 50 views

echo "📺 URL: $URL"
echo "🎯 Views: $VIEWS"
echo "🧅 Using TOR network for IP diversity"
echo "👤 Manual consent required (you'll click once)"
echo ""

# Run the system
python3 youtubeViews.py "$URL" "$VIEWS" --concurrent 5 --time 90
