#!/bin/bash

# CTF Terminal - Production PyPI Upload
# Run this script when ready to upload

echo "🚀 Uploading CTF Terminal to Production PyPI"
echo "============================================="
echo ""
echo "📦 Packages to upload:"
ls -lh dist/

echo ""
echo "⚠️  You will be prompted for:"
echo "   - Username: Your PyPI username"
echo "   - Password: Your PyPI password or API token"
echo ""
echo "💡 Get an API token from: https://pypi.org/manage/account/token/"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

cd /home/vision2030/Desktop/ctf

echo ""
echo "Uploading..."
twine upload dist/*

echo ""
echo "✅ Upload complete!"
echo ""
echo "Test installation with:"
echo "  pip install ctf-term"
echo ""
echo "Verify at: https://pypi.org/project/ctf-term/"

