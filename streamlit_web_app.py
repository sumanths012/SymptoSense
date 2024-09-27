# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import pickle
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Diabetes Prediction Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Set up the main header for the application
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Diabetes Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>Predict whether you are at risk of diabetes using Machine Learning</h3>", unsafe_allow_html=True)

# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved diabetes model
diabetes_model = pickle.load(open(r'C:/Users/suman/OneDrive/Desktop/Assignments/My Resume/Final_Project/ProjectFiles/SavedModels/diabetes_model.sav', 'rb'))


# Create a centered container layout for the input form
with st.container():
    st.markdown("<h4 style='text-align: center;'>Please enter the following details:</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

# Space to separate input and button
st.markdown("<br>", unsafe_allow_html=True)

# Code for prediction
diab_diagnosis = ''

# Create a centered button for prediction
if st.button('Predict Diabetes Risk', key="diabetes_test"):
    user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]

    # Convert inputs to float
    user_input = [float(x) for x in user_input]

    # Make prediction using the loaded model
    diab_prediction = diabetes_model.predict([user_input])

    if diab_prediction[0] == 1:
        diab_diagnosis = 'The person is diabetic'
    else:
        diab_diagnosis = 'The person is not diabetic'

    # Display result in a prominent style
    st.markdown(f"<h3 style='text-align: center; color: red;'>{diab_diagnosis}</h3>", unsafe_allow_html=True)

# Add footer or additional design elements if necessary
st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by Machine Learning</p>", unsafe_allow_html=True)
