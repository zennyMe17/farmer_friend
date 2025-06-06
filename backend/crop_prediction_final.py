    import pandas as pd
    import numpy as np
    import requests # Essential for fetching live weather data!
    import joblib # To load models and preprocessors
    import os # For path manipulation

    # --- Configuration ---
    # Your WeatherAPI key for fetching live weather data
    API_KEY = 'c8038b38b6be4e6c9a540208251505'
    # The location for which to fetch weather data. Remembered as Bengaluru.
    LOCATION = 'Bengaluru'

    # --- Helper Function: Estimate Moisture ---
    def estimate_moisture(humidity):
        """
        Estimates soil moisture based on humidity. This is a simplified estimation.
        For precise farming, consider dedicated soil moisture sensors.
        """
        print("  (💡 Estimating soil moisture based on humidity...)")
        if humidity > 80: return 70
        elif humidity > 60: return 60
        elif humidity > 40: return 50
        elif humidity > 20: return 40
        else: return 30

    # --- Helper Function: Fetch Live Weather Data ---
    def get_weather(api_key, location):
        """
        Fetches live temperature and humidity from WeatherAPI.
        Uses default values if the API call fails.
        """
        print(f"\n🌍 Fetching live weather data for {location}, India (Current Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S %Z')})...")
        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        try:
            response = requests.get(url)
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            temp = data['current']['temp_c']
            humidity = data['current']['humidity']
            print(f"  🌡️ Current Temperature: {temp}°C")
            print(f"  💧 Current Humidity: {humidity}%")
            return temp, humidity
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error fetching weather data from WeatherAPI: {e}")
            print("  Using default values (Temp=25°C, Humidity=60%) as a fallback. Please check your API key or internet connection. 🌧️")
            return 25, 60 # Default values if API call fails

    # --- Main Prediction Script ---
    if __name__ == "__main__":
        print("\n" + "="*70)
        print("🚀🚀🚀 Welcome to Your Smart Farming Assistant: Live Prediction! 🚀🚀🚀")
        print("--- Loading Your Trained Models & Preprocessing Tools ---")
        print("="*70 + "\n")

        models_dir = 'models' # Ensure your .joblib files are in a folder named 'models'

        try:
            # Load the trained machine learning models
            # model_crop_type: This expert predicts the best crop to grow for your conditions.
            model_crop_type = joblib.load(os.path.join(models_dir, 'model_crop_type.joblib'))
            # model_fertilizer_name: This expert recommends the ideal fertilizer.
            model_fertilizer_name = joblib.load(os.path.join(models_dir, 'model_fertilizer_name.joblib'))
            print("✅ Prediction models loaded successfully: **Crop Type** and **Fertilizer Name**.")

            # Load the preprocessing objects – these ensure new data is treated consistently
            # imputer: Fills in any missing numerical values (e.g., if you had NaNs during training).
            imputer = joblib.load(os.path.join(models_dir, 'imputer.joblib'))
            # scaler: Normalizes numerical features (e.g., puts values between 0 and 1).
            scaler = joblib.load(os.path.join(models_dir, 'scaler.joblib'))
            # encoder: Converts categorical text data (like 'Soil Type') into numbers.
            encoder = joblib.load(os.path.join(models_dir, 'encoder.joblib'))
            print("✅ Preprocessing objects loaded successfully: **Imputer**, **Scaler**, **Encoder**.")

            # Load the lists of column names. These are crucial for making sure your
            # input data for prediction has the exact same structure as your training data.
            input_cols = joblib.load(os.path.join(models_dir, 'input_cols.joblib'))
            numeric_cols = joblib.load(os.path.join(models_dir, 'numeric_cols.joblib'))
            categorical_cols = joblib.load(os.path.join(models_dir, 'categorical_cols.joblib'))
            print("✅ Column lists loaded successfully: **input_cols**, **numeric_cols**, **categorical_cols**.")

        except FileNotFoundError as e:
            print(f"❌ Oh no! A required file wasn't found: {e}")
            print(f"Please ensure all your '.joblib' files are correctly placed in the '{models_dir}/' directory.")
            exit() # Cannot proceed without all necessary files
        except Exception as e:
            print(f"❌ An unexpected error occurred during loading: {e}")
            print("Please check the integrity of your .joblib files or the models directory.")
            exit() # Cannot proceed if loading fails

        print("\n--- 🧑‍🌾 Let's get your farm's current conditions! ---")

        # Fetch live weather information for Bengaluru
        temperature, humidity = get_weather(API_KEY, LOCATION)
        moisture = estimate_moisture(humidity) # Estimate soil moisture

        # Get user input for soil nutrient levels
        print("\n--- Now, tell us about your soil's current nutrient levels: ---")
        nitrogen = int(input("  🧪 Enter Nitrogen (N) value in your soil (e.g., 37): "))
        potassium = int(input("  🧪 Enter Potassium (K) value in your soil (e.g., 0): "))
        phosphorous = int(input("  🧪 Enter Phosphorous (P) value in your soil (e.g., 0): "))

        # Get user input for soil type from the categories the encoder learned
        selected_soil = ''
        try:
            # Find the 'Soil Type' categories from the encoder's learned features
            soil_type_category_index = categorical_cols.index('Soil Type')
            soil_types_from_encoder = encoder.categories_[soil_type_category_index]

            print("\n--- Select Your Soil Type from the options below: ---")
            for i, s in enumerate(soil_types_from_encoder):
                print(f"  {i}: {s}")
            soil_choice = int(input("  🔢 Enter the number corresponding to your soil type: "))
            selected_soil = soil_types_from_encoder[soil_choice]
            print(f"  🌍 You selected: **{selected_soil}**")
        except (ValueError, IndexError):
            print("Warning: Could not automatically determine soil types from loaded encoder or invalid choice.")
            selected_soil = input("  Please enter your Soil Type manually (e.g., 'Sandy', 'Clayey', 'Loamy'): ")
            print(f"  🌍 You entered: **{selected_soil}**")


        print("\n--- Applying the Magic Dust (Preprocessing Your Live Input Data)... ---")

        # Create a DataFrame for your new raw input data
        new_input_data_raw = pd.DataFrame({
            'Temparature': [temperature],
            'Humidity': [humidity],
            'Moisture': [moisture],
            'Nitrogen': [nitrogen],
            'Potassium': [potassium],
            'Phosphorous': [phosphorous],
            'Soil Type': [selected_soil]
        })

        # Apply the exact same preprocessing steps using the loaded transformers!
        # 1. Impute numerical columns
        processed_numeric_data = imputer.transform(new_input_data_raw[numeric_cols])
        processed_numeric_data_df = pd.DataFrame(processed_numeric_data, columns=numeric_cols, index=new_input_data_raw.index)

        # 2. Scale numerical columns
        scaled_numeric_data = scaler.transform(processed_numeric_data_df)
        scaled_numeric_data_df = pd.DataFrame(scaled_numeric_data, columns=numeric_cols, index=new_input_data_raw.index)

        # 3. One-Hot Encode categorical columns
        encoded_categorical_data = encoder.transform(new_input_data_raw[categorical_cols])
        encoded_cols_names = list(encoder.get_feature_names_out(categorical_cols))
        encoded_categorical_data_df = pd.DataFrame(encoded_categorical_data, columns=encoded_cols_names, index=new_input_data_raw.index)

        # Combine all preprocessed features. This step is crucial for maintaining the
        # exact column order that the models were trained on.
        expected_feature_order = numeric_cols + encoded_cols_names
        combined_processed_data = pd.concat([scaled_numeric_data_df, encoded_categorical_data_df], axis=1)

        # Ensure the final DataFrame for prediction has columns in the precise order
        final_new_data_for_prediction = combined_processed_data[expected_feature_order]

        print("\n✨ Your Live Input Data is Perfectly Prepared for Our Experts! ✨")
        print("  Here's a glimpse of what our models will see (first 5 features):")
        print(final_new_data_for_prediction.iloc[:, :5].T.to_string()) # Display transposed for single row readability
        print(f"\n  Total Prepared Features: {final_new_data_for_prediction.shape[1]} columns.")

        print("\n" + "="*70)
        print("🎉🎉🎉 Harvesting Your Intelligent Recommendations! 🎉🎉🎉")
        print("--- Generating Predictions for Your Farm ---")
        print("="*70 + "\n")

        # Get predictions from your loaded models!
        predicted_crop_type = model_crop_type.predict(final_new_data_for_prediction)
        print(f"\n🔮 Based on your current conditions, the **Predicted Crop Type** for your farm is: \033[1m\033[92m{predicted_crop_type[0].upper()}\033[0m! (Go Green! 💚)")

        predicted_fertilizer_name = model_fertilizer_name.predict(final_new_data_for_prediction)
        print(f"🧪 And the **Predicted Fertilizer Name** to nourish your crop is: \033[1m\033[96m{predicted_fertilizer_name[0].upper()}\033[0m! (Boost Growth! 💙)")

        print("\n" + "="*70)
        print("✨ Your Smart Farming Assistant has delivered its precise insights! ✨")
        print("Happy Farming! May your yields be bountiful! 🧑‍🌾")
        print("="*70 + "\n")