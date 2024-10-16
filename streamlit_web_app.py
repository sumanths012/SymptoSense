import os
import pickle
import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Set up pytesseract path if needed (make sure this path is correct)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Set page configuration
st.set_page_config(page_title="Diabetes Prediction Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Set up the main header for the application
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Diabetes Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>Predict whether you are at risk of diabetes</h3>", unsafe_allow_html=True)

# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Load the saved diabetes model
diabetes_model = pickle.load(open(r'C:/Users/suman/OneDrive/Desktop/Assignments/My Resume/Final_Project/ProjectFiles/SavedModels/diabetes_model.sav', 'rb'))


# Function to process image and extract text
def process_image(image):
    """Process the image to extract text using pytesseract."""
    # Convert the image to grayscale (for better OCR results)
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Apply OCR to extract text from the image
    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text


# Function to parse extracted text and extract values
def parse_text(text):
    """Parse the extracted text to extract medical test values like Glucose, BMI, etc."""
    data = {
        'Glucose': None,
        'BMI': None,
        'Insulin': None
    }
    # Example parsing logic (you need to customize based on your report)
    if 'Glucose' in text or 'eAG' in text:
        data['Glucose'] = extract_value(text, 'Glucose', 'eAG')
    if 'BMI' in text:
        data['BMI'] = extract_value(text, 'BMI')
    if 'Insulin' in text:
        data['Insulin'] = extract_value(text, 'Insulin')
    return data


# Function to extract a specific value from the extracted text
def extract_value(text, *field_names):
    """Extract the numerical value after a given field name (like Glucose or BMI)."""
    lines = text.splitlines()
    for line in lines:
        for field_name in field_names:
            if field_name in line:
                parts = line.split()
                for part in parts:
                    if part.isdigit():
                        return part
                break
    return None

# Add JavaScript to handle auto-focus for camera
st.markdown("""
    <script>
        const videoElement = document.querySelector('video');
        if (videoElement) {
            videoElement.setAttribute('autofocus', true);
            videoElement.setAttribute('autoFocus', true);
        }
    </script>
""", unsafe_allow_html=True)

# Upload or Capture Image
st.title("Diabetes Prediction Web App")

# Upload or Capture Image
image_option = st.radio("How would you like to provide your test report?", ('Upload Image', 'Capture via Camera'))

# Placeholder for the glucose value (to allow auto-filling)
glucose_value = ""

# Handle image upload
if image_option == 'Upload Image':
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Extract text from the image (but don't display it)
        extracted_text = process_image(image)
        # Parse the extracted text to auto-fill data
        data = parse_text(extracted_text)
        # Set the auto-filled glucose value if extracted
        if data['Glucose']:
            glucose_value = data['Glucose']  # Auto-filled value
            st.success(f"Auto-filled Glucose value: {glucose_value}")
        else:
            st.warning("Could not extract Glucose value from the report.")

# Handle image capture from the camera
elif image_option == 'Capture via Camera':
    captured_image = st.camera_input("Take a picture of your test report")
    if captured_image is not None:
        image = Image.open(captured_image)
        # Extract text from captured image (but don't display it)
        extracted_text = process_image(image)
        # Parse the extracted text to auto-fill data
        data = parse_text(extracted_text)
        # Set the auto-filled glucose value if extracted
        if data['Glucose']:
            glucose_value = data['Glucose']  # Auto-filled value
            st.success(f"Auto-filled Glucose value: {glucose_value}")
        else:
            st.warning("Could not extract Glucose value from the report.")

# Space to separate input and auto-filled data
st.markdown("<hr>", unsafe_allow_html=True)

# Inputs for manual entry or auto-filling
st.markdown("<h4 style='text-align: center;'>Please enter the following details:</h4>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    Pregnancies = st.text_input('Number of Pregnancies')
with col2:
    # Auto-fill the glucose level if extracted
    Glucose = st.text_input('Glucose Level', value=glucose_value)
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
    try:
        user_input = [float(x) for x in user_input]
        # Make prediction using the loaded model
        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

        # Display result in a prominent style
        st.markdown(f"<h3 style='text-align: center; color: red;'>{diab_diagnosis}</h3>", unsafe_allow_html=True)

    except ValueError:
        st.error("Please enter valid numbers for all fields.")

# Add footer or additional design elements if necessary
st.markdown("<hr style='border:1px solid #eee;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by Machine Learning</p>", unsafe_allow_html=True)
