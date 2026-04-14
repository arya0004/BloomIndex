# backend/logic/bloom_score.py


from dataclasses import dataclass
from enum import Enum


class FailureReason(Enum):
    TIMING_MISMATCH   = 1.5   # Most recoverable
    TECH_NOT_READY    = 2.0
    CAPITAL_DROUGHT   = 2.5
    SOCIAL_UNREADY    = 3.0
    MARKET_FIT        = 4.0
    FUNDAMENTAL       = 5.0   # Hardest to revive


@dataclass
class EnvironmentSnapshot:
    tech_maturity: float       # T_now: 0–10 (AI, infra, hardware readiness)
    social_readiness: float    # S_now: 0–10 (adoption curve, post-war/pandemic need)
    capital_climate: float     # C_now: 0–10 (10 = easy money, 0 = tight)
    war_stability: float       # W_now: 0–10 (10 = fully peaceful)


@dataclass
class HistoricalIdea:
    name: str
    failure_year: int
    failure_reason: FailureReason
    original_bloom_score: float  # Score at time of failure (typically low)


def compute_bloom_score(
    idea: HistoricalIdea,
    env: EnvironmentSnapshot
) -> dict:
    """
    BloomScore = [(T_now × S_now) + (C_now × W_now)] / R_past


    Numerator: product of tech×social captures the 'demand pull'
    (is the world ready for this?), plus capital×stability captures
    the 'supply push' (can it actually be funded and scaled?).


    Denominator: R_past is the original failure weight — harder failures
    (fundamental market problems) suppress the score more than timing misses.


    Score is normalized 0–100. Above 70 = active bloom signal.
    """
    T = env.tech_maturity
    S = env.social_readiness
    C = env.capital_climate
    W = env.war_stability
    R = idea.failure_reason.value


    raw = ((T * S) + (C * W)) / R
    # Normalize: max raw = (10*10 + 10*10)/1.5 = 133.3 → map to 100
    score = min(100.0, round((raw / 133.3) * 100, 1))


    delta = score - idea.original_bloom_score
   
    return {
        "idea": idea.name,
        "bloom_score": score,
        "delta_from_original": round(delta, 1),
        "signal": "BLOOM" if score >= 70 else "EMERGING" if score >= 50 else "DORMANT",
        "components": {
            "demand_pull": round(T * S, 2),
            "supply_push": round(C * W, 2),
            "failure_weight": R,
            "timing_delta_years": 2026 - idea.failure_year
        }
    }
