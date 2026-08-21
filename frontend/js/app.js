/**
 * UniCat 2.0 - Core Application Logic
 * Clean, Practical, and Professional.
 */
import { ApiService } from './api.js';

const SAMPLE_DATA = [
  { name: "Frigidaire Dishwasher", cat: "Row 1", data: { Mfg_Part_Num: "PDSH4816AF", Part_Desc: "PDSH4816AF Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Whirlpool Eco Dishwasher", cat: "Row 2", data: { Mfg_Part_Num: "WDTS7024RZ", Part_Desc: "WDTS7024RZ Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Diablo Sanding Belt", cat: "1000 Set", data: { Mfg_Part_Num: "DCB518ASTS06G", Part_Desc: "Diablo 1/2x18 Sanding Belt", Part_Manuf: "Freud Inc", E1_Brand: "-- Unbranded --" } },
  { name: "Milwaukee Cut-Off Disc", cat: "1000 Set", data: { Mfg_Part_Num: "49-94-0013", Part_Desc: "Milw 5x.045 Metal Disc", Part_Manuf: "Milwaukee", E1_Brand: "-- Unbranded --" } },
  { name: "TimberTech Azek PVC Decking", cat: "Materials", data: { Mfg_Part_Num: "ADB15516CS", Part_Desc: "Coastline Sq Edge PVC", Part_Manuf: "Parksite", E1_Brand: "TIMBERTECH" } },
  { name: "Philips LED Bulb", cat: "Lighting", data: { Mfg_Part_Num: "565374", Part_Desc: "75W Led A19 Med 27k", Part_Manuf: "Phillips", E1_Brand: "-- Unbranded --" } }
];

const el = {
  startupOverlay: document.getElementById('startup-overlay'),
  navTabs: document.querySelectorAll('.nav-tab'),
  tabPanels: document.querySelectorAll('.tab-panel'),
  
  // Single Input
  quickSamples: document.getElementById('quick-samples-container'),
  inputMpn: document.getElementById('input-mpn'),
  inputDesc: document.getElementById('input-desc'),
  inputManuf: document.getElementById('input-manuf'),
  inputBrand: document.getElementById('input-e1-brand'),
  btnEnrich: document.getElementById('btn-enrich-single'),
  
  // Results
  studioEmpty: document.getElementById('studio-empty-state'),
  resultsPayload: document.getElementById('results-payload'),
  idTitle: document.getElementById('id-title'),
  idMeta: document.getElementById('id-meta'),
  confTxt: document.getElementById('conf-txt'),
  
  outInvoiceDesc: document.getElementById('out-invoice-desc'),
  outMobileDesc: document.getElementById('out-mobile-desc'),
  outShortDesc: document.getElementById('out-short-desc'),
  
  outFeatures: document.getElementById('out-features'),
  outAttributes: document.getElementById('out-attributes'),
  attrCountTxt: document.getElementById('attr-count-txt'),
  
  // Batch
  btnRunBatch: document.getElementById('btn-run-batch'),
  csvUpload: document.getElementById('csv-upload'),
  btnExpCsv: document.getElementById('btn-exp-csv'),
  btnExpXls: document.getElementById('btn-exp-xls'),
  
  statProd: document.getElementById('stat-prod'),
  statConf: document.getElementById('stat-conf'),
  statRev: document.getElementById('stat-rev'),
  
  batchProgress: document.getElementById('batch-progress'),
  progStatusTxt: document.getElementById('progress-status-txt'),
  progPctTxt: document.getElementById('progress-pct-txt'),
  progFillBar: document.getElementById('progress-fill-bar'),
  progSubtxt: document.getElementById('progress-subtext'),
  
  batchTbody: document.getElementById('batch-tbody')
};

document.addEventListener('DOMContentLoaded', initApp);

function initApp() {
  handleStartup();
  setupNavigation();
  setupSamples();
  setupEvents();
}

function handleStartup() {
  const hasSeen = sessionStorage.getItem('unicat_clean_intro');
  if (hasSeen) {
    el.startupOverlay.classList.add('hidden');
  } else {
    setTimeout(() => {
      el.startupOverlay.style.opacity = '0';
      setTimeout(() => {
        el.startupOverlay.classList.add('hidden');
        sessionStorage.setItem('unicat_clean_intro', '1');
      }, 300); // 300ms fade transition
    }, 800); // Total 800ms intro as requested
  }
}

function setupNavigation() {
  el.navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-tab');
      el.navTabs.forEach(t => t.classList.remove('active'));
      el.tabPanels.forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(`tab-${target}`).classList.add('active');
    });
  });
}

