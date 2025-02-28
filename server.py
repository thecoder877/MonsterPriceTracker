from flask import Flask, jsonify
from flask_cors import CORS
from monster import scrape_site, fetch_urls_from_sitemap  # Импортујте ваш скрепер

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/prices')
def get_prices():
    sitemap_path = 'monster.xml'
    urls = fetch_urls_from_sitemap(sitemap_path)
    if not urls:
        return jsonify({"error": "No URLs found in sitemap"}), 400
    all_data = []
    for url in urls:
        scraped_data = scrape_site(url)
        if scraped_data:
            all_data.extend(scraped_data)
    unique_data = {}
    for item in all_data:
        if item['name'] not in unique_data:
            unique_data[item['name']] = {
                'name': item['name'],
                'img_url': item['img_url'],
                'prices': []
            }
        unique_data[item['name']]['prices'].append({
            'store': item['store'],
            'price': item['price']
        })
    return jsonify(list(unique_data.values()))

if __name__ == '__main__':
    app.run(port=5000)