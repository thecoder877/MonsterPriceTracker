chrome.runtime.onInstalled.addListener(() => {
  chrome.alarms.create('dailyScrape', { periodInMinutes: 1440 }); // Set an alarm to trigger every 24 hours
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'dailyScrape') {
    fetchPrices();
  }
});

async function fetchPrices() {
  try {
    const response = await fetch('https://monsterpricetracker.onrender.com'); // Replace with your Render URL
    const data = await response.json();
    chrome.storage.local.set({ lastData: data, lastUpdate: new Date().toISOString() });
  } catch (error) {
    console.error('Error:', error);
  }
}
