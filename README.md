# Monster Price Tracker

Monster Price Tracker is a Chrome extension that tracks the prices of Monster energy drinks from various stores. The extension scrapes data from a specified website and displays the prices in a popup. Users can also filter which products to display.

## Features

- Scrapes prices of Monster energy drinks from a specified website.
- Displays the prices in a popup with a modern glassmorphism design.
- Allows users to filter which products to display.
- Automatically scrapes data daily when the browser is first opened.

## Installation

1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/yourusername/monster-price-tracker.git
   ```

2. Navigate to the project directory:
   ```sh
   cd monster-price-tracker
   ```

3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Update the `manifest.json` file with your API endpoint and other necessary details.

5. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`.
   - Enable "Developer mode" in the top right corner.
   - Click "Load unpacked" and select the project directory.

## Usage

1. Click on the Monster Price Tracker extension icon in the Chrome toolbar.
2. The popup will display the prices of Monster energy drinks.
3. Use the "Refresh" button to manually scrape new data.
4. Use the settings section to filter which products to display.

## Files

- `manifest.json`: The manifest file for the Chrome extension.
- `popup.html`: The HTML file for the extension popup.
- `popup.js`: The JavaScript file for the extension popup.
- `styles.css`: The CSS file for the extension popup.
- `background.js`: The background script for the extension.
- `server.py`: The Flask server for handling API requests.
- `monster.py`: The web scraper for scraping prices.
- `scraped_data.csv`: The CSV file containing the scraped data.
- `monster.xml`: The sitemap file for the website to scrape.

## Development

To run the Flask server locally, use the following command:
```sh
python server.py
```

## Deployment on Cloudflare

### Cloudflare Pages

1. Go to the Cloudflare dashboard and create a new Pages project.
2. Connect your GitHub repository to Cloudflare Pages.
3. Set the build command to:
   ```sh
   pip install -r requirements.txt && python server.py
   ```
4. Set the output directory to:
   ```sh
   .
   ```

### Cloudflare Workers

1. Create a new Cloudflare Worker.
2. Use the following script to proxy requests to your Flask API:

```javascript
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  url.hostname = 'your-flask-api-domain.com' // Replace with your Flask API domain
  const newRequest = new Request(url, request)
  return fetch(newRequest)
}
```

3. Deploy the Worker and bind it to your domain.

Now your Flask API should be accessible through Cloudflare.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
