"""
Entity Resolver & Master Data Normalizer.
Resolves messy supplier strings, manufacturer names, and MPN patterns to canonical
MANUFACTURER_NAME, BRAND_NAME, and TRADE_NAME with legal casing and ® / ™ symbols.
"""
import os
import json
import re
from typing import Dict, Any, Tuple, Optional
from rapidfuzz import process, fuzz

MASTER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "master_data")

MANUFACTURERS_DATA = {}
mfr_path = os.path.join(MASTER_DATA_DIR, "manufacturers.json")
if os.path.exists(mfr_path):
    with open(mfr_path, "r", encoding="utf-8") as f:
        MANUFACTURERS_DATA = json.load(f)

# Direct brand aliases
BRAND_LOOKUP = {
    "milwaukee": ("Milwaukee Electric Tool Corporation", "Milwaukee®"),
    "milw": ("Milwaukee Electric Tool Corporation", "Milwaukee®"),
    "diablo": ("Freud America, Inc.", "Diablo®"),
    "freud": ("Freud America, Inc.", "Diablo®"),
    "3m": ("3M Company", "3M®"),
    "mirka": ("Mirka Abrasives, Inc.", "Mirka®"),
    "dewalt": ("Stanley Black & Decker, Inc.", "DEWALT®"),
    "makita": ("Makita U.S.A., Inc.", "Makita®"),
    "festool": ("Festool USA", "Festool®"),
    "kreg": ("Kreg Tool Company", "Kreg®"),
    "philips": ("Signify North America Corporation", "Philips®"),
    "wiz": ("Signify North America Corporation", "WiZ®"),
    "satco": ("Satco Products, Inc.", "Satco®"),
    "nuvo": ("Satco Products, Inc.", "Nuvo®"),
    "kichler": ("Kichler Lighting LLC", "Kichler®"),
    "leviton": ("Leviton Manufacturing Co., Inc.", "Leviton®"),
    "southwire": ("Southwire Company, LLC", "Southwire®"),
    "trex": ("Trex Company, Inc.", "Trex®"),
    "timbertech": ("The AZEK Company LLC", "TimberTech®"),
    "azek": ("The AZEK Company LLC", "AZEK®"),
    "hunter": ("Hunter Fan Company", "Hunter®"),
    "edge": ("Edge Eyewear Inc.", "Edge®"),
    "wera": ("Wera Tools Inc.", "Wera®"),
    "vessel": ("Vessel Tools USA, Inc.", "Vessel®"),
    "marshalltown": ("Marshalltown Company", "Marshalltown®"),
    "wal-board": ("Marshalltown Company", "Wal-Board®"),
    "senco": ("KYOCERA Senco Industrial Tools, Inc.", "Senco®"),
    "paslode": ("National Nail Corp.", "Paslode®"),
    "amana": ("Amana Tool Corporation", "Amana Tool®"),
    "whiteside": ("Whiteside Machine Company", "Whiteside®"),
    "oliver": ("Oliver Machinery Company", "Oliver®"),
    "jet": ("JPW Industries Inc.", "JET®"),
    "sawstop": ("SawStop LLC", "SawStop®"),
    "grizzly": ("Woodstock International, Inc.", "Grizzly®"),
    "certainteed": ("CertainTeed Corporation", "CertainTeed®"),
    "zip system": ("Huber Engineered Woods LLC", "ZIP System®"),
    "james hardie": ("James Hardie Building Products Inc.", "James Hardie®"),
    "smartside": ("Louisiana-Pacific Corporation", "LP® SmartSide®"),
    "lp": ("Louisiana-Pacific Corporation", "LP® SmartSide®"),
    "speed queen": ("Alliance Laundry Systems LLC", "Speed Queen®"),
    "frigidaire": ("Rheem Manufacturing", "FRIGIDAIRE®"),
    "whirlpool": ("Whirlpool Corporation", "Whirlpool®"),
    "kitchenaid": ("Whirlpool Corporation", "KitchenAid®"),
    "ge": ("Haier US Appliance Solutions, Inc.", "GE®"),
    "lg": ("LG Electronics Inc.", "LG®"),
    "cafe": ("Haier US Appliance Solutions, Inc.", "Café™"),
    "café": ("Haier US Appliance Solutions, Inc.", "Café™"),
    "beko": ("Beko US Inc.", "Beko®"),
    "element": ("Element Electronics", "Element®"),
    "sharp": ("Sharp Electronics Corporation", "Sharp®"),
    "xo": ("XO Appliance", "XO®")
}

