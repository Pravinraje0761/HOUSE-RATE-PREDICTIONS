# House Price Prediction System

[![CI](https://github.com/Pravinraje0761/HOUSE-RATE-PREDICTIONS/actions/workflows/ci.yml/badge.svg)](https://github.com/Pravinraje0761/HOUSE-RATE-PREDICTIONS/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A complete end-to-end Machine Learning project for predicting house prices using regression algorithms.

## 📋 Project Overview

### Problem Statement
Predict the selling price of a house based on various features such as area, location, number of bedrooms, bathrooms, parking, age of the house, and amenities using Regression algorithms.

### Objectives
- Build a machine learning model to predict house prices accurately
- Perform comprehensive exploratory data analysis
- Engineer meaningful features to improve prediction
- Compare multiple regression algorithms
- Deploy an interactive web application for predictions

## 🎯 Technologies Used

- **Python**: Primary programming language
- **Jupyter Notebook**: Interactive development environment
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical data visualization
- **Scikit-Learn**: Machine learning library
- **Joblib**: Model persistence
- **Streamlit**: Web application framework

## 🤖 Algorithms Used

1. **Linear Regression**: Simple, interpretable baseline model
2. **Decision Tree Regressor**: Non-linear relationship capture
3. **Random Forest Regressor**: Ensemble method (best performer)

## 📊 Dataset Description

### Dataset Features
- **House_ID**: Unique identifier for each house
- **Area**: Area in square feet (500-5000 sq ft)
- **Location**: Location type (Downtown, Suburban, Urban, Rural, Coastal)
- **City**: City name (8 major US cities)
- **Number_of_Bedrooms**: Number of bedrooms (1-6)
- **Number_of_Bathrooms**: Number of bathrooms (1-5)
- **Number_of_Floors**: Number of floors (1-4)
- **Parking**: Number of parking spaces (0-3)
- **Age_of_House**: Age of house in years (0-50)
- **Furnishing_Status**: Furnishing status (Furnished, Semi-Furnished, Unfurnished)
- **Distance_to_City_Center**: Distance to city center in km (1-50 km)
- **Nearby_Schools**: Number of nearby schools (0-10)
- **Nearby_Hospitals**: Number of nearby hospitals (0-8)
- **Crime_Rate**: Crime rate (Low, Medium, High)
- **Property_Type**: Property type (Apartment, House, Villa, Condo, Townhouse)
- **Price**: Target variable - House price in dollars

### Dataset Statistics
- **Total Records**: 2,525 houses
- **Features**: 16 columns (15 features + 1 target)
- **Missing Values**: Handled during preprocessing
- **Price Range**: $214,400 - $1,624,400

## 🔄 Project Workflow

### Part 1: Data Loading
- Load dataset using Pandas
- Display first/last rows
- Dataset information and statistics
- Check for missing values

### Part 2: Data Preprocessing
- Handle missing values (median/mode imputation)
- Remove duplicate records
- Detect and remove outliers (IQR method)
- Encode categorical variables (Label & One-Hot Encoding)
- Feature scaling using StandardScaler

### Part 3: Exploratory Data Analysis (EDA)
- Histograms (Price, Area)
- Boxplots (Price, Area)
- Countplots (Property Types, Locations)
- Scatter plots (Area vs Price, Bedrooms vs Price, etc.)
- Correlation heatmap
- Violin plots
- Distribution plots

### Part 4: Feature Engineering
- Price per Square Foot
- Total Rooms
- Luxury Score (0-100)
- Accessibility Score (0-100)
- House Age Category
- Location Popularity Score (0-100)

### Part 5: Feature Selection
- Correlation analysis with target
- Remove highly correlated features
- Select features with |correlation| > 0.1

### Part 6: Train-Test Split
- 80% training data, 20% testing data
- Random state = 42 for reproducibility

### Part 7: Machine Learning Models
- Train Linear Regression
- Train Decision Tree Regressor
- Train Random Forest Regressor
- Compare model performance

### Part 8: Model Evaluation
- Actual vs Predicted plots
- Residual plots
- Feature importance graphs
- Prediction error distribution

### Part 9: Model Saving
- Save trained model using Joblib
- Save scaler for preprocessing
- Save feature names

### Part 10: User Prediction System
- Interactive prediction function
- Accepts user input features
- Returns predicted house price

### Part 11: Streamlit Web Application
- Beautiful UI with sidebar inputs
- Real-time price prediction
- Feature importance visualization
- Bulk CSV upload support

### Part 12: Bonus Features
- Hyperparameter tuning using GridSearchCV
- Cross-validation for robust evaluation
- Model comparison dashboard

## 📁 Project Structure

```
House_Price_Prediction/
│
├── dataset/
│   ├── generate_dataset.py
│   └── house_data.csv
│
├── notebooks/
│   └── House_Price_Prediction.ipynb
│
├── models/
│   ├── house_price_model.pkl
│   ├── house_price_model_tuned.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
│
├── app.py
├── requirements.txt
├── README.md
├── report.md
├── presentation.md
└── viva_questions.md
```

## 🚀 Installation Steps

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Project
```bash
git clone https://github.com/Pravinraje0761/HOUSE-RATE-PREDICTIONS.git
cd HOUSE-RATE-PREDICTIONS
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Dataset (if not already generated)
```bash
cd dataset
python generate_dataset.py
cd ..
```

### Step 5: Train the Model
```bash
python train.py      # trains and compares three models, saves the best to models/
```

The notebook (`notebooks/House_Price_Prediction.ipynb`) walks through the same analysis
step by step with plots; run `train.py` first, since its prediction examples use the saved model.

### Step 6: Run Streamlit App
```bash
streamlit run app.py
```

## 📈 Results

Measured by `python train.py` (80/20 split, seed 42; 5-fold CV on the training split). All
preprocessing is fitted on the training split only.

| Model | Test R² | MAE ($) | RMSE ($) | CV R² |
|-------|--------:|--------:|---------:|------:|
| Linear Regression | 0.866 | 67,296 | 87,092 | 0.864 ± 0.018 |
| Decision Tree | 0.683 | 100,779 | 133,792 | 0.662 ± 0.018 |
| Random Forest | 0.847 | 71,641 | 92,877 | 0.840 ± 0.019 |

**Linear regression is selected** (best cross-validated R²), explaining about 87% of the variance
in held-out prices, with a typical error of about $67,000.

### Correction

Earlier versions of this README reported R² 0.95+ for a random forest. Those figures are
withdrawn. The notebook used `Price_per_SqFt` (price ÷ area) as an input feature, which gives
the model the answer, and the app could not supply it at prediction time. Without it, the best
R² is about 0.87.

### Key findings
- Area is the strongest predictor of price.
- Location and property type shift prices substantially.
- On this dataset, a linear model matches or beats tree ensembles, which is consistent with how
  `dataset/generate_dataset.py` builds prices (a near-linear formula plus noise).

> **The data is synthetic.** Prices are generated from the features by a formula with random
> noise, so these results show the workflow, not real-estate predictive skill.

## 🧪 Tests

```bash
python train.py && pytest
```

Tests check that no input feature is derived from the price, that held-out R² is sensible
(and not suspiciously high), that predictions respond to area, that missing values are handled,
and that the Streamlit app predicts without errors. CI runs them on every push.

## 🔮 Future Scope

1. **Additional Features**
   - Include more geographical features (zip code, neighborhood)
   - Add economic indicators (interest rates, inflation)
   - Include seasonal trends in real estate market

2. **Model Improvements**
   - Try advanced algorithms (XGBoost, LightGBM, Neural Networks)
   - Implement deep learning models
   - Use ensemble methods with stacking

3. **Application Enhancements**
   - Add user authentication
   - Implement real-time data updates
   - Create mobile application
   - Add price trend analysis over time

4. **Deployment**
   - Deploy to cloud platforms (AWS, GCP, Azure)
   - Create REST API for predictions
   - Implement model monitoring and retraining pipeline

## 👨‍💻 Author

This project was developed as a final-year college mini project demonstrating practical application of machine learning in real estate domain.

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🙏 Acknowledgments

- Scikit-Learn documentation
- Streamlit documentation
- Real estate domain knowledge resources

---

**Note**: This project uses synthetic data for demonstration purposes. For real-world applications, use actual real estate data from reliable sources.
