/**
 * Minimal & Premium App Logic
 */
import { ApiService } from './api.js';

// Application State
const state = {
  currentTab: 'studio',
  activeProduct: null,
  batchResults: [],
};

// Preset Quick Samples
const SAMPLE_PRESETS = [
  { name: "Frigidaire Dishwasher", data: { Mfg_Part_Num: "PDSH4816AF", Part_Desc: "PDSH4816AF Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Whirlpool Eco", data: { Mfg_Part_Num: "WDTS7024RZ", Part_Desc: "WDTS7024RZ Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Diablo Sanding Belt", data: { Mfg_Part_Num: "DCB518ASTS06G", Part_Desc: "Diablo 1/2x18 Sanding Belt", Part_Manuf: "Freud Inc", E1_Brand: "-- Unbranded --" } },
  { name: "Milwaukee Cut Off Disc", data: { Mfg_Part_Num: "49-94-0013", Part_Desc: "Milw 5x.045 Metal Disc", Part_Manuf: "Milwaukee", E1_Brand: "-- Unbranded --" } },
  { name: "TimberTech PVC Decking", data: { Mfg_Part_Num: "ADB15516CS", Part_Desc: "Coastline Sq Edge PVC", Part_Manuf: "Parksite", E1_Brand: "TIMBERTECH" } },
  { name: "Philips LED Bulb", data: { Mfg_Part_Num: "565374", Part_Desc: "75W Led A19 Med 27k", Part_Manuf: "Phillips", E1_Brand: "-- Unbranded --" } }
];

// DOM Elements
const elements = {
  startupOverlay: document.getElementById('startup-overlay'),
  navTabs: document.querySelectorAll('.nav-tab'),
  tabPanels: document.querySelectorAll('.tab-panel'),
  
  // Single Enricher
  inputMpn: document.getElementById('input-mpn'),
  inputDesc: document.getElementById('input-desc'),
  inputManuf: document.getElementById('input-manuf'),
  inputE1Brand: document.getElementById('input-e1-brand'),
  btnEnrichSingle: document.getElementById('btn-enrich-single'),
  quickSamplesContainer: document.getElementById('quick-samples-container'),
  
  // Empty States & Panels
  resultTitle: document.getElementById('result-title'),
  resultStatusRow: document.getElementById('result-status-row'),
  resultConfidenceBadge: document.getElementById('result-confidence-badge'),
  
  descEmptyState: document.getElementById('desc-empty-state'),
  descContentGrid: document.getElementById('desc-content-grid'),
  invoiceDescText: document.getElementById('invoice-desc-text'),
  mobileDescText: document.getElementById('mobile-desc-text'),
  shortDescText: document.getElementById('short-desc-text'),
  
  featuresEmptyState: document.getElementById('features-empty-state'),
  itemFeaturesList: document.getElementById('item-features-list'),
  
  attrEmptyState: document.getElementById('attr-empty-state'),
  attributesGrid: document.getElementById('attributes-grid'),
  
  // Batch Manager
  btnRun1000Batch: document.getElementById('btn-run-1000-batch'),
  csvFileInput: document.getElementById('csv-file-input'),
  batchProgressBarContainer: document.getElementById('batch-progress-container'),
  batchProgressBar: document.getElementById('batch-progress-bar'),
  batchTableBody: document.getElementById('batch-table-body'),
  
  statTotal: document.getElementById('stat-total'),
  statConfidence: document.getElementById('stat-confidence'),
  statReview: document.getElementById('stat-review'),
  
  btnExportCsv: document.getElementById('btn-export-csv'),
  btnExportExcel: document.getElementById('btn-export-excel')
};

// Initialize Application
export async function initApp() {
  handleStartupAnimation();
  setupNavigation();
  setupQuickSamples();
  setupEventListeners();
}

// Startup Animation Logic
function handleStartupAnimation() {
  const hasSeenIntro = sessionStorage.getItem('unicat_intro_seen');
  
  if (hasSeenIntro) {
    elements.startupOverlay.style.display = 'none';
  } else {
    setTimeout(() => {
      elements.startupOverlay.style.opacity = '0';
      setTimeout(() => {
        elements.startupOverlay.style.display = 'none';
        sessionStorage.setItem('unicat_intro_seen', 'true');
      }, 400); // Wait for fade transition
    }, 1500); // 1.5s intro duration
  }
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
    chip.className = 'sample-pill';
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
    if (e.target.files.length > 0) handleCsvUpload(e.target.files[0]);
  });
  
  elements.btnExportCsv.addEventListener('click', () => window.open(ApiService.getExportCsvUrl(), '_blank'));
  elements.btnExportExcel.addEventListener('click', () => window.open(ApiService.getExportExcelUrl(), '_blank'));
}

// Single Item Enrichment
async function handleSingleEnrich() {
  const rawInput = {
    Mfg_Part_Num: elements.inputMpn.value.trim(),
    Part_Desc: elements.inputDesc.value.trim(),
    Part_Manuf: elements.inputManuf.value.trim(),
    E1_Brand: elements.inputE1Brand.value.trim()
  };
  
  elements.btnEnrichSingle.innerHTML = '<span class="spinner"></span> &nbsp; Processing...';
  elements.btnEnrichSingle.disabled = true;
  
  try {
    const product = await ApiService.enrichSingle(rawInput);
    state.activeProduct = product;
    renderEnrichedProduct(product);
  } catch (err) {
    alert("Error enriching product: " + err.message);
  } finally {
    elements.btnEnrichSingle.innerHTML = 'Enrich & Validate';
    elements.btnEnrichSingle.disabled = false;
  }
}

