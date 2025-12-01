import pandas as pd
import requests

# Load soil dataset
SOIL_DATA_PATH = "data/soil_reference.csv"
soil_df = pd.read_csv(SOIL_DATA_PATH)

# --- WEATHER API --- #
def fetch_weather(state, district):
    """
    Gets temperature, humidity, rainfall using Open-Meteo (Free API)
    Uses district name → latitude/longitude (via Open-Meteo geocoding)
    """

    # Geocoding API to convert district → coordinates
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={district}&count=1&language=en&format=json"
    geo_res = requests.get(geo_url).json()

    if "results" not in geo_res:
        return None, None, None

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    # Weather API
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relative_humidity_2m,rain"
    )

    weather_res = requests.get(weather_url).json()
    hourly = weather_res["hourly"]

    temperature = hourly["temperature_2m"][0]
    humidity = hourly["relative_humidity_2m"][0]
    rainfall = hourly["rain"][0]

    return temperature, humidity, rainfall


# --- MAIN FEATURE GENERATOR --- #
def generate_features(state, district):
    """
    Combines soil + weather to produce:
    N, P, K, pH, rainfall, temperature
    """

    # Filter soil data
    row = soil_df[
        (soil_df["state"].str.lower() == state.lower()) &
        (soil_df["district"].str.lower() == district.lower())
    ]

    if row.empty:
        return {"error": "Location not found in soil database"}

    row = row.iloc[0]

    # Soil features
    N = row["N"]
    P = row["P"]
    K = row["K"]
    pH = row["pH"]

    # Weather features
    temperature, humidity, rainfall = fetch_weather(state, district)

    return {
        "N": float(N),
        "P": float(P),
        "K": float(K),
        "pH": float(pH),
        "temperature": float(temperature),
        "humidity": float(humidity),
        "rainfall": float(rainfall)
    }
