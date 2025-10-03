# ☔ Weather Pro — Real-time AI Weather Prediction Pipeline

A complete end-to-end web application that integrates live weather data from OpenWeatherMap APIs with a trained Machine Learning model to predict the probability of rain in real time. The focus is on robust deployment capability.

---

## 📌 Project Overview

This project provides users with current weather information and a multi-day forecast, but its key feature is the **AI-driven rain prediction**. The system quickly processes live atmospheric variables to give a simple, actionable binary forecast ("Probable" / "Not Probable").

---

## 🎥 Demo Video
📺 Watch the full application demo here:

https://github.com/user-attachments/assets/a9282ecb-6cbb-45c9-9462-aedb0a778b2f


---

## 🚀 Features

- **Full-Stack Deployment:** Integrated Frontend (JavaScript/Leaflet) and Backend (Flask/Python).
- **Live Data Acquisition:** Fetching current and forecast data via OpenWeatherMap APIs.
- **AI Integration:** Hosting and executing the trained ML model in the Flask server.
- **Data Filtering Logic:** Optimized 5-day forecast by selecting the entry closest to noon (12:00 PM) for each day.
- **Geolocation Support:** Search by City Name (Geocoding) or by Coordinates (Map Click/GPS).
- **Theming:** Supports both Dark and Light UI modes.

---

## 🧠 Machine Learning Model Details

The model is a **Binary Classifier** deployed via the Flask backend (`app.py` endpoint: `/predict_weather`).

### 1. Model Specifications

| Description | Specification |
| :--- | :--- |
| **Algorithm Used** | **Random Forest Classifier** 🌳 |
| **Model Type** | **Binary Classification** (Predicts 'Rain' or 'No Rain') |
| **Deployment File** | `rain_predictor_model.pkl` (Loaded via `joblib`) |
| **Prediction Output** | `محتمل` (Probable) or `غير محتمل` (Not Probable) |

### 2. Input Features for Prediction

The model uses the following live atmospheric data as inputs:

1.  **Temperature** (`temp`)
2.  **Humidity** (`humidity`)
3.  **Wind Speed** (`wind_speed`)
4.  **Cloudiness** (`clouds`)

### 3. Model Performance (Accuracy)

| Metric | Achieved Value (on test set) | Notes |
| :---: | :---: | :--- |
| **Accuracy** | **$99.00\%$** | High classification accuracy achieved on the synthetic training dataset. |

---

## 🧰 Tech Stack

- Python 3.x (Backend)
- Flask (Web Framework)
- scikit-learn & joblib (ML Model Management)
- JavaScript & **Leaflet.js** (Frontend & Mapping)
- pandas (Data Preparation)

---

## ⚙️ How to Run Locally

To run this project, ensure you have both the Python backend and the HTML frontend configured.

### Prerequisites

1.  A valid OpenWeatherMap API Key (currently hardcoded in `app.py`).
2.  Python installed.

### 1. Backend Setup (Flask Server)

1.  Clone the repository and install the required libraries:
    ```bash
    pip install flask flask-cors requests pandas joblib scikit-learn
    ```
2.  Ensure the trained model file **`rain_predictor_model.pkl`** is in the root directory.
3.  Start the Flask server:
    ```bash
    python app.py
    ```
    The server will run on `http://127.0.0.1:5000`.

### 2. Frontend Launch

1.  Open the `index.html` file directly in your web browser (Chrome, Firefox, etc.).
2.  The application will automatically connect to the running Flask backend to fetch data and run the AI prediction.
