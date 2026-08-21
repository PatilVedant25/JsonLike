"""
Explainability & Provenance Audit Trail Generator.
Tracks per-field derivations, evidence sources, and confidence metrics.
"""
from typing import List, Dict, Any, Optional
from app.models.schema import ProvenanceRecord

def create_provenance_record(
    field: str,
    source_method: str,
    raw_evidence: Optional[str] = "",
    confidence: float = 1.0,
    notes: Optional[str] = ""
) -> ProvenanceRecord:
    """Creates a structured provenance entry."""
    return ProvenanceRecord(
        field=field,
        source_method=source_method,
        raw_evidence=raw_evidence or "",
        confidence=confidence,
        notes=notes or ""
    )