def resolve_cooperative_or_distributor(manuf_str: str, mpn: str, desc: str) -> Optional[Tuple[str, str, str]]:
    """Special handler for cooperatives like Appliance Dealers Cooperative (APPDE)."""
    if "appliance dealers cooperative" in manuf_str.lower() or "appde" in manuf_str.lower():
        appde_info = MANUFACTURERS_DATA.get("APPDE", {})
        patterns = appde_info.get("patterns", [])
        
        mpn_upper = mpn.upper()
        desc_upper = desc.upper()
        
        for p in patterns:
            prefix = p["prefix"]
            if mpn_upper.startswith(prefix) or desc_upper.startswith(prefix):
                return p["manufacturer"], p["brand"], p.get("series", "")
                
        # Check description text for brand mentions
        if "FRIGIDAIRE" in desc_upper:
            return "Rheem Manufacturing", "FRIGIDAIRE®", "Professional Series"
        elif "WHIRLPOOL" in desc_upper:
            return "Whirlpool Corporation", "Whirlpool®", "Eco Series"
        elif "KITCHEN AID" in desc_upper or "KITCHENAID" in desc_upper:
            return "Whirlpool Corporation", "KitchenAid®", "Architect Series"
        elif "SPEED QUEEN" in desc_upper or "SQ " in desc_upper:
            return "Alliance Laundry Systems LLC", "Speed Queen®", ""
        elif "LG " in desc_upper:
            return "LG Electronics Inc.", "LG®", ""
        elif "CAF" in desc_upper:
            return "Haier US Appliance Solutions, Inc.", "Café™", ""
        elif "GE " in desc_upper or "GE." in desc_upper:
            return "Haier US Appliance Solutions, Inc.", "GE®", ""
        elif "BEKO" in desc_upper:
            return "Beko US Inc.", "Beko®", ""
            
    return None

def resolve_entity(part_manuf: str, e1_brand: str, unilog_brand: str, dib_brand: str, mpn: str, desc: str) -> Tuple[str, str, str, str]:
    """
    Returns (MANUFACTURER_NAME, BRAND_NAME, TRADE_NAME, SERIES)
    """
    clean_manuf = part_manuf.strip() if part_manuf else ""
    clean_e1 = e1_brand.strip() if e1_brand else ""
    clean_unilog = unilog_brand.strip() if unilog_brand else ""
    clean_dib = dib_brand.strip() if dib_brand else ""
    
    # 1. Check Cooperative patterns first (highest precision for APPDE)
    if clean_manuf:
        coop_res = resolve_cooperative_or_distributor(clean_manuf, mpn, desc)
        if coop_res:
            mfr, brand, series = coop_res
            return mfr, brand, "", series
            
    # 2. Check direct manufacturer entries in Master Data
    if clean_manuf in MANUFACTURERS_DATA:
        entry = MANUFACTURERS_DATA[clean_manuf]
        mfr_name = entry.get("manufacturer", clean_manuf)
        brand_name = entry.get("brand", clean_manuf)
        
        # Check series keywords in description
        series = ""
        desc_upper = desc.upper()
        for kw, series_val in entry.get("series_keywords", {}).items():
            if kw in desc_upper or kw in mpn.upper():
                series = series_val
                break
        return mfr_name, brand_name, "", series
        
    # 3. Check explicit brand fields if populated
    for candidate in [clean_unilog, clean_e1, clean_dib]:
        if candidate and candidate.lower() not in ["-- unbranded --", "-- no unilog brand --", "-- no dib brand --", "-"]:
            cand_clean = candidate.lower().replace("®", "").replace("™", "").strip()
            if cand_clean in BRAND_LOOKUP:
                mfr_name, brand_name = BRAND_LOOKUP[cand_clean]
                return mfr_name, brand_name, "", ""
                
    # 4. Check description keywords against known brands
    desc_clean = desc.lower()
    for brand_key, (mfr_name, brand_name) in BRAND_LOOKUP.items():
        if re.search(r'\b' + re.escape(brand_key) + r'\b', desc_clean):
            return mfr_name, brand_name, "", ""
            
    # 5. Fuzzy match on clean_manuf
    if clean_manuf and clean_manuf != "-":
        manuf_keys = list(MANUFACTURERS_DATA.keys())
        match = process.extractOne(clean_manuf, manuf_keys, scorer=fuzz.token_sort_ratio)
        if match and match[1] >= 80:
            entry = MANUFACTURERS_DATA[match[0]]
            return entry.get("manufacturer", clean_manuf), entry.get("brand", clean_manuf), "", ""
            
    # Fallback to sanitized raw manufacturer
    mfr_fallback = re.sub(r'\s*\([^\)]*\)', '', clean_manuf).strip() if clean_manuf and clean_manuf != "-" else "Unassigned Manufacturer"
    brand_fallback = mfr_fallback
    return mfr_fallback, brand_fallback, "", ""
