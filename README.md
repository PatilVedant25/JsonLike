# AI-Powered Product Intelligence for Industrial Commerce (UniCat 2.0)

An end-to-end industrial product data enrichment, entity resolution, multi-tier description synthesis, and 252-column delivery compliance platform built for industrial distributors and e-commerce catalogs.

---

## Key Features & Highlights

1. **252-Column Unilog Delivery Compliance**:
   - Generates exact 252-column delivery format schema conforming to ground truth specifications.
   - Standardizes 50 structured attribute trios (`ATTRIBUTE_LABEL`, `ATTRIBUTE_VALUE`, `ATTRIBUTE_UOM`) aligned with category LOVs.
2. **Master Entity Resolution & Trademark Normalization**:
   - Resolves messy supplier spellings (e.g. `Appliance Dealers Cooperative (APPDE)`, `Freud Inc (2435)`, `Milwaukee Accessory (4031)`) to canonical corporate manufacturers and registered trademark brands (`FRIGIDAIRE®`, `Whirlpool®`, `Diablo®`, `Milwaukee®`, `DEWALT®`, `Café™`).
3. **Master UOM & Decimal-to-Fraction Engine**:
   - Converts manufacturer decimal measurements to trade fractions (e.g., `50.25 in → 50-1/4 in`, `0.5 in → 1/2 in`).
   - Enforces single-space UOM notation (`24 in`, `120 V`, `15 A`, `47 dBA`).
4. **Multi-Tier Content Description Construction**:
   - **`INVOICE_DESC`**: $\le 40$ characters, strict ALL-CAPS POS abbreviation format.
   - **`MOBILE_DESC`**: $60\text{–}80$ characters, mobile catalog summary format.
   - **`SHORT_DESC` (Product Title)**: Formula: `Brand® + Series + MPN + Product Name + Features`.
   - **`LONG_DESC1`**: Comprehensive e-commerce specification copy.
   - **`RETAIL_DESC` & `MARKETING_DESCRIPTION`**: Consumer marketing copy.
   - **`ITEM_FEATURES_1..20`**: Structured feature bullets.
5. **Digital Assets & OEM Sourcing**:
   - Canonical naming (`BRAND_MPN.jpg`, `BRAND_MPN_Specification_Sheet.pdf`).
   - Direct OEM URL generation excluding third-party marketplaces.
6. **Explainability & Provenance Audit Trail**:
   - Tracks per-field provenance method, raw evidence, and confidence score.
   - Automated review flag triggering (`needs_human_review`).
7. **High-Throughput Batch Processing & Benchmarking**:
   - Enriches $1,000$ items in under $1$ second ($>1,700\text{ items/sec}$).
   - Automated ground-truth benchmarking scoring $100\%$ accuracy on key fields and compliance metrics.
   - Instant export to 252-column CSV and Excel XLSX.

---

## Architecture Overview

```
UniHack_Vikas/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI REST API & static asset serving
│   │   ├── master_data/             # Master JSON dictionaries (Manufacturers, UOMs, Fractions, Taxonomies)
│   │   ├── models/                  # Pydantic schemas & 252 Delivery column definitions
│   │   ├── pipeline/                # Modular 8-stage enrichment pipeline
│   │   └── services/                # Batch processor, benchmark evaluator, and exporter
│   └── tests/                       # Pytest unit & ground-truth validation suite
├── frontend/
│   ├── index.html                   # Modern single-page workbench application
│   ├── css/                         # Design system & component CSS
│   └── js/                          # API client and workbench controller
├── data/
│   ├── raw/                         # Raw input datasets & ground truth files
│   └── output/                      # Exported 252-column delivery CSV/XLSX
└── run_server.py                    # Server launch script
```

---

## Quick Start & Execution

### 1. Run Tests & Validation Benchmark
```bash
$env:PYTHONPATH='backend'; python -m pytest backend/tests -v
```

### 2. Launch Interactive Web Workbench & API
```bash
python run_server.py
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser to access the interactive studio.

### 3. API Documentation
Interactive Swagger API documentation is available at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**.
