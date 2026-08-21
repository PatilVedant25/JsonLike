"""
Delivery Schema Validator & Quality Assurance Engine.
Enforces 252-column delivery constraints, casing rules, character limits, and review flags.
"""
from typing import Dict, Any, List, Tuple
from app.models.delivery_columns import DELIVERY_COLUMNS

def validate_enriched_product(delivery_row: Dict[str, Any]) -> Tuple[float, bool, List[str]]:
    """
    Validates a 252-column delivery dictionary.
    Returns:
    - confidence_score (0.0 to 100.0)
    - needs_human_review (bool)
    - review_reasons (List[str])
    """
    reasons = []
    score = 100.0
    
    # 1. Check Mandatory Fields
    mandatory_fields = [
        "MANUFACTURER_NAME",
        "BRAND_NAME",
        "Classpath",
        "INVOICE_DESC",
        "MOBILE_DESC",
        "SHORT_DESC",
        "LONG_DESC1"
    ]
    
    for f in mandatory_fields:
        val = delivery_row.get(f, "")
        if not val or str(val).strip() == "":
            reasons.append(f"Missing mandatory field: {f}")
            score -= 15.0
            
    # 2. Check INVOICE_DESC rules (<=40 chars, UPPERCASE)
    inv = delivery_row.get("INVOICE_DESC", "")
    if inv:
        if len(inv) > 40:
            reasons.append(f"INVOICE_DESC exceeds 40 chars ({len(inv)} chars)")
            score -= 10.0
        if inv != inv.upper():
            reasons.append("INVOICE_DESC must be in all-uppercase")
            score -= 5.0
            
    # 3. Check MOBILE_DESC rules (60-80 chars)
    mob = delivery_row.get("MOBILE_DESC", "")
    if mob:
        if len(mob) < 60 or len(mob) > 80:
            reasons.append(f"MOBILE_DESC outside 60-80 char guideline ({len(mob)} chars)")
            score -= 5.0
            
    # 4. Check Brand & Legal symbols
    brand = delivery_row.get("BRAND_NAME", "")
    if brand:
        if "®" not in brand and "™" not in brand:
            # Not all brands have symbols, but standard Unilog brands do
            score -= 2.0
            
    # 5. Check Attribute Coverage
    filled_attrs = sum(1 for i in range(1, 51) if delivery_row.get(f"ATTRIBUTE_LABEL {i}"))
    if filled_attrs < 3:
        reasons.append(f"Low attribute extraction depth ({filled_attrs} attributes)")
        score -= 10.0
        
    score = max(0.0, min(100.0, score))
    needs_review = score < 85.0 or len(reasons) > 0
    
    return round(score, 1), needs_review, reasons

def construct_delivery_row_dictionary(fields_map: Dict[str, Any]) -> Dict[str, Any]:
    """Ensures every single one of the 252 delivery columns exists in exact canonical order."""
    row = {}
    for col in DELIVERY_COLUMNS:
        row[col] = fields_map.get(col, "")
    return row
