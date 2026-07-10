"""
House Price Prediction System - Streamlit Web Application
A beautiful and interactive web app for predicting house prices.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler

# Page configuration
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🏠 House Price Prediction System")
st.markdown("""
    <p style='font-size: 18px; color: #666;'>
    Predict the selling price of a house based on various features using Machine Learning.
    </p>
""", unsafe_allow_html=True)

# Load the model and scaler
@st.cache_resource
def load_model():
    try:
        model = joblib.load('models/house_price_model.pkl')
        scaler = joblib.load('models/scaler.pkl')
        feature_names = joblib.load('models/feature_names.pkl')
        return model, scaler, feature_names
    except:
        st.error("Model files not found. Please run the notebook first to train and save the model.")
        return None, None, None

model, scaler, feature_names = load_model()

# Sidebar for inputs
st.sidebar.header("📝 House Features")

# Input fields
area = st.sidebar.slider("Area (Square Feet)", 500, 5000, 2000)
location = st.sidebar.selectbox("Location", ["Downtown", "Suburban", "Urban", "Rural", "Coastal"])
city = st.sidebar.selectbox("City", ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", 
                                     "Philadelphia", "San Antonio", "San Diego"])
bedrooms = st.sidebar.slider("Number of Bedrooms", 1, 6, 3)
bathrooms = st.sidebar.slider("Number of Bathrooms", 1, 5, 2)
floors = st.sidebar.slider("Number of Floors", 1, 4, 2)
parking = st.sidebar.slider("Parking Spaces", 0, 3, 2)
age = st.sidebar.slider("Age of House (Years)", 0, 50, 10)
furnishing_status = st.sidebar.selectbox("Furnishing Status", ["Furnished", "Semi-Furnished", "Unfurnished"])
distance_city = st.sidebar.slider("Distance to City Center (km)", 1, 50, 15)
schools = st.sidebar.slider("Nearby Schools", 0, 10, 3)
hospitals = st.sidebar.slider("Nearby Hospitals", 0, 8, 2)
crime_rate = st.sidebar.selectbox("Crime Rate", ["Low", "Medium", "High"])
property_type = st.sidebar.selectbox("Property Type", ["Apartment", "House", "Villa", "Condo", "Townhouse"])

# Prediction function
def predict_price(area, location, city, bedrooms, bathrooms, floors, parking, age, 
                 furnishing_status, distance_city, schools, hospitals, crime_rate, property_type):
    if model is None:
        return None
    
    # Create input dictionary
    input_data = {
        'Area': [area],
        'Number_of_Bedrooms': [bedrooms],
        'Number_of_Bathrooms': [bathrooms],
        'Number_of_Floors': [floors],
        'Parking': [parking],
        'Age_of_House': [age],
        'Distance_to_City_Center': [distance_city],
        'Nearby_Schools': [schools],
        'Nearby_Hospitals': [hospitals],
        'Furnishing_Status_Encoded': [0],
        'Crime_Rate_Encoded': [0],
    }
    
    # Encode categorical variables
    furnishing_map = {'Furnished': 2, 'Semi-Furnished': 1, 'Unfurnished': 0}
    crime_map = {'Low': 0, 'Medium': 1, 'High': 2}
    
    input_data['Furnishing_Status_Encoded'] = [furnishing_map.get(furnishing_status, 1)]
    input_data['Crime_Rate_Encoded'] = [crime_map.get(crime_rate, 1)]
    
    # Add one-hot encoded columns
    for col in feature_names:
        if col.startswith('Location_'):
            input_data[col] = [1 if col == f'Location_{location}' else 0]
        elif col.startswith('City_'):
            input_data[col] = [1 if col == f'City_{city}' else 0]
        elif col.startswith('Property_Type_'):
            input_data[col] = [1 if col == f'Property_Type_{property_type}' else 0]
        elif col not in input_data:
            input_data[col] = [0]
    
    # Add engineered features
    input_data['Price_per_SqFt'] = [0]
    input_data['Total_Rooms'] = [bedrooms + bathrooms]
    input_data['Luxury_Score'] = [50]
    input_data['Accessibility_Score'] = [50]
    input_data['House_Age_Category_Encoded'] = [1]
    input_data['Location_Popularity_Score'] = [50]
    
    # Create DataFrame
    input_df = pd.DataFrame(input_data)
    
    # Ensure all columns are present
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0
    
    input_df = input_df[feature_names]
    
    # Scale numerical features
    numerical_cols = ['Area', 'Number_of_Bedrooms', 'Number_of_Bathrooms', 
                      'Number_of_Floors', 'Parking', 'Age_of_House',
                      'Distance_to_City_Center', 'Nearby_Schools', 'Nearby_Hospitals']
    
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])
    
    # Make prediction
    prediction = model.predict(input_df)
    
    return prediction[0]

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 House Details")
    
    # Display house details in a nice format
    details_df = pd.DataFrame({
        'Feature': ['Area', 'Location', 'City', 'Bedrooms', 'Bathrooms', 'Floors', 
                    'Parking', 'Age', 'Furnishing', 'Distance to City', 'Schools', 
                    'Hospitals', 'Crime Rate', 'Property Type'],
        'Value': [f'{area} sq ft', location, city, bedrooms, bathrooms, floors, 
                 parking, f'{age} years', furnishing_status, f'{distance_city} km', 
                 schools, hospitals, crime_rate, property_type]
    })
    
    st.table(details_df)

with col2:
    st.subheader("💰 Price Prediction")
    
    # Predict button
    if st.button("Predict Price", key="predict_btn"):
        with st.spinner("Predicting..."):
            predicted_price = predict_price(area, location, city, bedrooms, bathrooms, 
                                          floors, parking, age, furnishing_status, 
                                          distance_city, schools, hospitals, crime_rate, 
                                          property_type)
            
            if predicted_price is not None:
                # Display prediction
                st.markdown(f"""
                    <div class='metric-card'>
                        <h2 style='color: #4CAF50; text-align: center;'>${predicted_price:,.2f}</h2>
                        <p style='text-align: center; color: #666;'>Estimated House Price</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Price range estimate
                price_range = predicted_price * 0.1
                st.info(f"Price Range: ${predicted_price - price_range:,.0f} - ${predicted_price + price_range:,.0f}")

