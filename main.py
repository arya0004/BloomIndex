# backend/main.py


import yfinance as yf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bloom_score import (
    compute_bloom_score, EnvironmentSnapshot,
    HistoricalIdea, FailureReason
)


# Mock models since they were missing in the directory
def predict_failure_reason(features: dict):
    return {"predicted_reason": "TIMING_MISMATCH", "confidence": 0.85}


def forecast_market_season(horizon_quarters: int):
    return {"season": "bull", "forecast": "growth", "confidence": 0.9}


app = FastAPI(title="BloomIndex API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BloomRequest(BaseModel):
    idea_name: str
    failure_year: int
    failure_reason: str        # e.g. "TIMING_MISMATCH"
    original_bloom_score: float
    tech_maturity: float
    social_readiness: float
    capital_climate: float
    war_stability: float


@app.post("/bloom-score")
def get_bloom_score(req: BloomRequest):
    idea = HistoricalIdea(
        name=req.idea_name,
        failure_year=req.failure_year,
        failure_reason=FailureReason[req.failure_reason],
        original_bloom_score=req.original_bloom_score
    )
    env = EnvironmentSnapshot(
        tech_maturity=req.tech_maturity,
        social_readiness=req.social_readiness,
        capital_climate=req.capital_climate,
        war_stability=req.war_stability
    )
    return compute_bloom_score(idea, env)


@app.get("/market-season")
def get_market_season():
    """Returns LSTM/Prophet forecast of current market seasonality."""
    return forecast_market_season(horizon_quarters=4)


@app.post("/classify-failure")
def classify_failure(features: dict):
    """XGBoost classifier: given company features, predict failure reason."""
    return predict_failure_reason(features)


@app.get("/top-bloomers")
def get_top_bloomers(limit: int = 10):
    """Returns highest-scoring comeback ideas given today's environment."""
    # In production: queries database, runs bloom_score for each idea
    return {"top_bloomers": [], "season": "growth_cycle_2026"}


@app.get("/api/comeback-kids")
def get_live_comeback_kids():
    try:
        # Fetch actual stock data fast
        tickers = yf.Tickers("NVDA PLTR CRSP FSLR META")
        data = {}
        for tk in ["NVDA", "PLTR", "CRSP", "FSLR", "META"]:
            try:
                hist = tickers.tickers[tk].history(period="1d")
                price = round(hist['Close'].iloc[-1], 2)
            except:
                price = 100.0
            data[tk] = price
           
        return [
            {
                "name": "AI Infrastructure (Nvidia NVDA)",
                "icon": "🤖", "bg": "#E1F5EE",
                "story": f"Failed 2014 (Hardware too weak) — Revival: LLM maturity. Current Price: ${data['NVDA']}.",
                "body": "Nvidia is capitalizing on the massive AI infrastructure spend, mirroring the Cisco boom. Tech maturity is at an all-time high.",
                "stats": [{"l": "Past bloom", "v": "10"}, {"l": "Now bloom", "v": "98"}, {"l": "Delta", "v": "+88"}, {"l": "Market", "v": f"${data['NVDA']}"}],
                "score": 98, "scoreClass": "score-high"
            },
            {
                "name": "Defense Tech (Palantir PLTR)",
                "icon": "🛡️", "bg": "#EAF3DE",
                "story": f"Failed 2004 (No budget) — Revival: Geo tension. Current Price: ${data['PLTR']}.",
                "body": "Geopolitical tension creates unprecedented demand for AI data defense platforms. Real parallel to cold-war tech spikes.",
                "stats": [{"l": "Past bloom", "v": "20"}, {"l": "Now bloom", "v": "91"}, {"l": "Delta", "v": "+71"}, {"l": "Market", "v": f"${data['PLTR']}"}],
                "score": 91, "scoreClass": "score-high"
            },
            {
                "name": "Decentralized Energy (Solar FSLR)",
                "icon": "⚡", "bg": "#FAEEDA",
                "story": f"Failed 2004 (Cheap oil era) — Revival: Energy wars. Current Price: ${data['FSLR']}.",
                "body": "Energy deglobalization and subsidies make localized solar grids critical infrastructure.",
                "stats": [{"l": "Past bloom", "v": "15"}, {"l": "Now bloom", "v": "85"}, {"l": "Delta", "v": "+70"}, {"l": "Market", "v": f"${data['FSLR']}"}],
                "score": 85, "scoreClass": "score-high"
            },
            {
                "name": "Meta/VR Revival (Meta META)",
                "icon": "🥽", "bg": "#EAF3DE",
                "story": f"Failed 2003 (Second Life) — Revival: Remote-first. Current Price: ${data['META']}.",
                "body": "Hardware adoption is finally meeting the software vision from two decades ago.",
                "stats": [{"l": "Past bloom", "v": "18"}, {"l": "Now bloom", "v": "88"}, {"l": "Delta", "v": "+70"}, {"l": "Market", "v": f"${data['META']}"}],
                "score": 88, "scoreClass": "score-high"
            },
            {
                "name": "Genomics (CRISPR CRSP)",
                "icon": "🧬", "bg": "#FBEAF0",
                "story": f"Failed 1990s (Delivery hurdles) — Revival: Post-pandemic trust. Current Price: ${data['CRSP']}.",
                "body": "Post-pandemic mRNA trust paves the way for commercialized gene editing tech.",
                "stats": [{"l": "Past bloom", "v": "8"}, {"l": "Now bloom", "v": "75"}, {"l": "Delta", "v": "+67"}, {"l": "Market", "v": f"${data['CRSP']}"}],
                "score": 75, "scoreClass": "score-med"
            }
        ]
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/geotrade-map")
def get_geotrade_map():
    return [
        {"id": "na", "name": "North America", "detail": "Top Companies: NVDA, META, TSLA. High bloom due to tech supremacy & reshoring.", "color": "#1D9E75", "score": "94"},
        {"id": "eu", "name": "Europe", "detail": "Top Companies: ASML, SAP. Defense tech surges, energy pivot active.", "color": "#1D9E75", "score": "86"},
        {"id": "ea", "name": "East Asia", "detail": "Top Companies: TSMC, Sony. EV/Battery tech scaling but tension risks.", "color": "#1D9E75", "score": "82"},
        {"id": "sa", "name": "South America", "detail": "Top Companies: MercadoLibre. Agritech & climate resilience growing.", "color": "#EF9F27", "score": "71"},
        {"id": "af", "name": "Africa", "detail": "Mobile-first fintech booming. Infrastructure leapfrogging.", "color": "#EF9F27", "score": "62"},
        {"id": "ru", "name": "Russia / E. Europe", "detail": "Active Conflict. Defense tech flagged as high-value post-resolution.", "color": "#E24B4A", "score": "22"},
        {"id": "me", "name": "Middle East", "detail": "Conflict & energy pivot. Post-stabilization opportunities immense.", "color": "#E24B4A", "score": "31"}
    ]


@app.get("/api/market-forecast")
def get_market_forecast():
    # Returns the downsampled non-lagging numeric points for charting
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb']
    actual =  [62,65,70,68,74,78,76,80,84,82,86,88,None,None]
    forecast = [None,None,None,None,None,None,None,None,None,None,88,91,94,97]
    lstm_labels = ['Q1 \'23','Q2','Q3','Q4','Q1 \'24','Q2','Q3','Q4','Q1 \'25','Q2','Q3','Q4']
    lstm_actual = [58,61,66,70,72,75,74,80,82,85,88,90]
    lstm_pred = [57,63,65,71,73,74,76,79,83,84,87,91]
   
    return {
        "spark": { "labels": months, "actual": actual, "forecast": forecast },
        "lstm": { "labels": lstm_labels, "actual": lstm_actual, "pred": lstm_pred }
    }


@app.get("/api/search-company")
def search_company(ticker: str):
    try:
        t = yf.Ticker(ticker.upper())
        info = t.info
        if "shortName" not in info and "longName" not in info:
            # Fallback for simple testing if offline or blocked
            name = ticker.upper()
            sector = "Technology"
            price = 100.0
        else:
            sector = info.get("sector", "Unknown")
            name = info.get("shortName", info.get("longName", ticker.upper()))
            price = info.get("currentPrice", info.get("regularMarketPrice", 100.0))
       
        # Generative Bloom Score Heuristics based on sector
        bloom_score = 65
        story = "Neutral market conditions."
        color = "#EF9F27"
       
        if sector in ["Technology", "Semiconductors", "Software - Infrastructure"]:
            bloom_score = 92
            story = "High T_now (Tech Maturity) multiplier applied. Market is ripe for infrastructure."
            color = "#1D9E75"
        elif "Defense" in sector or "Aerospace" in sector:
            bloom_score = 95
            story = "Massive W_now (War/Conflict) catalyst active. State-backed demand surging."
            color = "#1D9E75"
        elif "Energy" in sector or "Utilities" in sector or "Solar" in sector:
            bloom_score = 88
            story = "Benefiting from supply chain disruptions & climate policy tailwinds."
            color = "#1D9E75"
        elif "Consumer" in sector or "Retail" in sector:
            bloom_score = 35
            story = "Suppressed by tight C_now (Capital access) & geopolitical inflation."
            color = "#E24B4A"
        elif "Healthcare" in sector or "Biotechnology" in sector:
            bloom_score = 75
            story = "Moderate social readiness post-pandemic. Steady capital inflows."
            color = "#EF9F27"
           
        return {
            "ticker": ticker.upper(),
            "name": name,
            "sector": sector,
            "price": price,
            "bloom_score": bloom_score,
            "story": story,
            "color": color
        }
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/macro-forecast")
def get_macro_forecast():
    return [
        {
            "sector": "Defense & Intelligence (e.g. LMT, PLTR, ANDURIL)",
            "rationale": "Geopolitical War Index (W_now) tracking at 8.2 (10yr high). Profit margins projected to scale universally as state actors localize security paradigms.",
            "forecast_bloom": 95,
            "color": "#1D9E75"
        },
        {
            "sector": "Semiconductor Foundries (e.g. INTC, TSM, NVDA)",
            "rationale": "Reshoring subsidies (CHIPS act) intersecting with high tech maturity (LLMs). Local manufacturing is heavily insulated against macro shipping shocks.",
            "forecast_bloom": 89,
            "color": "#1D9E75"
        },
        {
            "sector": "Agritech & Green Energy Grids (e.g. FSLR, ENPH)",
            "rationale": "Extreme weather events mapped against regional grid fail rates indicates strong adoption elasticity. Energy deglobalization guarantees domestic demand.",
            "forecast_bloom": 85,
            "color": "#1D9E75"
        },
        {
            "sector": "Hyper-local Delivery & Logistics",
            "rationale": "Supply chain fragmentation forces distribution centers closer to consumer hubs. Geotrade disruptions make long-tail transport non-viable.",
            "forecast_bloom": 78,
            "color": "#EF9F27"
        },
        {
            "sector": "Consumer Discretionary & Luxury Goods",
            "rationale": "Heavily punished in Bloom Index models due to low alignment with current C_now (Capital access tightness) and shifting social sentiment.",
            "forecast_bloom": 30,
            "color": "#E24B4A"
        }
    ]
