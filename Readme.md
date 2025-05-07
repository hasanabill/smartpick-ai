# SmartPick.ai – AI-Powered Smartphone Recommendation Assistant

SmartPick.ai is an intelligent assistant that recommends smartphones based on user queries using machine learning. Users can input natural language queries (e.g., "Suggest phones under 20000 with 8GB RAM") and get top phone recommendations based on price, specs, and predicted user rating.

## 🚀 Features

- 💬 Chat-like interface with natural query input
- 🔍 Intelligent parsing of user requirements
- 🧠 ML-based prediction using linear regression
- 📊 Recommendations displayed in table format
- 🌐 Full-stack integration using React, Flask & scikit-learn

## 🖥️ Tech Stack

| Layer      | Tools/Frameworks                          |
| ---------- | ----------------------------------------- |
| Frontend   | React, Tailwind CSS                       |
| Backend    | Flask, Python, Axios                      |
| ML & Data  | scikit-learn, pandas, joblib              |
| Deployment | Vercel (Frontend), Render/Local (Backend) |

---

## 📁 Project Structure

```
smartpick-ai/
├── backend/
│ ├── app.py # Flask API
│ ├── phone_recommendation_model.pkl # Trained ML model
│ ├── recommend.py # Query parser & model inference
│ └── smartphones.csv # Dataset
├── frontend/
│ ├── src/
│ │ ├── App.jsx # React app with chat UI
│ │ └── ... # Other components/assets
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smartpick-ai.git
cd smartpick-ai
```

---

### 2. Backend Setup (Python + Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

- This starts the Flask server on `http://localhost:5000`
- Make sure `model.pkl` is already generated (or use `preprocess_and_train()` to create it)

---

### 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm run dev
```

- App runs on `http://localhost:5173` (or Vite's default port)
- Make sure the Flask backend is running for recommendations to work

---

## 🤖 How It Works

1. User types a natural query like:

   ```
   Recommend phones under 25000 with 8GB RAM and 5000mAh battery
   ```

2. The backend parses this query to extract filters.
3. A trained regression model predicts average ratings for matching phones.
4. Top 5 results are returned and shown in a table inside the chat UI.

---

## 📦 Requirements

**Backend (Python):**

- Flask
- pandas
- scikit-learn
- joblib

**Frontend (React):**

- React
- Axios
- Tailwind CSS
- Vite

---

## 🧠 Machine Learning Model

- Type: Linear Regression
- Input: Cleaned and preprocessed phone features (e.g. RAM, battery, camera, etc.)
- Output: Predicted average rating (used to rank phones)
- Serialized: `model.pkl` using `joblib`

---

## 🙌 Acknowledgments

Thanks to the contributors and open-source community for tools like React, Flask, scikit-learn, and Tailwind.

---
