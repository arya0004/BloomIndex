# data/feature_engineering.py


import pandas as pd


def build_bloom_features(
    company_df: pd.DataFrame,
    macro_df: pd.DataFrame,
    conflict_df: pd.DataFrame,
    climate_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Merges micro + macro + geopolitical + climate streams
    into a unified feature matrix for the ML models.
    """


    # 1. Temporal alignment — all series to quarterly frequency
    macro_q   = macro_df.resample('QE', on='date').mean()
    conflict_q = conflict_df.resample('QE', on='date').agg({
        'active_conflicts': 'max',
        'affected_trade_routes': 'sum',
        'conflict_intensity': 'mean'
    })
    climate_q = climate_df.resample('QE', on='date').agg({
        'global_temp_anomaly': 'mean',
        'extreme_weather_events': 'sum',
        'co2_ppm': 'last'
    })


    # 2. Derived "timing" features — the core of BloomIndex
    macro_q['tech_adoption_velocity'] = (
        macro_q['internet_users_pct'].pct_change(4)   # YoY change
    )
    macro_q['capital_season'] = (
        macro_q['fed_funds_rate'].apply(
            lambda r: max(0, 10 - r * 1.5)  # Maps rate → capital ease score
        )
    )
    conflict_q['war_stability_score'] = (
        10 - conflict_q['conflict_intensity'].clip(0, 10)
    )
    climate_q['green_urgency'] = (
        climate_q['extreme_weather_events'].clip(0, 20) / 2  # 0–10 scale
    )


    # 3. Lag features — past conditions vs current (timing delta)
    for col in ['tech_adoption_velocity', 'capital_season']:
        for lag in [4, 8, 12]:   # 1yr, 2yr, 3yr back
            macro_q[f'{col}_lag{lag}q'] = macro_q[col].shift(lag)


    # 4. Join everything to company events
    company_df['quarter'] = pd.PeriodIndex(
        company_df['founded_date'], freq='Q'
    ).to_timestamp()
   
    merged = (
        company_df
        .merge(macro_q.reset_index(),    on='quarter', how='left')
        .merge(conflict_q.reset_index(), on='quarter', how='left')
        .merge(climate_q.reset_index(),  on='quarter', how='left')
    )


    return merged
