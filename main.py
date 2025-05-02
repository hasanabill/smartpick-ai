import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import re

# Load the dataset
data = pd.read_csv("smartphones.csv")


def preprocess_and_train():
    # Define features and target
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
    target = "avg_rating"  # Use average rating as a proxy for recommendation score

    # Preprocess categorical and numerical features
    X = data[features]
    y = data[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define preprocessing and model pipeline
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(
        handle_unknown="ignore"
    )  # Encode categorical features

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numerical_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = Pipeline(
        steps=[("preprocessor", preprocessor), ("regressor", LinearRegression())]
    )

    # Train the model
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, "phone_recommendation_model.pkl")
    print("Model trained and saved successfully!")


def extract_features_from_query(query):
    # Simplified NLP processing
    query = query.lower()
    price = None
    ram = None
    battery = None
    camera = None
    rear_cameras = None

    # Extract price
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

    # Extract RAM
    if "gb ram" in query:
        ram = (
            int(re.search(r"(\d+) gb ram", query).group(1))
            if re.search(r"(\d+) gb ram", query)
            else None
        )

    # Extract battery capacity
    if "mah" in query:
        battery = (
            int(re.search(r"(\d+) mah", query).group(1))
            if re.search(r"(\d+) mah", query)
            else None
        )

    # Extract camera megapixels
    if "mp camera" in query:
        camera = (
            int(re.search(r"(\d+) mp camera", query).group(1))
            if re.search(r"(\d+) mp camera", query)
            else None
        )

    # Extract number of rear cameras
    if "rear cameras" in query:
        rear_cameras = (
            int(re.search(r"(\d+) rear cameras", query).group(1))
            if re.search(r"(\d+) rear cameras", query)
            else None
        )

    # Map extracted values to model features
    features = {
        "price": price if price else 50000,
        "ram_capacity": ram if ram else 6,
        "battery_capacity": battery if battery else 4000,
        "primary_camera_rear": camera if camera else 48,
        "num_rear_cameras": rear_cameras if rear_cameras else 2,
    }
    return features


def recommend_phones(query, top_n=5):
    # Load the trained model
    model = joblib.load("phone_recommendation_model.pkl")

    # Define features and categorical features
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

    # Extract features from the query
    query_features = extract_features_from_query(query)

    # Filter the dataset based on query constraints
    filtered_data = data.copy()

    # Handle brand-specific queries
    for brand in data["brand_name"].unique():
        if brand.lower() in query:
            filtered_data = filtered_data[
                filtered_data["brand_name"].str.lower() == brand.lower()
            ]
            break

    # Apply price constraint
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

    # Apply other constraints
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

    # If no phones match the constraints, return a message
    if filtered_data.empty:
        return "No phones match your query constraints."

    # Ensure filtered_data contains all required columns
    for col in features:
        if col not in filtered_data:
            filtered_data[col] = (
                0 if col in categorical_features else filtered_data[col].mean()
            )

    # Predict scores for the filtered dataset
    filtered_data["score"] = model.predict(filtered_data[features])

    # Sort by score and return top results
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


# Infinite terminal loop
if __name__ == "__main__":
    print("📱 SmartPick.ai – Ask me about phones! (Type 'exit' to quit)")
    preprocess_and_train()  # Train the model before starting the loop
    while True:
        query = input("\n🧠 Your Query: ").strip().lower()
        if query in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        result = recommend_phones(query)
        print("\n🔍 Top Results:\n")
        print(result if isinstance(result, str) else result.to_string(index=False))
