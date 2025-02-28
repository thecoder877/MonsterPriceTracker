document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('refresh').addEventListener('click', fetchPrices);
  loadCachedData();
  loadSettings();
});

async function fetchPrices() {
  showLoading(true);
  try {
    const response = await fetch('https://monsterpricetrackerextension.crnapagoda.workers.dev/api/prices'); // Replace with your Cloudflare Worker URL
    const data = await response.json();
    chrome.storage.local.set({ lastData: data, lastUpdate: new Date().toISOString() });
    renderData(data);
    loadSettings(); // Ensure settings are updated after fetching new data
  } catch (error) {
    console.error('Error:', error);
  }
  showLoading(false);
}

function renderData(data) {
  const container = document.getElementById('content');
  if (!Array.isArray(data)) {
    container.innerHTML = '<p>Error: Invalid data format</p>';
    return;
  }
  chrome.storage.local.get(['hiddenProducts'], ({ hiddenProducts }) => {
    const filteredData = data.filter(item => !hiddenProducts || !hiddenProducts.includes(item.name));
    container.innerHTML = filteredData.map(item => {
      const prices = item.prices && Array.isArray(item.prices) && item.prices.length > 0 ? item.prices : [];
      const lowestPrice = prices.reduce((min, price) => parseFloat(price.price.replace(',', '.')) < parseFloat(min.price.replace(',', '.')) ? price : min, prices[0] || { price: Infinity });
      const filteredPrices = prices.filter(price => price.store !== lowestPrice.store);
      return `
        <div class="product">
          <img src="${item.img_url || 'default_image.jpg'}" alt="${item.name}">
          <h3>${item.name}</h3>
          <div class="prices">
            ${lowestPrice.price !== Infinity ? `<p class="lowest-price">${lowestPrice.store}: ${lowestPrice.price}</p>` : ''}
            ${filteredPrices.length > 0 ? filteredPrices.map(price => `<p>${price.store}: ${price.price}</p>`).join('') : '<p>No prices available</p>'}
          </div>
        </div>
      `;
    }).join('');
  });
}

function loadCachedData() {
  chrome.storage.local.get(['lastData'], ({ lastData }) => {
    if (lastData) {
      renderData(lastData);
    } else {
      fetchPrices();
    }
  });
}

function showLoading(show) {
  document.getElementById('loading').style.display = show ? 'block' : 'none';
}

function loadSettings() {
  chrome.storage.local.get(['lastData', 'hiddenProducts'], ({ lastData, hiddenProducts }) => {
    if (lastData) {
      const settingsContainer = document.getElementById('settings');
      settingsContainer.innerHTML = lastData.map(item => `
        <div class="setting-item">
          <input type="checkbox" id="show-${item.name}" ${!hiddenProducts || !hiddenProducts.includes(item.name) ? 'checked' : ''}>
          <label for="show-${item.name}">${item.name}</label>
        </div>
      `).join('');
      settingsContainer.addEventListener('change', saveSettings);
    }
  });
}

function saveSettings() {
  const checkboxes = document.querySelectorAll('#settings input[type="checkbox"]');
  const hiddenProducts = Array.from(checkboxes).filter(checkbox => !checkbox.checked).map(checkbox => checkbox.id.replace('show-', ''));
  chrome.storage.local.set({ hiddenProducts });
  loadCachedData();
}