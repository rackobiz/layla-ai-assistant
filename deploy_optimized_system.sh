#!/bin/bash

# Optimized Dual Assistant System Deployment Script
# This script deploys the performance-optimized version while preserving all enhanced features

echo "🚀 Deploying Optimized Dual Assistant System..."
echo "================================================"

# Create backup of current files
echo "📦 Creating backup of current files..."
cp app.py app_backup_$(date +%Y%m%d_%H%M%S).py 2>/dev/null || echo "No existing app.py found"
cp src/static/index.html src/static/index_backup_$(date +%Y%m%d_%H%M%S).html 2>/dev/null || echo "No existing index.html found"

# Deploy optimized backend
echo "⚡ Deploying optimized backend (app.py)..."
cp /home/ubuntu/optimized_app.py app.py

# Deploy optimized frontend
echo "🎨 Deploying optimized frontend (index.html)..."
mkdir -p src/static
cp /home/ubuntu/optimized_index.html src/static/index.html

# Ensure logo file exists
echo "🖼️ Ensuring logo file is in place..."
if [ ! -f "src/static/logo.jpeg" ]; then
    if [ -f "/home/ubuntu/upload/sharifmetalsintl.jpeg" ]; then
        cp /home/ubuntu/upload/sharifmetalsintl.jpeg src/static/logo.jpeg
        echo "✅ Logo copied from upload directory"
    else
        echo "⚠️ Logo file not found - please ensure logo.jpeg is in src/static/"
    fi
else
    echo "✅ Logo file already exists"
fi

# Git operations for deployment
echo "📤 Deploying to production via git..."

# Add all changes
git add .

# Commit with descriptive message
git commit -m "🚀 Deploy optimized dual assistant system

✨ Performance Enhancements:
- Optimized frontend with smooth animations and transitions
- Enhanced backend with faster response times and caching
- Improved mobile responsiveness and touch interactions
- Better loading states and visual feedback
- Hardware-accelerated animations for smoothness

🔧 Technical Improvements:
- Reduced JavaScript execution time
- Optimized CSS with hardware acceleration
- Enhanced API response caching
- Better error handling and retry logic
- Performance monitoring and metrics

🎯 Features Preserved:
- All enhanced Layla trading capabilities
- All enhanced Alya logistics capabilities
- Live market data with real-time updates
- Premium branding and visual identity
- Seamless assistant switching
- Mobile responsive design

Deployment: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to production
echo "🌐 Pushing to Railway production..."
git push

echo ""
echo "🎉 OPTIMIZED DEPLOYMENT COMPLETE!"
echo "=================================="
echo ""
echo "✅ Performance Optimizations Applied:"
echo "   • Smooth animations and transitions"
echo "   • Faster API response times"
echo "   • Enhanced mobile responsiveness"
echo "   • Optimized loading states"
echo "   • Hardware-accelerated rendering"
echo ""
echo "✅ All Enhanced Features Preserved:"
echo "   • Layla's advanced trading capabilities"
echo "   • Alya's enhanced logistics features"
echo "   • Live market data updates"
echo "   • Premium branding elements"
echo "   • Seamless assistant switching"
echo ""
echo "🔗 Your optimized website will be available at:"
echo "   https://layla-sharif-ai.up.railway.app/"
echo ""
echo "⏱️ Deployment typically takes 2-3 minutes to complete."
echo "🧪 Ready for performance testing!"
echo ""

