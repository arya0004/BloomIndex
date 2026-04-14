# 🌱 BloomIndex AI  
**Business Timing Intelligence & Predictive Revival Engine**

---

## 📌 Overview  
BloomIndex AI is a predictive analytics platform designed to evaluate whether historically failed business ideas can succeed in today’s environment.

The system combines macroeconomic indicators, technological readiness, and machine learning models to generate a **Bloom Score**, which represents the probability of a successful revival.

---

## 🚀 Features  

- 📊 **Bloom Score Engine**  
  Calculates a normalized score (0–100) indicating business revival potential  

- 🤖 **Machine Learning Models**  
  - XGBoost for classification  
  - LSTM for time-series forecasting  

- 🌍 **Geotrade Intelligence**  
  Tracks global conditions such as:
  - War/conflict zones  
  - Trade disruptions  
  - Climate stress  

- 📈 **Interactive Dashboard**  
  - Real-time metrics visualization  
  - Bloom score gauges  
  - Market forecasts  
  - Global maps  

- 🔍 **Search & Compare**  
  Analyze companies and sectors using Bloom metrics  

---

## 🧠 Bloom Score Formula  
BloomScore = [(T_now × S_now) + (C_now × W_now)] ÷ R_past


### Variables:
- **T_now** → Technology maturity (0–10)  
- **S_now** → Social readiness (0–10)  
- **C_now** → Capital availability (0–10)  
- **W_now** → Geopolitical stability (0–10)  
- **R_past** → Historical failure weight (1–5)  

### Interpretation:
- **≥ 70** → Strong Bloom  
- **50–69** → Emerging  
- **< 50** → Dormant  

---

## 🏗️ Project Structure  
BloomIndex/
│
├── backend/
│ └── logic/
│ └── bloom_score.py
│
├── frontend/
│ └── Bloom_index_dashboard.html
│
├── api/
│ ├── comeback-kids
│ ├── geotrade-map
│ ├── market-forecast
│ └── search-company
│
└── README.md


---

## ⚙️ Installation  

### 1. Clone the repository  
git clone https://github.com/your-username/bloomindex-ai.git

cd bloomindex-ai


### 2. Install dependencies  

pip install -r requirements.txt


### 3. Run the backend server  

uvicorn main:app --reload


### 4. Run the frontend  
Open the file in your browser:

Bloom_index_dashboard.html


---

## 📊 Example Output  

```json
{
  "idea": "Hyper-local Delivery",
  "bloom_score": 94.0,
  "signal": "BLOOM",
  "components": {
    "demand_pull": 72.0,
    "supply_push": 54.0,
    "failure_weight": 1.5
  }
}


📈 Use Cases
Startup idea validation
Venture capital decision support
Market timing analysis
Business revival strategy
Predictive economic insights


🔬 Tech Stack
Backend: Python
Machine Learning: XGBoost, LSTM
Frontend: HTML, CSS, JavaScript
Visualization: Chart.js
📌 Future Enhancements
Real-time financial API integration
AI-powered idea recommendation engine
Cloud deployment (AWS / GCP)
Mobile-friendly dashboard
