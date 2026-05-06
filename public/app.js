const API_BASE = '/api';

// DOM Elements
const marketsList = document.getElementById('markets-list');
const blipsList = document.getElementById('blips-list');
const marketCount = document.getElementById('market-count');

const volThreshInput = document.getElementById('vol-thresh');
const priceThreshInput = document.getElementById('price-thresh');
const bothThreshInput = document.getElementById('both-thresh');
const saveSettingsBtn = document.getElementById('save-settings');
const settingsStatus = document.getElementById('settings-status');

// Fetch and apply settings
async function loadSettings() {
    try {
        const res = await fetch(`${API_BASE}/settings`);
        const json = await res.json();
        if (json.status === 'success') {
            const s = json.data;
            if (s.VOLUME_SPIKE_MULTIPLIER) volThreshInput.value = parseFloat(s.VOLUME_SPIKE_MULTIPLIER).toFixed(1);
            if (s.PRICE_DELTA_THRESHOLD) priceThreshInput.value = parseFloat(s.PRICE_DELTA_THRESHOLD).toFixed(2);
            if (s.BOTH_TRIGGERS_THRESHOLD) bothThreshInput.checked = s.BOTH_TRIGGERS_THRESHOLD.toLowerCase() === 'true';
        }
    } catch (err) {
        console.error("Error loading settings:", err);
    }
}

// Save settings
saveSettingsBtn.addEventListener('click', async () => {
    saveSettingsBtn.textContent = 'SAVING...';
    try {
        await fetch(`${API_BASE}/settings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: 'VOLUME_SPIKE_MULTIPLIER', value: volThreshInput.value })
        });
        await fetch(`${API_BASE}/settings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: 'PRICE_DELTA_THRESHOLD', value: priceThreshInput.value })
        });
        await fetch(`${API_BASE}/settings`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: 'BOTH_TRIGGERS_THRESHOLD', value: bothThreshInput.checked.toString() })
        });
        settingsStatus.textContent = '> CONFIG APPLIED';
        setTimeout(() => { settingsStatus.textContent = ''; }, 3000);
    } catch (err) {
        settingsStatus.textContent = '> ERROR SAVING';
        console.error("Error saving settings:", err);
    }
    saveSettingsBtn.textContent = 'APPLY CONFIG';
});

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
    marketCount.textContent = markets.length;
    
    if (markets.length === 0) {
        marketsList.innerHTML = `<div class="loading">NO ACTIVE MARKETS.</div>`;
        return;
    }
    
    marketsList.innerHTML = '';
    markets.forEach((m) => {
        const card = document.createElement('div');
        const isHot = m.state === 'HOT';
        card.className = `card ${isHot ? 'hot' : 'warm'}`;
        
        const price = (m.current_price * 100).toFixed(1);
        const volAvg = Math.round(m.rolling_volume_avg || 0).toLocaleString();
        
        card.innerHTML = `
            <div class="card-top">
                <div class="market-title">${m.question || 'Unknown Market'}</div>
                <span class="tag ${isHot ? 'hot' : 'warm'}">${m.state}</span>
            </div>
            <div class="data-grid">
                <div class="data-item">
                    <span class="data-label">PRICE</span>
                    <span class="data-value">${price}¢</span>
                </div>
                <div class="data-item">
                    <span class="data-label">VOL AVG (EWMA)</span>
                    <span class="data-value">$${volAvg}</span>
                </div>
                <div class="data-item" style="grid-column: 1 / -1">
                    <span class="data-label">ID</span>
                    <span class="data-value" style="font-size: 0.7rem; color: var(--text-secondary)">${m.condition_id}</span>
                </div>
            </div>
        `;
        marketsList.appendChild(card);
    });
}

function renderBlips(blips) {
    if (blips.length === 0) {
        blipsList.innerHTML = `<div class="loading">NO RECENT SIGNALS.</div>`;
        return;
    }
    
    blipsList.innerHTML = '';
    blips.forEach((b) => {
        const card = document.createElement('div');
        const trigger = b.trigger_type || 'unknown';
        card.className = `card ${trigger}`;
        
        const priceDelta = (b.price_delta * 100).toFixed(1);
        const volRatio = b.volume_ratio ? b.volume_ratio.toFixed(2) : '0.00';
        const isPriceUp = b.price_delta > 0;
        
        const timeAgo = Math.floor((new Date() - new Date(b.detected_at)) / 60000);
        const timeStr = isNaN(timeAgo) ? 'Just now' : (timeAgo < 1 ? '<1m ago' : `${timeAgo}m ago`);
        
        card.innerHTML = `
            <div class="card-top">
                <div class="market-title">${b.question || 'Unknown Market'}</div>
                <span class="tag ${trigger}-trigger">${trigger.toUpperCase()}</span>
            </div>
            <div class="data-grid">
                <div class="data-item">
                    <span class="data-label">PRICE DELTA</span>
                    <span class="data-value ${isPriceUp ? 'up' : 'down'}">Δ ${priceDelta}¢</span>
                </div>
                <div class="data-item">
                    <span class="data-label">VOL RATIO</span>
                    <span class="data-value ${volRatio > 2.0 ? 'up' : ''}">${volRatio}x</span>
                </div>
                <div class="data-item">
                    <span class="data-label">DETECTED</span>
                    <span class="data-value" style="font-size: 0.75rem">${timeStr}</span>
                </div>
                <div class="data-item">
                    <span class="data-label">HRS TO CLOSE</span>
                    <span class="data-value" style="font-size: 0.75rem">${b.hours_to_close < 0 ? 'N/A' : b.hours_to_close.toFixed(1)}h</span>
                </div>
            </div>
        `;
        blipsList.appendChild(card);
    });
}

// Initialization
loadSettings();
fetchMarkets();
fetchBlips();

// Polling
setInterval(() => {
    fetchMarkets();
    fetchBlips();
}, 5000); // 5 seconds for more responsive "live" feel
