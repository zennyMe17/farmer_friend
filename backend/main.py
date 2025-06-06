import pandas as pd
import numpy as np
import joblib
import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# Load environment variables
load_dotenv()
WEATHER_API_KEY = "c8038b38b6be4e6c9a540208251505"
LOCATION = "Bengaluru" # Remembered location from previous context

# Initialize FastAPI app
app = FastAPI(
    title="Smart Farming API",
    description="Provides crop and fertilizer recommendations based on soil data and live weather.",
    version="1.0.0"
)

# Add CORS middleware to allow requests from your Next.js frontend
# Adjust origins in production to your frontend's domain!
origins = [
    "http://localhost:3000",  # Allow your Next.js dev server
    "http://127.0.0.1:3000",
    # Add your deployed frontend URL here when you deploy:
    # "https://your-deployed-frontend.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global variables to store loaded models and preprocessors ---
model_crop_type = None
model_fertilizer_name = None
imputer = None
scaler = None
encoder = None
numeric_cols = None
categorical_cols = None
input_cols = None # To preserve original input column order for consistent prediction

# --- Helper Function: Estimate Moisture (same as before) ---
def estimate_moisture(humidity: float) -> float:
    """Estimates soil moisture based on humidity."""
    if humidity > 80: return 70.0
    elif humidity > 60: return 60.0
    elif humidity > 40: return 50.0
    elif humidity > 20: return 40.0
    else: return 30.0

# --- Helper Function: Fetch Live Weather Data ---
def get_weather(api_key: str, location: str) -> tuple[float, float]:
    """Fetches live temperature and humidity from WeatherAPI."""
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url, timeout=5) # Add a timeout
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        temp = data['current']['temp_c']
        humidity = data['current']['humidity']
        return float(temp), float(humidity)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data for {location}: {e}")
        # Fallback to default values if API call fails
        return 25.0, 60.0

# --- Pydantic Model for Request Body (defines what frontend sends) ---
class SoilInput(BaseModel):
    nitrogen: int
    potassium: int
    phosphorous: int
    soil_type: str

# --- Startup Event: Load models and preprocessors only once when the app starts ---
@app.on_event("startup")
async def load_all_models():
    global model_crop_type, model_fertilizer_name, imputer, scaler, encoder
    global numeric_cols, categorical_cols, input_cols

    models_dir = 'models'
    try:
        print("Loading models and preprocessors...")
        model_crop_type = joblib.load(os.path.join(models_dir, 'model_crop_type.joblib'))
        model_fertilizer_name = joblib.load(os.path.join(models_dir, 'model_fertilizer_name.joblib'))
        imputer = joblib.load(os.path.join(models_dir, 'imputer.joblib'))
        scaler = joblib.load(os.path.join(models_dir, 'scaler.joblib'))
        encoder = joblib.load(os.path.join(models_dir, 'encoder.joblib'))
        numeric_cols = joblib.load(os.path.join(models_dir, 'numeric_cols.joblib'))
        categorical_cols = joblib.load(os.path.join(models_dir, 'categorical_cols.joblib'))
        input_cols = joblib.load(os.path.join(models_dir, 'input_cols.joblib')) # This might not be strictly needed if we derive order from numeric_cols + encoded_cols
        print("Models and preprocessors loaded successfully!")
    except FileNotFoundError as e:
        print(f"ERROR: Model file not found - {e}. Ensure 'models/' directory is correctly placed and contains all .joblib files.")
        raise RuntimeError("Missing model files, application cannot start.") from e
    except Exception as e:
        print(f"ERROR: Failed to load models or preprocessors - {e}")
        raise RuntimeError("Failed to load ML components, application cannot start.") from e

# --- Endpoint to get soil types for dropdown in frontend ---
@app.get("/soil-types", response_model=List[str])
async def get_soil_types():
    if encoder is None or categorical_cols is None:
        raise HTTPException(status_code=500, detail="Models not loaded yet.")
    
    try:
        soil_type_idx = categorical_cols.index('Soil Type')
        return encoder.categories_[soil_type_idx].tolist()
    except ValueError:
        raise HTTPException(status_code=500, detail="'Soil Type' not found in categorical columns for encoding.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving soil types: {e}")

# --- Prediction Endpoint ---
@app.post("/predict")
async def predict(soil_input: SoilInput):
    if any(m is None for m in [model_crop_type, model_fertilizer_name, imputer, scaler, encoder, numeric_cols, categorical_cols]):
        raise HTTPException(status_code=500, detail="Models not loaded yet. Server might be starting or encountered an error.")

    # 1. Get live weather data
    temperature, humidity = get_weather(WEATHER_API_KEY, LOCATION)
    moisture = estimate_moisture(humidity)

    # 2. Create raw input DataFrame
    new_input_data_raw = pd.DataFrame({
        'Temparature': [temperature],
        'Humidity': [humidity],
        'Moisture': [moisture],
        'Nitrogen': [soil_input.nitrogen],
        'Potassium': [soil_input.potassium],
        'Phosphorous': [soil_input.phosphorous],
        'Soil Type': [soil_input.soil_type]
    })

    # 3. Apply preprocessing steps (same as training)
    try:
        # Ensure only numeric columns are passed to imputer/scaler
        processed_numeric_data = imputer.transform(new_input_data_raw[numeric_cols])
        processed_numeric_data_df = pd.DataFrame(processed_numeric_data, columns=numeric_cols, index=new_input_data_raw.index)

        scaled_numeric_data = scaler.transform(processed_numeric_data_df)
        scaled_numeric_data_df = pd.DataFrame(scaled_numeric_data, columns=numeric_cols, index=new_input_data_raw.index)

        # Ensure only categorical columns are passed to encoder
        encoded_categorical_data = encoder.transform(new_input_data_raw[categorical_cols])
        encoded_cols_names = list(encoder.get_feature_names_out(categorical_cols))
        encoded_categorical_data_df = pd.DataFrame(encoded_categorical_data, columns=encoded_cols_names, index=new_input_data_raw.index)

        # Combine all preprocessed features, ensuring correct column order
        # The feature order must match the order during model training (numeric_cols + encoded_cols_names)
        expected_feature_order = numeric_cols + encoded_cols_names
        combined_processed_data = pd.concat([scaled_numeric_data_df, encoded_categorical_data_df], axis=1)
        final_data_for_prediction = combined_processed_data[expected_feature_order]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing error: {e}")

    # 4. Make predictions
    try:
        predicted_crop_type = model_crop_type.predict(final_data_for_prediction)[0]
        predicted_fertilizer_name = model_fertilizer_name.predict(final_data_for_prediction)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    # 5. Return results
    return {
        "temperature_c": temperature,
        "humidity_percent": humidity,
        "moisture_estimate": moisture,
        "predicted_crop_type": predicted_crop_type,
        "predicted_fertilizer_name": predicted_fertilizer_name
    }

# To run the backend:
# Navigate to the 'backend' directory in your terminal.
# Install dependencies: pip install -r requirements.txt
# Run the server: uvicorn main:app --reload --host 0.0.0.0 --port 8000
# The --reload flag is for development, it reloads on code changes.
# The --host 0.0.0.0 allows access from outside localhost (e.g. if you're on a network or docker)