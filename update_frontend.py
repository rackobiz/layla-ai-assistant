import re

# Read the current HTML file
with open('src/static/index.html', 'r') as f:
    content = f.read()

# Find and replace the market data update function
new_market_data_function = '''
        function updateMarketData() {
            fetch('/api/market-data')
                .then(response => response.json())
                .then(data => {
                    const marketDataDiv = document.getElementById('market-data');
                    if (data && Object.keys(data).length > 0) {
                        let html = '<h3>Live LME Prices</h3>';
                        
                        const metals = ['copper', 'aluminum', 'zinc', 'lead', 'nickel', 'tin'];
                        metals.forEach(metal => {
                            if (data[metal]) {
                                const metalData = data[metal];
                                const changeColor = metalData.change >= 0 ? '#4CAF50' : '#f44336';
                                const changeSymbol = metalData.change >= 0 ? '+' : '';
                                
                                html += `
                                    <div class="metal-price">
                                        <div class="metal-name">${metal.charAt(0).toUpperCase() + metal.slice(1)}</div>
                                        <div class="metal-price-value">$${metalData.price}</div>
                                        <div class="metal-unit">${metalData.unit}</div>
                                        <div class="metal-change" style="color: ${changeColor}">
                                            ${changeSymbol}$${metalData.change} (${changeSymbol}${metalData.change_percent.toFixed(2)}%)
                                        </div>
                                        <div class="metal-range">
                                            H: $${metalData.day_high} | L: $${metalData.day_low}
                                        </div>
                                        <div class="metal-source">${metalData.source}</div>
                                    </div>
                                `;
                            }
                        });
                        
                        html += `<div class="last-updated">Last updated: ${new Date().toLocaleTimeString()}</div>`;
                        marketDataDiv.innerHTML = html;
                    } else {
                        document.getElementById('market-data').innerHTML = '<h3>Live LME Prices</h3><p>Loading market data...</p>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching market data:', error);
                    document.getElementById('market-data').innerHTML = '<h3>Live LME Prices</h3><p>Error loading market data</p>';
                });
        }'''

# Replace the existing updateMarketData function
pattern = r'function updateMarketData\(\)\s*\{[^}]*\}'
if re.search(pattern, content):
    content = re.sub(pattern, new_market_data_function.strip(), content, flags=re.DOTALL)
else:
    # If function doesn't exist, add it before the closing script tag
    content = content.replace('</script>', new_market_data_function + '\n        </script>')

# Add CSS for better styling of market data
new_css = '''
        .metal-price {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            border-left: 3px solid #2196F3;
        }
        
        .metal-name {
            font-weight: bold;
            font-size: 14px;
            color: #2196F3;
            margin-bottom: 4px;
        }
        
        .metal-price-value {
            font-size: 18px;
            font-weight: bold;
            color: #fff;
            margin-bottom: 2px;
        }
        
        .metal-unit {
            font-size: 11px;
            color: #ccc;
            margin-bottom: 4px;
        }
        
        .metal-change {
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 4px;
        }
        
        .metal-range {
            font-size: 11px;
            color: #ccc;
            margin-bottom: 4px;
        }
        
        .metal-source {
            font-size: 10px;
            color: #999;
            font-style: italic;
        }
        
        .last-updated {
            font-size: 10px;
            color: #999;
            text-align: center;
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }'''

# Add the CSS before the closing </style> tag
content = content.replace('</style>', new_css + '\n        </style>')

# Make sure the market data updates every 30 seconds
auto_update_code = '''
        // Auto-update market data every 30 seconds
        setInterval(updateMarketData, 30000);
        
        // Initial load
        updateMarketData();'''

# Add auto-update code before closing script tag
content = content.replace('</script>', auto_update_code + '\n        </script>')

# Write back to file
with open('src/static/index.html', 'w') as f:
    f.write(content)

print("Updated frontend to display real market data")
