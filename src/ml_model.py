from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_evacuation_model(df):
    features = [
        "population",
        "risk_level",
        "road_capacity",
        "distance_km",
        "avg_speed_kmph",
        "load_factor",
        "congestion_index",
    ]

    X = df[features]
    y = df["evac_time_min"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    return model, mae, r2

def get_feature_importance(model, feature_names):
    importances = model.feature_importances_
    importance_df = sorted(
        zip(feature_names, importances),
        key=lambda x: x[1],
        reverse=True
    )
    return importance_df
