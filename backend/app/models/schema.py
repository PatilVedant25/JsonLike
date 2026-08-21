from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

class RawProductInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    Mfg_Part_Num: Optional[str] = ""
    Part_Desc: str
    E1_Brand: Optional[str] = ""
    Unilog_Brand: Optional[str] = ""
    DIB_Brand: Optional[str] = ""
    Part_Manuf: Optional[str] = ""
    # Optional metadata if present in input sheet
    PART_NUMBER: Optional[str] = ""
    Dept: Optional[str] = ""
    Class: Optional[str] = ""
    Fine: Optional[str] = ""
    SKU: Optional[str] = Field(default="", alias="SKU - MY_PART_NUMBER")

class AttributeTrio(BaseModel):
    index: int
    label: str
    value: str
    uom: Optional[str] = ""

class ProvenanceRecord(BaseModel):
    field: str
    source_method: str
    raw_evidence: Optional[str] = ""
    confidence: float = 1.0
    notes: Optional[str] = ""

class EnrichedProduct(BaseModel):
    mfg_part_num: str
    part_desc: str
    clean_part_desc: str
    manufacturer_name: str
    brand_name: str
    trade_name: Optional[str] = ""
    manufacturer_part_number: str
    alternate_part_number: Optional[str] = ""
    dept: str
    class_name: str
    fine: str
    classpath: str
    product_name: str
    
    # Descriptions
    invoice_desc: str
    mobile_desc: str
    short_desc: str
    long_desc1: str
    retail_desc: str
    marketing_description: str
    item_features: List[str] = []
    
    # Qualifiers
    with_features: Optional[str] = ""
    standard_approvals: Optional[str] = ""
    prop_65: Optional[str] = ""
    application: Optional[str] = ""
    includes: Optional[str] = ""
    
    # Attributes (up to 50)
    attributes: List[AttributeTrio] = []
    
    # Identifiers & Physical Specs
    upc: Optional[str] = ""
    ean: Optional[str] = ""
    gtin: Optional[str] = ""
    unspsc: Optional[str] = ""
    warranty: Optional[str] = ""
    list_price: Optional[str] = ""
    selling_qty: Optional[str] = ""
    selling_uom: Optional[str] = ""
    standard_packaging: Optional[str] = ""
    length: Optional[str] = ""
    length_uom: Optional[str] = ""
    height: Optional[str] = ""
    height_uom: Optional[str] = ""
    width: Optional[str] = ""
    width_uom: Optional[str] = ""
    weight: Optional[str] = ""
    weight_uom: Optional[str] = ""
    volume: Optional[str] = ""
    volume_uom: Optional[str] = ""
    
    # Digital Assets
    mfr_url: Optional[str] = ""
    ref_urls: List[str] = []
    product_image: Optional[str] = ""
    alternate_images: List[str] = []
    specification_sheet: Optional[str] = ""
    owners_manual: Optional[str] = ""
    sds: Optional[str] = ""
    sds_1: Optional[str] = ""
    actual_image: str = "Yes"
    
    # Quality & Explainability
    confidence_score: float = 0.0
    needs_human_review: bool = False
    review_reasons: List[str] = []
    provenance: List[ProvenanceRecord] = []
    
    # 252 Delivery row map
    delivery_row: Dict[str, Any] = {}

class BatchProcessRequest(BaseModel):
    items: List[RawProductInput]

class BatchProcessResponse(BaseModel):
    total_processed: int
    success_count: int
    review_needed_count: int
    average_confidence: float
    results: List[EnrichedProduct]

class FieldScore(BaseModel):
    field_name: str
    match_rate: float
    total_scored: int
    exact_matches: int
    partial_matches: int

class BenchmarkSummary(BaseModel):
    total_samples: int
    overall_accuracy: float
    invoice_desc_compliance: float
    mobile_desc_compliance: float
    title_compliance: float
    brand_accuracy: float
    manufacturer_accuracy: float
    classpath_accuracy: float
    attribute_fill_rate: float
    field_breakdown: List[FieldScore] = []
