import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define paths to your saved models and preprocessors
MODELS_DIR = 'models'
CROP_MODEL_PATH = os.path.join(MODELS_DIR, 'model_crop_type.joblib')
FERTILIZER_MODEL_PATH = os.path.join(MODELS_DIR, 'model_fertilizer_name.joblib')
IMPUTER_PATH = os.path.join(MODELS_DIR, 'imputer.joblib')
SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.joblib')
ENCODER_PATH = os.path.join(MODELS_DIR, 'encoder.joblib')
INPUT_COLS_PATH = os.path.join(MODELS_DIR, 'input_cols.joblib')
NUMERIC_COLS_PATH = os.path.join(MODELS_DIR, 'numeric_cols.joblib')
CATEGORICAL_COLS_PATH = os.path.join(MODELS_DIR, 'categorical_cols.joblib')

# Global variables to hold loaded models and preprocessors
model_crop_type = None
model_fertilizer_name = None
imputer = None
scaler = None
encoder = None
input_cols = None
numeric_cols = None
categorical_cols = None

def load_models_and_preprocessors():
    """Loads all trained models and preprocessing objects."""
    global model_crop_type, model_fertilizer_name, imputer, scaler, encoder, input_cols, numeric_cols, categorical_cols
    try:
        print("Loading models and preprocessors...")
        model_crop_type = joblib.load(CROP_MODEL_PATH)
        model_fertilizer_name = joblib.load(FERTILIZER_MODEL_PATH)
        imputer = joblib.load(IMPUTER_PATH)
        scaler = joblib.load(SCALER_PATH)
        encoder = joblib.load(ENCODER_PATH)
        # Load the final input columns list (x_train.columns after preprocessing)
        input_cols = joblib.load(INPUT_COLS_PATH)
        numeric_cols = joblib.load(NUMERIC_COLS_PATH)
        categorical_cols = joblib.load(CATEGORICAL_COLS_PATH)

        print("All models and preprocessors loaded successfully!")
    except FileNotFoundError as e:
        print(f"Error loading files: {e}. Make sure you run the training script first to save them.")
        exit(1) # Exit if essential files are not found
    except Exception as e:
        print(f"An unexpected error occurred during loading: {e}")
        exit(1)

# Load models and preprocessors when the Flask app starts
load_models_and_preprocessors()

# Helper function to estimate moisture (copied from your original script)
def estimate_moisture(humidity):
    if humidity > 80: return 70
    elif humidity > 60: return 60
    elif humidity > 40: return 50
    elif humidity > 20: return 40
    else: return 30

@app.route('/')
def home():
    """Simple home route to check if the API is running."""
    return "Smart Farming Assistant API is running! Send POST requests to /predict."

@app.route('/predict', methods=['POST'])
def predict():
    """
    API endpoint to receive farm conditions and return crop and fertilizer predictions.
    Expected JSON input format:
    {
        "Temparature": 25.0,
        "Humidity": 60.0,
        "Nitrogen": 37,
        "Potassium": 0,
        "Phosphorous": 0,
        "Soil Type": "Clay"
    }
    Moisture will be estimated from Humidity server-side.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Validate incoming data
    required_keys = ['Temparature', 'Humidity', 'Nitrogen', 'Potassium', 'Phosphorous', 'Soil Type']
    if not all(key in data for key in required_keys):
        return jsonify({"error": f"Missing one or more required fields. Required: {required_keys}"}), 400

    try:
        # Extract inputs and estimate moisture
        temperature = float(data['Temparature'])
        humidity = float(data['Humidity'])
        moisture = estimate_moisture(humidity) # Estimate moisture server-side
        nitrogen = int(data['Nitrogen'])
        potassium = int(data['Potassium'])
        phosphorous = int(data['Phosphorous'])
        selected_soil = str(data['Soil Type'])

        # Create a DataFrame for the new raw input, matching the structure used during training
        new_input_df_raw = pd.DataFrame([{
            'Temparature': temperature,
            'Humidity': humidity,
            'Moisture': moisture, # Use estimated moisture
            'Nitrogen': nitrogen,
            'Potassium': potassium,
            'Phosphorous': phosphorous,
            'Soil Type': selected_soil
        }])

        # --- DEBUGGING PRINTS ---
        print(f"DEBUG: Data received from request: {data}")
        print(f"DEBUG: Raw input DataFrame created: \n{new_input_df_raw}")
        print(f"DEBUG: Loaded numeric_cols: {numeric_cols}")
        print(f"DEBUG: Loaded categorical_cols: {categorical_cols}")
        # --- END DEBUGGING PRINTS ---


        # Apply preprocessing using the loaded transformers
        # 1. Impute and Scale numeric columns
        processed_numeric_data = imputer.transform(new_input_df_raw[numeric_cols])
        processed_numeric_data = scaler.transform(processed_numeric_data)
        processed_numeric_df = pd.DataFrame(processed_numeric_data, columns=numeric_cols, index=new_input_df_raw.index)

        # 2. One-Hot Encode categorical features
        # Explicitly create a DataFrame for the categorical columns to ensure column name consistency
        categorical_input_for_encoder = pd.DataFrame(
            {col: new_input_df_raw[col] for col in categorical_cols},
            index=new_input_df_raw.index
        )
        print(f"DEBUG: Categorical DataFrame passed to encoder: \n{categorical_input_for_encoder}")
        print(f"DEBUG: Columns of categorical_input_for_encoder: {categorical_input_for_encoder.columns.tolist()}")

        processed_categorical_data = encoder.transform(categorical_input_for_encoder)
        encoded_feature_names = encoder.get_feature_names_out(categorical_cols)
        processed_categorical_df = pd.DataFrame(processed_categorical_data,
                                                 columns=encoded_feature_names,
                                                 index=new_input_df_raw.index)

        # Combine processed numeric and encoded categorical features
        # Create a DataFrame that has ALL columns expected by the model (i.e., input_cols)
        final_prediction_df = pd.DataFrame(0, index=[0], columns=input_cols)

        # Populate the combined DataFrame with processed numeric values
        for col in numeric_cols:
            if col in processed_numeric_df.columns:
                final_prediction_df[col] = processed_numeric_df[col].values

        # Populate the combined DataFrame with one-hot encoded categorical values
        for col in encoded_feature_names:
            if col in processed_categorical_df.columns:
                final_prediction_df[col] = processed_categorical_df[col].values

        print(f"DEBUG: Final DataFrame for prediction columns: {final_prediction_df.columns.tolist()}")
        print(f"DEBUG: Final DataFrame for prediction shape: {final_prediction_df.shape}")
        print(f"DEBUG: Final DataFrame for prediction head: \n{final_prediction_df.head()}")


        # Make predictions
        predicted_crop_type = model_crop_type.predict(final_prediction_df)[0]
        predicted_fertilizer_name = model_fertilizer_name.predict(final_prediction_df)[0]

        return jsonify({
            "predicted_crop_type": predicted_crop_type,
            "predicted_fertilizer_name": predicted_fertilizer_name
        }), 200

    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {e}. Please ensure numeric values are correct and soil type is a string."}), 400
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
        return jsonify({"error": f"An internal server error occurred: {e}"}), 500

if __name__ == '__main__':
    # For local testing, run: python app.py
    # For production deployment, use a WSGI server like Gunicorn.
    # e.g., gunicorn -w 4 app:app -b 0.0.0.0:5000
    app.run(debug=True, host='0.0.0.0', port=5000)
