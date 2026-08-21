/**
 * Main Application Logic & Interactive Workbench Controller
 */
import { ApiService } from './api.js';

// Application State
const state = {
  currentTab: 'studio',
  activeProduct: null,
  batchResults: [],
  sample1000Items: []
};

// Preset Quick Samples
const SAMPLE_PRESETS = [
  {
    name: "Frigidaire Dishwasher (Row 1)",
    data: {
      Mfg_Part_Num: "PDSH4816AF",
      Part_Desc: "PDSH4816AF Dishwasher SS - Display Only",
      Part_Manuf: "Appliance Dealers Cooperative (APPDE)",
      E1_Brand: "-- Unbranded --"
    }
  },
  {
    name: "Whirlpool Eco Dishwasher (Row 2)",
    data: {
      Mfg_Part_Num: "WDTS7024RZ",
      Part_Desc: "WDTS7024RZ Dishwasher SS - Display Only",
      Part_Manuf: "Appliance Dealers Cooperative (APPDE)",
      E1_Brand: "-- Unbranded --"
    }
  },
  {
    name: "Diablo Sanding Belt (1000 Set)",
    data: {
      Mfg_Part_Num: "DCB518ASTS06G",
      Part_Desc: "DCB518ASTS06G Diablo 1/2\"x18\" - Sanding Belt 6pc",
      Part_Manuf: "Freud Inc (2435)",
      E1_Brand: "-- Unbranded --"
    }
  },
  {
    name: "Milwaukee Cut Off Disc",
    data: {
      Mfg_Part_Num: "49-94-0013",
      Part_Desc: "49-94-0013 Milw 5\"x.045\"x7/8\" Metal Cut Off Disc",
      Part_Manuf: "Milwaukee Accessory (4031)",
      E1_Brand: "-- Unbranded --"
    }
  },
  {
    name: "TimberTech Azek PVC Decking",
    data: {
      Mfg_Part_Num: "ADB15516CS",
      Part_Desc: "1x6-16' Coastline Sq Edge - Vintage Azek PVC Decking",
      Part_Manuf: "Parksite (6151)",
      E1_Brand: "TIMBERTECH"
    }
  },
  {
    name: "Philips LED Bulb",
    data: {
      Mfg_Part_Num: "565374",
      Part_Desc: "565374 75W Led A19 Med 27k 4pk",
      Part_Manuf: "Phillips Lighting (5831)",
      E1_Brand: "-- Unbranded --"
    }
  }
];

// DOM Elements
const elements = {
  navTabs: document.querySelectorAll('.nav-tab'),
  tabPanels: document.querySelectorAll('.tab-panel'),
  
  // Single Enricher Elements
  inputMpn: document.getElementById('input-mpn'),
  inputDesc: document.getElementById('input-desc'),
  inputManuf: document.getElementById('input-manuf'),
  inputE1Brand: document.getElementById('input-e1-brand'),
  btnEnrichSingle: document.getElementById('btn-enrich-single'),
  quickSamplesContainer: document.getElementById('quick-samples-container'),
  
  // Single Output Display
  resultTitle: document.getElementById('result-title'),
  resultMfrPill: document.getElementById('result-mfr-pill'),
  resultBrandPill: document.getElementById('result-brand-pill'),
  resultClasspathPill: document.getElementById('result-classpath-pill'),
  resultConfidenceBadge: document.getElementById('result-confidence-badge'),
  
  invoiceDescText: document.getElementById('invoice-desc-text'),
  invoiceMeter: document.getElementById('invoice-meter'),
  mobileDescText: document.getElementById('mobile-desc-text'),
  mobileMeter: document.getElementById('mobile-meter'),
  shortDescText: document.getElementById('short-desc-text'),
  itemFeaturesList: document.getElementById('item-features-list'),
  attributesGrid: document.getElementById('attributes-grid'),
  
  // Batch Manager Elements
  btnRun1000Batch: document.getElementById('btn-run-1000-batch'),
  csvFileInput: document.getElementById('csv-file-input'),
  batchProgressBar: document.getElementById('batch-progress-bar'),
  batchProgressText: document.getElementById('batch-progress-text'),
  batchStatsContainer: document.getElementById('batch-stats-container'),
  batchTableBody: document.getElementById('batch-table-body'),
  batchSearchInput: document.getElementById('batch-search-input'),
  btnExportCsv: document.getElementById('btn-export-csv'),
  btnExportExcel: document.getElementById('btn-export-excel')
};

// Initialize Application
export async function initApp() {
  setupNavigation();
  setupQuickSamples();
  setupEventListeners();
}

