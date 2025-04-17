import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load data
df = pd.read_csv("smartphones.csv")


# 2. Create target variable
def categorize_price(price):
    if price < 20000:
        return "low"
    elif price < 50000:
        return "mid"
    else:
        return "high"


df["price_category"] = df["price"].apply(categorize_price)

# 3. Drop unused columns
#    - 'model' is unique identifier
#    - 'price' used to create target
df = df.drop(columns=["model", "price"])

# 4. Identify feature types
numeric_features = [
    "avg_rating",
    "5G_or_not",
    "num_cores",
    "processor_speed",
    "battery_capacity",
    "fast_charging",
    "ram_capacity",
    "internal_memory",
    "screen_size",
    "refresh_rate",
    "num_rear_cameras",
    "primary_camera_rear",
    "primary_camera_front",
    "extended_memory_available",
    "resolution_height",
    "resolution_width",
]

categorical_features = ["brand_name", "processor_brand", "os"]

# 5. Preprocessing pipelines
numeric_pipeline = Pipeline(
    [
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),  # median imputation :contentReference[oaicite:0]{index=0}
        (
            "scaler",
            StandardScaler(),
        ),  # standard scaling :contentReference[oaicite:1]{index=1}
    ]
)

categorical_pipeline = Pipeline(
    [
        (
            "imputer",
            OneHotEncoder(handle_unknown="ignore"),
        ),  # treat missing as separate category :contentReference[oaicite:2]{index=2}
        # Note: OneHotEncoder here implicitly handles missing values
    ]
)

preprocessor = ColumnTransformer(
    [
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features),
    ],
    remainder="drop",
)  # drop any other columns :contentReference[oaicite:3]{index=3}

# 6. Full modeling pipeline
model_pipeline = Pipeline(
    [
        ("preprocess", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42)),
    ]
)

# 7. Split data
X = df.drop("price_category", axis=1)
y = df["price_category"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 8. Train
model_pipeline.fit(X_train, y_train)

# 9. Evaluate
y_pred = model_pipeline.predict(X_test)
print("Test Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 10. Save trained pipeline
joblib.dump(model_pipeline, "smartpick_ai_model.pkl")
print("Model saved to smartpick_ai_model.pkl")
