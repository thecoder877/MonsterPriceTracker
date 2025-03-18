# Monster Price Tracker

Monster Price Tracker is a Chrome extension that tracks the prices of Monster energy drinks from various stores. The extension scrapes data from a specified website and displays the prices in a popup. Users can also filter which products to display.

## Features

- Scrapes prices of Monster energy drinks from a specified website (cenoteka.rs).
- Displays the prices in a popup with a modern design.
- Allows users to filter which products (flavor) to display.
- Automatically scrapes data daily when the browser is first opened. (WIP)

## Installation

1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/thecoder877/monster-price-tracker.git
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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
