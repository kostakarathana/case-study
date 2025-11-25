"""
PartSelect Product Scraper
Scrapes refrigerator and dishwasher parts from partselect.com
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin

BASE_URL = "https://www.partselect.com"

# Categories to scrape
CATEGORIES = {
    "refrigerator": [
        "/Refrigerator-Parts.htm",
        "/Whirlpool-Refrigerator-Parts.htm",
        "/GE-Refrigerator-Parts.htm",
    ],
    "dishwasher": [
        "/Dishwasher-Parts.htm",
        "/Whirlpool-Dishwasher-Parts.htm",
        "/GE-Dishwasher-Parts.htm",
    ]
}

def get_soup(url):
    """Fetch and parse a URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_part_number(text):
    """Extract part number from text"""
    # Common patterns: PS12345678, W10123456, WPW10123456
    match = re.search(r'(PS\d{8,10}|W\d{8,10}|WP\d{8,10}|WPW\d{8,10})', text)
    return match.group(1) if match else None

def scrape_product_listing(category_url, appliance_type):
    """Scrape products from a category listing page"""
    print(f"Scraping {category_url}...")
    
    soup = get_soup(urljoin(BASE_URL, category_url))
    if not soup:
        return []
    
    products = []
    
    # Find product listings (adjust selectors based on actual HTML)
    product_items = soup.find_all('div', class_=['product-item', 'part-result', 'product'])
    
    print(f"Found {len(product_items)} potential products")
    
    for item in product_items[:20]:  # Limit to 20 per category
        try:
            # Extract part name
            name_elem = item.find(['h2', 'h3', 'h4', 'a'], class_=['product-title', 'part-title', 'title'])
            if not name_elem:
                name_elem = item.find('a', href=re.compile(r'/PS\d+'))
            
            if not name_elem:
                continue
                
            name = name_elem.get_text(strip=True)
            
            # Extract part number
            part_number = extract_part_number(name) or extract_part_number(str(item))
            if not part_number:
                continue
            
            # Extract product URL
            link_elem = item.find('a', href=True)
            product_url = urljoin(BASE_URL, link_elem['href']) if link_elem else ""
            
            # Extract price
            price_elem = item.find(['span', 'div'], class_=['price', 'product-price'])
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$?([\d.]+)', price_text)
                price = float(price_match.group(1)) if price_match else 49.99
            else:
                price = 49.99
            
            # Extract description
            desc_elem = item.find(['p', 'div'], class_=['description', 'product-desc'])
            description = desc_elem.get_text(strip=True) if desc_elem else f"OEM {appliance_type} part"
            
            product = {
                "part_number": part_number,
                "name": name,
                "type": appliance_type,
                "brand": "Whirlpool",  # Most common
                "description": description[:200],
                "price": price,
                "product_url": product_url,
                "image_url": f"https://www.partselect.com/images/part/{part_number}.jpg"
            }
            
            products.append(product)
            print(f"  ✓ {part_number}: {name}")
            
        except Exception as e:
            print(f"  Error parsing product: {e}")
            continue
    
    return products

def scrape_top_parts():
    """Scrape top/popular parts from main page"""
    print("Scraping popular parts from main page...")
    
    soup = get_soup(f"{BASE_URL}/refrigerator-parts.htm")
    if not soup:
        return []
    
    products = []
    
    # Look for "Top Parts" or "Popular Parts" sections
    popular_sections = soup.find_all(['div', 'section'], 
                                     class_=re.compile(r'popular|top-parts|featured'))
    
    for section in popular_sections:
        links = section.find_all('a', href=re.compile(r'/PS\d+'))
        
        for link in links[:10]:
            try:
                part_number = extract_part_number(link['href'])
                if not part_number:
                    continue
                
                name = link.get_text(strip=True)
                
                products.append({
                    "part_number": part_number,
                    "name": name,
                    "type": "refrigerator",
                    "brand": "Whirlpool",
                    "description": f"Popular replacement part for refrigerators",
                    "price": 39.99,
                    "product_url": urljoin(BASE_URL, link['href']),
                    "image_url": f"https://www.partselect.com/images/part/{part_number}.jpg"
                })
                
                print(f"  ✓ {part_number}: {name}")
                
            except Exception as e:
                continue
    
    return products

