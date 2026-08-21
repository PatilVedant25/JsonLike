"""
Export Service for 252-Column Delivery Format.
Exports enriched records directly to CSV and Excel (XLSX) format.
"""
import os
import pandas as pd
from typing import List, Dict, Any
from app.models.delivery_columns import DELIVERY_COLUMNS
from app.models.schema import EnrichedProduct

def export_to_csv(products: List[EnrichedProduct], output_path: str) -> str:
    """Exports list of EnrichedProduct objects to 252-column CSV."""
    rows = [p.delivery_row for p in products]
    df = pd.DataFrame(rows, columns=DELIVERY_COLUMNS)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path

def export_to_excel(products: List[EnrichedProduct], output_path: str) -> str:
    """Exports list of EnrichedProduct objects to 252-column Excel XLSX."""
    rows = [p.delivery_row for p in products]
    df = pd.DataFrame(rows, columns=DELIVERY_COLUMNS)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    df.to_excel(output_path, index=False, engine="openpyxl")
    return output_path
