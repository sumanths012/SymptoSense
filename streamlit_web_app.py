import pickle
import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Set up pytesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set page configuration
st.set_page_config(page_title="Diabetes Prediction Assistant", layout="wide", page_icon="🧑‍⚕️")

# Load the saved diabetes model
diabetes_model = pickle.load(open(r'C:/Users/suman/OneDrive/Desktop/Assignments/My Resume/Final_Project/ProjectFiles/SavedModels/diabetes_model.sav', 'rb'))


# Function to process image and extract text
def process_image(image):
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text


# Function to parse extracted text and extract values
def parse_text(text, report_type):
    data = {'Glucose': None, 'Insulin': None}
    if report_type == 'glucose' and ('Glucose' in text or 'eAG' in text):
        data['Glucose'] = extract_value(text, 'Glucose', 'eAG')
    elif report_type == 'insulin' and ('Insulin' in text or 'C-PEPTIDE FASTING, SERUM' in text):
        data['Insulin'] = extract_value(text, 'Insulin', 'C-PEPTIDE FASTING, SERUM')
    return data


# Function to extract a specific value from the extracted text
def extract_value(text, *field_names):
    lines = text.splitlines()
    for line in lines:
        for field_name in field_names:
            if field_name in line:
                parts = line.split()
                for part in parts:
                    if part.replace('.', '', 1).isdigit():
                        return part
                break
    return None


# Header section
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Diabetes Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>Predict whether you are at risk of diabetes</h3>", unsafe_allow_html=True)


# Glucose Report Section
with st.expander("Upload or Capture Glucose Report"):
    glucose_image_option = st.radio("How would you like to provide your Glucose Report?", ('Upload Image', 'Capture via Camera'), key="glucose_radio")
    glucose_value = ""
    if glucose_image_option == 'Upload Image':
        uploaded_glucose_file = st.file_uploader("Choose an image for the Glucose report...", type=["jpg", "jpeg", "png"], key="glucose")
        if uploaded_glucose_file:
            glucose_image = Image.open(uploaded_glucose_file)
            extracted_glucose_text = process_image(glucose_image)
            glucose_data = parse_text(extracted_glucose_text, 'glucose')
            if glucose_data['Glucose']:
                glucose_value = glucose_data['Glucose']
                st.success(f"Auto-filled Glucose value: {glucose_value}")
            else:
                st.warning("Could not extract Glucose value.")
    elif glucose_image_option == 'Capture via Camera':
        captured_glucose_image = st.camera_input("Take a picture of your Glucose report", key="glucose_cam")
        if captured_glucose_image:
            glucose_image = Image.open(captured_glucose_image)
            extracted_glucose_text = process_image(glucose_image)
            glucose_data = parse_text(extracted_glucose_text, 'glucose')
            if glucose_data['Glucose']:
                glucose_value = glucose_data['Glucose']
                st.success(f"Auto-filled Glucose value: {glucose_value}")
            else:
                st.warning("Could not extract Glucose value.")


# Insulin Report Section
with st.expander("Upload or Capture Insulin Report"):
    insulin_image_option = st.radio("How would you like to provide your Insulin Report?", ('Upload Image', 'Capture via Camera'), key="insulin_radio")
    insulin_value = ""
    if insulin_image_option == 'Upload Image':
        uploaded_insulin_file = st.file_uploader("Choose an image for the Insulin report...", type=["jpg", "jpeg", "png"], key="insulin")
        if uploaded_insulin_file:
            insulin_image = Image.open(uploaded_insulin_file)
            extracted_insulin_text = process_image(insulin_image)
            insulin_data = parse_text(extracted_insulin_text, 'insulin')
            if insulin_data['Insulin']:
                insulin_value = insulin_data['Insulin']
                st.success(f"Auto-filled Insulin value: {insulin_value}")
            else:
                st.warning("Could not extract Insulin value.")
    elif insulin_image_option == 'Capture via Camera':
        captured_insulin_image = st.camera_input("Take a picture of your Insulin report", key="insulin_cam")
        if captured_insulin_image:
            insulin_image = Image.open(captured_insulin_image)
            extracted_insulin_text = process_image(insulin_image)
            insulin_data = parse_text(extracted_insulin_text, 'insulin')
            if insulin_data['Insulin']:
                insulin_value = insulin_data['Insulin']
                st.success(f"Auto-filled Insulin value: {insulin_value}")
            else:
                st.warning("Could not extract Insulin value.")


# Group inputs in columns to save space
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Please enter the following details:</h4>", unsafe_allow_html=True)

# Split into columns
col1, col2, col3 = st.columns(3)
with col1:
    Pregnancies = st.text_input('Number of Pregnancies')
    SkinThickness = st.text_input('Skin Thickness value')
    DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')
with col2:
    Glucose = st.text_input('Glucose Level', value=glucose_value)
    Insulin = st.text_input('Insulin Level', value=insulin_value)
    Age = st.text_input('Age of the Person')
with col3:
    BloodPressure = st.text_input('Blood Pressure value')
    BMI = st.text_input('BMI value')


# Prediction Button and Result
if st.button('Predict Diabetes Risk', key="diabetes_test"):
    user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
    try:
        user_input = [float(x) for x in user_input]
        diab_prediction = diabetes_model.predict([user_input])
        if diab_prediction[0] == 1:
            st.success('The person is diabetic')
        else:
            st.success('The person is not diabetic')
    except ValueError:
        st.error("Please ensure all fields are filled in correctly with numerical values.")