// Navigation Tabs
function setupNavigation() {
  elements.navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      state.currentTab = target;
      
      elements.navTabs.forEach(t => t.classList.remove('active'));
      elements.tabPanels.forEach(p => p.classList.remove('active'));
      
      tab.classList.add('active');
      const activePanel = document.getElementById(`tab-${target}`);
      if (activePanel) activePanel.classList.add('active');
    });
  });
}

// Quick Sample Chips
function setupQuickSamples() {
  elements.quickSamplesContainer.innerHTML = '';
  SAMPLE_PRESETS.forEach(sample => {
    const chip = document.createElement('button');
    chip.className = 'sample-chip';
    chip.textContent = sample.name;
    chip.addEventListener('click', () => {
      loadSampleIntoForm(sample.data);
      handleSingleEnrich();
    });
    elements.quickSamplesContainer.appendChild(chip);
  });
}

function loadSampleIntoForm(data) {
  elements.inputMpn.value = data.Mfg_Part_Num || '';
  elements.inputDesc.value = data.Part_Desc || '';
  elements.inputManuf.value = data.Part_Manuf || '';
  elements.inputE1Brand.value = data.E1_Brand || '';
}

// Event Listeners
function setupEventListeners() {
  elements.btnEnrichSingle.addEventListener('click', handleSingleEnrich);
  
  elements.btnRun1000Batch.addEventListener('click', run1000Batch);
  
  elements.csvFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleCsvUpload(e.target.files[0]);
    }
  });
  
  elements.batchSearchInput.addEventListener('input', (e) => {
    filterBatchTable(e.target.value);
  });
  
  elements.btnExportCsv.addEventListener('click', () => {
    window.open(ApiService.getExportCsvUrl(), '_blank');
  });
  
  elements.btnExportExcel.addEventListener('click', () => {
    window.open(ApiService.getExportExcelUrl(), '_blank');
  });
}

// Single Item Enrichment
async function handleSingleEnrich() {
  const rawInput = {
    Mfg_Part_Num: elements.inputMpn.value.trim(),
    Part_Desc: elements.inputDesc.value.trim(),
    Part_Manuf: elements.inputManuf.value.trim(),
    E1_Brand: elements.inputE1Brand.value.trim()
  };
  
  elements.btnEnrichSingle.innerHTML = '<span class="spinner"></span> Enriching...';
  elements.btnEnrichSingle.disabled = true;
  
  try {
    const product = await ApiService.enrichSingle(rawInput);
    state.activeProduct = product;
    renderEnrichedProduct(product);
  } catch (err) {
    alert("Error enriching product: " + err.message);
  } finally {
    elements.btnEnrichSingle.innerHTML = '⚡ Enrich & Validate';
    elements.btnEnrichSingle.disabled = false;
  }
}

// Render Enriched Product on Live Studio View
function renderEnrichedProduct(p) {
  // Title & Identity
  elements.resultTitle.textContent = p.short_desc || p.product_name;
  elements.resultMfrPill.textContent = p.manufacturer_name;
  elements.resultBrandPill.textContent = p.brand_name;
  elements.resultClasspathPill.textContent = p.classpath;
  
  // Confidence Badge
  elements.resultConfidenceBadge.textContent = `${p.confidence_score}% Confidence`;
  elements.resultConfidenceBadge.className = `badge ${p.confidence_score >= 90 ? 'badge-emerald' : p.confidence_score >= 80 ? 'badge-cyan' : 'badge-amber'}`;
  
  // Descriptions & Live Constraint Meters
  elements.invoiceDescText.textContent = p.invoice_desc;
  const invLen = p.invoice_desc.length;
  elements.invoiceMeter.textContent = `${invLen}/40 Chars`;
  
  elements.mobileDescText.textContent = p.mobile_desc;
  const mobLen = p.mobile_desc.length;
  elements.mobileMeter.textContent = `${mobLen} Chars (Goal: 60-80)`;
  
  elements.shortDescText.textContent = p.short_desc;
  
  // Item Features
  elements.itemFeaturesList.innerHTML = '';
  p.item_features.forEach(feat => {
    const li = document.createElement('li');
    li.textContent = feat;
    elements.itemFeaturesList.appendChild(li);
  });
  
  // 50-Slot Attribute Grid (showing filled attributes)
  elements.attributesGrid.innerHTML = '';
  const activeAttrs = p.attributes.filter(a => a.label && a.value);
  activeAttrs.forEach(attr => {
    const card = document.createElement('div');
    card.className = 'attr-card';
    card.innerHTML = `
      <span class="attr-label">${attr.label}</span>
      <span class="attr-value">${attr.value} ${attr.uom || ''}</span>
    `;
    elements.attributesGrid.appendChild(card);
  });
}

