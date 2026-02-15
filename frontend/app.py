import streamlit as st
import requests

# Config
API_URL = "http://127.0.0.1:8000/api/predict"

st.set_page_config(page_title="AI Pricing Predictor", layout="centered")

st.title("💰 AI Product Pricing Predictor")
st.markdown("Predict optimal product price using AI")


# Input Form
with st.form("pricing_form"):
    product_name = st.text_input("Product Name", "Low Fat Milk")

    weight = st.number_input("Weight (kg)", min_value=0.1, value=1.0)

    fat_content = st.selectbox(
        "Fat Content", ["Low Fat", "Regular"]
    )

    product_type = st.text_input("Product Type", "Dairy")

    outlet_type = st.selectbox(
        "Outlet Type",
        ["Supermarket Type1", "Supermarket Type2", "Grocery Store"]
    )

    outlet_size = st.selectbox(
        "Outlet Size", ["Small", "Medium", "High"]
    )

    location_type = st.selectbox(
        "Location Type", ["Tier 1", "Tier 2", "Tier 3"]
    )

    establishment_year = st.number_input(
        "Outlet Establishment Year", min_value=1950, value=2005
    )

    visibility = st.number_input(
        "Product Visibility", min_value=0.0, value=0.03
    )

    submitted = st.form_submit_button("Predict Price")


# API Call
if submitted:
    payload = {
        "product_name": product_name,
        "weight": weight,
        "fat_content": fat_content,
        "product_type": product_type,
        "outlet_type": outlet_type,
        "outlet_size": outlet_size,
        "location_type": location_type,
        "establishment_year": establishment_year,
        "visibility": visibility
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success(f"💸 Predicted Price: ₹ {result['predicted_price']}")
            st.caption(f"Confidence: {result['confidence']}")
        else:
            st.error("Prediction failed. Please try again.")

    except Exception as e:
        st.error("Backend not reachable. Is FastAPI running?")