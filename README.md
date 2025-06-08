# 🌿 Smart Farming Assistant: Cultivate Success with AI!

Welcome, future-forward farmer! 🌱 Are you ready to revolutionize your agricultural practices? The Smart Farming Assistant is your personal digital agronomist, an innovative application designed to empower you with intelligent, data-driven insights for bountiful harvests. Say goodbye to guesswork and hello to precision farming!

By seamlessly blending real-time environmental data with cutting-edge machine learning, this assistant doesn't just predict; it helps you make the most informed decisions about what to plant and how to nourish your crops, leading to healthier yields and a truly efficient farm.

---

## ✨ Why Choose the Smart Farming Assistant?

In a world where every crop counts, making the right choices is paramount. Our assistant cuts through the complexity, offering you:

- **Live from the Field:** No more relying on outdated weather forecasts! Get real-time temperature and humidity data for your precise location.
- **Tailored to Your Soil:** Our intelligent models don't just guess; they deeply analyze your specific soil nutrient levels (Nitrogen, Potassium, Phosphorous, and potentially Sodium) and soil type to offer hyper-personalized recommendations.
- **Simplicity Meets Sophistication:** We've distilled advanced agricultural science into a beautifully simple and intuitive web interface, making complex insights accessible to everyone.
- **Unlock Your Farm's Potential:** Aim for unprecedented yields and vibrant, healthy crops with the precision guidance of AI-powered recommendations.

---

## 🚀 Your Farm's Future: Key Features

Explore the powerful capabilities that make this assistant an indispensable tool for modern agriculture:

