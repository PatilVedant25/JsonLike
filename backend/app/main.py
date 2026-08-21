"""
FastAPI Application Entry Point.
Provides REST API endpoints for single enrichment, batch processing, file uploads,
ground-truth benchmarking, export, and frontend static assets serving.
"""
import os
import io
import pandas as pd
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

from app.models.schema import (
    RawProductInput,
    EnrichedProduct,
    BatchProcessRequest,
    BatchProcessResponse,
    BenchmarkSummary
)
from app.pipeline.orchestrator import EnrichmentPipeline
from app.services.batch_processor import BatchProcessor
from app.services.benchmark import evaluate_ground_truth
from app.services.exporter import export_to_csv, export_to_excel
from app.models.delivery_columns import DELIVERY_COLUMNS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

if os.environ.get("VERCEL") == "1":
    DATA_OUT_DIR = os.path.join("/tmp", "data", "output")
else:
    DATA_OUT_DIR = os.path.join(BASE_DIR, "data", "output")

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

os.makedirs(DATA_OUT_DIR, exist_ok=True)



app = FastAPI(
    title="AI-Powered Product Intelligence Platform",
    description="Transforms raw, abbreviated catalog records into 252-column commerce-ready intelligence.",
    version="1.0.0"
)

# Enable CORS for development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = EnrichmentPipeline()
batch_processor = BatchProcessor()

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI-Powered Product Intelligence Platform",
        "version": "1.0.0",
        "delivery_columns_count": len(DELIVERY_COLUMNS)
    }

@app.post("/api/enrich/single", response_model=EnrichedProduct)
async def enrich_single_product(input_data: RawProductInput):
    """Enriches a single raw product input into full 252-column intelligence."""
    try:
        enriched = pipeline.enrich_product(input_data)
        return enriched
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enrich/batch", response_model=BatchProcessResponse)
async def enrich_batch_products(request: BatchProcessRequest):
    """Enriches a batch of raw product inputs."""
    try:
        response = batch_processor.process_batch(request.items)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/enrich/upload")
async def upload_and_enrich_csv(file: UploadFile = File(...), max_rows: int = 1000):
    """Uploads a raw CSV file, parses it, and enriches rows."""
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Clean column names
        df.columns = [c.strip() for c in df.columns]
        
        items = []
        for _, row in df.head(max_rows).iterrows():
            items.append(RawProductInput(
                Mfg_Part_Num=str(row.get("Mfg_Part_Num", "") if pd.notna(row.get("Mfg_Part_Num")) else ""),
                Part_Desc=str(row.get("Part_Desc", "") if pd.notna(row.get("Part_Desc")) else ""),
                E1_Brand=str(row.get("E1_Brand", "") if pd.notna(row.get("E1_Brand")) else ""),
                Unilog_Brand=str(row.get("Unilog_Brand", "") if pd.notna(row.get("Unilog_Brand")) else ""),
                DIB_Brand=str(row.get("DIB_Brand", "") if pd.notna(row.get("DIB_Brand")) else ""),
                Part_Manuf=str(row.get("Part_Manuf", "") if pd.notna(row.get("Part_Manuf")) else ""),
                PART_NUMBER=str(row.get("PART_NUMBER", "") if pd.notna(row.get("PART_NUMBER")) else ""),
                Dept=str(row.get("Dept", "") if pd.notna(row.get("Dept")) else ""),
                Class=str(row.get("Class", "") if pd.notna(row.get("Class")) else ""),
                Fine=str(row.get("Fine", "") if pd.notna(row.get("Fine")) else ""),
                SKU=str(row.get("SKU - MY_PART_NUMBER", "") if pd.notna(row.get("SKU - MY_PART_NUMBER")) else "")
            ))
            
        response = batch_processor.process_batch(items)
        
        # Save output CSV automatically
        out_csv_path = os.path.join(DATA_OUT_DIR, "latest_enriched_delivery.csv")
        export_to_csv(response.results, out_csv_path)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@app.get("/api/benchmark", response_model=BenchmarkSummary)
async def run_ground_truth_benchmark():
    """Runs automated evaluation and accuracy scoring against labelled ground truth."""
    gt_path = os.path.join(DATA_RAW_DIR, "Unihack_ Expected Output - Delivery Format.csv")
    if not os.path.exists(gt_path):
        raise HTTPException(status_code=404, detail="Ground truth dataset not found.")
    summary = evaluate_ground_truth(gt_path)
    return summary

@app.get("/api/sample/1000")
async def get_1000_sample_items(limit: int = 50, offset: int = 0):
    """Fetches paginated raw items from the 1000-item dataset."""
    sample_csv = os.path.join(DATA_RAW_DIR, "Unihack_ Sample Dataset - Input.csv")
    if not os.path.exists(sample_csv):
        raise HTTPException(status_code=404, detail="1000 items dataset not found.")
    df = pd.read_csv(sample_csv)
    total_count = len(df)
    subset = df.iloc[offset:offset + limit].fillna("").to_dict(orient="records")
    return {
        "total": total_count,
        "offset": offset,
        "limit": limit,
        "items": subset
    }

@app.get("/api/ground_truth/samples")
async def get_ground_truth_samples():
    """Returns ground truth delivery rows for side-by-side verification."""
    gt_path = os.path.join(DATA_RAW_DIR, "Unihack_ Expected Output - Delivery Format.csv")
    if not os.path.exists(gt_path):
        raise HTTPException(status_code=404, detail="Ground truth dataset not found.")
    df = pd.read_csv(gt_path).fillna("")
    return {
        "count": len(df),
        "columns": list(df.columns),
        "rows": df.to_dict(orient="records")
    }

@app.get("/api/export/latest/csv")
async def download_latest_csv():
    """Downloads the latest enriched 252-column delivery CSV file."""
    csv_path = os.path.join(DATA_OUT_DIR, "latest_enriched_delivery.csv")
    if not os.path.exists(csv_path):
        # Generate on the fly if not yet created
        sample_csv = os.path.join(DATA_RAW_DIR, "Unihack_ Sample Dataset - Input.csv")
        df = pd.read_csv(sample_csv).fillna("")
        items = [RawProductInput(**r) for r in df.head(100).to_dict(orient="records")]
        resp = batch_processor.process_batch(items)
        export_to_csv(resp.results, csv_path)
        
    return FileResponse(
        path=csv_path,
        filename="enriched_delivery_format_252_columns.csv",
        media_type="text/csv"
    )

@app.get("/api/export/latest/excel")
async def download_latest_excel():
    """Downloads the latest enriched 252-column delivery Excel XLSX file."""
    xlsx_path = os.path.join(DATA_OUT_DIR, "latest_enriched_delivery.xlsx")
    csv_path = os.path.join(DATA_OUT_DIR, "latest_enriched_delivery.csv")
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df.to_excel(xlsx_path, index=False, engine="openpyxl")
    else:
        sample_csv = os.path.join(DATA_RAW_DIR, "Unihack_ Sample Dataset - Input.csv")
        df = pd.read_csv(sample_csv).fillna("")
        items = [RawProductInput(**r) for r in df.head(100).to_dict(orient="records")]
        resp = batch_processor.process_batch(items)
        export_to_excel(resp.results, xlsx_path)
        
    return FileResponse(
        path=xlsx_path,
        filename="enriched_delivery_format_252_columns.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Mount Frontend static files if directory exists
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
