"""
Pipeline Cleaner & Preprocessor:
- Filters out placeholder values ('-- Unbranded --', '-- No Unilog Brand --', '-- No DIB Brand --', '-', 'null')
- Extracts MPN from description if missing
- Normalizes token spaces, quotes, and common abbreviations
"""
import re
from typing import Dict, Any, Tuple

PLACEHOLDERS = {
    "-- unbranded --",
    "-- no unilog brand --",
    "-- no dib brand --",
    "unbranded",
    "no brand",
    "-",
    "null",
    "none",
    "n/a",
    ""
}

ABBREVIATIONS = {
    r"\bSS\b": "Stainless Steel",
    r"\bSST\b": "Stainless Steel",
    r"\bBSS\b": "Black Stainless Steel",
    r"\bWh\b": "White",
    r"\bWH\b": "White",
    r"\bWHT\b": "White",
    r"\bBk\b": "Black",
    r"\bBK\b": "Black",
    r"\bBLK\b": "Black",
    r"\bLA\b": "Light Almond",
    r"\bMB\b": "Matte Black",
    r"\bMW\b": "Matte White",
    r"\bBN\b": "Brushed Nickel",
    r"\bNI\b": "Brushed Nickel",
    r"\bCH\b": "Chrome",
    r"\bCPZ\b": "Champagne Bronze",
    r"\bDBZ\b": "Dark Bronze",
    r"\bElect\b": "Electric",
    r"\bSq\b": "Square",
    r"\bRd\b": "Round",
    r"\bAlm\b": "Aluminum",
    r"\bAlum\b": "Aluminum",
    r"\bHoriz\b": "Horizontal",
    r"\bHor\b": "Horizontal",
    r"\bStr\b": "Stair",
    r"\bMed\b": "Medium Base",
    r"\bCand\b": "Candelabra",
    r"\bIncan\b": "Incandescent",
    r"\bFlor\b": "Fluorescent",
    r"\bCirc\b": "Circular",
    r"\bOTR\b": "Over-the-Range",
    r"\bCF\b": "cu-ft",
    r"\bLt\b": "Light",
    r"\bSq Edg\b": "Square Edge",
    r"\bSq Edge\b": "Square Edge",
    r"\bGroov\b": "Grooved",
    r"\bGroove\b": "Grooved"
}

def clean_placeholder(val: Any) -> str:
    """Returns empty string if value is a placeholder, else stripped string."""
    if val is None:
        return ""
    s = str(val).strip()
    if s.lower() in PLACEHOLDERS:
        return ""
    return s

def clean_description(raw_desc: str) -> str:
    """Normalizes whitespace and standard quotes in description."""
    if not raw_desc:
        return ""
    # Clean double double-quotes from CSV escapes
    text = raw_desc.replace('""', '"').strip()
    # Normalize excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_mpn_and_desc(raw_mpn: str, raw_desc: str) -> Tuple[str, str]:
    """Ensures a clean MPN is extracted and paired with a sanitized description."""
    mpn = clean_placeholder(raw_mpn)
    desc = clean_description(raw_desc)
    
    # If MPN is empty but description starts with an alphanumeric token
    if not mpn and desc:
        match = re.match(r'^([A-Z0-9\-\./_]+)\b', desc)
        if match:
            potential_mpn = match.group(1)
            # Check if it looks like a valid part number (has letters and numbers or dashes)
            if len(potential_mpn) >= 3:
                mpn = potential_mpn
                
    # If description starts with MPN, we keep it but know the clean suffix
    return mpn, desc

def expand_abbreviations(text: str) -> str:
    """Expands shorthand technical words to standardized catalog vocabulary."""
    result = text
    for pattern, replacement in ABBREVIATIONS.items():
        result = re.sub(pattern, replacement, result)
    return result