- **🌦️ Dynamic Weather Intelligence:** Integrates directly with [WeatherAPI.com](https://weatherapi.com/) to pull live weather specifics, ensuring every decision is rooted in your farm's current climate reality.
- **💧 Smart Soil Moisture Forecast:** Beyond just humidity, our system intelligently estimates your soil's moisture content, a vital indicator for optimal irrigation and plant health.
- **🌽 Crop Whisperer AI:** Our sophisticated machine learning model processes your unique environmental and soil blueprint to pinpoint the best crop type for your specific conditions, helping you plant with confidence.
- **🧪 Nutrient Navigator:** Get precise, data-backed suggestions for the ideal fertilizer that will provide your recommended crop with exactly what it needs to thrive and maximize its growth, taking into account essential nutrients like Nitrogen, Potassium, Phosphorous, and Sodium.
- **🖥️ Farmer-Friendly Dashboard:** A sleek, responsive web interface (crafted with Next.js and Tailwind CSS) makes entering your soil data a breeze and displays your personalized recommendations with crystal clarity.
- **🧠 Seamless Data Pipeline:** Behind the scenes, robust pre-trained data transformers (imputer, scaler, encoder) ensure that all your live input data is processed perfectly, mirroring the exact conditions the models were trained on.
- **⚡ Blazing-Fast Backend:** Powered by a high-performance FastAPI backend, all the complex data crunching and prediction generation happen swiftly, delivering insights almost instantly to your frontend.

---

## ❓ Frequently Asked Questions (FAQ)

### 1. **How does the Smart Farming Assistant work?**
The assistant collects your **soil data** (nutrient levels, soil type), **location**, and pulls **live weather data**. This information is processed by advanced machine learning models to recommend the most suitable crop and fertilizer for your situation.

### 2. **What data do I need to enter?**
You’ll need to provide:
- **Soil Nutrients:** Nitrogen (N), Phosphorous (P), Potassium (K), and optionally Sodium (Na) levels.
- **Soil Type:** Choose from a list (auto-fetched from backend).
- **Your Location:** For local weather data (city, town, or GPS coordinates).

> **Tip:** Unsure about your soil data? Many local agricultural services offer soil testing at low cost!

### 3. **How is weather data used?**
The app uses your location to fetch **real-time temperature and humidity** from WeatherAPI, which are then factored into crop and fertilizer recommendations—making your predictions as accurate as possible.

### 4. **Can I use this on my phone?**
Absolutely! The responsive design works smoothly on smartphones, tablets, and desktops. Just open the app in your browser.

### 5. **What if I get an error or invalid result?**
- Ensure all required fields are filled in.
- Double-check that your WeatherAPI Key is set correctly in `backend/main.py`.
- If the problem persists, check your internet connection or [open an issue](#-join-our-farming-community-contributing).

### 6. **How is my data handled?**
All processing happens locally—your input data is only used for predictions and is not stored unless you choose to save it. **No personal data leaves your device unless you submit an issue or feedback.**

### 7. **Can I add new crops or soil types?**
Currently, the assistant uses a fixed list from the trained model. For custom crops or soil types, you’re welcome to [contribute](#-join-our-farming-community-contributing) or suggest features!

### 8. **Is it possible to retrain the model with my own data?**
Yes! If you’re familiar with Python and scikit-learn, you can retrain the model using your own dataset and update the `.joblib` files in the `backend/models/` directory. See the [Contributing](#-join-our-farming-community-contributing) section.

### 9. **Can I use this for large commercial farms?**
The assistant is designed for both small and large-scale farms. For highly specialized operations, consult with your agronomist and consider using the assistant as a supplementary tool.

### 10. **How do I get help while using the app?**
- Hover over form fields for tooltips and explanations.
- Click the "Help" or "FAQ" button in the app for instant answers.
- Join our [GitHub Discussions](https://github.com/zennyMe17/smart_farming_assistant/discussions) or open an issue.

---

## 🛠️ The Engine Room: Our Tech Stack

This project is a harmonious blend of cutting-edge technologies, bringing together the power of Python for intelligent decision-making and the versatility of JavaScript for a rich user experience.

### Backend: The Brain (Python FastAPI)

- **Python 3.x:** The sturdy foundation for all our backend logic and sophisticated machine learning models.
- **FastAPI:** A modern, incredibly fast, and developer-friendly Python web framework. It builds APIs with Python 3.7+ using standard type hints, making development efficient and robust.
- **uvicorn:** The powerhouse ASGI server that swiftly brings the FastAPI application to life.
- **pandas & numpy:** Your go-to libraries for powerful data manipulation and high-performance numerical operations.
- **requests:** The workhorse for making seamless HTTP calls to external services like WeatherAPI.com.
- **joblib:** Our secret sauce for quickly and reliably loading those crucial pre-trained machine learning models and data preprocessing pipelines.
- **scikit-learn:** The robust and widely-used machine learning library that forms the very intelligence core of our prediction models.
- **python-dotenv:** Ensures your sensitive configuration, like API keys, are loaded securely from environment variables, keeping your code clean and safe.

### Frontend: The Interface (Next.js with React)

- **Next.js:** A dynamic React framework that excels at server-side rendering and static site generation, ensuring your farm assistant loads fast and looks great on any device.
- **React:** The declarative JavaScript library that makes building interactive, component-based user interfaces a pure delight.
- **Tailwind CSS:** A utility-first CSS framework that allows for lightning-fast and highly customizable styling directly within your HTML/JSX, giving you full control over the visual appeal.
- **React Icons (io5):** Provides a vast collection of crisp, scalable vector icons, adding intuitive visual cues and enhancing the overall clarity of the interface.

---

## 🚀 Ready to Grow? Getting Started!

Let's get your Smart Farming Assistant up and running! This project consists of two main parts: the powerful backend API and the interactive frontend web application.

### Prerequisites: Gather Your Tools

Before you begin, make sure you have these essentials installed:

- Python 3.x and its package installer, `pip`
- Node.js and its package manager, `npm`
- A WeatherAPI Key (a free tier is available – grab yours from [WeatherAPI.com](https://weatherapi.com/))

---

### 1. Get Your WeatherAPI Key

1. Visit [WeatherAPI.com](https://weatherapi.com/).
2. Sign up for a free account and locate your unique API key.
3. **Important:** Open the file `backend/main.py` and replace the placeholder API key with your actual key:

    ```python
    WEATHER_API_KEY = "YOUR_ACTUAL_WEATHERAPI_KEY_HERE" # Update this line!
    ```

---

### 2. Clone the Repository

Start by cloning the project files to your local machine:

```sh
git clone https://github.com/zennyMe17/smart_farming_assistant.git
cd smart_farming_assistant
```

---

### 3. Backend Setup: Ignite the Intelligence!

Navigate into the backend directory to set up and launch your API:

```sh
cd backend
```

#### a. Create a Python Virtual Environment (Highly Recommended!)

Isolate your Python dependencies for a clean and conflict-free setup:

```sh
python -m venv venv
```

#### b. Activate Your Virtual Environment

- **On Windows:**
    ```sh
    .\venv\Scripts\activate
    ```
- **On macOS/Linux:**
    ```sh
    source venv/bin/activate
    ```

#### c. Install Backend Dependencies

Install all the Python libraries required for the backend:

```sh
pip install -r requirements.txt
```

#### d. Models Directory: The AI's Core

Ensure you have a directory named `models` located inside your `backend` folder. This directory must contain all the pre-trained machine learning models and preprocessing tools (the `.joblib` files). Without these, the prediction engine cannot function!

- `model_crop_type.joblib`
- `model_fertilizer_name.joblib`
- `imputer.joblib`
- `scaler.joblib`
- `encoder.joblib`
- `input_cols.joblib`
- `numeric_cols.joblib`
- `categorical_cols.joblib`

(These essential files are generated during the model training phase of the project.)

---

### 4. Frontend Setup: Bring the Experience to Life!

Open a brand new terminal window (keep your backend terminal running in the first one!) and navigate to your frontend directory:

```sh
cd ../frontend # This command takes you back up to the main project folder, then into 'frontend'
```

#### a. Install Frontend Dependencies

Install all the necessary Node.js packages for your Next.js application:

```sh
npm install
```

---

## 🧑‍🌾 Cultivating Your Results: How to Run the Assistant!

With both the backend and frontend meticulously set up, it's time to unleash your Smart Farming Assistant!

### 1. Launch the Backend API (Terminal 1)

In your first terminal window (where you performed the backend setup), make sure your virtual environment is still active, then start the FastAPI server:

```sh
cd backend
# If your virtual environment isn't active, activate it again:
# .\venv\Scripts\activate  (Windows)
# source venv/bin/activate (macOS/Linux)

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You'll see messages indicating that the FastAPI application is running. You can even check its interactive documentation by opening [http://localhost:8000/docs](http://localhost:8000/docs) in your web browser.

---

### 2. Start the Frontend Web Application (Terminal 2)

In your second, separate terminal window (where you set up the frontend), navigate to the frontend directory and fire up the Next.js development server:

```sh
cd frontend
npm run dev
```

The frontend application will typically launch on [http://localhost:3000](http://localhost:3000). Open this URL in your web browser, and you'll be greeted by your Smart Farming Assistant, ready to transform your farming with intelligent recommendations!

---

## 🔬 Under the Hood: A Glimpse at the Frontend Magic (Next.js with React)

For developers keen on understanding the client-side experience, here's a quick peek at the `HomePage` component:

- **'use client' Directive:** This little line makes HomePage a Client Component, allowing it to leverage interactive features like state management and event listeners directly within the user's browser.

- **Intuitive State Management:**
    - `formData`: Smoothly keeps track of all your essential inputs (Nitrogen, Potassium, Phosphorous, Sodium, Soil Type, Location).
    - `prediction`: Stores and proudly displays the valuable insights received from the backend.
    - `loading`: Provides instant visual feedback (like a spinning animation) while API calls are in progress.
    - `error`: Catches and clearly communicates any issues that pop up during data fetching or processing.
    - `soilTypes`: Dynamically populates the soil type dropdown, fetching available options from your FastAPI backend when the page loads.

- **Seamless API Communication:**
    - An `useEffect` hook springs into action when the component mounts, ensuring the list of available soil types is fetched from the `/soil-types` endpoint.
    - The `handleSubmit` function is the maestro, orchestrating the entire prediction process by sending your soil data (including Nitrogen, Potassium, Phosphorous, and Sodium) and location to the backend's `/predict` endpoint.

- **Smart Form Interactions:**
    - The `handleChange` function ensures every input and selection you make instantly updates the `formData` state, providing a fluid user experience.
    - Includes essential client-side validation to make sure all required fields are filled before submitting.

- **Dynamic and Delightful User Interface:**
    - Styling is powered by Tailwind CSS, delivering a modern, responsive, and visually appealing design that works beautifully across devices.
    - Integrates React Icons (`io5`) to add engaging and informative visual cues, like a leafy icon for crops or a water droplet for humidity.

    - Provides clear, dynamic feedback:
        - A friendly loading spinner when predictions are being calculated.
        - Prominent, easy-to-understand error messages if anything goes awry.
        - A beautifully formatted and impactful display of the predicted crop type and fertilizer name, along with the live weather details, helping you make informed decisions at a glance.

---

## 🤝 Join Our Farming Community: Contributing!

We believe in collaborative growth! If you have bright ideas for new features, spotted a pesky bug, or want to contribute code improvements, please don't hesitate:

- **Open an Issue:** Describe your suggestion or the bug you've uncovered.
- **Submit a Pull Request:** Share your code changes with the community.

Let's nurture this Smart Farming Assistant together and make it an even more powerful tool for farmers worldwide!

---

## 🧑‍💻 About the Creator

This Smart Farming Assistant was conceptualized and developed by **Hemanth S**, a dedicated student of Computer Science and Cyber Security Engineering at Ramaiah Institute of Technology.

---

## 🙏 A Big Thank Thank You! (Acknowledgements)

We extend our gratitude to the amazing tools and communities that made this project possible:

- **WeatherAPI.com:** For providing accessible and crucial real-time weather data.
- **scikit-learn:** For the robust and powerful machine learning tools that drive our predictions.
- **FastAPI:** For an incredibly efficient, modern, and developer-friendly API framework.
- **Next.js and React:** For enabling the creation of such a modern, responsive, and engaging web user interface.

---

Happy Farming! 🌾
