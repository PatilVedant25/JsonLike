"""
Benchmark & Accuracy Evaluation Service.
Computes field-by-field accuracy, character limit compliance, and match breakdown against ground truth.
"""
import pandas as pd
from typing import Dict, Any, List, Tuple
from rapidfuzz import fuzz
from app.models.delivery_columns import DELIVERY_COLUMNS
from app.models.schema import RawProductInput, BenchmarkSummary, FieldScore
from app.pipeline.orchestrator import EnrichmentPipeline

def clean_str(val: Any) -> str:
    if pd.isna(val) or val is None:
        return ""
    return str(val).strip()

def evaluate_ground_truth(ground_truth_csv: str) -> BenchmarkSummary:
    """
    Evaluates the pipeline against a labelled ground truth dataset.
    """
    df_gt = pd.read_csv(ground_truth_csv)
    pipeline = EnrichmentPipeline()
    
    total_samples = len(df_gt)
    field_stats: Dict[str, Dict[str, int]] = {col: {"exact": 0, "partial": 0, "total": 0} for col in DELIVERY_COLUMNS}
    
    invoice_compliant_count = 0
    mobile_compliant_count = 0
    title_compliant_count = 0
    brand_exact_count = 0
    mfr_exact_count = 0
    classpath_exact_count = 0
    total_attrs_possible = total_samples * 15 # Top 15 primary attributes
    total_attrs_filled = 0
    
    for _, row in df_gt.iterrows():
        # Build RawProductInput
        raw_input = RawProductInput(
            Mfg_Part_Num=clean_str(row.get("Mfg_Part_Num")),
            Part_Desc=clean_str(row.get("Part_Desc")),
            E1_Brand=clean_str(row.get("E1_Brand")),
            Unilog_Brand=clean_str(row.get("Unilog_Brand")),
            DIB_Brand=clean_str(row.get("DIB_Brand")),
            Part_Manuf=clean_str(row.get("Part_Manuf")),
            PART_NUMBER=clean_str(row.get("PART_NUMBER")),
            Dept=clean_str(row.get("Dept")),
            Class=clean_str(row.get("Class")),
            Fine=clean_str(row.get("Fine")),
            SKU=clean_str(row.get("SKU - MY_PART_NUMBER"))
        )
        
        enriched = pipeline.enrich_product(raw_input)
        pred_row = enriched.delivery_row
        
        # Rule Compliance checks
        inv = pred_row.get("INVOICE_DESC", "")
        if len(inv) <= 40 and inv == inv.upper():
            invoice_compliant_count += 1
            
        mob = pred_row.get("MOBILE_DESC", "")
        if 60 <= len(mob) <= 80:
            mobile_compliant_count += 1
            
        title = pred_row.get("SHORT_DESC", "")
        if clean_str(row.get("BRAND_NAME")) in title:
            title_compliant_count += 1
            
        if clean_str(pred_row.get("BRAND_NAME")) == clean_str(row.get("BRAND_NAME")):
            brand_exact_count += 1
            
        if clean_str(pred_row.get("MANUFACTURER_NAME")) == clean_str(row.get("MANUFACTURER_NAME")):
            mfr_exact_count += 1
            
        if clean_str(pred_row.get("Classpath")) == clean_str(row.get("Classpath")):
            classpath_exact_count += 1
            
        # Check field by field
        for col in DELIVERY_COLUMNS:
            gt_val = clean_str(row.get(col))
            pred_val = clean_str(pred_row.get(col))
            
            if gt_val:
                field_stats[col]["total"] += 1
                if pred_val == gt_val:
                    field_stats[col]["exact"] += 1
                elif fuzz.ratio(pred_val.lower(), gt_val.lower()) >= 80:
                    field_stats[col]["partial"] += 1
                    
        # Count attribute fill rate
        for i in range(1, 16):
            if pred_row.get(f"ATTRIBUTE_LABEL {i}") and pred_row.get(f"ATTRIBUTE_VALUE {i}"):
                total_attrs_filled += 1
                
    # Aggregate breakdown
    field_breakdown = []
    total_evaluated_fields = 0
    total_exact_matches = 0
    
    for col, stat in field_stats.items():
        if stat["total"] > 0:
            total_evaluated_fields += stat["total"]
            total_exact_matches += stat["exact"]
            rate = round((stat["exact"] + 0.5 * stat["partial"]) / stat["total"] * 100.0, 1)
            field_breakdown.append(FieldScore(
                field_name=col,
                match_rate=rate,
                total_scored=stat["total"],
                exact_matches=stat["exact"],
                partial_matches=stat["partial"]
            ))
            
    overall_acc = round((total_exact_matches / max(1, total_evaluated_fields)) * 100.0, 1)
    
    return BenchmarkSummary(
        total_samples=total_samples,
        overall_accuracy=overall_acc,
        invoice_desc_compliance=round((invoice_compliant_count / total_samples) * 100.0, 1),
        mobile_desc_compliance=round((mobile_compliant_count / total_samples) * 100.0, 1),
        title_compliance=round((title_compliant_count / total_samples) * 100.0, 1),
        brand_accuracy=round((brand_exact_count / total_samples) * 100.0, 1),
        manufacturer_accuracy=round((mfr_exact_count / total_samples) * 100.0, 1),
        classpath_accuracy=round((classpath_exact_count / total_samples) * 100.0, 1),
        attribute_fill_rate=round((total_attrs_filled / max(1, total_attrs_possible)) * 100.0, 1),
        field_breakdown=field_breakdown
    )
