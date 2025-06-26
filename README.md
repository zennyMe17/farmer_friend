# Smart Farming Assistant

## Description

The **Smart Farming Assistant** is an AI-powered web application that helps farmers make informed decisions based on real-time weather conditions and soil nutrient levels. It uses machine learning to recommend the most suitable crop and the ideal fertilizer for your land, leading to optimized agricultural productivity.

---

## Features

- Real-time weather integration (via WeatherAPI)
- Soil moisture estimation
- Crop recommendation engine
- Fertilizer prediction system
- Responsive frontend with live validation
- Fast and efficient FastAPI backend
- Pre-trained ML pipeline (imputer, scaler, encoder)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/zennyMe17/smart_farming_assistant.git
cd smart_farming_assistant
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Add Your WeatherAPI Key

Open `backend/main.py` and replace the placeholder with your actual key:

```python
WEATHER_API_KEY = "YOUR_API_KEY"
```

### 4. Ensure Model Files Exist

Inside `backend/models/`, make sure the following `.joblib` files are present:

- `model_crop_type.joblib`
- `model_fertilizer_name.joblib`
- `imputer.joblib`
- `scaler.joblib`
- `encoder.joblib`
- `input_cols.joblib`
- `numeric_cols.joblib`
- `categorical_cols.joblib`

### 5. Frontend Setup

In a new terminal:

```bash
cd ../frontend
npm install
```

### 6. Run the Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs) to test the API.

### 7. Run the Frontend

```bash
cd frontend
npm run dev
```

Visit: [http://localhost:3000](http://localhost:3000) to use the app.

---

## Technology Stack

### Backend

- Python
- FastAPI
- scikit-learn
- joblib
- pandas
- numpy
- python-dotenv

### Frontend

- Next.js
- React
- Tailwind CSS
- React Icons

---

## Contributing

We welcome contributions to improve this project. Feel free to:

- Open issues for bugs and suggestions.
- Submit pull requests.
- Enhance model accuracy or add new features.
