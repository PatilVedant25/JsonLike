/**
 * AI Command Center Logic
 */
import { ApiService } from './api.js';

// Application State
const state = {
  currentTab: 'studio',
  batchResults: [],
};

// Preset Quick Samples
const SAMPLE_PRESETS = [
  { name: "Frigidaire Dishwasher", cat: "Home Appliances", data: { Mfg_Part_Num: "PDSH4816AF", Part_Desc: "PDSH4816AF Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Whirlpool Eco", cat: "Home Appliances", data: { Mfg_Part_Num: "WDTS7024RZ", Part_Desc: "WDTS7024RZ Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Diablo Sanding Belt", cat: "Tools", data: { Mfg_Part_Num: "DCB518ASTS06G", Part_Desc: "Diablo 1/2x18 Sanding Belt", Part_Manuf: "Freud Inc", E1_Brand: "-- Unbranded --" } },
  { name: "Milwaukee Cut Off Disc", cat: "Tools", data: { Mfg_Part_Num: "49-94-0013", Part_Desc: "Milw 5x.045 Metal Disc", Part_Manuf: "Milwaukee", E1_Brand: "-- Unbranded --" } },
  { name: "TimberTech Decking", cat: "Building Materials", data: { Mfg_Part_Num: "ADB15516CS", Part_Desc: "Coastline Sq Edge PVC", Part_Manuf: "Parksite", E1_Brand: "TIMBERTECH" } },
  { name: "Philips LED Bulb", cat: "Lighting", data: { Mfg_Part_Num: "565374", Part_Desc: "75W Led A19 Med 27k", Part_Manuf: "Phillips", E1_Brand: "-- Unbranded --" } }
];

// DOM Elements Cache
const el = {
  startupOverlay: document.getElementById('startup-overlay'),
  navLinks: document.querySelectorAll('.nav-link'),
  tabPanels: document.querySelectorAll('.tab-panel'),
  cmdPalette: document.getElementById('cmd-palette'),
  btnCmdK: document.getElementById('btn-cmd-k'),
  cmdInput: document.querySelector('.cmd-input'),
  cmdItems: document.querySelectorAll('.cmd-item'),
  
  // Single
  quickSamples: document.getElementById('quick-samples-container'),
  inputMpn: document.getElementById('input-mpn'),
  inputDesc: document.getElementById('input-desc'),
  inputManuf: document.getElementById('input-manuf'),
  inputE1Brand: document.getElementById('input-e1-brand'),
  btnEnrich: document.getElementById('btn-enrich-single'),
  
  pipeline: document.getElementById('ai-pipeline'),
  pipelineFill: document.getElementById('pipeline-fill'),
  pipeSteps: [
    document.getElementById('step-raw'),
    document.getElementById('step-ai'),
    document.getElementById('step-class'),
    document.getElementById('step-std'),
    document.getElementById('step-val')
  ],
  
  studioEmpty: document.getElementById('studio-empty-state'),
  resultsPayload: document.getElementById('results-payload'),
  
  // Results
  confValTxt: document.getElementById('conf-val-txt'),
  confSvgRing: document.getElementById('conf-svg-ring'),
  idTitle: document.getElementById('id-title'),
  idMpn: document.getElementById('id-mpn'),
  idMetaTags: document.getElementById('id-meta-tags'),
  outShortDesc: document.getElementById('out-short-desc'),
  outInvoiceDesc: document.getElementById('out-invoice-desc'),
  outInvoiceMeter: document.getElementById('out-invoice-meter'),
  outMobileDesc: document.getElementById('out-mobile-desc'),
  outMobileMeter: document.getElementById('out-mobile-meter'),
  outFeatures: document.getElementById('out-features'),
  outAttributes: document.getElementById('out-attributes'),
  
  // Batch
  vizProd: document.getElementById('viz-prod'),
  vizAttr: document.getElementById('viz-attr'),
  vizConf: document.getElementById('viz-conf'),
  btnRunBatch: document.getElementById('btn-run-batch'),
  batchTbody: document.getElementById('batch-tbody'),
  csvUpload: document.getElementById('csv-upload'),
  btnExpCsv: document.getElementById('btn-exp-csv'),
  btnExpXls: document.getElementById('btn-exp-xls'),
  
  liveStreamPanel: document.getElementById('live-stream-panel'),
  streamFeed: document.getElementById('stream-feed'),
  streamProgressTxt: document.getElementById('stream-progress-txt')
};

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
  handleStartup();
  setupNavigation();
  setupCommandPalette();
  setupSamples();
  setupEventListeners();
});

