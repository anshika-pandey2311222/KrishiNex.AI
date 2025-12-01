// KrishiNex React UI
// Paste entire file into src/App.jsx

import React, { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function App() {
  const [stateName, setStateName] = useState("");
  const [district, setDistrict] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function handlePredict(e) {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!stateName || !district) {
      setError("Please enter both state and district.");
      return;
    }

    setLoading(true);
    try {
      const url = `${API_BASE_URL}/predict?state=${encodeURIComponent(
        stateName
      )}&district=${encodeURIComponent(district)}`;

      const res = await fetch(url);
      if (!res.ok) throw new Error(`Server responded ${res.status}`);

      const data = await res.json();

      if (data.status === "failed") {
        setError(data.message || "Prediction failed");
      } else {
        setResult(data);
      }
    } catch (err) {
      console.error(err);
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="max-w-3xl w-full bg-white rounded-2xl shadow-lg p-6">
        <header className="mb-6">
          <h1 className="text-2xl font-semibold">KrishiNex</h1>
          <p className="text-sm text-gray-500 mt-1">
            Location-based crop recommendation (state + district)
          </p>
        </header>

        <form
          onSubmit={handlePredict}
          className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4"
        >
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              State
            </label>
            <input
              value={stateName}
              onChange={(e) => setStateName(e.target.value)}
              placeholder="e.g. Uttar Pradesh"
              className="w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-300"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              District
            </label>
            <input
              value={district}
              onChange={(e) => setDistrict(e.target.value)}
              placeholder="e.g. Kanpur"
              className="w-full border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-300"
            />
          </div>

          <div className="md:col-span-2">
            <button
              type="submit"
              className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 text-white font-medium hover:bg-indigo-700 transition"
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg
                    className="w-4 h-4 animate-spin"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <circle
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="white"
                      strokeWidth="4"
                      opacity="0.2"
                    ></circle>
                    <path
                      d="M4 12a8 8 0 018-8"
                      stroke="white"
                      strokeWidth="4"
                      strokeLinecap="round"
                    ></path>
                  </svg>
                  Predicting...
                </>
              ) : (
                "Predict Crop"
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 text-red-700">
            {error}
          </div>
        )}

        {result && (
          <div className="border border-gray-100 rounded-lg p-4 bg-gray-50">
            <h2 className="text-lg font-semibold mb-2">Recommendation</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="text-sm text-gray-600">Location</div>
                <div className="font-medium">
                  {result.location.state} — {result.location.district}
                </div>

                <div className="text-sm text-gray-600 mt-3">
                  Predicted crop
                </div>
                <div className="text-2xl font-bold text-green-700">
                  {result.recommended_crop}
                </div>

                <div className="mt-3 text-sm text-gray-600">Features used</div>
                <ul className="list-disc pl-5 text-sm text-gray-700">
                  <li>N: {result.features_used.N}</li>
                  <li>P: {result.features_used.P}</li>
                  <li>K: {result.features_used.K}</li>
                  <li>pH: {result.features_used.pH}</li>
                  <li>Temperature: {result.features_used.temperature} °C</li>
                  <li>Humidity: {result.features_used.humidity} %</li>
                  <li>Rainfall: {result.features_used.rainfall} mm</li>
                </ul>
              </div>

              <div>
                <div className="text-sm text-gray-600">Quick tips</div>
                <div className="mt-2 bg-white p-3 rounded-lg shadow-sm">
                  <p className="text-sm text-gray-700">
                    Make sure the state + district pair exists in your
                    soil_reference.csv file. Add more rows if needed.
                  </p>
                </div>

                <div className="mt-4 text-sm text-gray-600">Actions</div>
                <div className="mt-2 flex gap-2">
                  <button
                    className="px-3 py-2 rounded-lg border border-gray-200 text-sm"
                    onClick={() => {
                      navigator.clipboard.writeText(
                        JSON.stringify(result, null, 2)
                      );
                      alert("Result copied to clipboard");
                    }}
                  >
                    Copy JSON
                  </button>

                  <button
                    className="px-3 py-2 rounded-lg bg-white border border-gray-200 text-sm"
                    onClick={() => window.location.reload()}
                  >
                    New Prediction
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        <footer className="mt-6 text-xs text-gray-400">
          KrishiNex · Powered by FastAPI & React
        </footer>
      </div>
    </div>
  );
}
