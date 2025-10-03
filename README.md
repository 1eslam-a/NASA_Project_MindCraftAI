# ☔ Weather Pro App — Real-time AI Weather Prediction

This is a full-stack web application designed to provide current weather data, a 5-day forecast, and a real-time, AI-driven probability prediction for rain.

The project seamlessly integrates live data from external APIs with a custom-trained Machine Learning model deployed on a Flask backend.

---

## 🚀 Project Architecture (Tech Stack)

The application follows a robust client-server architecture:

| Component | Technology / Library | Primary Role |
| :--- | :--- | :--- |
| **Frontend (UI)** | HTML, CSS, **JavaScript** | Displays the map, controls, and visualizes data using the **Leaflet.js** library. |
| **Backend (API Server)** | **Python (Flask)** | Handles routing, API calls to OpenWeatherMap, loads the ML model, and executes the rain prediction logic. |
| **Machine Learning** | **Scikit-learn (Random Forest)** | Provides the core intelligence for the binary rain prediction. |
| **Data Source** | **OpenWeatherMap APIs** | Supplies live data for current weather, 5-day forecasts, and geographical coordinates (Geocoding). |

---

## 🧠 Machine Learning Model Details

The core functionality of the app is its rain prediction feature, which runs an inference every time a user searches for a location.

### 1. Model Specifications

| Description | Specification |
| :--- | :--- |
| **Algorithm Used** | **Random Forest Classifier** 🌳 |
| **Model Type** | **Binary Classification** (Predicts 'Rain' or 'No Rain') |
| **Deployment File** | `rain_predictor_model.pkl` (Loaded via `joblib` in `app.py`) |

### 2. Input Features for Prediction

The model uses four key atmospheric features, which are extracted from the live OpenWeatherMap data:

1.  **Temperature** (`temp`)
2.  **Humidity** (`humidity`)
3.  **Wind Speed** (`wind_speed`)
4.  **Cloudiness** (`clouds`)

### 3. Model Performance (Accuracy)

The model was trained to identify patterns highly indicative of rain.

| Metric | Achieved Value (on test set) | Note |
| :---: | :---: | :--- |
| **Accuracy** | **$99.00\%$** | This high score demonstrates the model's strong classification ability on the training dataset. |

---

## 📹 Project Demonstration Video

Showcase your application in action! Replace the placeholder link and image below with your actual YouTube video link and a screenshot of your video thumbnail.

```markdown
[![Watch the App Demo](https://drive.google.com/file/d/1h2zLxATfggSXXizvY9eTxDyYera7Sq7V/view?usp=sharing)](YOUR_FULL_YOUTUBE_LINK)

**[Click here to watch the full application demonstration]** (Replace with your direct video link)
