# 🌿 Smart Farming Assistant: Cultivate Success with AI!

Welcome, future-forward farmer! 🌱 Are you ready to revolutionize your agricultural practices? The **Smart Farming Assistant** is your personal digital agronomist, an innovative application designed to help you make smarter, data-driven decisions—maximizing yields, optimizing resources, and growing healthier crops.

By seamlessly blending real-time environmental data with cutting-edge machine learning, this assistant doesn't just predict; it **guides you step-by-step** through the complexities of modern farming, empowering you to choose the best crops and fertilizers for your unique conditions.

---

## ✨ Why Choose the Smart Farming Assistant?

In a world where every crop counts, making the right choices is paramount. Our assistant cuts through the complexity, offering you:

- **Live from the Field:** No more relying on outdated weather forecasts! Get real-time temperature and humidity data for your precise location.
- **Tailored to Your Soil:** Intelligent models deeply analyze your specific soil nutrient levels (Nitrogen, Potassium, Phosphorous, Sodium) and soil type to provide personalized recommendations.
- **Simplicity Meets Sophistication:** Advanced agricultural science distilled into a beautifully simple, intuitive web interface—accessible to everyone, regardless of tech experience.
- **Unlock Your Farm's Potential:** Achieve unprecedented yields and vibrant, healthy crops with precision AI-powered guidance.
- **Interactive Guidance:** Answers to your most common (and uncommon!) farming questions—right inside the app.

---

## 🚀 Key Features at a Glance

- **🌦️ Dynamic Weather Intelligence:** Integrates with [WeatherAPI.com](https://weatherapi.com/) for live weather, ensuring every recommendation is grounded in real-time conditions.
- **💧 Smart Soil Moisture Forecast:** Intelligently estimates your soil's moisture content for optimal irrigation and plant health.
- **🌽 Crop Whisperer AI:** Our machine learning model analyzes your environment and soil to pinpoint the best crop for your conditions.
- **🧪 Nutrient Navigator:** Precise, data-backed suggestions for the ideal fertilizer, customized for your crop and soil.
- **🖥️ Farmer-Friendly Dashboard:** Modern, responsive web interface (Next.js + Tailwind CSS) makes entering and viewing your data a breeze.
- **🧠 Robust Data Pipeline:** Pre-trained data transformers (imputer, scaler, encoder) ensure live input data is processed just as during model training.
- **⚡ Lightning-Fast Backend:** FastAPI and Uvicorn power rapid, reliable predictions.
- **👨‍🌾 Interactive Help:** In-app guidance, tooltips, and FAQ—get instant answers as you use the assistant!

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

## 🕹️ Interactive User Experience

- **Dynamic Tooltips:** Hover over any input for quick info about what’s needed.
- **Live Feedback:** See a loading spinner while AI crunches your data, and clear messages if something goes wrong.
- **Step-by-Step Guidance:** The form guides you through the process, validating your entries and highlighting missing data.
- **Instant Insights:** Get a summary card with your recommended crop, fertilizer, and a snapshot of the weather at your location.
- **In-App FAQ:** Click the FAQ button in the dashboard to open this section as a popup—never leave the page while learning!

---

## 🛠️ Tech Stack Overview

### Backend: The Brain (Python FastAPI)
- **Python 3.x**
- **FastAPI**, **uvicorn**
- **pandas**, **numpy**, **requests**
- **joblib**, **scikit-learn**
- **python-dotenv** for secure config

### Frontend: The Interface (Next.js with React)
- **Next.js** & **React**
- **Tailwind CSS**
- **React Icons (io5)**

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.x & `pip`
- Node.js & `npm`
- WeatherAPI Key ([Get yours for free](https://weatherapi.com/))

### Backend Setup

```sh
git clone https://github.com/zennyMe17/smart_farming_assistant.git
cd smart_farming_assistant/backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
# Place your trained .joblib files in the 'models' directory
```
> **Don't forget:** Update your WeatherAPI key in `main.py`.

### Frontend Setup

```sh
cd ../frontend
npm install
```

### Running the Assistant

- **Start Backend:**  
  ```sh
  cd backend
  source venv/bin/activate
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```
- **Start Frontend:**  
  ```sh
  cd frontend
  npm run dev
  ```

- **Open [http://localhost:3000](http://localhost:3000) in your browser.**

---

## 👩‍💻 Developer Glimpse: What's Inside the Code?

- **HomePage Component:**  
  - `"use client"` for interactivity  
  - **State:** `formData`, `prediction`, `loading`, `error`, `soilTypes`
  - **API Calls:** Fetches soil types and submits user data to backend
  - **UX:** Loading spinner, error handling, result display

- **Data Pipeline:**  
  - Pre-trained transformers ensure live inputs match model expectations
  - Modular FastAPI endpoints

- **Styling:**  
  - Tailwind + React Icons for a user-friendly look

---

## 🤝 Join Our Farming Community: Contributing!

We believe in collaborative growth! If you have ideas for features, find a bug, or want to contribute code:

- **Open an Issue:** Describe your suggestion or bug.
- **Submit a Pull Request:** Share your improvements.
- **Join Discussions:** Ask questions or help others in [GitHub Discussions](https://github.com/zennyMe17/smart_farming_assistant/discussions).

Let’s nurture this project together for a smarter, greener future!

---

## 👨‍💻 About the Creator

This Smart Farming Assistant was conceptualized and developed by **Hemanth S**, Computer Science and Cyber Security Engineering student, Ramaiah Institute of Technology.

---

## 🙏 Acknowledgements

- **WeatherAPI.com:** For real-time weather data
- **scikit-learn:** Machine learning tools
- **FastAPI:** Efficient backend API
- **Next.js & React:** Modern frontend experience

---

Happy Farming! 🌾  
*Have more questions? Hit the FAQ in the app, or join our community!*
