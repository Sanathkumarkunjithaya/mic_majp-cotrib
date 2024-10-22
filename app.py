import streamlit as st
import numpy as np
import pandas as pd
import joblib
from stens import EnsembleModel

# Load the ensemble model
ensemble_model = joblib.load('ensemble_model.pkl')

st.image('arecimg.jpg')  # Adjust path accordingly

# Title and description
st.title("Microbial Insights: Leveraging Soil Health for Predictive Crop Analytics")
st.write("Predict the yield of Arecanut trees using microbial, nutritional, and environmental data.")

# Input fields
variety = st.selectbox("Choose a variety", ['Mangala', 'SK Local', 'Sumangala', 'Shreemangala'])
soil_ph = st.number_input("Soil pH", min_value=4.0, max_value=9.0, step=0.1)

# Nutrients
nitrogen = st.number_input("Nitrogen (N)", min_value=0, value=100)
phosphorus = st.number_input("Phosphorus (P)", min_value=0, value=50)
potassium = st.number_input("Potassium (K)", min_value=0, value=150)

# Organic Matter
organic_matter = st.number_input("Organic Matter (kg compost)", min_value=0.0, step=0.1)

# Microbes with 10^ scale
beneficial_microbes_scale = st.radio("Beneficial Microbes (CFU/g) Scale", ['10^7', '10^8', '10^9'])
beneficial_microbes = st.number_input(f"Beneficial Microbes ({beneficial_microbes_scale} CFU/g)", min_value=0.0, step=0.1)
beneficial_microbes = beneficial_microbes * (10 ** int(beneficial_microbes_scale[-1]))

harmful_microbes_scale = st.radio("Harmful Microbes (CFU/g) Scale", ['0', '10^5'])
if harmful_microbes_scale == '0':
    harmful_microbes = 0
else:
    harmful_microbes = st.number_input(f"Harmful Microbes ({harmful_microbes_scale} CFU/g)", min_value=0.0, step=0.1)
    harmful_microbes = harmful_microbes * (10 ** 5)

# Microbial Biomass and Soil Organic Carbon
microbial_biomass = st.number_input("Microbial Biomass C (g/kg)", min_value=0.0, value=330.0, step=0.1)
soil_organic_carbon = st.number_input("Soil Organic Carbon (%)", min_value=0.0, max_value=100.0, step=0.1)

# Microbial Activity and Soil Enzyme Activity
microbial_activity = st.radio("Microbial Activity", ['High', 'Moderate', 'Low'])
soil_enzyme_activity = st.radio("Soil Enzyme Activity", ['High', 'Moderate', 'Low'])

# Disease and Nutrition Deficiency
disease_present = st.radio("Is there any disease?", ['No', 'Yes'])
if disease_present == 'Yes':
    disease_name = st.selectbox("Select Disease", ['Koleroga (Mahali)', 'Spindle Bug'])

nutrient_deficiency = st.radio("Is there any nutrient deficiency?", ['No', 'Yes'])
if nutrient_deficiency == 'Yes':
    nutrient_deficiency_name = st.selectbox("Select Nutrient Deficiency", ['Nitrogen Deficiency', 'Phosphorus Deficiency', 'Potassium Deficiency'])

# Submit button
if st.button('Predict Crop Yield'):
    # Create a DataFrame with the input values
    input_data = {
        'Variety_Mangala': [1 if variety == 'Mangala' else 0],
        'Variety_SK Local': [1 if variety == 'SK Local' else 0],
        'Variety_Shreemangala': [1 if variety == 'Shreemangala' else 0],
        'Variety_Sumangala': [1 if variety == 'Sumangala' else 0],
        'Soil_pH': [soil_ph],
        'N (Nitrogen)': [nitrogen],
        'P (Phosphorus)': [phosphorus],
        'K (Potassium)': [potassium],
        'Organic_Matter (kg compost)': [organic_matter],
        'Beneficial_Microbes (CFU/g)': [beneficial_microbes],
        'Harmful_Microbes (CFU/g)': [harmful_microbes],
        'Microbial_Biomass_C (g/kg)': [microbial_biomass],
        'Soil_Organic_Carbon': [soil_organic_carbon / 100],  # Convert percentage to fraction
        'Microbial_Activity_High': [1 if microbial_activity == 'High' else 0],
        'Microbial_Activity_Moderate': [1 if microbial_activity == 'Moderate' else 0],
        'Microbial_Activity_Low': [1 if microbial_activity == 'Low' else 0],
        'Soil_Enzyme_Activity_High': [1 if soil_enzyme_activity == 'High' else 0],
        'Soil_Enzyme_Activity_Moderate': [1 if soil_enzyme_activity == 'Moderate' else 0],
        'Soil_Enzyme_Activity_Low': [1 if soil_enzyme_activity == 'Low' else 0],
        'Disease (Yes/No)_Yes': [1 if disease_present == 'Yes' else 0],
        'Disease_Name_Koleroga': [1 if disease_present == 'Yes' and disease_name == 'Koleroga (Mahali)' else 0],
        'Disease_Name_Spindle Bug': [1 if disease_present == 'Yes' and disease_name == 'Spindle Bug' else 0],
        'Nutrient_Deficiency_Nitrogen': [1 if nutrient_deficiency == 'Yes' and nutrient_deficiency_name == 'Nitrogen Deficiency' else 0],
        'Nutrient_Deficiency_Phosphorus': [1 if nutrient_deficiency == 'Yes' and nutrient_deficiency_name == 'Phosphorus Deficiency' else 0],
        'Nutrient_Deficiency_Potassium': [1 if nutrient_deficiency == 'Yes' and nutrient_deficiency_name == 'Potassium Deficiency' else 0],
        'Weather_Condition_Humid': [1],
        'Weather_Condition_Dry': [0],
        'Weather_Condition_Rainy': [0]
    }

    # Convert input_data to a DataFrame and align with training columns
    input_df = pd.DataFrame(input_data)
    input_df = input_df.reindex(columns=ensemble_model.scaler.feature_names_in_, fill_value=0)

    # Scale the input using the same scaler
    input_scaled = ensemble_model.scaler.transform(input_df)

    # Predict the crop yield using the ensemble model
    yield_prediction = ensemble_model.predict(input_df)

    # Display the prediction result
    st.success(f"Predicted Crop Yield: {yield_prediction[0]:.2f} kg/palm")
