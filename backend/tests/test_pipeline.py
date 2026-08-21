"""
Unit Tests for Enrichment Pipeline Stages.
"""
import pytest
from app.models.schema import RawProductInput
from app.pipeline.cleaner import clean_placeholder, extract_mpn_and_desc, expand_abbreviations
from app.pipeline.uom_normalizer import decimal_to_fraction, normalize_uom, format_value_with_uom
from app.pipeline.entity_resolver import resolve_entity
from app.pipeline.classifier import classify_product
from app.pipeline.orchestrator import EnrichmentPipeline
from app.models.delivery_columns import DELIVERY_COLUMNS

def test_clean_placeholder():
    assert clean_placeholder("-- Unbranded --") == ""
    assert clean_placeholder("-- No Unilog Brand --") == ""
    assert clean_placeholder("-- No DIB Brand --") == ""
    assert clean_placeholder("-") == ""
    assert clean_placeholder("DEWALT") == "DEWALT"

def test_decimal_to_fraction():
    assert decimal_to_fraction(50.25) == "50-1/4"
    assert decimal_to_fraction(0.5) == "1/2"
    assert decimal_to_fraction(33.4375) == "33-7/16"
    assert decimal_to_fraction(24.0) == "24"

def test_uom_normalization():
    assert normalize_uom("inches") == "in"
    assert normalize_uom("volts") == "V"
    assert normalize_uom("amps") == "A"
    assert format_value_with_uom("120", "V") == "120 V"
    assert format_value_with_uom("15", "A") == "15 A"

def test_entity_resolution():
    mfr, brand, trade, series = resolve_entity(
        part_manuf="Appliance Dealers Cooperative (APPDE)",
        e1_brand="-- Unbranded --",
        unilog_brand="",
        dib_brand="",
        mpn="PDSH4816AF",
        desc="PDSH4816AF Dishwasher SS - Display Only"
    )
    assert "FRIGIDAIRE" in brand
    assert "Rheem" in mfr

def test_252_column_delivery_completeness():
    pipeline = EnrichmentPipeline()
    raw = RawProductInput(
        Mfg_Part_Num="PDSH4816AF",
        Part_Desc="PDSH4816AF Dishwasher SS - Display Only",
        Part_Manuf="Appliance Dealers Cooperative (APPDE)",
        Dept="Appliances",
        Class="Large Appliances",
        Fine="Dishwashers",
        SKU="1515863",
        PART_NUMBER="20887830"
    )
    res = pipeline.enrich_product(raw)
    
    assert len(res.delivery_row) == 252
    assert res.delivery_row["MANUFACTURER_PART_NUMBER"] == "PDSH4816AF"
    assert res.delivery_row["INVOICE_DESC"] == res.delivery_row["INVOICE_DESC"].upper()
    assert len(res.delivery_row["INVOICE_DESC"]) <= 40
    assert 60 <= len(res.delivery_row["MOBILE_DESC"]) <= 80
    assert res.delivery_row["Product Image"] == "FRIGIDAIRE_PDSH4816AF.jpg"
    assert res.delivery_row["Specification Sheet"] == "FRIGIDAIRE_PDSH4816AF_Specification_Sheet.pdf"