function setupSamples() {
  el.quickSamples.innerHTML = '';
  SAMPLE_DATA.forEach(s => {
    const item = document.createElement('div');
    item.className = 'sample-item';
    item.innerHTML = `
      <div><strong style="color:var(--text-primary); font-weight:500;">${s.name}</strong> <span style="font-size:0.75rem; margin-left:0.5rem;">${s.cat}</span></div>
      <div class="sample-item-icon">→</div>
    `;
    item.addEventListener('click', () => {
      el.inputMpn.value = s.data.Mfg_Part_Num || '';
      el.inputDesc.value = s.data.Part_Desc || '';
      el.inputManuf.value = s.data.Part_Manuf || '';
      el.inputBrand.value = s.data.E1_Brand || '';
      
      // Auto-trigger without crazy animations
      runSingleEnrichment();
    });
    el.quickSamples.appendChild(item);
  });
}

function setupEvents() {
  el.btnEnrich.addEventListener('click', runSingleEnrichment);
  el.btnRunBatch.addEventListener('click', runBatchProcessing);
  el.csvUpload.addEventListener('change', (e) => {
    if (e.target.files.length) handleCsvUpload(e.target.files[0]);
  });
  el.btnExpCsv.addEventListener('click', () => window.open(ApiService.getExportCsvUrl(), '_blank'));
  el.btnExpXls.addEventListener('click', () => window.open(ApiService.getExportExcelUrl(), '_blank'));
}

/* =======================================
   SINGLE ENRICHMENT
   ======================================= */
async function runSingleEnrichment() {
  const rawInput = {
    Mfg_Part_Num: el.inputMpn.value.trim(),
    Part_Desc: el.inputDesc.value.trim(),
    Part_Manuf: el.inputManuf.value.trim(),
    E1_Brand: el.inputBrand.value.trim()
  };
  
  if (!rawInput.Mfg_Part_Num && !rawInput.Part_Desc) return;
  
  el.btnEnrich.innerHTML = 'Enriching...';
  el.btnEnrich.disabled = true;
  el.studioEmpty.classList.add('hidden');
  el.resultsPayload.classList.add('hidden');
  
  try {
    const product = await ApiService.enrichSingle(rawInput);
    renderResults(product);
  } catch (err) {
    alert("Enrichment failed: " + err.message);
  } finally {
    el.btnEnrich.innerHTML = '⚡ Enrich & Validate';
    el.btnEnrich.disabled = false;
  }
}

function renderResults(p) {
  el.resultsPayload.classList.remove('hidden');
  
  el.idTitle.textContent = p.short_desc || p.product_name || p.mfg_part_num;
  
  let brand = p.brand_name || 'No Brand';
  let cat = p.classpath ? p.classpath.split('>').pop().trim() : 'Uncategorized';
  el.idMeta.textContent = `${brand} · ${cat}`;
  
  el.confTxt.textContent = `${p.confidence_score}% confidence`;
  
  el.outInvoiceDesc.textContent = p.invoice_desc;
  el.outMobileDesc.textContent = p.mobile_desc;
  el.outShortDesc.textContent = p.short_desc;
  
  el.outFeatures.innerHTML = '';
  p.item_features.forEach(f => {
    const li = document.createElement('li');
    li.textContent = f;
    el.outFeatures.appendChild(li);
  });
  
  el.outAttributes.innerHTML = '';
  const validAttrs = p.attributes.filter(a => a.label && a.value);
  el.attrCountTxt.textContent = `${validAttrs.length} attributes standardized`;
  
  validAttrs.forEach(attr => {
    const row = document.createElement('div');
    row.className = 'attr-row';
    row.innerHTML = `<div class="attr-key">${attr.label}</div><div class="attr-val">${attr.value} ${attr.uom||''}</div>`;
    el.outAttributes.appendChild(row);
  });
}

