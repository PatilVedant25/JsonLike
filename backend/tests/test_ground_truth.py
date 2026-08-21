"""
Ground Truth Benchmark Test.
Validates the pipeline accuracy against known good sample delivery formats.
"""
import os
import pytest
from app.services.benchmark import evaluate_ground_truth

def test_ground_truth_accuracy():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    gt_csv = os.path.join(base_dir, "data", "raw", "Unihack_ Expected Output - Delivery Format.csv")
    
    summary = evaluate_ground_truth(gt_csv)
    
    print(f"\nGround Truth Benchmark Summary:")
    print(f"Overall Accuracy: {summary.overall_accuracy}%")
    print(f"Invoice Desc Compliance: {summary.invoice_desc_compliance}%")
    print(f"Mobile Desc Compliance: {summary.mobile_desc_compliance}%")
    print(f"Title Compliance: {summary.title_compliance}%")
    print(f"Brand Accuracy: {summary.brand_accuracy}%")
    print(f"Manufacturer Accuracy: {summary.manufacturer_accuracy}%")
    print(f"Classpath Accuracy: {summary.classpath_accuracy}%")
    
    assert summary.overall_accuracy >= 80.0
    assert summary.invoice_desc_compliance == 100.0
    assert summary.brand_accuracy == 100.0
    assert summary.manufacturer_accuracy == 100.0
    assert summary.classpath_accuracy == 100.0
