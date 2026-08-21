/**
 * API Service Client for AI Product Intelligence Platform
 */
const API_BASE = window.location.origin;

export const ApiService = {
  async healthCheck() {
    const res = await fetch(`${API_BASE}/api/health`);
    return await res.json();
  },

  async enrichSingle(rawInput) {
    const res = await fetch(`${API_BASE}/api/enrich/single`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(rawInput)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Enrichment failed");
    }
    return await res.json();
  },

  async enrichBatch(items) {
    const res = await fetch(`${API_BASE}/api/enrich/batch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Batch processing failed");
    }
    return await res.json();
  },

  async uploadCsv(file, maxRows = 1000) {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${API_BASE}/api/enrich/upload?max_rows=${maxRows}`, {
      method: "POST",
      body: formData
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "CSV upload failed");
    }
    return await res.json();
  },

  async getBenchmark() {
    const res = await fetch(`${API_BASE}/api/benchmark`);
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to fetch benchmark");
    }
    return await res.json();
  },

  async get1000Samples(limit = 50, offset = 0) {
    const res = await fetch(`${API_BASE}/api/sample/1000?limit=${limit}&offset=${offset}`);
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to fetch sample catalog");
    }
    return await res.json();
  },

  async getGroundTruthSamples() {
    const res = await fetch(`${API_BASE}/api/ground_truth/samples`);
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Failed to fetch ground truth");
    }
    return await res.json();
  },

  getExportCsvUrl() {
    return `${API_BASE}/api/export/latest/csv`;
  },

  getExportExcelUrl() {
    return `${API_BASE}/api/export/latest/excel`;
  }
};
