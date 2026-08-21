"""
Taxonomy Classifier & Classpath Mapper.
Determines Dept, Class, Fine, Classpath, and canonical Product Name.
"""
import os
import json
import re
from typing import Dict, Any, Tuple, Optional

MASTER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "master_data")

TAXONOMIES_DATA = {}
tax_path = os.path.join(MASTER_DATA_DIR, "taxonomies.json")
if os.path.exists(tax_path):
    with open(tax_path, "r", encoding="utf-8") as f:
        TAXONOMIES_DATA = json.load(f)

# Keyword patterns for category detection
CATEGORY_RULES = [
    # Appliances
    (r"\b(?:dishwasher|dishwashers)\b", "dishwashers"),
    (r"\b(?:gas dryer|elect dryer|dryer|dryers)\b", "dryers"),
    (r"\b(?:washer|washers|washing machine|laundry center)\b", "washers"),
    (r"\b(?:cooktop|range|electric range|gas range|oven|wall oven)\b", "ranges"),
    (r"\b(?:fridge|refrigerator|freezer|beverage center)\b", "refrigerators"),
    (r"\b(?:microwave|otr microwave|microwave drawer)\b", "microwaves"),
    (r"\b(?:coffee maker|espresso machine|toaster|toaster oven)\b", "coffee_makers"),
    
    # Tools & Accessories
    (r"\b(?:saw blade|cut off disc|cut-off disc|cutting disc|diamond blade|track saw blade|dado)\b", "saw_blades"),
    (r"\b(?:sanding belt|sanding disc|sanding sponge|abranet|hiolit|abrasive)\b", "abrasives"),
    (r"\b(?:drill|impact driver|impact wrench|hammer drill|nailer|stapler|router|grinder|sander|planer|bandsaw|table saw|miter saw|jig saw|recip saw|circular saw)\b", "power_tools"),
    
    # Building Materials
    (r"\b(?:decking|deck board|fascia|rail kit|baluster|post sleeve|post trim|drywall|skylight|rainscreen|r-sheathing|siding|hardieplank|smart lap)\b", "decking"),
    
    # Lighting & Electrical
    (r"\b(?:led bulb|incan|candelabra|halogen|downlight|flat panel|chandelier|pendant|wall lt|wall light|bath light|ceiling lt|strip light|highbay)\b", "lighting"),
    (r"\b(?:dimmer|switch|outlet|box cover|oct box|square box|timer|wire|cable|cord|breaker|load center)\b", "electrical")
]

def classify_product(
    desc: str,
    mpn: str,
    brand: str,
    given_dept: str = "",
    given_class: str = "",
    given_fine: str = "",
    given_classpath: str = ""
) -> Tuple[str, str, str, str, str, str]:
    """
    Returns (Dept, Class, Fine, Classpath, Product Name, Category Key)
    """
    # 1. If explicit classpath is provided
    if given_classpath:
        cp = given_classpath.strip()
        dept = given_dept or (cp.split(">")[0] if ">" in cp else "Appliances")
        cls = given_class or (cp.split(">")[1] if len(cp.split(">")) > 1 else "")
        fine = given_fine or (cp.split(">")[-1] if ">" in cp else "")
        
        # Product name deduction
        pname = fine.rstrip("s")
        if "dishwasher" in cp.lower():
            pname = "Dishwasher"
        elif "dryer" in cp.lower():
            pname = "Dryer"
        elif "refrigerator" in cp.lower():
            pname = "Refrigerator"
            
        return dept, cls, fine, cp, pname, "explicit"

    # 2. Check category rules against description & MPN
    combined_text = f"{desc} {mpn} {brand}".lower()
    
    matched_cat_key = "power_tools" # default
    for pattern, cat_key in CATEGORY_RULES:
        if re.search(pattern, combined_text):
            matched_cat_key = cat_key
            break
            
    cat_info = TAXONOMIES_DATA.get(matched_cat_key, TAXONOMIES_DATA.get("dishwashers", {}))
    
    dept = given_dept or cat_info.get("dept", "Tools & Hardware")
    cls = given_class or cat_info.get("class", "Power Tools")
    fine = given_fine or cat_info.get("fine", "Accessories")
    classpath = cat_info.get("classpath", f"{dept}>{cls}>{fine}")
    product_name = cat_info.get("product_name", "Industrial Product")
    
    # Fine-tune Product Name based on specific item keywords
    if "dishwasher" in combined_text:
        product_name = "Dishwasher"
    elif "dryer" in combined_text:
        product_name = "Dryer"
    elif "washer" in combined_text and "sander" not in combined_text:
        product_name = "Washing Machine"
    elif "refrigerator" in combined_text or "fridge" in combined_text:
        product_name = "Refrigerator"
    elif "microwave" in combined_text:
        product_name = "Microwave"
    elif "saw blade" in combined_text or "cut off disc" in combined_text:
        product_name = "Saw Blade" if "saw" in combined_text else "Cut-Off Disc"
    elif "decking" in combined_text:
        product_name = "Decking Board"
    elif "fascia" in combined_text:
        product_name = "Fascia Board"
    elif "downlight" in combined_text:
        product_name = "Downlight"
    elif "chandelier" in combined_text:
        product_name = "Chandelier"
    elif "pendant" in combined_text:
        product_name = "Pendant Light"
    elif "bulb" in combined_text:
        product_name = "Bulb"
    elif "drill" in combined_text:
        product_name = "Drill Driver"
    elif "sander" in combined_text:
        product_name = "Sander"
        
    return dept, cls, fine, classpath, product_name, matched_cat_key