/* =======================================
   BATCH PROCESSING
   ======================================= */
async function runBatchProcessing() {
  startBatchProgress(1000);
  try {
    const sampleData = await ApiService.get1000Samples(1000, 0);
    const response = await ApiService.enrichBatch(sampleData.items);
    finishBatchProgress(response);
  } catch (err) {
    alert("Batch error: " + err.message);
    resetBatchProgress();
  }
}

async function handleCsvUpload(file) {
  startBatchProgress(1000);
  try {
    const response = await ApiService.uploadCsv(file, 1000);
    finishBatchProgress(response);
  } catch (err) {
    alert("CSV error: " + err.message);
    resetBatchProgress();
  }
}

let batchInterval;

function startBatchProgress(total) {
  el.btnRunBatch.disabled = true;
  el.batchProgress.classList.remove('hidden');
  
  let current = 0;
  el.progSubtxt.textContent = 'Standardizing product attributes...';
  
  batchInterval = setInterval(() => {
    current += Math.floor(Math.random() * 80) + 20;
    if (current >= total) current = total - Math.floor(Math.random() * 5); // Hang just below 100% until API finishes
    
    let pct = Math.floor((current / total) * 100);
    el.progStatusTxt.textContent = `Processing ${current.toLocaleString()} of ${total.toLocaleString()} items`;
    el.progPctTxt.textContent = `${pct}%`;
    el.progFillBar.style.width = `${pct}%`;
    
  }, 150);
}

function finishBatchProgress(res) {
  clearInterval(batchInterval);
  
  el.progStatusTxt.textContent = `${res.total_processed.toLocaleString()} items processed successfully`;
  el.progPctTxt.textContent = `100%`;
  el.progFillBar.style.width = `100%`;
  el.progSubtxt.textContent = 'Enrichment complete.';
  
  el.btnRunBatch.disabled = false;
  
  // Clean count animations
  animateValue(el.statProd, 0, res.total_processed, 500);
  animateValue(el.statConf, 0, res.average_confidence, 500, '%');
  animateValue(el.statRev, 0, res.review_needed_count, 500);
  
  renderTable(res.results);
  
  setTimeout(() => el.batchProgress.classList.add('hidden'), 2500);
}

function resetBatchProgress() {
  clearInterval(batchInterval);
  el.btnRunBatch.disabled = false;
  el.batchProgress.classList.add('hidden');
}

function renderTable(results) {
  el.batchTbody.innerHTML = '';
  const displayItems = results.slice(0, 50);
  
  displayItems.forEach((p) => {
    const tr = document.createElement('tr');
    
    let badgeHtml = p.needs_human_review 
      ? '<span class="badge badge-warning">Review</span>'
      : '<span class="badge badge-success">Validated</span>';
      
    tr.innerHTML = `
      <td style="font-family:monospace;">${p.mfg_part_num}</td>
      <td style="font-weight:500;">${p.brand_name}</td>
      <td style="font-size:0.75rem; color:var(--text-secondary);">${p.classpath}</td>
      <td style="font-family:monospace;">${p.invoice_desc}</td>
      <td style="font-weight:500;">${p.confidence_score}%</td>
      <td>${badgeHtml}</td>
    `;
    el.batchTbody.appendChild(tr);
  });
}

function animateValue(obj, start, end, duration, suffix = '') {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start) + suffix;
    if (progress < 1) window.requestAnimationFrame(step);
    else obj.innerHTML = end + suffix;
  };
  window.requestAnimationFrame(step);
}
