#!/bin/bash

# CTF Terminal - PyPI Upload Script
# Created by Sherin Joseph Roy

echo "🚀 CTF Terminal - PyPI Upload Helper"
echo "====================================="
echo ""

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "⚠️  Twine not found. Installing..."
    pip install twine --break-system-packages
fi

echo "📦 Built packages:"
ls -lh dist/

echo ""
echo "📋 Upload Options:"
echo "1. Upload to TestPyPI (recommended for first upload)"
echo "2. Upload to Production PyPI"
echo ""
read -p "Choose option (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "🧪 Uploading to TestPyPI..."
        echo "You'll need a TestPyPI account: https://test.pypi.org/account/register/"
        echo ""
        twine upload --repository testpypi dist/*
        echo ""
        echo "✅ Uploaded to TestPyPI!"
        echo "Test installation with:"
        echo "  pip install --index-url https://test.pypi.org/simple/ ctf-term"
        ;;
    2)
        echo ""
        echo "⚠️  You are about to upload to Production PyPI!"
        echo "Make sure you have:"
        echo "  - PyPI account: https://pypi.org/account/register/"
        echo "  - Twine credentials configured"
        echo ""
        read -p "Continue? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            echo ""
            echo "🚀 Uploading to PyPI..."
            twine upload dist/*
            echo ""
            echo "✅ Uploaded to PyPI!"
            echo "Install with: pip install ctf-term"
        else
            echo "❌ Upload cancelled"
        fi
        ;;
    *)
        echo "❌ Invalid option"
        ;;
esac

echo ""
echo "📚 Documentation: See DEPLOYMENT.md for details"

