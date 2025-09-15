import re

# Read the HTML file
with open('src/static/index.html', 'r') as f:
    content = f.read()

# Replace the updateMarketData function with a working one
new_update_function = '''
        function updateMarketData() {
            fetch('/api/market-data')
                .then(response => response.json())
                .then(data => {
                    const marketDataDiv = document.getElementById('market-data');
                    if (data && Object.keys(data).length > 0) {
                        let html = '';
                        
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
                                            ${changeSymbol}${metalData.change} (${changeSymbol}${metalData.change_percent.toFixed(2)}%)
                                        </div>
                                        <div class="metal-range">
                                            H: $${metalData.day_high} | L: $${metalData.day_low}
                                        </div>
                                        <div class="metal-source">${metalData.source}</div>
                                    </div>
                                `;
                            }
                        });
                        
                        html += '<div style="font-size: 10px; color: #999; text-align: center; margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.1);">Last updated: ' + new Date().toLocaleTimeString() + '</div>';
                        marketDataDiv.innerHTML = html;
                    } else {
                        document.getElementById('market-data').innerHTML = '<p>Loading market data...</p>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching market data:', error);
                    document.getElementById('market-data').innerHTML = '<p>Error loading market data</p>';
                });
        }'''

# Find and replace the updateMarketData function
content = re.sub(
    r'function updateMarketData\(\)\s*\{[^}]*\}',
    new_update_function.strip(),
    content,
    flags=re.DOTALL
)

# Write back
with open('src/static/index.html', 'w') as f:
    f.write(content)

print("Fixed market data display function")
