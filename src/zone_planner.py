from src.recommendation_engine import recommend_routes

def generate_zone_plan(df, top_k=2):
    plans = {}

    for zone, zone_df in df.groupby("zone"):
        ranked = recommend_routes(zone_df)
        plans[zone] = ranked.head(top_k)

    return plans
