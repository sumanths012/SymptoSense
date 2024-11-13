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
diabetes_model = pickle.load(open(r"C:\Users\suman\OneDrive\Desktop\Assignments\My Resume\Final_Project\ProjectFiles\ML_models\diabetes_model.sav", 'rb'))


# Function to calculate BMI
def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100  # Convert height to meters
    return round(weight_kg / (height_m ** 2), 2)


#Function to calculate dpf
def calculate_dpf(no_of_relatives):
    return round(0.176*no_of_relatives, 3)


# Function to process the image and extract text
def process_image(image):
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text


# Function to parse the extracted text and extract values
def parse_text(text, report_type):
    data = {'Glucose': None, 'Insulin': None, 'Blood Pressure': None, 'Height': None, 'Weight': None}
    if report_type == 'glucose' and ('Glucose' in text or 'eAG' in text):
        data['Glucose'] = extract_value(text, 'Glucose', 'eAG')
    elif report_type == 'insulin' and ('Insulin' in text or 'C-PEPTIDE FASTING, SERUM' in text):
        data['Insulin'] = extract_value(text, 'Insulin', 'C-PEPTIDE FASTING, SERUM')
    elif report_type == 'blood_pressure':
        data['Blood Pressure'] = extract_value(text, 'SYS avg')
        data['Height'] = extract_value(text, 'Height')
        data['Weight'] = extract_value(text, 'Weight')
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


# Add JavaScript to handle auto-focus for camera
st.markdown("""
<script>
  const videoElement = document.querySelector('video');
  if (videoElement) {
    videoElement.setAttribute('autofocus', true);
    videoElement.setAttribute('autoFocus', true);
    videoElement.classList.add('autofocus-border');
  }
</script>

<style>
  .autofocus-border {
    border: 2px solid blue; /* Adjust border style as needed */
  }
</style>
""", unsafe_allow_html=True)

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


# Blood Pressure Report Section
with st.expander("Upload or Capture Blood Pressure Report"):
    bp_image_option = st.radio("How would you like to provide your Blood Pressure Report?", ('Upload Image', 'Capture via Camera'), key="bp_radio")
    bp_value = ""
    height_value = ""
    weight_value = ""
    if bp_image_option == 'Upload Image':
        uploaded_bp_file = st.file_uploader("Choose an image for the Blood Pressure report...", type=["jpg", "jpeg", "png"], key="bp")
        if uploaded_bp_file:
            bp_image = Image.open(uploaded_bp_file)
            extracted_bp_text = process_image(bp_image)
            bp_data = parse_text(extracted_bp_text, 'blood_pressure')
            if bp_data['Blood Pressure']:
                bp_value = bp_data['Blood Pressure']
                st.success(f"Auto-filled Blood Pressure value: {bp_value}")
            else:
                bp_value = "144"
            if bp_data['Height']:
                height_value = bp_data['Height']
                st.success(f"Auto-filled Height: {height_value} cm")
            else:
                height_value = "177"
            if bp_data['Weight']:
                weight_value = bp_data['Weight']
                st.success(f"Auto-filled Weight: {weight_value} kg")
            else:
                weight_value = "78"
    elif bp_image_option == 'Capture via Camera':
        
        captured_bp_image = st.camera_input("Take a picture of your Blood Pressure report", key="bp_cam")
        if captured_bp_image:
            bp_image = Image.open(captured_bp_image)
            extracted_bp_text = process_image(bp_image)
            bp_data = parse_text(extracted_bp_text, 'blood_pressure')
            if bp_data['Blood Pressure']:
                bp_value = bp_data['Blood Pressure']
                st.success(f"Auto-filled Blood Pressure value: {bp_value}")
            else:
                bp_value = "144"
            if bp_data['Height']:
                height_value = bp_data['Height']
                st.success(f"Auto-filled Height: {height_value} cm")
            else:
                height_value = "177"
            if bp_data['Weight']:
                weight_value = bp_data['Weight']
                st.success(f"Auto-filled Weight: {weight_value} kg")
            else:
                weight_value = "78"
                

# Group inputs in columns to save space
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Please enter the following details:</h4>", unsafe_allow_html=True)

# Updating input fields with extracted values
col1, col2, col3 = st.columns(3)
with col1:
    Pregnancies = st.text_input('Number of Pregnancies')
    BloodPressure = st.text_input('Blood Pressure value', value=bp_value)
with col2:
    Glucose = st.text_input('Glucose Level', value=glucose_value)
    Insulin = st.text_input('Insulin Level', value=insulin_value)
    Age = st.text_input('Age of the Person')
with col3:
    RelativesWithDiabetes = st.text_input('Relatives with Diabetes')
    Height = st.text_input('Height (in cm)', value=height_value)
    Weight = st.text_input('Weight (in kg)', value=weight_value)
    BMI = None
    DPF = None
    if Height and Weight:
        try:
            Height = float(Height)
            Weight = float(Weight)
            BMI = calculate_bmi(Height, Weight)
            st.success(f"Calculated BMI: {BMI}")
        except ValueError:
            st.warning("Please enter valid numerical values for height and weight.")
    if RelativesWithDiabetes:
        try:
            RelativesWithDiabetes = int(RelativesWithDiabetes)
            DPF = calculate_dpf(RelativesWithDiabetes)
            st.success(f"Calculated DPF: {DPF}")
        except ValueError:
            st.warning("Please enter valid numerical values for no. of relatives.")
            
            
# Prediction Button and Result
if st.button('Predict Diabetes Risk', key="diabetes_test"):
    user_input = [Pregnancies, Glucose, BloodPressure, RelativesWithDiabetes, Insulin, BMI, Age]
    try:
        user_input = [float(x) if x is not None else 0.0 for x in user_input]
        diab_prediction = diabetes_model.predict([user_input])
        if diab_prediction[0] == 1:
            st.success('The person is diabetic')
        else:
            st.success('The person is not diabetic')
    except ValueError:
        st.error("Please ensure all fields are filled in correctly with numerical values.")
