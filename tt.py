import os
import numpy as np
import pickle
import tensorflow as tf
import streamlit as st

# Load models
model_path = r'C:\Jaris\College\Projects\AI Heart Attack Detection\path_to_save\heart_model.pkl'
scaler_path = r'C:\Jaris\College\Projects\AI Heart Attack Detection\path_to_save\heart_scaler.pkl'
image_model_path = r'C:\Jaris\College\Projects\AI Heart Attack Detection\path_to_your_model\heart_ecg_model.keras'

with open(model_path, 'rb') as f:
    heart_model = pickle.load(f)
with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)
image_model = tf.keras.models.load_model(image_model_path)

# ECG preprocessing
def preprocess_image(uploaded_file):
    try:
        img = tf.keras.preprocessing.image.load_img(uploaded_file, target_size=(200, 200))
        img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
        return np.expand_dims(img_array, axis=0)
    except Exception as e:
        st.error(f"Image preprocessing error: {e}")
        return None

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Risk Prediction", "📊 Patient Analysis (Power BI)"])

# Page 1: Prediction
if page == "🏠 Risk Prediction":
    st.title("🫀 Heart Attack Risk Prediction App")
    st.markdown("This app uses clinical and ECG data to assess heart attack risk.")

    st.sidebar.header("🧾 Enter Clinical Data")
    ldl = st.sidebar.number_input("LDL (mg/dL)", 0, 300)
    systolic = st.sidebar.number_input("Systolic Blood Pressure", 80, 200)
    diastolic = st.sidebar.number_input("Diastolic Blood Pressure", 40, 130)
    smoking = st.sidebar.number_input("Smoking (Cigarettes/day)", 0, 60)
    hdl = st.sidebar.number_input("HDL (mg/dL)", 10, 100)
    bmi = st.sidebar.number_input("BMI (kg/m²)", 10.0, 50.0)
    fasting_sugar = st.sidebar.number_input("Fasting Blood Sugar (mg/dL)", 50, 300)
    diet = st.sidebar.selectbox("Diet", [0, 1], format_func=lambda x: "Vegetarian" if x == 0 else "Non-Vegetarian")
    age = st.sidebar.number_input("Age", 18, 100)
    sex = st.sidebar.selectbox("Sex", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male")

    uploaded_file = st.sidebar.file_uploader("📷 Upload ECG Image", type=["jpg", "jpeg", "png"])

    if st.sidebar.button("🧠 Predict Risk"):
        features = np.array([[ldl, systolic, diastolic, smoking, hdl, bmi,
                              fasting_sugar, diet, age, sex]])
        try:
            scaled = scaler.transform(features)
            clinical_pred = heart_model.predict(scaled)[0]
        except Exception as e:
            st.error(f"❌ Error during clinical prediction: {e}")
            st.stop()

        image_label = "Not Provided"
        if uploaded_file:
            img_array = preprocess_image(uploaded_file)
            if img_array is not None:
                prediction = image_model.predict(img_array)
                class_names = ['Myocardial Infarction', 'Abnormal Heartbeat', 'History of MI', 'Normal']
                class_index = np.argmax(prediction)
                image_label = class_names[class_index]
                st.write(f"🩺 ECG Prediction: **{image_label}**")
        else:
            st.warning("⚠️ No ECG image uploaded. Prediction based only on clinical data.")

        # Final Risk Assessment
        if clinical_pred == 0 and image_label == 'Normal':
            risk = "✅ Heart attack risk is **less than 10%**."
        elif clinical_pred == 1 and image_label in ['Normal', 'History of MI']:
            risk = "⚠️ Heart attack risk is **below 50%**."
        elif clinical_pred == 0 and image_label in ['Myocardial Infarction', 'Abnormal Heartbeat', 'History of MI']:
            risk = "⚠️ Heart attack risk is **below 50%**."
        elif clinical_pred == 1 and image_label in ['Myocardial Infarction', 'Abnormal Heartbeat']:
            risk = "🔴 Heart attack risk is **above 50%**."
        else:
            risk = "❓ Unable to determine risk."

        st.success(risk)

# Page 2: Power BI Dashboard
elif page == "📊 Patient Analysis (Power BI)":
    st.title("📊 Patient Data Insights - Power BI Dashboard")
    st.markdown("This dashboard provides detailed analysis of patient health records and heart attack trends.")

    # Power BI Embed (Use your real link here)
    st.markdown(
        """
        <iframe title="new" width="1140" height="541.25"
        src="https://app.powerbi.com/reportEmbed?reportId=4b5837a7-2ff3-4ef3-ba11-d25c3ee68f0f&autoAuth=true&ctid=085c606c-851a-4f29-9538-639c1a6f40ee"
        frameborder="0" allowFullScreen="true"></iframe>
        """,
        unsafe_allow_html=True
    )

