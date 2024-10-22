import streamlit as st
import pandas as pd
import joblib
from stens import EnsembleModel

# Load the ensemble model
ensemble_model = joblib.load('ensemble_model.pkl')

# Custom CSS for enhanced styling with dark theme
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }
    .css-18e3th9 {
        padding: 0rem 0rem 10rem;
    }
    .stApp {
        background-color: #121212;
    }
    .title {
        color: #00bcd4;
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .description {
        color: #b0bec5;
        font-size: 18px;
        text-align: center;
        margin-bottom: 2em;
    }
    .input-title {
        font-size: 22px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    .input-container {
        background-color: #424242;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stButton>button {
        background-color: #00bcd4;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #008c9e;
        color: white;
    }
    .navbar {
        display: flex;
        justify-content: space-around;
        background-color: #00bcd4;
        padding: 1em;
        margin-bottom: 2em;
        border-radius: 10px;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        font-size: 20px;
        font-weight: bold;
    }
    .navbar a:hover {
        color: #f0f2f6;
    }
    .section-header {
        font-size: 28px;
        font-weight: bold;
        color: #00bcd4;
        text-align: center;
        margin-bottom: 1em;
    }
    .about-container {
        padding: 20px;
        background-color: #424242;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .about-container p {
        font-size: 18px;
        color: #b0bec5;
        margin-bottom: 1em;
    }
    .image-container {
        text-align: center;
        margin-bottom: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# Function to handle navigation
def main():
    # Navbar
    st.markdown("""
        <div class="navbar">
            <a href="?page=home">Home</a>
            <a href="?page=disease">Disease Details</a>
            <a href="?page=breed">Breed Details</a>
            <a href="?page=conditions">Conditions</a>
            <a href="?page=about">About Us</a>
        </div>
    """, unsafe_allow_html=True)

    # Get the page query parameter to determine which page to show
    page = st.experimental_get_query_params().get("page", ["home"])[0]

    # Route based on selected page
    if page == "home":
        show_home()
    elif page == "disease":
        show_disease_details()
    elif page == "breed":
        show_breed_details()
    elif page == "conditions":
        show_conditions()
    elif page == "about":
        show_about_us()

# Home Page: Prediction Form
def show_home():
    st.image('arecimg.jpg')  # Adjust path accordingly
    st.markdown("<h1 class='title'>Microbial Insights: Leveraging Soil Health for Predictive Crop Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p class='description'>Predict the yield of Arecanut trees using microbial, nutritional, and environmental data.</p>", unsafe_allow_html=True)

    # Input fields
    st.markdown("<div class='input-title'>Soil and Crop Information</div>", unsafe_allow_html=True)
    variety = st.selectbox("Choose a variety", ['Mangala', 'SK Local', 'Sumangala', 'Shreemangala'], key="variety")
    soil_ph = st.number_input("Soil pH", min_value=4.0, max_value=9.0, step=0.1, key="soil_ph")

    # Nutrient Inputs
    st.markdown("<div class='input-title'>Nient Levels</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    nitrogen = st.number_input("Nitrogen (N)", min_value=0, value=100, key="nitrogen")
    phosphorus = st.number_input("Phosphorus (P)", min_value=0, value=50, key="phosphorus")
    potassium = st.number_input("Potassium (K)", min_value=0, value=150, key="potassium")
    st.markdown("</div>", unsafe_allow_html=True)

    # Organic Matter and Microbes
    st.markdown("<div class='input-title'>Organic Matter and Microbes</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    organic_matter = st.number_input("Organic Matter (kg compost)", min_value=0.0, step=0.1, key="organic_matter")
    beneficial_microbes = st.number_input("Beneficial Microbes (10^7 CFU/g)", min_value=0.0, step=0.1, key="beneficial_microbes")
    harmful_microbes = st.number_input("Harmful Microbes (10^5 CFU/g)", min_value=0.0, step=0.1, key="harmful_microbes")
    st.markdown("</div>", unsafe_allow_html=True)

    # Other Inputs
    microbial_biomass = st.number_input("Microbial Biomass C (g/kg)", min_value=0.0, value=330.0, step=0.1, key="microbial_biomass")
    soil_organic_carbon = st.number_input("Soil Organic Carbon (%)", min_value=0.0, max_value=100.0, step=0.1, key="soil_organic_carbon")
    microbial_activity = st.radio("Microbial Activity", ['High', 'Moderate', 'Low'], key="microbial_activity")
    soil_enzyme_activity = st.radio("Soil Enzyme Activity", ['High', 'Moderate', 'Low'], key="soil_enzyme_activity")

    # Disease and Deficiency
    disease_present = st.radio("Is there any disease?", ['No', 'Yes'], key="disease_present")
    if disease_present == 'Yes':
        disease_name = st.selectbox("Select Disease", ['Koleroga (Mahali)', 'Spindle Bug'], key="disease_name")
    nutrient_deficiency = st.radio("Is there any nutrient deficiency?", ['No', 'Yes'], key="nutrient_deficiency")
    if nutrient_deficiency == 'Yes':
        nutrient_deficiency_name = st.selectbox("Select Nutrient Deficiency", ['Nitrogen Deficiency', 'Phosphorus Deficiency', 'Potassium Deficiency'], key="nutrient_deficiency_name")

    # Submit button for prediction
    if st.button('Predict Crop Yield'):
        input_data = {
            'Variety_Mangala': [1 if variety == 'Mangala' else 0],
            'Variety_SK Local': [1 if variety == 'SK Local' else 0],
            'Variety_Sumangala': [1 if variety == 'Sumangala' else 0],
            'Variety_Shreemangala': [1 if variety == 'Shreemangala' else 0],
            'Soil_pH': [soil_ph],
            'N (Nitrogen)': [nitrogen],
            'P (Phosphorus)': [phosphorus],
            'K (Potassium)': [potassium],
            'Organic_Matter (kg compost)': [organic_matter],
            'Beneficial_Microbes (CFU/g)': [beneficial_microbes * 1e7],
            'Harmful_Microbes (CFU/g)': [harmful_microbes * 1e5],
            'Microbial_Biomass_C (g/kg)': [microbial_biomass],
            'Soil_Organic_Carbon': [soil_organic_carbon / 100],
            'Microbial_Activity_High': [1 if microbial_activity == 'High' else 0],
            'Soil_Enzyme_Activity_High': [1 if soil_enzyme_activity == 'High' else 0],
            'Disease (Yes/No)': [1 if disease_present == 'Yes' else 0],
            'Disease_Name_Koleroga (Mahali)': [1 if disease_present == 'Yes' and disease_name == 'Koleroga (Mahali)' else 0],
            'Disease_Name_Spindle Bug': [1 if disease_present == 'Yes' and disease_name == 'Spindle Bug' else 0],
            'Nutrient_Deficiency (Yes/No)_Yes': [1 if nutrient_deficiency == 'Yes' else 0],
            'Nutrient_Deficiency_Nitrogen': [1 if nutrient_deficiency == 'Yes' and nutrient_deficiency_name == 'Nitrogen Deficiency' else 0],
            'Nutrient_Deficiency_Phosphorus': [1 if nutrient_deficiency == 'Yes' and nutrient_deficiency_name == 'Phosphorus Deficiency' else 0],
            'Nutrient_Deficiency_Potassium': [1 if nutrient_deficiency == 'Yes' and nutrient_deficiency_name == 'Potassium Deficiency' else 0],
        }

        input_df = pd.DataFrame(input_data)

        # Predict crop yield
        prediction = ensemble_model.predict(input_df)

        # Display the result
        st.markdown(f"<div class='prediction-result'>Predicted Crop Yield: {prediction[0]:.2f} kg/palm</div>", unsafe_allow_html=True)

# Disease Details Page
def show_disease_details():
    st.markdown("<h1 class='section-header'>Disease Details</h1>", unsafe_allow_html=True)
    st.image('Koleroga.jpg', caption='Koleroga (Mahali) - Symptoms include wilting and yellowing of leaves.')  # Adjust path accordingly
    st.image('Spindle Bug.jpg', caption='Spindle Bug - This pest damages the Arecanut crop by sucking sap from leaves.')  # Adjust path accordingly
    st.markdown("""
        <div class='about-container'>
        <p><strong>Koleroga (Mahali):</strong> A serious disease affecting Arecanut palms, leading to severe yield loss.</p>
        <p><strong>Spindle Bug:</strong> This pest damages the Arecanut crop by sucking sap from leaves, affecting overall health and yield.</p>
        </div>
    """, unsafe_allow_html=True)

# Breed Details Page
def show_breed_details():
    st.markdown("<h1 class='section-header'>Breed Details</h1>", unsafe_allow_html=True)
    st.image('Mangala.jpg', caption='Mangala - A high-yielding variety known for its resilience against diseases.')  # Adjust path accordingly
    st.image('SK Local.jpg', caption='SK Local - A local variety with a lower yield compared to Mangala.')  # Adjust path accordingly
    st.image('Sumangala.jpg', caption='Sumangala - An emerging variety with favorable traits.')  # Adjust path accordingly
    st.image('Shreemangala.jpg', caption='Shreemangala - A traditional variety valued for its flavor.')  # Adjust path accordingly
    st.markdown("""
        <div class='about-container'>
        <p>The following varieties of Arecanut are commonly cultivated:</p>
        </div>
    """, unsafe_allow_html=True)

# Conditions Page
def show_conditions():
    st.markdown("<h1 class='section-header'>Conditions Affecting Yield</h1>", unsafe_allow_html=True)
    st.image('arecimg.jpg', caption='Factors affecting Arecanut yield.')  # Adjust path accordingly
    st.markdown("""
        <div class='about-container'>
        <p>The yield of Arecanut is influenced by several factors including:</p>
        <ul>
            <li><strong>Soil Health:</strong> Nutrient levels and pH affect plant growth.</li>
            <li><strong>Microbial Activity:</strong> Beneficial microbes enhance soil fertility.</li>
            <li><strong>Disease Presence:</strong> Diseases can drastically reduce yield.</li>
            <li><strong>Weather Conditions:</strong> Adequate rainfall and temperature are crucial.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

# About Us Page
def show_about_us():
    st.markdown("<h1 class='section-header'>About Us</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class='about-container'>
        <p>We are dedicated to advancing agricultural practices through data science. Our goal is to empower farmers with predictive insights for better crop management.</p>
        <p>Our team combines expertise in machine learning, soil science, and agronomy to create models that predict crop yield based on various soil and environmental factors.</p>
        </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
