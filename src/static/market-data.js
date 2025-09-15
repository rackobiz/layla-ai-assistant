function loadMarketData( ) {
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let textNode, lmeContainer = null;
    
    while (textNode = walker.nextNode()) {
        if (textNode.textContent.includes('Live LME Prices') || textNode.textContent.includes('Error loading market data')) {
            lmeContainer = textNode.parentElement;
            break;
        }
    }
    
    if (lmeContainer) {
        lmeContainer.innerHTML = '<h3 style="color: #4CAF50;">📊 Live LME Prices</h3><p style="color: #ccc;">Loading...</p>';
        
        fetch('/api/market-data')
            .then(response => response.json())
            .then(data => {
                lmeContainer.innerHTML = \`
                    <h3 style="color: #4CAF50; margin-bottom: 15px;">📊 Live LME Prices</h3>
                    <div style="color: white;">
                        <div style="margin: 8px 0; padding: 8px; background: rgba(76, 175, 80, 0.1); border-left: 3px solid #4CAF50;">
                            <strong>Copper:</strong> $\${data.copper.price.toLocaleString()}/tonne 
                            <span style="color: \${data.copper.change >= 0 ? '#4CAF50' : '#f44336'};">(\${data.copper.change >= 0 ? '+' : ''}\${data.copper.change.toFixed(2)}%)</span>
                        </div>
                        <div style="margin: 8px 0; padding: 8px; background: rgba(76, 175, 80, 0.1); border-left: 3px solid #4CAF50;">
                            <strong>Aluminum:</strong> $\${data.aluminum.price.toLocaleString()}/tonne 
                            <span style="color: \${data.aluminum.change >= 0 ? '#4CAF50' : '#f44336'};">(\${data.aluminum.change >= 0 ? '+' : ''}\${data.aluminum.change.toFixed(2)}%)</span>
                        </div>
                        <div style="margin: 8px 0; padding: 8px; background: rgba(76, 175, 80, 0.1); border-left: 3px solid #4CAF50;">
                            <strong>Zinc:</strong> $\${data.zinc.price.toLocaleString()}/tonne 
                            <span style="color: \${data.zinc.change >= 0 ? '#4CAF50' : '#f44336'};">(\${data.zinc.change >= 0 ? '+' : ''}\${data.zinc.change.toFixed(2)}%)</span>
                        </div>
                        <div style="margin: 8px 0; padding: 8px; background: rgba(76, 175, 80, 0.1); border-left: 3px solid #4CAF50;">
                            <strong>Lead:</strong> $\${data.lead.price.toLocaleString()}/tonne 
                            <span style="color: \${data.lead.change >= 0 ? '#4CAF50' : '#f44336'};">(\${data.lead.change >= 0 ? '+' : ''}\${data.lead.change.toFixed(2)}%)</span>
                        </div>
                        <div style="margin: 8px 0; padding: 8px; background: rgba(76, 175, 80, 0.1); border-left: 3px solid #4CAF50;">
                            <strong>Nickel:</strong> $\${data.nickel.price.toLocaleString()}/tonne 
                            <span style="color: \${data.nickel.change >= 0 ? '#4CAF50' : '#f44336'};">(\${data.nickel.change >= 0 ? '+' : ''}\${data.nickel.change.toFixed(2)}%)</span>
                        </div>
                        <div style="margin: 8px 0; padding: 8px; background: rgba(76, 175, 80, 0.1); border-left: 3px solid #4CAF50;">
                            <strong>Tin:</strong> $\${data.tin.price.toLocaleString()}/tonne 
                            <span style="color: \${data.tin.change >= 0 ? '#4CAF50' : '#f44336'};">(\${data.tin.change >= 0 ? '+' : ''}\${data.tin.change.toFixed(2)}%)</span>
                        </div>
                    </div>
                \`;
            })
            .catch(error => {
                lmeContainer.innerHTML = '<h3 style="color: #f44336;">📊 Live LME Prices</h3><p style="color: #f44336;">Error loading market data</p>';
            });
    }
}

function startMarketDataUpdates() {
    loadMarketData();
    setInterval(loadMarketData, 30000);
}

document.addEventListener('DOMContentLoaded', startMarketDataUpdates);
if (document.readyState !== 'loading') {
    startMarketDataUpdates();
}
