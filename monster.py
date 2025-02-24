from selenium.webdriver.common.by import By
import requests
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time
import pandas as pd
from urllib.parse import unquote
import shutil
import os

def is_chrome_installed():
    return shutil.which("google-chrome") is not None
def get_chrome_path():
    possible_paths = ["/usr/bin/google-chrome", "/usr/local/bin/google-chrome", "/usr/bin/chrome"]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

chrome_path = get_chrome_path()
if chrome_path is None:
    raise FileNotFoundError("Google Chrome nije instaliran ili nije na očekivanoj putanji.")

print(f"✅ Google Chrome pronađen: {chrome_path}")


def init_driver():
    chromedriver_autoinstaller.install()  # Automatska instalacija chromedrivera
    
    chrome_path = "/usr/bin/google-chrome"
    if not shutil.which(chrome_path):
        raise FileNotFoundError(f"Google Chrome nije pronađen na {chrome_path}")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.binary_location = chrome_path  # Ispravan put do Chrome-a

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

        try:
            img_element = product.find_element(By.CSS_SELECTOR, "a.product_image img")
            srcset = img_element.get_attribute("srcset")
            src = img_element.get_attribute("src")

            img_url = "N/A"
            candidate_url = None

            if srcset:
                entries = [entry.strip() for entry in srcset.split(',')]
                if entries:
                    first_entry = entries[0].split()[0]
                    candidate_url = first_entry.strip()

            if not candidate_url and src:
                candidate_url = src.strip()

            if candidate_url:
                if '/_next/image' in candidate_url and 'url=' in candidate_url:
                    url_parts = candidate_url.split('url=')
                    if len(url_parts) > 1:
                        encoded_part = url_parts[1].split('&')[0]
                        decoded_url = unquote(encoded_part)
                        img_url = decoded_url
                else:
                    img_url = candidate_url

            print(f"Final image URL: {img_url}")

        except Exception as e:
            print(f"Error extracting image: {e}")
            img_url = "N/A"

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

        sitemap_content = sitemap_content.strip()  

        root = ET.fromstring(sitemap_content)
        
        namespace = {
            'default': 'https://www.sitemaps.org/schemas/sitemap/0.9'
        }
        
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
    sitemap_path = r'C:\Users\admin\Desktop\web_scraping_project\monster.xml'
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

        df = pd.DataFrame(all_data)
        print(df.head())  
        df.to_csv("scraped_data.csv", index=False)
        print("Data saved to scraped_data.csv")
