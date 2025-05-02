import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model import recommend_phones  # Import after modifying sys.path

app = Flask(__name__)
CORS(app)

# Load the trained model and dataset
model = joblib.load("./phone_recommendation_model.pkl")
data = pd.read_csv("./smartphones.csv")


@app.route("/recommend", methods=["POST"])
def recommend():
    query = request.json.get("query", "").lower()
    top_n = request.json.get("top_n", 5)

    result = recommend_phones(query, top_n)

    if isinstance(result, str):
        return jsonify({"message": result}), 404
    else:
        return jsonify(result.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
