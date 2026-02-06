import streamlit as st
import numpy as np
import pickle

# Load trained model
model = pickle.load(open("best_model.pkl", "rb"))

st.title("📈 Sales Increase/Decrease Prediction App")

st.write("Enter Advertisement Spending Values:")

# Input fields
tv = st.number_input("TV Advertisement Budget", min_value=0.0)
radio = st.number_input("Radio Advertisement Budget", min_value=0.0)
newspaper = st.number_input("Newspaper Advertisement Budget", min_value=0.0)

# Prediction button
if st.button("Predict Sales Trend"):

    input_data = np.array([[tv, radio, newspaper]])

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success("✅ Sales Will Increase 📈")
    else:
        st.error("❌ Sales Will Decrease 📉")