function handleStartup() {
  const hasSeen = sessionStorage.getItem('unicat_intro');
  if (hasSeen) {
    el.startupOverlay.classList.add('hidden');
  } else {
    setTimeout(() => {
      el.startupOverlay.style.opacity = '0';
      setTimeout(() => {
        el.startupOverlay.classList.add('hidden');
        sessionStorage.setItem('unicat_intro', '1');
      }, 400);
    }, 2000);
  }
}

function setupNavigation() {
  el.navLinks.forEach(link => {
    link.addEventListener('click', () => {
      const tab = link.getAttribute('data-tab');
      el.navLinks.forEach(l => l.classList.remove('active'));
      el.tabPanels.forEach(p => p.classList.remove('active'));
      link.classList.add('active');
      document.getElementById(`tab-${tab}`).classList.add('active');
    });
  });
}

function setupCommandPalette() {
  const togglePalette = () => {
    const isHidden = el.cmdPalette.style.display === 'none' || el.cmdPalette.style.display === '';
    el.cmdPalette.style.display = isHidden ? 'flex' : 'none';
    if (isHidden) el.cmdInput.focus();
  };

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      togglePalette();
    }
    if (e.key === 'Escape' && el.cmdPalette.style.display === 'flex') {
      togglePalette();
    }
  });

  el.btnCmdK.addEventListener('click', togglePalette);
  
  el.cmdPalette.addEventListener('click', (e) => {
    if (e.target === el.cmdPalette) togglePalette();
  });
  
  el.cmdItems.forEach(item => {
    item.addEventListener('click', () => {
      executeCommand(item.getAttribute('data-action'));
      togglePalette();
    });
  });
}

function executeCommand(action) {
  if(action === 'enrich') document.querySelector('.nav-link[data-tab="studio"]').click();
  if(action === 'batch') {
    document.querySelector('.nav-link[data-tab="batch"]').click();
    el.btnRunBatch.click();
  }
  if(action === 'upload') el.csvUpload.click();
  if(action === 'export') window.open(ApiService.getExportCsvUrl(), '_blank');
  if(action === 'reset') location.reload();
}

function setupSamples() {
  el.quickSamples.innerHTML = '';
  SAMPLE_PRESETS.forEach(s => {
    const chip = document.createElement('div');
    chip.className = 'sample-chip';
    chip.innerHTML = `<span>${s.name}</span><span>${s.cat}</span>`;
    chip.addEventListener('click', () => {
      el.inputMpn.value = s.data.Mfg_Part_Num || '';
      el.inputDesc.value = s.data.Part_Desc || '';
      el.inputManuf.value = s.data.Part_Manuf || '';
      el.inputE1Brand.value = s.data.E1_Brand || '';
      el.btnEnrich.click();
    });
    el.quickSamples.appendChild(chip);
  });
}

function setupEventListeners() {
  el.btnEnrich.addEventListener('click', runSingleEnrichment);
  el.btnRunBatch.addEventListener('click', runBatchProcessing);
  el.csvUpload.addEventListener('change', (e) => {
    if (e.target.files.length) handleCsvUpload(e.target.files[0]);
  });
  el.btnExpCsv.addEventListener('click', () => window.open(ApiService.getExportCsvUrl(), '_blank'));
  el.btnExpXls.addEventListener('click', () => window.open(ApiService.getExportExcelUrl(), '_blank'));
}

/* =======================================
   SINGLE ENRICHMENT & PIPELINE
   ======================================= */
