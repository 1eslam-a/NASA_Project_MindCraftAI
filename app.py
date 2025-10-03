from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import joblib
import pandas as pd
import warnings
import sys
from datetime import datetime, timedelta

# ----------------------------------------------------
# 🎯 CONFIGURATION
# ----------------------------------------------------
API_KEY = "acf6163dc7a827c6a7e678fc251f705a" 
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast" 
MODEL_FILENAME = 'rain_predictor_model.pkl'

app = Flask(__name__)
CORS(app) 

# Load the trained model globally
warnings.filterwarnings("ignore")
if 'model' not in locals():
    try:
        model = joblib.load(MODEL_FILENAME)
        print("✅ الموديل تم تحميله بنجاح.")
    except FileNotFoundError:
        print(f"❌ خطأ: ملف الموديل ({MODEL_FILENAME}) غير موجود.")
        sys.exit()

# ----------------------------------------------------
# UTILITY FUNCTION: Get Current Weather Data
# ----------------------------------------------------
def get_current_weather_data(lat, lon):
    url = f"{WEATHER_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

# ----------------------------------------------------
# UTILITY FUNCTION: Get 5-Day Forecast Data (Daily Aggregation)
# ----------------------------------------------------
def get_5day_forecast_data(lat, lon):
    url = f"{FORECAST_API_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    forecast_data = response.json()
    
    daily_forecasts = {}
    
    # Iterate over all 40 entries (5 days x 8 periods)
    for entry in forecast_data['list']:
        dt_object = datetime.fromtimestamp(entry['dt'])
        day_date = dt_object.date()
        
        # We target the forecast entry closest to noon (12:00 PM) for daily aggregation
        if day_date not in daily_forecasts:
            daily_forecasts[day_date] = entry
        else:
            # Check if this entry is closer to noon (12:00) than the one saved
            current_noon_diff = abs(dt_object.hour - 12)
            saved_dt = datetime.fromtimestamp(daily_forecasts[day_date]['dt'])
            saved_noon_diff = abs(saved_dt.hour - 12)
            
            if current_noon_diff < saved_noon_diff:
                daily_forecasts[day_date] = entry

    # Format the aggregated results
    simplified_forecast = []
    
    # Ensure we only include 5 days (sorted by date)
    sorted_days = sorted(daily_forecasts.keys())
    
    for day_date in sorted_days[:5]:
        entry = daily_forecasts[day_date]
        simplified_forecast.append({
            'date': day_date.strftime('%Y-%m-%d'),
            'time_of_entry': datetime.fromtimestamp(entry['dt']).strftime('%H:%M'),
            'temp': entry['main']['temp'],
            'description': entry['weather'][0]['description'],
            'humidity': entry['main']['humidity']
        })
    return simplified_forecast

# ----------------------------------------------------
# UTILITY FUNCTION: Geocoding
# ----------------------------------------------------
def get_coords_from_name(city_name):
    url = f"{GEOCODING_URL}?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if data:
        # returns lat, lon
        return data[0]['lat'], data[0]['lon']
    return None, None

# ----------------------------------------------------
# API ROUTE 1: Current Weather Prediction (Uses ML Model)
# ----------------------------------------------------
@app.route('/predict_weather', methods=['GET'])
def predict_weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    city_name = request.args.get('name', type=str)
    
    # 1. Geocoding logic
    if city_name:
        lat, lon = get_coords_from_name(city_name)
        if lat is None or lon is None:
            return jsonify({"error": f"الموقع غير موجود لـ: {city_name}"}), 404

    if lat is None or lon is None:
        return jsonify({"error": "يجب إدخال إحداثيات الموقع."}), 400

    try:
        data = get_current_weather_data(lat, lon)
        
        # Extract features for ML model
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        clouds = data['clouds']['all']
        weather_main = data['weather'][0]['main']
        city_name_output = data.get('name', 'الموقع المحدد')
        
        # 🛑 NEW: Extract and format observation time 🛑
        observation_time_unix = data['dt']
        observation_time_str = datetime.fromtimestamp(observation_time_unix).strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Prepare DataFrame for ML model
        features_df = pd.DataFrame(
            [[temp, humidity, wind_speed, clouds]], 
            columns=['temp', 'humidity', 'wind_speed', 'clouds']
        )
        
        # Prediction
        prediction = model.predict(features_df)[0]
        rain_status_model = "محتمل" if prediction == 1 else "غير محتمل"
        
        return jsonify({
            "status": "success",
            "location": city_name_output,
            "latitude": lat,
            "longitude": lon,
            "temperature": temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "clouds": clouds,
            "current_weather": weather_main,
            "observation_time": observation_time_str, # <--- NEW FIELD
            "rain_prediction": rain_status_model
        })

    except Exception as e:
        return jsonify({"error": f"خطأ داخلي في الخادم: {e}"}), 500


# ----------------------------------------------------
# API ROUTE 2: 5-Day Forecast (Uses OpenWeather Data)
# ----------------------------------------------------
@app.route('/get_forecast', methods=['GET'])
def forecast_route():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({"error": "Missing coordinates for forecast."}), 400

    try:
        # Get forecast results (daily aggregated)
        forecast_results = get_5day_forecast_data(lat, lon)
        
        # Get city name for display purposes
        city_data = get_current_weather_data(lat, lon)
        
        return jsonify({
            "status": "success",
            "location_name": city_data.get('name', 'الموقع المحدد'),
            "forecast": forecast_results
        })

    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"OpenWeather Forecast API Error: {e}"}), 502
    except Exception as e:
        return jsonify({"error": f"Internal Server Error during forecast fetch: {e}"}), 500

# ----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
