#!/bin/bash

echo "🔧 Starting precise fix for market data duplication..."

# Create backup
cp src/static/index.html src/static/index.html.backup.$(date +%Y%m%d_%H%M%S)
echo "✅ Backup created"

# Create a temporary file to work with
cp src/static/index.html temp_index.html

# Use Python to precisely remove the problematic script block
python3 << 'PYTHON_EOF'
import re

# Read the HTML file
with open('temp_index.html', 'r') as f:
    content = f.read()

# Define the exact pattern to match the problematic script
pattern = r'<script[^>]*>\s*function loadMarketData\(\).*?</script>'

# Remove the problematic script (using DOTALL flag to match across lines)
cleaned_content = re.sub(pattern, '', content, flags=re.DOTALL)

# Write the cleaned content back
with open('temp_index.html', 'w') as f:
    f.write(cleaned_content)

print("✅ Problematic script removed")
PYTHON_EOF

# Replace the original file with the cleaned version
mv temp_index.html src/static/index.html

echo "✅ HTML file updated"

# Deploy the fix
git add .
git commit -m "Remove problematic loadMarketData script causing duplication"
git push

echo "🎉 Fix deployed! The duplication should now be resolved."