// Render Enriched Product on Live Studio View
function renderEnrichedProduct(p) {
  // Title & Status Row
  elements.resultTitle.textContent = p.short_desc || p.product_name;
  elements.resultStatusRow.style.display = 'flex';
  
  elements.resultConfidenceBadge.textContent = `${p.confidence_score}% Confidence`;
  elements.resultConfidenceBadge.className = `status-pill ${p.confidence_score >= 90 ? 'success' : 'neutral'}`;
  
  // Hide empty states, show grids
  elements.descEmptyState.classList.add('hidden');
  elements.featuresEmptyState.classList.add('hidden');
  elements.attrEmptyState.classList.add('hidden');
  
  elements.descContentGrid.classList.remove('hidden');
  elements.itemFeaturesList.classList.remove('hidden');
  elements.attributesGrid.classList.remove('hidden');
  
  // Descriptions
  elements.invoiceDescText.textContent = p.invoice_desc;
  elements.mobileDescText.textContent = p.mobile_desc;
  elements.shortDescText.textContent = p.short_desc;
  
  // Staggered Feature Bullets
  elements.itemFeaturesList.innerHTML = '';
  p.item_features.forEach((feat, idx) => {
    const li = document.createElement('li');
    li.textContent = feat;
    li.className = 'stagger-item';
    li.style.animationDelay = `${idx * 100}ms`; // Stagger delay
    elements.itemFeaturesList.appendChild(li);
    
    // Trigger animation
    requestAnimationFrame(() => li.classList.add('visible'));
  });
  
  // Attributes Chips
  elements.attributesGrid.innerHTML = '';
  const activeAttrs = p.attributes.filter(a => a.label && a.value);
  activeAttrs.forEach((attr, idx) => {
    const chip = document.createElement('div');
    chip.className = 'attr-chip stagger-item';
    chip.style.animationDelay = `${idx * 50}ms`; // Fast stagger
    chip.innerHTML = `
      <span class="attr-chip-label">${attr.label}</span>
      <span class="attr-chip-value">${attr.value} ${attr.uom || ''}</span>
    `;
    elements.attributesGrid.appendChild(chip);
    
    requestAnimationFrame(() => chip.classList.add('visible'));
  });
}

// Batch Processing
async function run1000Batch() {
  elements.btnRun1000Batch.innerHTML = '<span class="spinner"></span> &nbsp; Processing...';
  elements.btnRun1000Batch.disabled = true;
  elements.batchProgressBarContainer.classList.add('active');
  elements.batchProgressBar.style.width = '20%';
  
  try {
    const sampleData = await ApiService.get1000Samples(1000, 0);
    elements.batchProgressBar.style.width = '60%';
    
    const response = await ApiService.enrichBatch(sampleData.items);
    state.batchResults = response.results;
    
    elements.batchProgressBar.style.width = '100%';
    
    animateValue(elements.statTotal, 0, response.total_processed, 1000);
    animateValue(elements.statConfidence, 0, response.average_confidence, 1000, '%');
    animateValue(elements.statReview, 0, response.review_needed_count, 1000);
    
    renderBatchTable(response.results);
    
  } catch (err) {
    alert("Batch error: " + err.message);
  } finally {
    setTimeout(() => elements.batchProgressBarContainer.classList.remove('active'), 1000);
    elements.btnRun1000Batch.innerHTML = 'Process 1,000 Sample Items';
    elements.btnRun1000Batch.disabled = false;
  }
}

async function handleCsvUpload(file) {
  elements.batchProgressBarContainer.classList.add('active');
  elements.batchProgressBar.style.width = '40%';
  
  try {
    const response = await ApiService.uploadCsv(file, 1000);
    state.batchResults = response.results;
    elements.batchProgressBar.style.width = '100%';
    
    animateValue(elements.statTotal, 0, response.total_processed, 1000);
    animateValue(elements.statConfidence, 0, response.average_confidence, 1000, '%');
    animateValue(elements.statReview, 0, response.review_needed_count, 1000);
    
    renderBatchTable(response.results);
  } catch (err) {
    alert("CSV upload failed: " + err.message);
  } finally {
    setTimeout(() => elements.batchProgressBarContainer.classList.remove('active'), 1000);
  }
}

// Animate counting numbers
function animateValue(obj, start, end, duration, suffix = '') {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const easeProgress = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    obj.innerHTML = Math.floor(easeProgress * (end - start) + start) + suffix;
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      obj.innerHTML = end + suffix;
    }
  };
  window.requestAnimationFrame(step);
}

// Render Batch Table with Staggered Rows
function renderBatchTable(products) {
  elements.batchTableBody.innerHTML = '';
  
  // Only render first 50 immediately for performance, the rest in background if needed
  const displayItems = products.slice(0, 50);
  
  displayItems.forEach((p, idx) => {
    const tr = document.createElement('tr');
    tr.className = 'stagger-item';
    tr.style.animationDelay = `${Math.min(idx * 30, 800)}ms`; // Cap max delay
    
    tr.innerHTML = `
      <td>${idx + 1}</td>
      <td class="td-mono">${p.mfg_part_num}</td>
      <td>${p.manufacturer_name}</td>
      <td style="font-weight:600;">${p.brand_name}</td>
      <td style="font-size:0.7rem; color:var(--text-muted);">${p.classpath}</td>
      <td class="td-mono" style="font-size:0.7rem;">${p.invoice_desc}</td>
      <td><span class="status-pill ${p.confidence_score >= 90 ? 'success' : 'neutral'}">${p.confidence_score}%</span></td>
      <td><span class="status-pill ${p.needs_human_review ? 'neutral' : 'success'}">${p.needs_human_review ? 'Review' : 'Approved'}</span></td>
    `;
    elements.batchTableBody.appendChild(tr);
    
    requestAnimationFrame(() => tr.classList.add('visible'));
  });
}

// Start application on DOM ready
document.addEventListener('DOMContentLoaded', initApp);
