import requests
import joblib
import pandas as pd
import warnings
import sys
import numpy as np # ضروري لوظائف NumPy

# =========================================================================
# 🎯 الإعدادات
# =========================================================================
API_KEY = "acf6163dc7a827c6a7e678fc251f705a" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
MODEL_FILENAME = 'rain_predictor_model.pkl'

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------
# 1. تحميل الموديل المدرب
# ---------------------------------------------------------------------
try:
    # ⚠️ تأكد أن هذا الملف موجود في مجلد الكود
    model = joblib.load(MODEL_FILENAME)
    print(f"✅ تم تحميل الموديل ({MODEL_FILENAME}) بنجاح.")
except FileNotFoundError:
    print(f"❌ خطأ: لم يتم العثور على ملف الموديل ({MODEL_FILENAME}). يرجى تدريب وحفظ الموديل أولاً.")
    sys.exit()


# ---------------------------------------------------------------------
# 2. طلب الموقع من المستخدم
# ---------------------------------------------------------------------
try:
    print("-" * 50)
    print("🌍 نظام التنبؤ بالمطر (المدخلات التفاعلية)")
    
    # طلب خط العرض والطول
    lat = float(input("الرجاء إدخال خط العرض (Latitude) (مثلاً: 30.04): "))
    lon = float(input("الرجاء إدخال خط الطول (Longitude) (مثلاً: 31.23): "))

except ValueError:
    print("\n❌ خطأ: يجب إدخال أرقام صحيحة لخطوط الطول والعرض.")
    sys.exit()

# ---------------------------------------------------------------------
# 3. جلب البيانات والتنبؤ
# ---------------------------------------------------------------------
url = f"{BASE_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

print(f"\n⏳ جاري جلب البيانات لـ (Lat: {lat}, Lon: {lon})...")

try:
    # 🛑 تم زيادة المهلة إلى 30 ثانية
    response = requests.get(url, timeout=30) 
    response.raise_for_status() 
    data = response.json()
    
    # استخراج المدخلات (Features) بنفس ترتيب التدريب (يجب أن يكون temp, humidity, wind_speed, clouds)
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    clouds = data['clouds']['all']
    weather_main = data['weather'][0]['main']
    
    # تجهيز البيانات في DataFrame للتنبؤ (ضروري لـ Scikit-Learn)
    # ⚠️ ملاحظة: يجب أن تتطابق أسماء الأعمدة مع أسماء أعمدة التدريب (مثلاً: temp, humidity, wind_speed, clouds)
    features_df = pd.DataFrame(
        [[temp, humidity, wind_speed, clouds]], 
        columns=['temp', 'humidity', 'wind_speed', 'clouds']
    )
    
    # 🎯 التنبؤ باستخدام الموديل
    prediction = model.predict(features_df)[0]
    rain_status_model = "نعم (يُحتمل)" if prediction == 1 else "لا (غير محتمل)"
    
    # حالة المطر الفعلية (الحالية)
    rain_status_current = "نعم" if 'rain' in weather_main.lower() or 'drizzle' in weather_main.lower() else "لا"
    
    # طباعة النتائج
    print("-" * 50)
    print(f"✅ تفاصيل الطقس الحالي في {data.get('name', 'الموقع المحدد')}:")
    print(f"   - الحرارة: {temp}°C، الرطوبة: {humidity}%")
    print(f"   - الغيوم: {clouds}%، الرياح: {wind_speed} m/s")
    print(f"   - حالة الطقس الفعلية (الآن): {weather_main} ({rain_status_current})")
    print("-" * 50)
    print(f"   - **تنبؤ الموديل بالمطر:** {rain_status_model}")
    print("-" * 50)

except requests.exceptions.Timeout:
    print(f"❌ فشل جلب البيانات: انتهت المهلة (30 ثانية). تأكد من استقرار اتصالك بالإنترنت.")
except requests.exceptions.RequestException as e:
    print(f"❌ فشل جلب البيانات. الخطأ: {e}")