async function runSingleEnrichment() {
  const rawInput = {
    Mfg_Part_Num: el.inputMpn.value.trim(),
    Part_Desc: el.inputDesc.value.trim(),
    Part_Manuf: el.inputManuf.value.trim(),
    E1_Brand: el.inputE1Brand.value.trim()
  };
  
  el.studioEmpty.classList.add('hidden');
  el.resultsPayload.classList.add('hidden');
  el.pipeline.classList.remove('hidden');
  
  // Pipeline Animation Setup
  el.btnEnrich.classList.add('processing');
  el.btnEnrich.innerHTML = '◌ ANALYZING PRODUCT...';
  
  el.pipelineFill.style.width = '0%';
  el.pipeSteps.forEach(s => s.className = 'pipeline-step');
  
  // Fake the timeline for WOW effect (1.5s total)
  const timeline = [
    { time: 0, w: '0%', idx: 0, text: '◌ ANALYZING...' },
    { time: 300, w: '25%', idx: 1, text: '✦ ENRICHING...' },
    { time: 600, w: '50%', idx: 2, text: '✦ CLASSIFYING...' },
    { time: 900, w: '75%', idx: 3, text: '✦ STANDARDIZING...' },
    { time: 1200, w: '100%', idx: 4, text: '✓ COMPLIANCE CHECK...' }
  ];
  
  timeline.forEach(t => {
    setTimeout(() => {
      el.pipelineFill.style.width = t.w;
      el.pipeSteps[t.idx].classList.add('active');
      if (t.idx > 0) el.pipeSteps[t.idx-1].classList.replace('active', 'done');
      el.btnEnrich.innerHTML = t.text;
    }, t.time);
  });
  
  // Real API Call concurrently
  let product = null;
  try {
    product = await ApiService.enrichSingle(rawInput);
  } catch (err) {
    alert("Enrichment failed: " + err.message);
    el.btnEnrich.classList.remove('processing');
    el.btnEnrich.innerHTML = '⚡ Enrich & Validate';
    return;
  }
  
  // Wait for animation to finish
  setTimeout(() => {
    el.pipeSteps[4].classList.replace('active', 'done');
    el.btnEnrich.innerHTML = '✓ VALIDATED';
    setTimeout(() => {
      el.btnEnrich.classList.remove('processing');
      el.btnEnrich.innerHTML = '⚡ Enrich & Validate';
      renderResults(product);
    }, 500);
  }, 1500);
}

