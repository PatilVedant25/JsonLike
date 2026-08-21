/**
 * UniCat 2.0 - Premium Minimal AI SaaS
 */
import { ApiService } from './api.js';

const SAMPLE_DATA = [
  { name: "Frigidaire Dishwasher", cat: "Home Appliances", data: { Mfg_Part_Num: "PDSH4816AF", Part_Desc: "PDSH4816AF Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Whirlpool Eco Dishwasher", cat: "Home Appliances", data: { Mfg_Part_Num: "WDTS7024RZ", Part_Desc: "WDTS7024RZ Dishwasher SS", Part_Manuf: "Appliance Dealers Coop", E1_Brand: "-- Unbranded --" } },
  { name: "Diablo Sanding Belt", cat: "Power Tools", data: { Mfg_Part_Num: "DCB518ASTS06G", Part_Desc: "Diablo 1/2x18 Sanding Belt", Part_Manuf: "Freud Inc", E1_Brand: "-- Unbranded --" } },
  { name: "Milwaukee Cut-Off Disc", cat: "Power Tools", data: { Mfg_Part_Num: "49-94-0013", Part_Desc: "Milw 5x.045 Metal Disc", Part_Manuf: "Milwaukee", E1_Brand: "-- Unbranded --" } },
  { name: "TimberTech Azek PVC Decking", cat: "Building Materials", data: { Mfg_Part_Num: "ADB15516CS", Part_Desc: "Coastline Sq Edge PVC", Part_Manuf: "Parksite", E1_Brand: "TIMBERTECH" } },
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
  
  // Single Results
  studioEmpty: document.getElementById('studio-empty-state'),
  resultsPayload: document.getElementById('results-payload'),
  resStatus: document.getElementById('res-status'),
  studioPipeline: document.getElementById('studio-pipeline'),
  pipeSteps: document.querySelectorAll('#studio-pipeline .pipeline-step'),
  
  idTitle: document.getElementById('id-title'),
  idMeta: document.getElementById('id-meta'),
  confTxt: document.getElementById('conf-txt'),
  
  outInvoiceDesc: document.getElementById('out-invoice-desc'),
  outMobileDesc: document.getElementById('out-mobile-desc'),
  outShortDesc: document.getElementById('out-short-desc'),
  
  outFeatures: document.getElementById('out-features'),
  outAttributes: document.getElementById('out-attributes'),
  notesTxt: document.getElementById('notes-txt'),
  
  // Batch
  btnRunBatch: document.getElementById('btn-run-batch'),
  csvUpload: document.getElementById('csv-upload'),
  btnExpCsv: document.getElementById('btn-exp-csv'),
  btnExpXls: document.getElementById('btn-exp-xls'),
  
  statProd: document.getElementById('stat-prod'),
  statConf: document.getElementById('stat-conf'),
  statRev: document.getElementById('stat-rev'),
  
  batchProgress: document.getElementById('batch-progress'),
  progStatusTxt: document.getElementById('prog-status-txt'),
  progPctTxt: document.getElementById('prog-pct-txt'),
  progFill: document.getElementById('prog-fill'),
  batchPipeSteps: document.querySelectorAll('#batch-pipeline .pipeline-step'),
  liveFeed: document.getElementById('live-feed'),
  
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
  const hasSeen = sessionStorage.getItem('unicat_prem_intro');
  if (hasSeen) {
    el.startupOverlay.classList.add('hidden');
  } else {
    setTimeout(() => {
      el.startupOverlay.style.opacity = '0';
      setTimeout(() => {
        el.startupOverlay.classList.add('hidden');
        sessionStorage.setItem('unicat_prem_intro', '1');
      }, 400); 
    }, 1000); 
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
      <span style="font-weight:500; color:var(--text-primary);">${s.name}</span>
      <span class="sample-item-icon">→</span>
    `;
    item.addEventListener('click', () => {
      el.inputMpn.value = s.data.Mfg_Part_Num || '';
      el.inputDesc.value = s.data.Part_Desc || '';
      el.inputManuf.value = s.data.Part_Manuf || '';
      el.inputBrand.value = s.data.E1_Brand || '';
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
  
  document.querySelectorAll('.btn-copy').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const val = e.target.nextElementSibling.nextElementSibling.textContent;
      navigator.clipboard.writeText(val);
      e.target.textContent = '✓ Copied';
      setTimeout(() => e.target.textContent = 'Copy', 1500);
    });
  });
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
  
  // UI State: Processing
  el.btnEnrich.innerHTML = '<div class="spinner"></div> Enriching product...';
  el.btnEnrich.disabled = true;
  el.studioEmpty.classList.add('hidden');
  el.resultsPayload.classList.add('hidden');
  el.studioPipeline.classList.remove('hidden');
  
  el.resStatus.innerHTML = '<div class="status-dot" style="background:var(--accent-blue);"></div> Processing';
  
  // Reset pipeline
  el.pipeSteps.forEach(s => s.className = 'pipeline-step');
  
  // Fake animation timing (Total ~800ms)
  setTimeout(() => el.pipeSteps[0].classList.add('done'), 100);
  setTimeout(() => { el.pipeSteps[1].classList.add('active'); }, 200);
  setTimeout(() => { el.pipeSteps[1].classList.replace('active', 'done'); el.pipeSteps[2].classList.add('active'); }, 500);
  
  let product = null;
  try {
    product = await ApiService.enrichSingle(rawInput);
  } catch (err) {
    alert("Enrichment failed: " + err.message);
    el.btnEnrich.innerHTML = '<span>⚡</span> Enrich & Validate';
    el.btnEnrich.disabled = false;
    return;
  }
  
  setTimeout(() => { 
    el.pipeSteps[2].classList.replace('active', 'done');
    el.pipeSteps[3].classList.add('done');
    el.resStatus.innerHTML = '<div class="status-dot"></div> Complete';
    el.btnEnrich.innerHTML = '✓ Enrichment complete';
    
    setTimeout(() => {
      el.btnEnrich.innerHTML = '<span>⚡</span> Enrich & Validate';
      el.btnEnrich.disabled = false;
      renderResults(product);
    }, 400);
    
  }, 800);
}

function renderResults(p) {
  // Reset staggers
  const staggers = el.resultsPayload.querySelectorAll('.stagger-in');
  staggers.forEach(el => el.classList.remove('visible'));
  
  el.resultsPayload.classList.remove('hidden');
  
  el.idTitle.textContent = p.short_desc || p.product_name || p.mfg_part_num;
  el.idMeta.textContent = `${p.brand_name || 'No Brand'} · ${p.classpath ? p.classpath.split('>').pop().trim() : 'Uncategorized'}`;
  
  el.outInvoiceDesc.textContent = p.invoice_desc;
  el.outMobileDesc.textContent = p.mobile_desc;
  el.outShortDesc.textContent = p.short_desc;
  
  el.outFeatures.innerHTML = '';
  p.item_features.forEach(f => {
    const li = document.createElement('li');
    li.textContent = f;
    li.className = 'stagger-in';
    el.outFeatures.appendChild(li);
  });
  
  el.outAttributes.innerHTML = '';
  const validAttrs = p.attributes.filter(a => a.label && a.value);
  validAttrs.forEach(attr => {
    const row = document.createElement('div');
    row.className = 'attr-row';
    row.innerHTML = `<div class="attr-key">${attr.label}</div><div class="attr-val">${attr.value} ${attr.uom||''}</div>`;
    el.outAttributes.appendChild(row);
  });
  
  // Calculate confidence animation
  el.confTxt.textContent = '0%';
  animateValue(el.confTxt, 0, p.confidence_score, 800, '%');
  
  // Re-fetch staggers (now including dynamic features)
  const allStaggers = el.resultsPayload.querySelectorAll('.stagger-in');
  allStaggers.forEach((elem, idx) => {
    elem.style.animationDelay = `${idx * 40}ms`;
    requestAnimationFrame(() => elem.classList.add('visible'));
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
  el.btnRunBatch.innerHTML = '<div class="spinner" style="margin-right:0.5rem; display:inline-block;"></div> Processing...';
  el.batchProgress.classList.remove('hidden');
  el.batchPipeSteps.forEach(s => s.className = 'pipeline-step');
  el.batchPipeSteps[0].classList.add('active');
  
  let current = 0;
  el.liveFeed.innerHTML = '';
  
  // Zero stats
  el.statProd.textContent = '0';
  el.statConf.textContent = '0%';
  el.statRev.textContent = '0';
  
  batchInterval = setInterval(() => {
    current += Math.floor(Math.random() * 45) + 15;
    if (current >= total) current = total - Math.floor(Math.random() * 5); 
    
    let pct = Math.floor((current / total) * 100);
    el.progStatusTxt.textContent = `Processing Catalog... ${current.toLocaleString()} / ${total.toLocaleString()}`;
    el.progPctTxt.textContent = `${pct}%`;
    el.progFill.style.width = `${pct}%`;
    
    // update pipeline
    if (pct > 20) { el.batchPipeSteps[0].classList.replace('active','done'); el.batchPipeSteps[1].classList.add('active'); }
    if (pct > 60) { el.batchPipeSteps[1].classList.replace('active','done'); el.batchPipeSteps[2].classList.add('active'); }
    if (pct > 90) { el.batchPipeSteps[2].classList.replace('active','done'); el.batchPipeSteps[3].classList.add('active'); }
    
    // add fake log
    const msgs = [
      `<span class="scs">✓</span> PDSH4816AF enriched`,
      `<span class="scs">✓</span> 12345-AB classified`,
      `<span class="wrn">⚠</span> 8742-X human review`,
      `<span class="scs">✓</span> M18-CUT validated`
    ];
    const log = document.createElement('div');
    log.className = 'feed-item';
    log.innerHTML = msgs[Math.floor(Math.random() * msgs.length)];
    el.liveFeed.appendChild(log);
    
    if (el.liveFeed.children.length > 3) {
      el.liveFeed.removeChild(el.liveFeed.firstChild);
    }
  }, 250);
}

function finishBatchProgress(res) {
  clearInterval(batchInterval);
  
  el.progStatusTxt.textContent = `Completed ${res.total_processed.toLocaleString()} records`;
  el.progPctTxt.textContent = `100%`;
  el.progFill.style.width = `100%`;
  
  el.batchPipeSteps[3].classList.replace('active','done');
  
  el.btnRunBatch.disabled = false;
  el.btnRunBatch.innerHTML = '⚡ Process 1,000 Sample Items';
  
  animateValue(el.statProd, 0, res.total_processed, 800);
  animateValue(el.statConf, 0, res.average_confidence, 800, '%');
  animateValue(el.statRev, 0, res.review_needed_count, 800);
  
  renderTable(res.results);
  
  setTimeout(() => el.batchProgress.classList.add('hidden'), 3500);
}

function resetBatchProgress() {
  clearInterval(batchInterval);
  el.btnRunBatch.disabled = false;
  el.btnRunBatch.innerHTML = '⚡ Process 1,000 Sample Items';
  el.batchProgress.classList.add('hidden');
}

function renderTable(results) {
  el.batchTbody.innerHTML = '';
  const displayItems = results.slice(0, 50);
  
  displayItems.forEach((p, idx) => {
    const tr = document.createElement('tr');
    tr.style.opacity = 0;
    tr.style.animation = `textFade 300ms ease-out ${idx*10}ms forwards`;
    
    let badge = p.needs_human_review 
      ? '<span class="badge badge-rev">REVIEW</span>'
      : '<span class="badge badge-val">VALIDATED</span>';
      
    tr.innerHTML = `
      <td style="color:var(--text-tertiary);">${idx+1}</td>
      <td style="font-family:monospace; color:var(--text-secondary);">${p.mfg_part_num}</td>
      <td style="font-weight:500;">${p.brand_name}</td>
      <td style="font-size:0.75rem; color:var(--text-secondary);">${p.classpath}</td>
      <td style="font-family:monospace; font-size:0.8rem;">${p.invoice_desc}</td>
      <td>
        <span style="font-weight:500;">${p.confidence_score}%</span>
        <div class="conf-bar-wrap"><div class="conf-bar" style="width:${p.confidence_score}%;"></div></div>
      </td>
      <td>${badge}</td>
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
    obj.innerHTML = (progress === 1 ? end : Math.floor(ease * (end - start) + start)) + suffix;
    if (progress < 1) window.requestAnimationFrame(step);
  };
  window.requestAnimationFrame(step);
}
