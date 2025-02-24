from selenium.webdriver.common.by import By
import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
import pandas as pd
from urllib.parse import unquote

def init_driver():
    chromedriver_autoinstaller.install()  # Automatically install chromedriver
    options = Options()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = '/usr/bin/google-chrome'  # Specify the path to google-chrome
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_site(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(5)

    data = []

    products = driver.find_elements(By.CSS_SELECTOR, ".product_wrap")
    print(f"Found {len(products)} products on {url}")

    for product in products:
        try:
            name = product.find_element(By.CSS_SELECTOR, ".product_info.text-center.pt-2.pb-4 a").text
        except:
            name = "N/A"

        price_elements = product.find_elements(By.CSS_SELECTOR, ".product_info_wrap .row")
        print(f"Found {len(price_elements)} price elements for product {name}")

        prices = []
        for price_element in price_elements:
            try:
                store = price_element.find_element(By.TAG_NAME, "img").get_attribute("alt")
                price = price_element.find_element(By.CLASS_NAME, "product_price").text
                prices.append({"store": store, "price": price})
            except:
                continue

        # Revised image URL extraction logic
        try:
            img_element = product.find_element(By.CSS_SELECTOR, "a.product_image img")
            srcset = img_element.get_attribute("srcset")
            src = img_element.get_attribute("src")

            img_url = "N/A"
            candidate_url = None

            # Parse srcset to get the first URL
            if srcset:
                entries = [entry.strip() for entry in srcset.split(',')]
                if entries:
                    first_entry = entries[0].split()[0]  # Get URL part before descriptor
                    candidate_url = first_entry.strip()

            # Fallback to src if no candidate from srcset
            if not candidate_url and src:
                candidate_url = src.strip()

            # Process candidate URL
            if candidate_url:
                # Check if URL contains '/_next/image' and 'url=' parameter
                if '/_next/image' in candidate_url and 'url=' in candidate_url:
                    # Extract the encoded part
                    url_parts = candidate_url.split('url=')
                    if len(url_parts) > 1:
                        encoded_part = url_parts[1].split('&')[0]
                        decoded_url = unquote(encoded_part)
                        img_url = decoded_url
                else:
                    img_url = candidate_url
            else:
                img_url = "N/A"

            print(f"Final image URL: {img_url}")  # Debug output

        except Exception as e:
            print(f"Error extracting image: {e}")
            img_url = "N/A"

        # Collect data
        if prices:
            for price in prices:
                data.append({
                    "name": name,
                    "img_url": img_url,
                    "store": price["store"],
                    "price": price["price"]
                })

    driver.quit()
    return data

def fetch_urls_from_sitemap(sitemap_path):
    try:
        with open(sitemap_path, 'r', encoding='utf-8') as file:
            sitemap_content = file.read()

        # Clean up XML formatting issues if any
        sitemap_content = sitemap_content.strip()  

        # Parse the XML content
        root = ET.fromstring(sitemap_content)
        
        # Define the CORRECT namespace (match exactly what's in the XML)
        namespace = {
            'default': 'https://www.sitemaps.org/schemas/sitemap/0.9'  # Note the https
        }
        
        # Extract URLs using the default namespace
        urls = [
            loc.text 
            for loc in root.findall(".//default:loc", namespace)
        ]
        
        print(f"Found {len(urls)} URLs in sitemap")
        return urls
        
    except Exception as e:
        print(f"Error reading the sitemap: {str(e)}")
        return []

if __name__ == "__main__":
    # Provide the local path to your sitemap.xml
    sitemap_path = r'C:\Users\admin\Desktop\web_scraping_project\monster.xml'  # Local path to your sitemap file
    urls = fetch_urls_from_sitemap(sitemap_path)
    
    if not urls:
        print("No URLs found in the sitemap. Exiting...")
    else:
        all_data = []
        for url in urls:
            print(f"Scraping: {url}")
            data = scrape_site(url)
            if data:
                all_data.extend(data)

        rows = []
        for item in all_data:
            rows.append({
                "name": item["name"],
                "img_url": item["img_url"],
                "store": item["store"],
                "price": item["price"]
            })

        df = pd.DataFrame(rows)
        print(df.head())  
        df.to_csv("scraped_data.csv", index=False)
        print("Data saved to scraped_data.csv")
