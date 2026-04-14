import re


file_path = r"C:\Users\Arya Manve\Downloads\bloomindex\bloomindex_dashboard.html"


with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()


# 1. Update Tabs
html = html.replace(
    """    <div class="tabs">
      <button class="tab active" onclick="switchTab('overview')">Overview</button>""",
    """    <div class="tabs">
      <button class="tab active" onclick="switchTab('home')">Home</button>
      <button class="tab" onclick="switchTab('overview')">Signals</button>"""
)


# 2. Add Home Panel & hide overview
home_panel = """
  <!-- HOME PANEL -->
  <div id="panel-home" class="panel active">
    <div class="card" style="margin-bottom: 2rem;">
      <h2 style="margin-bottom: 1rem; color: var(--color-text-success);">Welcome to BloomIndex AI</h2>
      <p style="color: var(--color-text-secondary); margin-bottom: 1.5rem; font-size: 15px; line-height: 1.6;">
        BloomIndex is a global predictive engine that analyzes historical business failures and scores their probability of success <strong>today</strong> based on real-time macro conditions. We cross-reference live stock market data, active geopolitical conflict zones (trade disruption), tech maturity, and capital availability.<br><br>
        <strong>Key Variables:</strong><br><br>
        • <strong>Tₙ (Tech Maturity):</strong> Measures if AI/hardware can now support the idea.<br>
        • <strong>Sₙ (Social Readiness):</strong> Measures if society/culture is ready to adopt it post-pandemic.<br>
        • <strong>Cₙ (Capital Access):</strong> Evaluates fed interest rates and VC funding climate.<br>
        • <strong>Wₙ (War/Stability):</strong> Geopolitical tension which disrupts supply chains but creates opportunities for defense/local tech.<br>
        • <strong>Rₚ (Failure Weight):</strong> How fundamentally flawed the original failure was.
      </p>
      <button onclick="switchTab('overview')" style="padding: 10px 20px; font-weight: 600; background: var(--color-background-success); color: var(--color-text-success); border: 1px solid var(--color-text-success); border-radius: 8px;">Explore Active Signals ↗</button>
    </div>
  </div>


  <!-- OVERVIEW PANEL -->
  <div id="panel-overview" class="panel">"""


html = html.replace(
    """  <!-- OVERVIEW PANEL -->\n  <div id="panel-overview" class="panel active">""",
    home_panel
)


# 3. Chart wrappers
html = html.replace(
    """<canvas id="sparkChart" height="160" role="img" aria-label="Time series forecast of market bloom cycles"></canvas>""",
    """<div style="height: 180px; position: relative; width: 100%;"><canvas id="sparkChart" role="img" aria-label="Time series forecast of market bloom cycles"></canvas></div>"""
)
html = html.replace(
    """<canvas id="lstmChart" height="160" role="img" aria-label="LSTM market seasonality forecast showing predicted vs actual bloom cycles"></canvas>""",
    """<div style="height: 180px; position: relative; width: 100%;"><canvas id="lstmChart" role="img" aria-label="LSTM market seasonality forecast showing predicted vs actual bloom cycles"></canvas></div>"""
)


# 4. JavaScript Replacement
# We'll use regex to isolate the <script> block content after Chart.js inclusion
script_replacement = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
let ideaData = [];
const isDark = matchMedia('(prefers-color-scheme: dark)').matches;
const gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)';
const textColor = isDark ? '#888780' : '#73726c';


