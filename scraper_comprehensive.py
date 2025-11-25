"""
Comprehensive PartSelect Scraper
Scrapes actual products from PartSelect.com using known popular part numbers
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.partselect.com"

# Comprehensive list of popular refrigerator and dishwasher parts
KNOWN_PARTS = [
    # Whirlpool Refrigerator Parts
    {"ps": "PS11752778", "mfr": "W10873791", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11755972", "mfr": "WPW10304490", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11755766", "mfr": "WP2304134", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11755774", "mfr": "WPW10312695", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS2366063", "mfr": "WPW10613606", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11739119", "mfr": "WP2188656", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11739697", "mfr": "WP2211581", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11755770", "mfr": "WP2252130", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11739091", "mfr": "WP2255499", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11752309", "mfr": "W10321302", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11756027", "mfr": "WPW10350375", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11739643", "mfr": "WP2188664", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11756030", "mfr": "WPW10508950", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11756043", "mfr": "WP67003637", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11739706", "mfr": "W10193691", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11755987", "mfr": "WPW10321304", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11756052", "mfr": "WPW10424118", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11739694", "mfr": "W10190965", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11756024", "mfr": "WPW10295370", "brand": "Whirlpool", "type": "refrigerator"},
    {"ps": "PS11739640", "mfr": "WP2156022", "brand": "Whirlpool", "type": "refrigerator"},
    
    # GE Refrigerator Parts
    {"ps": "PS12745711", "mfr": "WR17X11653", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12745712", "mfr": "WR17X30359", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12746803", "mfr": "WR55X10942", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12364191", "mfr": "WR60X10074", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12729089", "mfr": "WR55X10025", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12746806", "mfr": "WR60X29623", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12729077", "mfr": "WR02X12657", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12364181", "mfr": "WR17X30377", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12746802", "mfr": "WR55X10856", "brand": "GE", "type": "refrigerator"},
    {"ps": "PS12729090", "mfr": "WR55X10942K", "brand": "GE", "type": "refrigerator"},
    
    # Whirlpool Dishwasher Parts
    {"ps": "PS11756119", "mfr": "W10465232", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756074", "mfr": "WPW10195417", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS1960680", "mfr": "W10195416", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756093", "mfr": "W10712395", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756141", "mfr": "W10807920", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756071", "mfr": "WPW10082853", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756140", "mfr": "W10802681", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11739701", "mfr": "W10350375", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756090", "mfr": "WPW10518394", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756142", "mfr": "W10861023", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756118", "mfr": "W10380990", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11739688", "mfr": "W10077838", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756096", "mfr": "WPW10728849", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756122", "mfr": "W10491683", "brand": "Whirlpool", "type": "dishwasher"},
    {"ps": "PS11756086", "mfr": "WPW10503549", "brand": "Whirlpool", "type": "dishwasher"},
    
    # GE Dishwasher Parts
    {"ps": "PS11722229", "mfr": "WD28X10369", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722254", "mfr": "WD01X10462", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722237", "mfr": "WD12X10422", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722244", "mfr": "WD28X10394", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722252", "mfr": "WD01X21408", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722240", "mfr": "WD21X10519", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722241", "mfr": "WD22X10045", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722268", "mfr": "WD35X10054", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722234", "mfr": "WD01X10506", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722247", "mfr": "WD28X25134", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722266", "mfr": "WD34X21678", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722265", "mfr": "WD34X20643", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722235", "mfr": "WD01X10524", "brand": "GE", "type": "dishwasher"},
    {"ps": "PS11722262", "mfr": "WD28X26008", "brand": "GE", "type": "dishwasher"},
]

def scrape_part_detail(part_info):
    """Scrape detailed information from a part page"""
    ps = part_info["ps"]
    mfr = part_info["mfr"]
    brand = part_info["brand"]
    part_type = part_info["type"]
    
    # Try multiple URL formats
    url_formats = [
        f"{BASE_URL}/{ps}.htm",
        f"{BASE_URL}/{ps}-{brand}-{mfr}.htm",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    for url in url_formats:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract part name from title or h1
                name = ""
                title_tag = soup.find('title')
                if title_tag:
                    title_text = title_tag.get_text()
                    # Parse "Ice Maker Assembly WPW10873791" format
                    name = title_text.split('|')[0].strip()
                    name = re.sub(r'\s+' + re.escape(mfr) + r'.*', '', name)
                    name = re.sub(r'\s+' + re.escape(ps) + r'.*', '', name)
                    name = name.strip()
                
                if not name:
                    h1 = soup.find('h1')
                    if h1:
                        name = h1.get_text(strip=True)
                        name = re.sub(r'\s+' + re.escape(mfr) + r'.*', '', name)
                
                # Extract price
                price = 0.0
                price_patterns = [
                    soup.find('span', class_='price'),
                    soup.find('div', class_='price'),
                    soup.find('span', itemprop='price'),
                    soup.find('meta', {'property': 'product:price:amount'})
                ]
                
                for price_elem in price_patterns:
                    if price_elem:
                        if price_elem.name == 'meta':
                            price_text = price_elem.get('content', '')
                        else:
                            price_text = price_elem.get_text(strip=True)
                        
                        price_match = re.search(r'\$?([\d,]+\.?\d*)', price_text)
                        if price_match:
                            price = float(price_match.group(1).replace(',', ''))
                            if price > 0:
                                break
                
                # Extract description
                description = ""
                desc_selectors = [
                    soup.find('div', class_='product-description'),
                    soup.find('div', itemprop='description'),
                    soup.find('div', class_='description'),
                    soup.find('p', class_='description')
                ]
                
                for desc_elem in desc_selectors:
                    if desc_elem:
                        desc_text = desc_elem.get_text(strip=True)
                        if len(desc_text) > 50:
                            description = desc_text[:800]
                            break
                
                # Extract symptoms
                symptoms = []
                symptoms_text = soup.find(string=re.compile(r'fixes? the following symptoms?', re.I))
                if symptoms_text:
                    parent = symptoms_text.find_parent()
                    if parent:
                        for li in parent.find_all('li'):
                            symptom = li.get_text(strip=True).replace('•', '').strip().lower()
                            if symptom and len(symptom) > 5:
                                symptoms.append(symptom)
                
                # If no symptoms found, try alternative method
                if not symptoms:
                    for elem in soup.find_all(string=re.compile(r'symptom|problem|issue', re.I)):
                        parent = elem.find_parent()
                        if parent:
                            for li in parent.find_all('li')[:5]:
                                symptom = li.get_text(strip=True).replace('•', '').strip().lower()
                                if symptom and len(symptom) > 5:
                                    symptoms.append(symptom)
                            if symptoms:
                                break
                
                # Extract compatible models
                models = []
                models_text = soup.find(string=re.compile(r'works? with.*following|compatible.*model', re.I))
                if models_text:
                    parent = models_text.find_parent()
                    if parent:
                        # Look for model links or list items
                        for link in parent.find_all('a', href=re.compile(r'/Models/'))[:15]:
                            model = link.get_text(strip=True)
                            if model and len(model) > 3:
                                models.append(model)
                
                # Extract installation instructions
                install_steps = []
                install_headers = soup.find_all(string=re.compile(r'installation|how to (install|replace)', re.I))
                for header in install_headers:
                    parent = header.find_parent()
                    if parent:
                        ol = parent.find_next('ol')
                        if ol:
                            for idx, li in enumerate(ol.find_all('li')[:15], 1):
                                step_text = li.get_text(strip=True)
                                if step_text:
                                    install_steps.append(step_text)
                            break
                
                # Create part object
                part_data = {
                    "part_number": ps,
                    "manufacturer_part_number": mfr,
                    "name": name if name else f"{brand} {part_type.title()} Part",
                    "type": part_type,
                    "brand": brand,
                    "price": round(price, 2) if price > 0 else None,
                    "description": description if description else f"Genuine OEM {brand} replacement part for {part_type}s.",
                    "compatible_models": models if models else [],
                    "symptoms_fixed": symptoms if symptoms else [],
                    "install_instructions": "\n".join([f"{i+1}. {s}" for i, s in enumerate(install_steps)]) if install_steps else "",
                    "image_url": f"{BASE_URL}/images/part/{ps}.jpg",
                    "product_url": url
                }
                
                print(f"✅ {ps}: {name[:40]} - ${price}")
                return part_data
                
        except Exception as e:
            continue
    
    print(f"❌ {ps}: Failed to scrape")
    return None

def main():
    print("=" * 70)
    print("COMPREHENSIVE PARTSELECT SCRAPER")
    print("=" * 70)
    print(f"\nScraping {len(KNOWN_PARTS)} parts...\n")
    
    all_parts = []
    failed = 0
    
    # Use threading for faster scraping
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_part = {executor.submit(scrape_part_detail, part): part for part in KNOWN_PARTS}
        
        for future in as_completed(future_to_part):
            part_data = future.result()
            if part_data:
                all_parts.append(part_data)
            else:
                failed += 1
            
            # Small delay to be respectful
            time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print(f"SCRAPING COMPLETE")
    print("=" * 70)
    print(f"✅ Successfully scraped: {len(all_parts)} parts")
    print(f"❌ Failed to scrape: {failed} parts")
    
    # Statistics
    fridge_parts = [p for p in all_parts if p['type'] == 'refrigerator']
    dish_parts = [p for p in all_parts if p['type'] == 'dishwasher']
    whirlpool_parts = [p for p in all_parts if p['brand'] == 'Whirlpool']
    ge_parts = [p for p in all_parts if p['brand'] == 'GE']
    
    prices = [p['price'] for p in all_parts if p['price']]
    
    print(f"\n📊 Statistics:")
    print(f"   Refrigerator parts: {len(fridge_parts)}")
    print(f"   Dishwasher parts: {len(dish_parts)}")
    print(f"   Whirlpool parts: {len(whirlpool_parts)}")
    print(f"   GE parts: {len(ge_parts)}")
    if prices:
        print(f"   Price range: ${min(prices):.2f} - ${max(prices):.2f}")
        print(f"   Average price: ${sum(prices)/len(prices):.2f}")
    
    # Save to JSON
    output_file = "backend/data/seedParts.json"
    output_data = {"parts": all_parts}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
