'use client'; // This directive makes the component a Client Component

import { useState, useEffect } from 'react';
import { IoLeaf, IoWater, IoThermometer, IoCloudy, IoFlask, IoNutrition } from 'react-icons/io5';

// Define types for prediction response and form inputs
interface PredictionResponse {
  temperature_c: number;
  humidity_percent: number;
  moisture_estimate: number;
  predicted_crop_type: string;
  predicted_fertilizer_name: string;
}

interface FormData {
  nitrogen: number | '';
  potassium: number | '';
  phosphorous: number | '';
  soil_type: string;
  location: string; // Added location to form data
}

// Define the backend API URL
const BACKEND_API_URL = 'http://localhost:8000'; // Make sure this matches your FastAPI backend URL

export default function HomePage() {
  const [formData, setFormData] = useState<FormData>({
    nitrogen: '',
    potassium: '',
    phosphorous: '',
    soil_type: '',
    location: 'Bengaluru', // Default location as per your backend
  });
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [soilTypes, setSoilTypes] = useState<string[]>([]);

  useEffect(() => {
    // Fetch soil types from backend when component mounts
    const fetchSoilTypes = async () => {
      try {
        const response = await fetch(`${BACKEND_API_URL}/soil-types`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: string[] = await response.json();
        setSoilTypes(data);
        if (data.length > 0) {
          setFormData((prev) => ({ ...prev, soil_type: data[0] })); // Set default soil type
        }
      } catch (err: any) {
        console.error('Failed to fetch soil types:', err);
        setError(`Failed to load soil types: ${err.message}. Please ensure backend is running.`);
      }
    };
    fetchSoilTypes();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'nitrogen' || name === 'potassium' || name === 'phosphorous'
        ? value === '' ? '' : Number(value)
        : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null); // Clear previous prediction

    // Basic validation
    if (formData.nitrogen === '' || formData.potassium === '' || formData.phosphorous === '' || formData.soil_type === '' || formData.location === '') {
      setError("Please fill in all fields, including location.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`${BACKEND_API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nitrogen: formData.nitrogen,
          potassium: formData.potassium,
          phosphorous: formData.phosphorous,
          soil_type: formData.soil_type,
          location: formData.location, // Send location to backend
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data: PredictionResponse = await response.json();
      setPrediction(data);
    } catch (err: any) {
      console.error('Failed to fetch prediction:', err);
      setError(`Prediction failed: ${err.message}. Ensure backend is running and correct data is provided.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-100 via-lime-100 to-sky-100 flex items-center justify-center p-4 sm:p-8">
      <div className="bg-white p-6 sm:p-10 rounded-3xl shadow-2xl w-full max-w-xl xl:max-w-3xl border border-gray-100 transform hover:shadow-3xl transition-all duration-300">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-center text-green-800 mb-8 tracking-tight leading-tight">
          <span className="inline-block animate-bounce-slow origin-bottom">🌱</span> Smart Farming Assistant <span className="inline-block animate-bounce-slow origin-bottom animation-delay-500">🧑‍🌾</span>
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
            <div>
              <label htmlFor="nitrogen" className="block text-sm sm:text-base font-semibold text-gray-700 mb-1">
                Nitrogen (N) Value:
              </label>
              <input
                type="number"
                id="nitrogen"
                name="nitrogen"
                value={formData.nitrogen}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 sm:py-3 border border-gray-300 rounded-xl shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-base bg-gray-50 text-gray-900 transition duration-200 hover:border-green-400 focus:bg-white"
                placeholder="e.g., 37"
                min="0"
              />
            </div>
            <div>
              <label htmlFor="potassium" className="block text-sm sm:text-base font-semibold text-gray-700 mb-1">
                Potassium (K) Value:
              </label>
              <input
                type="number"
                id="potassium"
                name="potassium"
                value={formData.potassium}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 sm:py-3 border border-gray-300 rounded-xl shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-base bg-gray-50 text-gray-900 transition duration-200 hover:border-green-400 focus:bg-white"
                placeholder="e.g., 0"
                min="0"
              />
            </div>
            <div>
              <label htmlFor="phosphorous" className="block text-sm sm:text-base font-semibold text-gray-700 mb-1">
                Phosphorous (P) Value:
              </label>
              <input
                type="number"
                id="phosphorous"
                name="phosphorous"
                value={formData.phosphorous}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 sm:py-3 border border-gray-300 rounded-xl shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-base bg-gray-50 text-gray-900 transition duration-200 hover:border-green-400 focus:bg-white"
                placeholder="e.g., 0"
                min="0"
              />
            </div>
            <div>
              <label htmlFor="soil_type" className="block text-sm sm:text-base font-semibold text-gray-700 mb-1">
                Select Soil Type:
              </label>
              <select
                id="soil_type"
                name="soil_type"
                value={formData.soil_type}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 sm:py-3 border border-gray-300 rounded-xl shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-base bg-gray-50 text-gray-900 appearance-none pr-8 transition duration-200 hover:border-green-400 focus:bg-white"
              >
                {soilTypes.length === 0 ? (
                  <option value="">Loading soil types...</option>
                ) : (
                  <>
                    <option value="">-- Select a Soil Type --</option>
                    {soilTypes.map((type) => (
                      <option key={type} value={type}>
                        {type}
                      </option>
                    ))}
                  </>
                )}
              </select>
            </div>
            {/* New: Location Input Field */}
            <div className="md:col-span-2"> {/* Make it span full width on medium screens */}
              <label htmlFor="location" className="block text-sm sm:text-base font-semibold text-gray-700 mb-1">
                Location (for Weather Data):
              </label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                required
                className="mt-1 block w-full px-4 py-2 sm:py-3 border border-gray-300 rounded-xl shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-base bg-gray-50 text-gray-900 transition duration-200 hover:border-green-400 focus:bg-white"
                placeholder="e.g., Bengaluru, India"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full flex justify-center py-3 px-6 border border-transparent rounded-lg shadow-lg text-lg font-semibold text-white bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition duration-300 ease-in-out transform hover:scale-105 active:scale-98"
            disabled={loading || soilTypes.length === 0}
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Getting Recommendations...
              </span>
            ) : (
              'Get Recommendations'
            )}
          </button>
        </form>

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6 shadow-md" role="alert">
            <div className="flex items-center">
              <div className="py-1"><svg className="fill-current h-6 w-6 text-red-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"/></svg></div>
              <div>
                <strong className="font-bold">Error!</strong>
                <span className="block sm:inline ml-2">{error}</span>
              </div>
            </div>
          </div>
        )}

        {prediction && (
          <div className="bg-blue-50 p-6 sm:p-8 rounded-xl shadow-inner border border-blue-200">
            <h2 className="text-2xl sm:text-3xl font-bold text-blue-700 mb-6 text-center">Your Personalized Farm Insights:</h2>
            <div className="space-y-4 sm:space-y-6">
              {/* Weather Insights */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="flex flex-col items-center p-4 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg shadow-md border border-blue-300 transform hover:scale-103 transition duration-300">
                  <IoThermometer className="text-3xl text-blue-600 mb-2" />
                  <span className="text-sm font-medium text-gray-700">Temperature:</span>
                  <span className="text-xl font-bold text-blue-800">{prediction.temperature_c.toFixed(1)}°C</span>
                </div>
                <div className="flex flex-col items-center p-4 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg shadow-md border border-blue-300 transform hover:scale-103 transition duration-300">
                  <IoWater className="text-3xl text-blue-600 mb-2" />
                  <span className="text-sm font-medium text-gray-700">Humidity:</span>
                  <span className="text-xl font-bold text-blue-800">{prediction.humidity_percent.toFixed(1)}%</span>
                </div>
                <div className="flex flex-col items-center p-4 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg shadow-md border border-blue-300 transform hover:scale-103 transition duration-300">
                  <IoCloudy className="text-3xl text-blue-600 mb-2" />
                  <span className="text-sm font-medium text-gray-700">Est. Soil Moisture:</span>
                  <span className="text-xl font-bold text-blue-800">{prediction.moisture_estimate.toFixed(1)}%</span>
                </div>
              </div>

              {/* Core Predictions */}
              <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 pt-4">
                <div className="flex-1 flex flex-col items-center p-6 bg-gradient-to-br from-green-200 to-green-300 rounded-xl shadow-lg border border-green-400 transform hover:scale-103 transition duration-300">
                  <IoLeaf className="text-4xl text-green-700 mb-3" />
                  <span className="block text-md sm:text-lg font-bold text-green-800 mb-1">Predicted Crop Type:</span>
                  <span className="block text-3xl sm:text-4xl font-extrabold text-green-900 text-center leading-tight">
                    {prediction.predicted_crop_type.toUpperCase()}
                  </span>
                </div>
                <div className="flex-1 flex flex-col items-center p-6 bg-gradient-to-br from-yellow-200 to-yellow-300 rounded-xl shadow-lg border border-yellow-400 transform hover:scale-103 transition duration-300">
                  <IoNutrition className="text-4xl text-yellow-700 mb-3" />
                  <span className="block text-md sm:text-lg font-bold text-yellow-800 mb-1">Recommended Fertilizer:</span>
                  <span className="block text-3xl sm:text-4xl font-extrabold text-yellow-900 text-center leading-tight">
                    {prediction.predicted_fertilizer_name.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}