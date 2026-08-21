"""
Digital Asset & Sourcing URL Manager.
Constructs canonical asset filenames (Images, Spec Sheets, SDS, Manuals) and direct OEM URLs.
"""
import re
from typing import Dict, Any, List, Tuple

OEM_URL_TEMPLATES = {
    "frigidaire": "https://www.frigidaire.com/en/p/owner-center/product-support/{mpn}",
    "whirlpool": "https://learnwhirlpool.com/smartsearchresults?searchtext={mpn}",
    "kitchenaid": "https://www.kitchenaid.com/search.html?text={mpn}",
    "ge": "https://www.geappliances.com/appliance/specs/{mpn}",
    "lg": "https://www.lg.com/us/support/product/{mpn}",
    "cafe": "https://www.cafeappliances.com/appliances/{mpn}/specs",
    "speed queen": "https://speedqueen.com/products/{mpn}",
    "milwaukee": "https://www.milwaukeetool.com/Products/{mpn}",
    "diablo": "https://www.diablotools.com/products/{mpn}",
    "dewalt": "https://www.dewalt.com/product/{mpn}",
    "makita": "https://www.makitatools.com/products/details/{mpn}",
    "festool": "https://www.festoolusa.com/products/{mpn}",
    "trex": "https://www.trex.com/products/{mpn}",
    "timbertech": "https://www.timbertech.com/products/{mpn}",
    "satco": "https://www.satco.com/products/{mpn}",
    "philips": "https://www.lighting.philips.com/main/prof/{mpn}",
    "leviton": "https://www.leviton.com/en/products/{mpn}"
}

def sanitize_filename_brand(brand_name: str) -> str:
    """Extracts a clean uppercase brand prefix for digital asset filenames."""
    clean = brand_name.replace("®", "").replace("™", "").replace(" ", "").strip().upper()
    return clean or "PRODUCT"

def build_digital_assets(brand_name: str, mpn: str) -> Dict[str, Any]:
    """
    Generates standard Unilog digital asset filenames and OEM URLs.
    """
    brand_prefix = sanitize_filename_brand(brand_name)
    clean_mpn = mpn.replace("/", "_").replace(" ", "_")
    
    # Base canonical name: BRAND_MPN
    base_name = f"{brand_prefix}_{clean_mpn}"
    
    # MFR URL
    mfr_url = ""
    brand_lower = brand_name.lower()
    for key, template in OEM_URL_TEMPLATES.items():
        if key in brand_lower:
            mfr_url = template.format(mpn=clean_mpn)
            break
            
    if not mfr_url:
        mfr_url = f"https://www.manufacturer.com/products/{clean_mpn}"
        
    # Spec sheet & images
    spec_sheet = f"{base_name}_Specification_Sheet.pdf"
    prod_image = f"{base_name}.jpg"
    alt_images = [f"{base_name}_{i}.jpg" for i in range(1, 5)]
    
    return {
        "mfr_url": mfr_url,
        "product_image": prod_image,
        "alternate_images": alt_images,
        "specification_sheet": spec_sheet,
        "actual_image": "Yes"
    }