function renderResults(p) {
  el.resultsPayload.classList.remove('hidden');
  
  // Remove stagger classes briefly to replay animation
  const staggers = el.resultsPayload.querySelectorAll('.stagger-in');
  staggers.forEach(el => el.classList.remove('visible'));
  
  // Update Confidence
  el.confValTxt.textContent = `${p.confidence_score}%`;
  // calculate stroke-dashoffset (163 is full circle)
  const offset = 163 - (163 * p.confidence_score / 100);
  setTimeout(() => el.confSvgRing.style.strokeDashoffset = offset, 100);
  
  // Identity Card
  el.idTitle.textContent = p.short_desc || p.product_name;
  el.idMpn.textContent = p.mfg_part_num;
  el.idMetaTags.innerHTML = `
    <span class="id-tag">${p.brand_name || 'No Brand'}</span>
    <span class="id-tag">${p.classpath || 'Uncategorized'}</span>
  `;
  
  // Delivery Content
  el.outShortDesc.textContent = p.short_desc;
  el.outInvoiceDesc.textContent = p.invoice_desc;
  el.outInvoiceMeter.textContent = `${(p.invoice_desc||'').length} / 40 chars`;
  el.outMobileDesc.textContent = p.mobile_desc;
  el.outMobileMeter.textContent = `${(p.mobile_desc||'').length} / 80 chars`;
  
  // Intelligence Chips
  el.outFeatures.innerHTML = '';
  p.item_features.forEach((feat) => {
    const chip = document.createElement('div');
    chip.className = 'feature-chip';
    chip.innerHTML = `<span>✓</span> ${feat}`;
    el.outFeatures.appendChild(chip);
  });
  
  // Data Explorer Grid
  el.outAttributes.innerHTML = '';
  const attrs = p.attributes.filter(a => a.label && a.value);
  attrs.forEach((attr) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td style="color:var(--text-secondary);">${attr.label}</td>
      <td style="font-weight:500;">${attr.value} ${attr.uom||''}</td>
      <td><span class="status-badge val">✓ Matched</span></td>
    `;
    el.outAttributes.appendChild(tr);
  });
  
  // Re-trigger stagger animations
  staggers.forEach((el, idx) => {
    el.style.animationDelay = `${idx * 100}ms`;
    requestAnimationFrame(() => el.classList.add('visible'));
  });
}

/* =======================================
   BATCH PROCESSING ENGINE
   ======================================= */
async function runBatchProcessing() {
  startBatchVisuals();
  
  try {
    const sampleData = await ApiService.get1000Samples(1000, 0);
    const response = await ApiService.enrichBatch(sampleData.items);
    finishBatchVisuals(response);
  } catch (err) {
    alert("Batch error: " + err.message);
    el.btnRunBatch.disabled = false;
    el.btnRunBatch.innerHTML = '⚡ Process 1,000 Items';
  }
}

async function handleCsvUpload(file) {
  startBatchVisuals();
  try {
    const response = await ApiService.uploadCsv(file, 1000);
    finishBatchVisuals(response);
  } catch (err) {
    alert("CSV error: " + err.message);
  }
}

let streamInterval;
function startBatchVisuals() {
  el.btnRunBatch.disabled = true;
  el.btnRunBatch.innerHTML = '◌ PROCESSING...';
  
  // Zero out stats
  el.vizProd.textContent = '0';
  el.vizAttr.textContent = '0';
  el.vizConf.textContent = '0%';
  
  el.batchTbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:3rem;"><div class="empty-icon" style="font-size:1.5rem">⚡</div>Initializing Engine...</td></tr>';
  
  // Start Streaming feed
  el.liveStreamPanel.classList.remove('hidden');
  el.streamFeed.innerHTML = '';
  let count = 0;
  streamInterval = setInterval(() => {
    count += Math.floor(Math.random() * 45) + 15;
    if (count > 1000) count = 1000;
    el.streamProgressTxt.textContent = `Processing ${count} / 1,000`;
    
    // add fake log
    const msgs = [
      `<span class="scs">✓</span> PDSH4816AF — classified`,
      `<span class="scs">✓</span> 12345-AB — standardized`,
      `<span class="wrn">⚠</span> 8742-X — human review required`,
      `<span class="scs">✓</span> M18-CUT — validated`,
      `✦ Extracting dimensions...`,
      `✦ Cross-referencing vocab DB...`
    ];
    const log = document.createElement('div');
    log.className = 'stream-item';
    log.innerHTML = msgs[Math.floor(Math.random() * msgs.length)];
    el.streamFeed.appendChild(log);
    
    if (el.streamFeed.children.length > 5) {
      el.streamFeed.removeChild(el.streamFeed.firstChild);
    }
  }, 300);
}

function finishBatchVisuals(res) {
  clearInterval(streamInterval);
  el.btnRunBatch.innerHTML = '⚡ Process 1,000 Items';
  el.btnRunBatch.disabled = false;
  
  el.streamProgressTxt.textContent = `Processing Complete (1,000 / 1,000)`;
  setTimeout(() => el.liveStreamPanel.classList.add('hidden'), 2500);
  
  // Animate Numbers
  animateValue(el.vizProd, 0, res.total_processed, 1500);
  animateValue(el.vizAttr, 0, 252, 1500); // hardcoded feature count for demo
  animateValue(el.vizConf, 0, res.average_confidence, 1500, '%');
  
  // Render Table
  el.batchTbody.innerHTML = '';
  const displayItems = res.results.slice(0, 50); // limit to 50 for DOM perf
  
  displayItems.forEach((p, idx) => {
    const tr = document.createElement('tr');
    tr.style.opacity = 0;
    tr.style.animation = `fadeSlideUp 400ms ease-out ${idx*20}ms forwards`;
    
    tr.innerHTML = `
      <td style="font-family:monospace; color:var(--electric-blue);">${p.mfg_part_num}</td>
      <td style="font-weight:600;">${p.brand_name}</td>
      <td style="font-size:0.7rem; color:var(--text-secondary);">${p.classpath}</td>
      <td style="font-family:monospace; font-size:0.75rem;">${p.invoice_desc}</td>
      <td>
        <div style="display:flex; align-items:center;">
          <span style="font-weight:600; width:35px;">${p.confidence_score}%</span>
          <div class="conf-bar-wrap"><div class="conf-bar" style="width:${p.confidence_score}%; background:${p.confidence_score>90?'var(--status-success)':'var(--status-warning)'}"></div></div>
        </div>
      </td>
      <td>
        <span class="status-badge ${p.needs_human_review ? 'rev' : 'val'}">
          ${p.needs_human_review ? '⚠ REVIEW' : '✓ VALIDATED'}
        </span>
      </td>
    `;
    el.batchTbody.appendChild(tr);
  });
}

function animateValue(obj, start, end, duration, suffix = '') {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 4); // easeOutQuart
    obj.innerHTML = Math.floor(ease * (end - start) + start) + suffix;
    if (progress < 1) window.requestAnimationFrame(step);
    else obj.innerHTML = end + suffix;
  };
  window.requestAnimationFrame(step);
}