// Batch Processing
async function run1000Batch() {
  elements.btnRun1000Batch.innerHTML = '<span class="spinner"></span> Processing 1000 Items...';
  elements.btnRun1000Batch.disabled = true;
  elements.batchProgressBar.style.width = '20%';
  elements.batchProgressText.textContent = 'Loading 1,000 raw catalog rows...';
  
  try {
    const sampleData = await ApiService.get1000Samples(1000, 0);
    elements.batchProgressBar.style.width = '50%';
    elements.batchProgressText.textContent = 'Enriching and standardizing across 252 delivery columns...';
    
    const response = await ApiService.enrichBatch(sampleData.items);
    state.batchResults = response.results;
    
    elements.batchProgressBar.style.width = '100%';
    elements.batchProgressText.textContent = `Completed! ${response.total_processed} items enriched in under 1 second (${response.average_confidence}% Avg Confidence).`;
    
    renderBatchStats(response);
    renderBatchTable(response.results);
  } catch (err) {
    alert("Batch error: " + err.message);
  } finally {
    elements.btnRun1000Batch.innerHTML = '🚀 Process 1,000 Sample Items';
    elements.btnRun1000Batch.disabled = false;
  }
}

async function handleCsvUpload(file) {
  elements.batchProgressBar.style.width = '40%';
  elements.batchProgressText.textContent = `Uploading and parsing ${file.name}...`;
  
  try {
    const response = await ApiService.uploadCsv(file, 1000);
    state.batchResults = response.results;
    
    elements.batchProgressBar.style.width = '100%';
    elements.batchProgressText.textContent = `Enriched ${response.total_processed} items from uploaded file.`;
    
    renderBatchStats(response);
    renderBatchTable(response.results);
  } catch (err) {
    alert("CSV upload failed: " + err.message);
  }
}

function renderBatchStats(resp) {
  elements.batchStatsContainer.innerHTML = `
    <div class="stat-card">
      <span class="stat-label">Total Processed</span>
      <span class="stat-value">${resp.total_processed}</span>
    </div>
    <div class="stat-card">
      <span class="stat-label">Delivery Columns</span>
      <span class="stat-value">252</span>
    </div>
    <div class="stat-card">
      <span class="stat-label">Average Confidence</span>
      <span class="stat-value">${resp.average_confidence}%</span>
    </div>
    <div class="stat-card">
      <span class="stat-label">Human Review Needed</span>
      <span class="stat-value">${resp.review_needed_count}</span>
    </div>
  `;
}

function renderBatchTable(products) {
  elements.batchTableBody.innerHTML = '';
  products.slice(0, 100).forEach((p, idx) => {
    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.addEventListener('click', () => {
      state.activeProduct = p;
      renderEnrichedProduct(p);
      // Switch to studio tab
      document.querySelector('[data-tab="studio"]').click();
    });
    
    tr.innerHTML = `
      <td>${idx + 1}</td>
      <td style="font-family:monospace; font-weight:600; color:var(--accent-cyan);">${p.mfg_part_num}</td>
      <td>${p.manufacturer_name}</td>
      <td><strong>${p.brand_name}</strong></td>
      <td style="font-size:0.75rem; color:var(--text-muted);">${p.classpath}</td>
      <td style="font-family:monospace; font-size:0.75rem;">${p.invoice_desc}</td>
      <td><span class="badge ${p.confidence_score >= 90 ? 'badge-emerald' : 'badge-cyan'}">${p.confidence_score}%</span></td>
      <td><span class="badge ${p.needs_human_review ? 'badge-amber' : 'badge-emerald'}">${p.needs_human_review ? 'Review' : 'Approved'}</span></td>
    `;
    elements.batchTableBody.appendChild(tr);
  });
}

function filterBatchTable(query) {
  if (!state.batchResults) return;
  const q = query.toLowerCase();
  const filtered = state.batchResults.filter(p => 
    p.mfg_part_num.toLowerCase().includes(q) ||
    p.brand_name.toLowerCase().includes(q) ||
    p.manufacturer_name.toLowerCase().includes(q) ||
    p.part_desc.toLowerCase().includes(q)
  );
  renderBatchTable(filtered);
}

// Start application on DOM ready
document.addEventListener('DOMContentLoaded', initApp);
