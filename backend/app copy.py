from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import re

# Load model and dataset
model = joblib.load("../phone_recommendation_model.pkl")
data = pd.read_csv("../smartphones.csv")

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend


# Existing feature extraction and recommendation logic
def extract_features_from_query(query):
    query = query.lower()
    price = None
    ram = None
    battery = None
    camera = None
    rear_cameras = None

    if "under" in query:
        price = (
            int(re.search(r"under (\d+)", query).group(1))
            if re.search(r"under (\d+)", query)
            else None
        )
    elif "above" in query:
        price = (
            int(re.search(r"above (\d+)", query).group(1))
            if re.search(r"above (\d+)", query)
            else None
        )

    if "gb ram" in query:
        ram = (
            int(re.search(r"(\d+) gb ram", query).group(1))
            if re.search(r"(\d+) gb ram", query)
            else None
        )

    if "mah" in query:
        battery = (
            int(re.search(r"(\d+) mah", query).group(1))
            if re.search(r"(\d+) mah", query)
            else None
        )

    if "mp camera" in query:
        camera = (
            int(re.search(r"(\d+) mp camera", query).group(1))
            if re.search(r"(\d+) mp camera", query)
            else None
        )

    if "rear cameras" in query:
        rear_cameras = (
            int(re.search(r"(\d+) rear cameras", query).group(1))
            if re.search(r"(\d+) rear cameras", query)
            else None
        )

    features = {
        "price": price if price else 50000,
        "ram_capacity": ram if ram else 6,
        "battery_capacity": battery if battery else 4000,
        "primary_camera_rear": camera if camera else 48,
        "num_rear_cameras": rear_cameras if rear_cameras else 2,
    }
    return features


def recommend_phones(query, top_n=5):
    model = joblib.load("../phone_recommendation_model.pkl")

    numerical_features = [
        "price",
        "ram_capacity",
        "battery_capacity",
        "internal_memory",
        "primary_camera_rear",
        "primary_camera_front",
        "processor_speed",
        "screen_size",
        "refresh_rate",
        "num_cores",
        "resolution_height",
        "resolution_width",
    ]
    categorical_features = [
        "5G_or_not",
        "fast_charging_available",
        "fast_charging",
        "extended_memory_available",
        "processor_brand",
        "os",
    ]
    features = numerical_features + categorical_features

    query_features = extract_features_from_query(query)

    filtered_data = data.copy()

    for brand in data["brand_name"].unique():
        if brand.lower() in query:
            filtered_data = filtered_data[
                filtered_data["brand_name"].str.lower() == brand.lower()
            ]
            break

    if "under" in query:
        filtered_data = filtered_data[
            filtered_data["price"].notnull()
            & (filtered_data["price"] <= query_features["price"])
        ]
    elif "above" in query:
        filtered_data = filtered_data[
            filtered_data["price"].notnull()
            & (filtered_data["price"] >= query_features["price"])
        ]

    if query_features.get("ram_capacity") is not None:
        filtered_data = filtered_data[
            filtered_data["ram_capacity"] >= query_features["ram_capacity"]
        ]
    if query_features.get("battery_capacity") is not None:
        filtered_data = filtered_data[
            filtered_data["battery_capacity"] >= query_features["battery_capacity"]
        ]
    if query_features.get("primary_camera_rear") is not None:
        filtered_data = filtered_data[
            filtered_data["primary_camera_rear"]
            >= query_features["primary_camera_rear"]
        ]
    if query_features.get("num_rear_cameras") is not None:
        filtered_data = filtered_data[
            filtered_data["num_rear_cameras"] >= query_features["num_rear_cameras"]
        ]

    if filtered_data.empty:
        return "No phones match your query constraints."

    for col in features:
        if col not in filtered_data:
            filtered_data[col] = (
                0 if col in categorical_features else filtered_data[col].mean()
            )

    filtered_data["score"] = model.predict(filtered_data[features])

    top = filtered_data.sort_values(by="score", ascending=False).head(top_n)
    return top[
        [
            "brand_name",
            "model",
            "price",
            "ram_capacity",
            "battery_capacity",
            "primary_camera_rear",
            "avg_rating",
        ]
    ]


@app.route("/api/recommend", methods=["POST"])
def recommend():
    query = request.json.get("query", "")
    recommendations = recommend_phones(query)
    if isinstance(recommendations, str):
        return jsonify({"message": recommendations, "data": []})
    return jsonify(
        {"message": "success", "data": recommendations.to_dict(orient="records")}
    )


if __name__ == "__main__":
    app.run(port=5000)
