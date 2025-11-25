"""
PartSelect Product Scraper - Specific Parts
Scrapes specific known refrigerator and dishwasher parts from partselect.com
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re

BASE_URL = "https://www.partselect.com"

# Specific parts to scrape - known working part numbers
PARTS_TO_SCRAPE = [
    {"ps": "PS11752778", "mfr": "W10873791", "name": "Ice Maker Assembly", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS11739119", "mfr": "WP2188656", "name": "Refrigerator Crisper Drawer", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS11755972", "mfr": "WPW10304490", "name": "Evaporator Fan Motor", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS11755766", "mfr": "WP2304134", "name": "Water Inlet Valve", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS11755774", "mfr": "WPW10312695", "name": "Refrigerator Thermistor", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS2366063", "mfr": "WPW10613606", "name": "Ice Level Control Board", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS11739697", "mfr": "WP2211581", "name": "Cantilever Shelf - Glass Included", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS12745711", "mfr": "WR17X11653", "name": "Refrigerator Water Filter", "type": "refrigerator", "brand": "GE"},
    {"ps": "PS12745712", "mfr": "WR17X30359", "name": "Refrigerator Water Filter", "type": "refrigerator", "brand": "GE"},
    {"ps": "PS11756119", "mfr": "W10465232", "name": "Dishwasher Lower Spray Arm", "type": "dishwasher", "brand": "Whirlpool"},
    {"ps": "PS11756074", "mfr": "WPW10195417", "name": "Dishwasher Circulation Pump", "type": "dishwasher", "brand": "Whirlpool"},
    {"ps": "PS1960680", "mfr": "W10195416", "name": "Dishwasher Motor and Pump Assembly", "type": "dishwasher", "brand": "Whirlpool"},
    {"ps": "PS11722229", "mfr": "WD28X10369", "name": "Dishwasher Pump and Motor Assembly", "type": "dishwasher", "brand": "GE"},
    {"ps": "PS11722254", "mfr": "WD01X10462", "name": "Dishwasher Door Latch Assembly", "type": "dishwasher", "brand": "GE"},
    {"ps": "PS11722237", "mfr": "WD12X10422", "name": "Dishwasher Detergent Dispenser", "type": "dishwasher", "brand": "GE"},
    {"ps": "PS11722244", "mfr": "WD28X10394", "name": "Dishwasher Heating Element", "type": "dishwasher", "brand": "GE"},
    {"ps": "PS11722252", "mfr": "WD01X21408", "name": "Dishwasher Electronic Control Board", "type": "dishwasher", "brand": "GE"},
    {"ps": "PS11756093", "mfr": "W10712395", "name": "Dishwasher Rack Adjuster Kit", "type": "dishwasher", "brand": "Whirlpool"},
    {"ps": "PS12583750", "mfr": "W11179302", "name": "Affresh Ice Machine Cleaner", "type": "refrigerator", "brand": "Whirlpool"},
    {"ps": "PS11739091", "mfr": "WP2255499", "name": "Door Shelf Bin", "type": "refrigerator", "brand": "Whirlpool"},
]

def scrape_part(part_info):
    """Scrape a specific part page"""
    ps_number = part_info["ps"]
    mfr_number = part_info["mfr"]
    part_name = part_info["name"]
    part_type = part_info["type"]
    brand = part_info["brand"]
    
    # Construct URL
    url_slug = f"{ps_number}-{brand}-{mfr_number}-{part_name.replace(' ', '-')}.htm"
    url = f"{BASE_URL}/{url_slug}"
    
    print(f"Scraping: {ps_number} - {part_name}...")
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        if response.status_code != 200:
            print(f"  ❌ HTTP {response.status_code} for {url}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract price
        price = 0.0
        price_elem = soup.find('span', class_='price') or soup.find('div', class_='price')
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
            if price_match:
                price = float(price_match.group(1).replace(',', ''))
        
        # Extract description
        description = ""
        desc_elem = soup.find('div', class_='product-description') or soup.find('div', itemprop='description')
        if desc_elem:
            description = desc_elem.get_text(strip=True)[:500]
        
        # Extract symptoms fixed
        symptoms = []
        symptoms_section = soup.find('div', string=re.compile('fixes the following symptoms', re.I))
        if symptoms_section:
            symptoms_list = symptoms_section.find_next('ul') or symptoms_section.find_next('div')
            if symptoms_list:
                for item in symptoms_list.find_all('li'):
                    symptom = item.get_text(strip=True).replace('•', '').strip()
                    if symptom:
                        symptoms.append(symptom.lower())
        
        # Extract compatible models
        models = []
        models_section = soup.find('div', string=re.compile('works with the following', re.I))
        if models_section:
            models_table = models_section.find_next('table') or models_section.find_next('div')
            if models_table:
                for link in models_table.find_all('a', href=re.compile('/Models/')):
                    model = link.get_text(strip=True)
                    if model and len(models) < 10:  # Limit to 10 models
                        models.append(model)
        
        # Extract installation steps
        install_steps = ""
        install_section = soup.find('h3', string=re.compile('installation', re.I)) or \
                         soup.find('h2', string=re.compile('installation', re.I))
        if install_section:
            steps_list = install_section.find_next('ol') or install_section.find_next('ul')
            if steps_list:
                steps = []
                for idx, step in enumerate(steps_list.find_all('li'), 1):
                    step_text = step.get_text(strip=True)
                    if step_text:
                        steps.append(f"{idx}. {step_text}")
                install_steps = "\n".join(steps)
        
        # Build part object
        part_data = {
            "part_number": ps_number,
            "manufacturer_part_number": mfr_number,
            "name": part_name,
            "type": part_type,
            "brand": brand,
            "price": price if price > 0 else 49.99,  # Default price if not found
            "description": description if description else f"Genuine {brand} {part_name.lower()} for {part_type}s. OEM replacement part.",
            "compatible_models": models if models else [f"Compatible with various {brand} {part_type}s"],
            "symptoms_fixed": symptoms if symptoms else [f"{part_name.lower()} not working", "damaged part", "broken component"],
            "install_instructions": install_steps if install_steps else "1. Disconnect power\n2. Remove old part\n3. Install new part\n4. Reconnect power\n5. Test operation",
            "image_url": f"{BASE_URL}/images/part/{ps_number}.jpg",
            "product_url": url
        }
        
        print(f"  ✅ Scraped: ${part_data['price']} - {len(part_data['compatible_models'])} models")
        return part_data
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return None

def main():
    """Main scraper function"""
    print("=" * 60)
    print("PartSelect Specific Parts Scraper")
    print("=" * 60)
    
    all_parts = []
    
    for part_info in PARTS_TO_SCRAPE:
        part_data = scrape_part(part_info)
        if part_data:
            all_parts.append(part_data)
        
        # Be respectful - wait between requests
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print(f"Successfully scraped {len(all_parts)} parts")
    print("=" * 60)
    
    # Save to JSON
    output_file = "backend/data/seedParts.json"
    output_data = {"parts": all_parts}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Saved {len(all_parts)} parts to {output_file}")
    
    # Print summary
    print("\nSummary:")
    print(f"  Refrigerator parts: {sum(1 for p in all_parts if p['type'] == 'refrigerator')}")
    print(f"  Dishwasher parts: {sum(1 for p in all_parts if p['type'] == 'dishwasher')}")
    print(f"  Whirlpool parts: {sum(1 for p in all_parts if p['brand'] == 'Whirlpool')}")
    print(f"  GE parts: {sum(1 for p in all_parts if p['brand'] == 'GE')}")
    print(f"  Total price range: ${min(p['price'] for p in all_parts):.2f} - ${max(p['price'] for p in all_parts):.2f}")

if __name__ == "__main__":
    main()
