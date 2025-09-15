// Simple market data fetcher
function updateMarketData( ) {
    console.log('Fetching market data...');
    
    fetch('/api/market-data')
        .then(response => {
            console.log('Market data response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Market data received:', data);
            displayMarketData(data);
        })
        .catch(error => {
            console.error('Error fetching market data:', error);
            document.querySelector('.market-data-container').innerHTML = 'Error loading market data';
        });
}

function displayMarketData(data) {
    const container = document.querySelector('.market-data-container');
    if (!container) {
        console.error('Market data container not found');
        return;
    }
    
    let html = '<h3>Live LME Prices</h3>';
    
    Object.keys(data).forEach(metal => {
        const metalData = data[metal];
        const changeClass = metalData.change >= 0 ? 'positive' : 'negative';
        const changeSign = metalData.change >= 0 ? '+' : '';
        
        html += `
            <div class="metal-price">
                <div class="metal-name">${metal.charAt(0).toUpperCase() + metal.slice(1)}</div>
                <div class="price">$${metalData.price.toLocaleString()}</div>
                <div class="unit">per tonne</div>
                <div class="change ${changeClass}">${changeSign}${metalData.change.toFixed(2)}%</div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Start updating market data when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, starting market data updates');
    updateMarketData();
    setInterval(updateMarketData, 30000); // Update every 30 seconds
});