async function initDashboard() {
  try {
    // 1. Fetch live Comeback Kids
    const kidsRes = await fetch('http://127.0.0.1:8000/api/comeback-kids');
    ideaData = await kidsRes.json();
   
    let htmlStr = '';
    ideaData.forEach((d, i) => {
      htmlStr += `
        <div class="kid" onclick="showDetail(${i})">
          <div class="kid-icon" style="background:${d.bg}">${d.icon}</div>
          <div>
            <div class="kid-name">${d.name}</div>
            <div class="kid-meta">${d.story}</div>
          </div>
          <div class="kid-score ${d.scoreClass}">${d.score}</div>
        </div>`;
    });
    document.getElementById('kids-list').innerHTML = htmlStr;


    // 2. Fetch Map Data
    const mapRes = await fetch('http://127.0.0.1:8000/api/geotrade-map');
    const mapData = await mapRes.json();
    // Pre-populate SVG mappings dynamically if required, here we just bind the data to an array for now
    window.mapDataCache = mapData;
   
    // 3. Fetch Graph Data
    const chartRes = await fetch('http://127.0.0.1:8000/api/market-forecast');
    const chartData = await chartRes.json();
   
    // Render Spark Chart
    new Chart(document.getElementById('sparkChart'), {
      type: 'line',
      data: {
        labels: chartData.spark.labels,
        datasets: [
          { label:'Actual', data: chartData.spark.actual, borderColor:'#1D9E75', backgroundColor:'rgba(29,158,117,0.08)', tension:0.4, borderWidth:2, pointRadius:3, fill:true },
          { label:'Forecast', data: chartData.spark.forecast, borderColor:'#EF9F27', borderDash:[5,4], backgroundColor:'rgba(239,159,39,0.05)', tension:0.4, borderWidth:2, pointRadius:3, fill:true }
        ]
      },
      options: { animation: false, responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}},y:{min:50,max:100,grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}}}}
    });


    // Render LSTM Chart
    new Chart(document.getElementById('lstmChart'), {
      type: 'line',
      data: {
        labels: chartData.lstm.labels,
        datasets: [
          { label:'Actual', data: chartData.lstm.actual, borderColor:'#1D9E75', tension:0.4, borderWidth:2, pointRadius:2 },
          { label:'LSTM pred', data: chartData.lstm.pred, borderColor:'#534AB7', borderDash:[4,3], tension:0.4, borderWidth:1.5, pointRadius:2 }
        ]
      },
      options: { animation: false, responsive:true, maintainAspectRatio:false, plugins:{legend:{labels:{font:{size:10},color:textColor,boxWidth:12}}}, scales:{x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:9}}},y:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}}}}
    });


  } catch (err) {
    console.error("Error fetching live data:", err);
  }
}


function showDetail(i) {
  const d = ideaData[i];
  document.getElementById('detail-icon').style.background = d.bg;
  document.getElementById('detail-icon').textContent = d.icon;
  document.getElementById('detail-name').textContent = d.name;
  document.getElementById('detail-story').textContent = d.story;
  document.getElementById('detail-body').textContent = d.body;
  const grid = document.getElementById('detail-grid');
  grid.innerHTML = d.stats.map(s=>`<div class="detail-stat"><div class="detail-stat-val">${s.v}</div><div class="detail-stat-label">${s.l}</div></div>`).join('');
  document.getElementById('detail-panel').classList.add('visible');
}


function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('panel-'+tab).classList.add('active');
}


function showRegion(name, detail, color, score) {
  // If we have dynamic data, override parameters
  if (window.mapDataCache) {
      const match = window.mapDataCache.find(r => r.name.includes(name) || name.includes(r.name));
      if (match) {
          detail = match.detail;
          color = match.color;
          score = match.score;
      }
  }


  document.getElementById('map-info-name').textContent = name + ' — Bloom: ' + score;
  document.getElementById('map-info-detail').textContent = detail.substring(0, 90) + '…';
  const badge = document.getElementById('map-info-badge');
  badge.setAttribute('fill', color);
  badge.setAttribute('opacity', '0.9');
  badge.setAttribute('width', '70');
  const scoreEl = document.getElementById('map-info-score');
  scoreEl.textContent = score;
  scoreEl.setAttribute('x', '465');
  scoreEl.setAttribute('opacity', '1');
}


function calcBloom() {
  const t = parseFloat(document.getElementById('t_now').value);
  const s = parseFloat(document.getElementById('s_now').value);
  const c = parseFloat(document.getElementById('c_now').value);
  const w = parseFloat(document.getElementById('w_now').value);
  const r = parseFloat(document.getElementById('r_past').value);
  document.getElementById('t_val').textContent = t.toFixed(1);
  document.getElementById('s_val').textContent = s.toFixed(1);
  document.getElementById('c_val').textContent = c.toFixed(1);
  document.getElementById('w_val').textContent = w.toFixed(1);
  document.getElementById('r_val').textContent = r.toFixed(1);
  const raw = ((t * s) + (c * w)) / r;
  const score = Math.min(100, Math.round(raw * 100 / 25));
  document.getElementById('bloom-score-val').textContent = score;
  const color = score >= 75 ? '#1D9E75' : score >= 50 ? '#EF9F27' : '#E24B4A';
  const label = score >= 75 ? 'Strong bloom' : score >= 50 ? 'Emerging bloom' : 'Dormant';
  document.getElementById('bloom-ring').setAttribute('stroke', color);
  document.getElementById('bloom-ring').setAttribute('stroke-dashoffset', Math.round(440 * (1 - score/100)));
  document.getElementById('bloom-label').textContent = label;
  document.getElementById('bloom-label').setAttribute('fill', color);
}


document.addEventListener('DOMContentLoaded', initDashboard);
</script>
"""


# Replace script using regex
pattern = re.compile(r'<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart\.js/4\.4\.1/chart\.umd\.js"></script>.*?</script>', re.DOTALL)
html = pattern.sub(script_replacement, html)


with open(file_path, "w", encoding="utf-8") as f:
    f.write(html)


