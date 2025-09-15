#!/bin/bash

# Remove any existing market data scripts from HTML
sed -i '/market-data/d' src/static/index.html
sed -i '/loadMarketData/d' src/static/index.html
sed -i '/updateLME/d' src/static/index.html

# Add ONE clean script before closing body tag
sed -i 's|</body>|<script>let marketLoaded=false;function loadOnce(){if(marketLoaded)return;marketLoaded=true;const container=Array.from(document.querySelectorAll("*")).find(el=>el.textContent&&el.textContent.includes("Error loading market data"));if(container){fetch("/api/market-data").then(r=>r.json()).then(d=>{container.innerHTML=`<h3 style="color:#4CAF50">📊 Live LME Prices</h3><div>${Object.keys(d).map(m=>`<div style="margin:8px 0;padding:8px;background:rgba(76,175,80,0.1);border-left:3px solid #4CAF50"><strong>${m.charAt(0).toUpperCase()+m.slice(1)}:</strong> $${d[m].price.toLocaleString()}/tonne <span style="color:${d[m].change>=0?"#4CAF50":"#f44336}">(${d[m].change>=0?"+":""}${d[m].change.toFixed(2)}%)</span></div>`).join("")}</div>`}).catch(()=>{container.innerHTML="Error loading market data"})}}document.addEventListener("DOMContentLoaded",loadOnce);if(document.readyState!=="loading")loadOnce();</script>\n</body>|' src/static/index.html

echo "✅ Clean script added"
git add .
git commit -m "Add single clean market data script"
git push
echo "🎉 Deployed! No more duplication."