def generate_mock_details(products):
    """Add mock compatible models and symptoms to products"""
    
    refrigerator_models = [
        "WRS325SDHZ", "WRF555SDFZ", "MFI2570FEZ", "ED5FHEXVB00",
        "WDT780SAEM1", "WRS571CIHZ", "WRX735SDHZ"
    ]
    
    dishwasher_models = [
        "WDT750SAHZ0", "WDF520PADM7", "KDFE104HPS0", "WDT730PAHZ0",
        "KDTE334GPS0", "WDF520PADW7"
    ]
    
    refrigerator_symptoms = [
        ["ice maker not working", "no ice production", "ice maker stopped making ice"],
        ["refrigerator not cooling", "freezer not cold enough", "warm refrigerator"],
        ["water dispenser not working", "no water flow", "slow water dispenser"],
        ["frost buildup in freezer", "ice buildup on back wall", "defrost issues"],
        ["water leaking", "puddle under refrigerator", "water on floor"]
    ]
    
    dishwasher_symptoms = [
        ["dishes not cleaning properly", "poor wash performance", "food residue on dishes"],
        ["dishwasher not draining", "water in bottom of dishwasher", "standing water"],
        ["dishwasher not heating", "dishes not drying", "poor drying performance"],
        ["dishwasher won't start", "control panel not working", "no power"],
        ["loud noise during cycle", "grinding noise", "rattling sound"]
    ]
    
    for product in products:
        # Add compatible models
        if product["type"] == "refrigerator":
            product["compatible_models"] = refrigerator_models[:4]
            product["symptoms_fixed"] = refrigerator_symptoms[hash(product["part_number"]) % len(refrigerator_symptoms)]
        else:
            product["compatible_models"] = dishwasher_models[:4]
            product["symptoms_fixed"] = dishwasher_symptoms[hash(product["part_number"]) % len(dishwasher_symptoms)]
        
        # Generate installation instructions
        product["install_instructions"] = generate_installation_steps(product["type"])
    
    return products

def generate_installation_steps(appliance_type):
    """Generate generic installation steps"""
    if appliance_type == "refrigerator":
        return """1. Unplug the refrigerator or turn off the circuit breaker.
2. Remove any shelves or bins blocking access to the part.
3. Locate the old part and remove mounting screws if applicable.
4. Disconnect any wire harnesses or connections.
5. Remove the old part carefully.
6. Install the new part in reverse order.
7. Reconnect all wire harnesses and secure with mounting hardware.
8. Replace any shelves or bins that were removed.
9. Restore power to the refrigerator.
10. Allow 24 hours for the appliance to reach proper operating temperature."""
    else:
        return """1. Turn off power to the dishwasher at the circuit breaker.
2. Remove the lower dish rack to access the part.
3. Remove any mounting screws or clips securing the old part.
4. Disconnect wire harnesses if applicable.
5. Remove the old part from the dishwasher.
6. Position the new part in place.
7. Secure with mounting screws or clips.
8. Reconnect any wire harnesses.
9. Replace the lower dish rack.
10. Restore power and run a test cycle."""

def main():
    """Main scraping function"""
    print("Starting PartSelect scraper...")
    print("=" * 60)
    
    all_products = []
    
    # Try to scrape popular parts first
    popular = scrape_top_parts()
    all_products.extend(popular)
    
    # Scrape category pages
    for appliance_type, urls in CATEGORIES.items():
        for url in urls:
            products = scrape_product_listing(url, appliance_type)
            all_products.extend(products)
            time.sleep(1)  # Be nice to the server
    
    # Remove duplicates based on part number
    seen = set()
    unique_products = []
    for product in all_products:
        if product["part_number"] not in seen:
            seen.add(product["part_number"])
            unique_products.append(product)
    
    # Add mock details
    unique_products = generate_mock_details(unique_products)
    
    print("=" * 60)
    print(f"Total unique products scraped: {len(unique_products)}")
    
    # Save to JSON
    output = {"parts": unique_products}
    
    with open('backend/data/seedParts.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ Saved {len(unique_products)} products to backend/data/seedParts.json")
    
    # Print summary
    refrigerator_count = sum(1 for p in unique_products if p["type"] == "refrigerator")
    dishwasher_count = sum(1 for p in unique_products if p["type"] == "dishwasher")
    
    print(f"   - Refrigerator parts: {refrigerator_count}")
    print(f"   - Dishwasher parts: {dishwasher_count}")

if __name__ == "__main__":
    main()