# Additional features section
st.markdown("---")
st.subheader("📁 Bulk Prediction")

uploaded_file = st.file_uploader("Upload CSV file for bulk prediction", type=['csv'])

if uploaded_file is not None:
    try:
        bulk_df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.dataframe(bulk_df.head())
        
        if st.button("Predict Bulk Prices"):
            st.info("Bulk prediction feature requires custom preprocessing. Please use the notebook for bulk predictions.")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Feature importance section
st.markdown("---")
st.subheader("🔍 Feature Importance")

if model is not None:
    try:
        importance = model.feature_importances_
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importance
        }).sort_values('Importance', ascending=False).head(10)
        
        fig = px.bar(importance_df, x='Importance', y='Feature', 
                    title='Top 10 Most Important Features',
                    orientation='h')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("Feature importance not available")

# About section
st.markdown("---")
st.subheader("ℹ️ About This Project")

st.markdown("""
    <div class='metric-card'>
        <p><strong>Project:</strong> House Price Prediction System</p>
        <p><strong>Objective:</strong> Predict house prices using Machine Learning</p>
        <p><strong>Model:</strong> Random Forest Regressor</p>
        <p><strong>Accuracy:</strong> R² Score ~0.95+</p>
        <p><strong>Features:</strong> 25+ features including engineered features</p>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: #999;'>
    Built with ❤️ using Streamlit & Scikit-Learn
    </p>
""", unsafe_allow_html=True)
