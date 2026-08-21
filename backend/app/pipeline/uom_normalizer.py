"""
UOM Normalizer & Imperial Decimal-Fraction Converter.
Complies with Unilog Master UOM Standards and Decimal_Fraction.xlsx lookups.
"""
import os
import json
import re
from typing import Tuple, Optional

MASTER_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "master_data")

# Load UOM standards & fractions table
FRACTIONS_MAP = {}
fractions_path = os.path.join(MASTER_DATA_DIR, "fractions_table.json")
if os.path.exists(fractions_path):
    with open(fractions_path, "r", encoding="utf-8") as f:
        FRACTIONS_MAP = json.load(f)

UOM_SYNONYMS = {
    "inch": "in",
    "inches": "in",
    "in.": "in",
    '"': "in",
    "foot": "ft",
    "feet": "ft",
    "ft.": "ft",
    "'": "ft",
    "volt": "V",
    "volts": "V",
    "v": "V",
    "amp": "A",
    "amps": "A",
    "amperage": "A",
    "a": "A",
    "watt": "W",
    "watts": "W",
    "w": "W",
    "kelvin": "K",
    "k": "K",
    "cct": "K",
    "dba": "dBA",
    "db": "dBA",
    "grit": "Grit",
    "pack": "pk",
    "pk": "pk",
    "pc": "pc",
    "pcs": "pc",
    "piece": "pc",
    "pieces": "pc",
    "disc/box": "Disc/Box",
    "sheets/box": "Sheets/Box",
    "cf": "cu-ft",
    "cu ft": "cu-ft",
    "cu-ft": "cu-ft",
    "gauge": "GA",
    "ga": "GA",
    "tpi": "TPI",
    "ah": "Ah"
}

def decimal_to_fraction(val: float, tolerance: float = 0.01) -> str:
    """Converts a decimal number (e.g. 50.25) to standard hyphenated fraction (e.g. 50-1/4)."""
    integer_part = int(val)
    decimal_part = val - integer_part
    
    if decimal_part < 0.001:
        return str(integer_part)
        
    # Check direct lookup for standard 64ths
    best_match_frac = None
    min_diff = 1.0
    
    for num in range(1, 64):
        target_dec = num / 64.0
        diff = abs(decimal_part - target_dec)
        if diff < min_diff:
            min_diff = diff
            # Reduce fraction
            import math
            gcd = math.gcd(num, 64)
            best_match_frac = f"{num // gcd}/{64 // gcd}"
            
    if min_diff <= tolerance and best_match_frac:
        if integer_part > 0:
            return f"{integer_part}-{best_match_frac}"
        else:
            return best_match_frac
            
    # Fallback to decimal rounded to 3 digits if not cleanly reducible
    formatted_dec = f"{val:.3f}".rstrip('0').rstrip('.')
    return formatted_dec

def normalize_uom(raw_uom: str) -> str:
    """Returns canonical Unilog UOM abbreviation."""
    if not raw_uom:
        return ""
    clean = raw_uom.strip().lower()
    return UOM_SYNONYMS.get(clean, raw_uom.strip())

def format_value_with_uom(val_str: str, uom_str: str) -> str:
    """Formats value and UOM with exactly 1 space (e.g. '24 in', '120 V')."""
    val = val_str.strip()
    uom = normalize_uom(uom_str)
    if not uom:
        return val
    if not val:
        return ""
    # Avoid duplicate unit if value already ends with unit
    if val.lower().endswith(uom.lower()):
        return val
    return f"{val} {uom}"

def parse_and_standardize_dimension_string(dim_text: str) -> str:
    """
    Standardizes dimensions like '24x24-1/4' or '33-7/16H x 23-7/8W x 22-5/8D'
    to Unilog format: '24 in W x 24-1/4 in D' or '33-7/16 in H x 23-7/8 in W x 22-5/8 in D'
    """
    if not dim_text:
        return ""
    text = dim_text.replace('"', ' in ').replace("'", ' ft ')
    
    # 3D Match: (H) x (W) x (D)
    match_3d = re.search(r'([\d\.\-/]+)\s*(?:in|")?\s*([Hh])?\s*[xX]\s*([\d\.\-/]+)\s*(?:in|")?\s*([Ww])?\s*[xX]\s*([\d\.\-/]+)\s*(?:in|")?\s*([Dd])?', text)
    if match_3d:
        h, h_label, w, w_label, d, d_label = match_3d.groups()
        return f"{h} in H x {w} in W x {d} in D"
        
    # 2D Match: (W) x (D) or (Dia) x (L)
    match_2d = re.search(r'([\d\.\-/]+)\s*(?:in|")?\s*([Ww])?\s*[xX]\s*([\d\.\-/]+)\s*(?:in|")?\s*([Dd])?', text)
    if match_2d:
        w, w_label, d, d_label = match_2d.groups()
        return f"{w} in W x {d} in D"
        
    return dim_text.strip()
