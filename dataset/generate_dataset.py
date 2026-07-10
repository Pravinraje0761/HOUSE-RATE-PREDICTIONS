"""
House Price Prediction System - Synthetic Dataset Generator
This script generates a realistic synthetic dataset for house price prediction.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Number of records
n_records = 2500

# Generate House_ID
house_ids = [f"H{i:04d}" for i in range(1, n_records + 1)]

# Generate Area (Square Feet) - Realistic range: 500 to 5000 sq ft
area = np.random.randint(500, 5000, n_records)

# Generate Location - Different neighborhoods with different price ranges
locations = ['Downtown', 'Suburban', 'Urban', 'Rural', 'Coastal']
location = np.random.choice(locations, n_records, p=[0.2, 0.3, 0.25, 0.15, 0.1])

# Generate City
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego']
city = np.random.choice(cities, n_records)

# Generate Number of Bedrooms - 1 to 6
bedrooms = np.random.randint(1, 7, n_records)

# Generate Number of Bathrooms - 1 to 5
bathrooms = np.random.randint(1, 6, n_records)

# Generate Number of Floors - 1 to 4
floors = np.random.randint(1, 5, n_records)

# Generate Parking - 0 to 3
parking = np.random.randint(0, 4, n_records)

# Generate Age of House - 0 to 50 years
age = np.random.randint(0, 51, n_records)

# Generate Furnishing Status
furnishing = np.random.choice(['Furnished', 'Semi-Furnished', 'Unfurnished'], n_records, p=[0.3, 0.4, 0.3])

# Generate Distance to City Center (km) - 1 to 50 km
distance_city = np.random.uniform(1, 50, n_records)

# Generate Nearby Schools - count within 5km radius
nearby_schools = np.random.randint(0, 10, n_records)

# Generate Nearby Hospitals - count within 5km radius
nearby_hospitals = np.random.randint(0, 8, n_records)

# Generate Crime Rate - Low, Medium, High
crime_rate = np.random.choice(['Low', 'Medium', 'High'], n_records, p=[0.4, 0.35, 0.25])

# Generate Property Type
property_type = np.random.choice(['Apartment', 'House', 'Villa', 'Condo', 'Townhouse'], n_records, p=[0.35, 0.3, 0.1, 0.15, 0.1])

# Create DataFrame
df = pd.DataFrame({
    'House_ID': house_ids,
    'Area': area,
    'Location': location,
    'City': city,
    'Number_of_Bedrooms': bedrooms,
    'Number_of_Bathrooms': bathrooms,
    'Number_of_Floors': floors,
    'Parking': parking,
    'Age_of_House': age,
    'Furnishing_Status': furnishing,
    'Distance_to_City_Center': distance_city,
    'Nearby_Schools': nearby_schools,
    'Nearby_Hospitals': nearby_hospitals,
    'Crime_Rate': crime_rate,
    'Property_Type': property_type
})

# Calculate Price based on features with some randomness
# Base price calculation
base_price = 50000  # Base price

# Area contribution ($100-200 per sq ft based on location)
location_multiplier = {'Downtown': 200, 'Suburban': 150, 'Urban': 160, 'Rural': 100, 'Coastal': 180}
price = base_price + df['Area'] * df['Location'].map(location_multiplier)

# Bedroom contribution
price += df['Number_of_Bedrooms'] * 25000

# Bathroom contribution
price += df['Number_of_Bathrooms'] * 15000

# Floor contribution
price += df['Number_of_Floors'] * 20000

# Parking contribution
price += df['Parking'] * 10000

# Age depreciation (houses lose value with age)
price -= df['Age_of_House'] * 500

# Furnishing contribution
furnishing_multiplier = {'Furnished': 50000, 'Semi-Furnished': 25000, 'Unfurnished': 0}
price += df['Furnishing_Status'].map(furnishing_multiplier)

# Distance to city center (closer is more expensive)
price -= df['Distance_to_City_Center'] * 1000

# Nearby amenities contribution
price += df['Nearby_Schools'] * 5000
price += df['Nearby_Hospitals'] * 3000

# Crime rate penalty
crime_penalty = {'Low': 0, 'Medium': -20000, 'High': -50000}
price += df['Crime_Rate'].map(crime_penalty)

# Property type contribution
property_multiplier = {'Apartment': 0, 'House': 30000, 'Villa': 100000, 'Condo': 20000, 'Townhouse': 40000}
price += df['Property_Type'].map(property_multiplier)

# Add random variation (+/- 15%)
random_variation = np.random.uniform(0.85, 1.15, n_records)
price = price * random_variation

# Ensure price is positive and realistic
price = np.maximum(price, 50000)  # Minimum price $50,000

# Round price to nearest 100
price = np.round(price / 100) * 100

# Add Price column
df['Price'] = price.astype(int)

# Introduce some missing values for preprocessing practice
# Randomly set 2-5% of values to NaN for some columns
missing_cols = ['Area', 'Number_of_Bedrooms', 'Number_of_Bathrooms', 'Parking', 'Age_of_House', 
                'Furnishing_Status', 'Distance_to_City_Center', 'Nearby_Schools']

for col in missing_cols:
    missing_indices = np.random.choice(df.index, size=int(len(df) * np.random.uniform(0.02, 0.05)), replace=False)
    df.loc[missing_indices, col] = np.nan

# Introduce some duplicates (about 1%)
duplicate_indices = np.random.choice(df.index, size=int(len(df) * 0.01), replace=False)
duplicates = df.loc[duplicate_indices]
df = pd.concat([df, duplicates], ignore_index=True)

# Save to CSV
output_path = 'house_data.csv'
df.to_csv(output_path, index=False)

print(f"Dataset generated successfully!")
print(f"Total records: {len(df)}")
print(f"Saved to: {output_path}")
print(f"\nDataset Info:")
print(df.info())
print(f"\nStatistical Summary:")
print(df.describe())
print(f"\nMissing Values:")
print(df.isnull().sum())
print(f"\nFirst 5 rows:")
print(df.head())
