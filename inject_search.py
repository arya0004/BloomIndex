import re


file_path = r"C:\Users\Arya Manve\Downloads\bloomindex\bloomindex_dashboard.html"


with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()


# 1. Add Tabs HTML
tabs_html = """    <div class="tabs">
      <button class="tab active" onclick="switchTab('home')">Home</button>
      <button class="tab" onclick="switchTab('overview')">Signals</button>
      <button class="tab" onclick="switchTab('map')">Geotrade Map</button>
      <button class="tab" onclick="switchTab('search')">Search & Compare</button>
      <button class="tab" onclick="switchTab('forecast')">Forecast</button>
      <button class="tab" onclick="switchTab('model')">ML Engine</button>
      <button class="tab" onclick="switchTab('formula')">Bloom Formula</button>
    </div>"""


html = re.sub(r'<div class="tabs">.*?</div>', tabs_html, html, flags=re.DOTALL)


# 2. Add New Panels HTML
panels_html = """
  <!-- SEARCH PANEL -->
  <div id="panel-search" class="panel">
    <div class="card" style="margin-bottom: 1rem;">
      <div class="card-title">Live Company Search & Compare</div>
      <div style="display:flex; gap:10px; margin-bottom:1rem;">
        <input type="text" id="searchInput" placeholder="Enter Ticker (e.g. AAPL, TSLA)" style="flex:1; padding:10px; background:var(--color-background-secondary); border:1px solid var(--color-border-secondary); color:var(--color-text-primary); border-radius:4px;">
        <button onclick="doSearch()" style="padding:10px 20px; font-weight:bold;">Search</button>
      </div>
      <div id="searchControls" style="display:none; margin-bottom:1rem;">
         <input type="text" id="compareInput" placeholder="Compare with..." style="padding:8px; background:var(--color-background-secondary); border:1px solid var(--color-border-secondary); color:var(--color-text-primary); border-radius:4px;">
         <button onclick="doCompare()" style="padding:8px 16px;">Add to Compare</button>
         <button onclick="resetSearch()" style="padding:8px 16px; margin-left:10px; background:var(--color-background-tertiary);">Clear</button>
      </div>
     
      <!-- Compare Grid -->
      <div id="compareGrid" style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
        <!-- Container for Company 1 -->
        <div id="searchRes1"></div>
        <!-- Container for Company 2 -->
        <div id="searchRes2"></div>
      </div>
    </div>
  </div>


  <!-- FORECAST PANEL -->
  <div id="panel-forecast" class="panel">
    <div class="card">
      <div class="card-title">Macro Predictive Profitability Forecast</div>
      <p style="font-size:12px; color:var(--color-text-secondary); margin-bottom:1rem;">Based on live global indices (War Index, Climate Stress, Capital Tightness). Models project long-term capital advantage flows.</p>
      <div id="forecast-list" style="display:flex; flex-direction:column; gap:12px;"></div>
    </div>
  </div>


  <!-- ML ENGINE PANEL -->"""


html = html.replace("<!-- ML ENGINE PANEL -->", panels_html)


# 3. Add Javascript Logic inside the <script> block
js_logic = """
async function fetchForecast() {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/macro-forecast');
    const data = await res.json();
    let htmlStr = '';
    data.forEach(item => {
      htmlStr += `
        <div style="background:var(--color-background-secondary); padding:16px; border-radius:8px; border-left:4px solid ${item.color};">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-weight:600; font-size:14px; color:var(--color-text-primary);">${item.sector}</div>
            <div style="font-weight:bold; font-size:18px; color:${item.color};">Bloom: ${item.forecast_bloom}</div>
          </div>
          <div style="font-size:12px; color:var(--color-text-secondary); line-height:1.5;">${item.rationale}</div>
        </div>
      `;
    });
    document.getElementById('forecast-list').innerHTML = htmlStr;
  } catch (err) {
    console.error(err);
  }
}


function renderCompanyCard(data) {
  if (data.error) return `<div style="color:var(--color-text-danger);">${data.error}</div>`;
  return `
    <div style="padding:16px; background:var(--color-background-tertiary); border:1px solid var(--color-border-secondary); border-radius:8px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
         <div style="font-size:18px; font-weight:bold; color:var(--color-text-primary);">${data.ticker} <span style="font-size:12px; font-weight:normal; color:var(--color-text-secondary);">${data.sector}</span></div>
         <div style="font-size:24px; font-weight:900; color:${data.color};">${data.bloom_score}</div>
      </div>
      <div style="font-size:14px; margin-top:4px;">${data.name}</div>
      <div style="font-size:20px; font-family:monospace; margin-top:8px;">$${data.price}</div>
      <div style="margin-top:12px; font-size:12px; line-height:1.5; color:var(--color-text-secondary); border-top:1px solid var(--color-border-secondary); padding-top:8px;">
        ${data.story}
      </div>
    </div>
  `;
}


async function doSearch() {
  const ticker = document.getElementById('searchInput').value;
  if (!ticker) return;
  document.getElementById('searchRes1').innerHTML = "Loading...";
  try {
    const res = await fetch('http://127.0.0.1:8000/api/search-company?ticker=' + ticker);
    const data = await res.json();
    document.getElementById('searchRes1').innerHTML = renderCompanyCard(data);
    document.getElementById('searchControls').style.display = 'flex';
  } catch(e) {
    document.getElementById('searchRes1').innerHTML = "Error loading.";
  }
}


async function doCompare() {
  const ticker = document.getElementById('compareInput').value;
  if (!ticker) return;
  document.getElementById('searchRes2').innerHTML = "Loading...";
  try {
    const res = await fetch('http://127.0.0.1:8000/api/search-company?ticker=' + ticker);
    const data = await res.json();
    document.getElementById('searchRes2').innerHTML = renderCompanyCard(data);
  } catch(e) {
    document.getElementById('searchRes2').innerHTML = "Error loading.";
  }
}


function resetSearch() {
  document.getElementById('searchInput').value = '';
  document.getElementById('compareInput').value = '';
  document.getElementById('searchRes1').innerHTML = '';
  document.getElementById('searchRes2').innerHTML = '';
  document.getElementById('searchControls').style.display = 'none';
}


// Intercept switchTab to initiate forecast fetch
const oldSwitchTab = switchTab;
window.switchTab = function(tab) {
  oldSwitchTab(tab);
  if (tab === 'forecast') fetchForecast();
}
"""


html = html.replace("document.addEventListener('DOMContentLoaded', initDashboard);", js_logic + "\ndocument.addEventListener('DOMContentLoaded', initDashboard);")


with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)


