const API_BASE = '/api';

async function fetchMarkets() {
    try {
        const res = await fetch(`${API_BASE}/markets`);
        const json = await res.json();
        if (json.status === 'success') {
            renderMarkets(json.data);
        }
    } catch (err) {
        console.error("Error fetching markets:", err);
    }
}

async function fetchBlips() {
    try {
        const res = await fetch(`${API_BASE}/blips`);
        const json = await res.json();
        if (json.status === 'success') {
            renderBlips(json.data);
        }
    } catch (err) {
        console.error("Error fetching blips:", err);
    }
}

function renderMarkets(markets) {
    const list = document.getElementById('markets-list');
    const count = document.getElementById('market-count');
    
    count.textContent = markets.length;
    
    if (markets.length === 0) {
        list.innerHTML = `<div class="loading">No active HOT/WARM markets currently.</div>`;
        return;
    }
    
    list.innerHTML = '';
    markets.forEach((m, idx) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.animationDelay = `${idx * 0.05}s`;
        
        const stateClass = m.state === 'HOT' ? 'hot' : 'warm';
        const price = (m.current_price * 100).toFixed(1);
        
        card.innerHTML = `
            <div class="card-top">
                <div class="market-title">${m.question || 'Unknown Market'}</div>
                <span class="tag ${stateClass}">${m.state}</span>
            </div>
            <div class="card-meta">
                <span>Cat: ${m.category || 'N/A'}</span>
                <span class="price">${price}¢</span>
            </div>
        `;
        list.appendChild(card);
    });
}

function renderBlips(blips) {
    const list = document.getElementById('blips-list');
    
    if (blips.length === 0) {
        list.innerHTML = `<div class="loading">No recent blips detected.</div>`;
        return;
    }
    
    list.innerHTML = '';
    blips.forEach((b, idx) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.style.animationDelay = `${idx * 0.05}s`;
        
        const triggerClass = b.trigger_type.includes('vol') ? 'vol-trigger' : 'price-trigger';
        const triggerLabel = b.trigger_type.toUpperCase();
        
        let metricStr = "";
        if (b.trigger_type === 'price' || b.trigger_type === 'both') {
            metricStr += `Δ ${(b.price_delta * 100).toFixed(1)}¢ `;
        }
        if (b.trigger_type === 'volume' || b.trigger_type === 'both') {
            metricStr += `Vol ${b.volume_ratio.toFixed(1)}x`;
        }
        
        const timeAgo = Math.floor((new Date() - new Date(b.detected_at)) / 60000);
        const timeStr = isNaN(timeAgo) ? 'Recently' : (timeAgo < 1 ? 'Just now' : `${timeAgo}m ago`);
        
        card.innerHTML = `
            <div class="card-top">
                <div class="market-title">${b.question || 'Unknown Market'}</div>
                <span class="tag ${triggerClass}">${triggerLabel}</span>
            </div>
            <div class="card-meta">
                <span>${timeStr}</span>
                <span style="color: var(--text-primary); font-weight: 500;">${metricStr}</span>
            </div>
        `;
        list.appendChild(card);
    });
}

// Initial fetch
fetchMarkets();
fetchBlips();

// Poll every 10 seconds
setInterval(() => {
    fetchMarkets();
    fetchBlips();
}, 10000);
