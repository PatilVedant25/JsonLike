"""
Canonical list of all 252 Delivery Format columns in exact ground-truth order.
"""

DELIVERY_COLUMNS = [
    # 1 - 6: Reference & Sourcing URLs
    "MFR URL",
    "Ref URL 1",
    "Ref URL 2",
    "Ref URL 3",
    "Ref URL 4",
    "Ref URL 5",
    # 7 - 11: Taxonomy & Internal Keys
    "PART_NUMBER",
    "Dept",
    "Class",
    "Fine",
    "SKU - MY_PART_NUMBER",
    # 12 - 17: Raw Input Echo
    "Mfg_Part_Num",
    "Part_Desc",
    "E1_Brand",
    "Unilog_Brand",
    "DIB_Brand",
    "Part_Manuf",
    # 18 - 23: Master Entities & Taxonomy
    "MANUFACTURER_NAME",
    "BRAND_NAME",
    "TRADE_NAME",
    "MANUFACTURER_PART_NUMBER",
    "ALTERNATE_PART_NUMBER",
    "Classpath",
    # 24 - 29: Multi-Tier Content Descriptions
    "MOBILE_DESC",
    "INVOICE_DESC",
    "SHORT_DESC",
    "LONG_DESC1",
    "RETAIL_DESC",
    "MARKETING_DESCRIPTION",
    # 30 - 49: Item Features (1 - 20)
    "ITEM_FEATURES_1",
    "ITEM_FEATURES_2",
    "ITEM_FEATURES_3",
    "ITEM_FEATURES_4",
    "ITEM_FEATURES_5",
    "ITEM_FEATURES_6",
    "ITEM_FEATURES_7",
    "ITEM_FEATURES_8",
    "ITEM_FEATURES_9",
    "ITEM_FEATURES_10",
    "ITEM_FEATURES_11",
    "ITEM_FEATURES_12",
    "ITEM_FEATURES_13",
    "ITEM_FEATURES_14",
    "ITEM_FEATURES_15",
    "ITEM_FEATURES_16",
    "ITEM_FEATURES_17",
    "ITEM_FEATURES_18",
    "ITEM_FEATURES_19",
    "ITEM_FEATURES_20",
    # 50 - 55: Qualifiers & Classification
    "With",
    "Standard/Approvals",
    "Prop 65",
    "Application",
    "Includes",
    "Product Name",
]

# Add 50 Attribute Trios (Columns 56 - 205)
for i in range(1, 51):
    DELIVERY_COLUMNS.extend([
        f"ATTRIBUTE_LABEL {i}",
        f"ATTRIBUTE_VALUE {i}",
        f"ATTRIBUTE_UOM {i}"
    ])

# 206 - 252: Identifiers, Packaging, Physical Specs, Assets & Compliance
DELIVERY_COLUMNS.extend([
    # Identifiers & Trade
    "UPC",
    "EAN",
    "GTIN",
    "UNSPSC",
    "Warranty",
    "List Price",
    "Selling Qty",
    "Selling UOM",
    "Standard Packaging Information",
    # Physical Dimensions & UOMs
    "LENGTH",
    "LENGTH_UOM",
    "HEIGHT",
    "HEIGHT_UOM",
    "WIDTH",
    "WIDTH_UOM",
    "WEIGHT",
    "WEIGHT_UOM",
    "VOLUME",
    "VOLUME_UOM",
    # Digital Assets
    "Product Image",
    "Alternate Image 1",
    "Alternate Image 2",
    "Alternate Image 3",
    "Alternate Image 4",
    "SDS",
    "SDS_1",
    "Warranty Information",
    "Catalog",
    "Specification Sheet",
    "Instruction/Installation Manual",
    "Service Manual",
    "Owners/User Manual",
    "Line Drawing",
    "MTR",
    "RoHS",
    "Full Engineering Drawing",
    "Energy Star Guide",
    "Technical Bulletin",
    "Submittal",
    "Compatibility Chart",
    "Size Chart",
    "Product Label/Insert",
    "Video Link",
    "Video Link 1",
    # Regulatory & Status
    "Country Of Origin",
    "Discontinued",
    "Actual Image (Yes/No)"
])

assert len(DELIVERY_COLUMNS) == 252, f"Expected exactly 252 columns, got {len(DELIVERY_COLUMNS)}"
