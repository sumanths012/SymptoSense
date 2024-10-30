import pickle
import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np


# Set up pytesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Initialize session state for toggle
if 'show_symptoms' not in st.session_state:
    st.session_state.show_symptoms = False


# Set page configuration
st.set_page_config(page_title="Diabetes Prediction Assistant", layout="wide", page_icon="🧑‍⚕️")


# CSS Styling
st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .symptoms-container {
        margin-top: 10px;
        background-color: white;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


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


# Function to process frame for real-time border detection
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        approx = cv2.approxPolyDP(largest_contour, 0.01 * cv2.arcLength(largest_contour, True), True)
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)  # Draw green border
    return frame


# Header section
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Diabetes Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555;'>Predict whether you are at risk of diabetes</h3>", unsafe_allow_html=True)


# Glucose Report Section
with st.expander("Upload, Capture, or Take Real-Time Glucose Report"):
    glucose_image_option = st.radio("How would you like to provide your Glucose Report?", ('Upload Image', 'Capture via Camera', 'Real-time Capture with Border Detection'), key="glucose_radio")
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
    
    elif glucose_image_option == 'Real-time Capture with Border Detection':
        st.write("Align the Glucose report, and borders will be detected in real-time. When ready, capture the image.")
        cap = cv2.VideoCapture(0)
        video_placeholder = st.empty()
        capture_button = st.button("Capture Glucose Report")

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Error accessing the camera.")
                break

            processed_frame = process_frame(frame)
            video_placeholder.image(processed_frame, channels="BGR")

            if capture_button:
                captured_glucose_frame = frame
                break

        cap.release()
        if 'captured_glucose_frame' in locals():
            st.success("Glucose report captured!")
            glucose_image = Image.fromarray(cv2.cvtColor(captured_glucose_frame, cv2.COLOR_BGR2RGB))
            st.image(glucose_image, caption="Captured Glucose Report", use_column_width=True)
            extracted_glucose_text = process_image(glucose_image)
            glucose_data = parse_text(extracted_glucose_text, 'glucose')
            if glucose_data['Glucose']:
                glucose_value = glucose_data['Glucose']
                st.success(f"Auto-filled Glucose value: {glucose_value}")
            else:
                st.warning("Could not extract Glucose value.")


# Insulin Report Section
with st.expander("Upload, Capture, or Take Real-Time Insulin Report"):
    insulin_image_option = st.radio("How would you like to provide your Insulin Report?", ('Upload Image', 'Capture via Camera', 'Real-time Capture with Border Detection'), key="insulin_radio")
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
    
    elif insulin_image_option == 'Real-time Capture with Border Detection':
        st.write("Align the Insulin report, and borders will be detected in real-time. When ready, capture the image.")
        cap = cv2.VideoCapture(0)
        video_placeholder = st.empty()
        capture_button = st.button("Capture Insulin Report")

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Error accessing the camera.")
                break

            processed_frame = process_frame(frame)
            video_placeholder.image(processed_frame, channels="BGR")

            if capture_button:
                captured_insulin_frame = frame
                break

        cap.release()
        if 'captured_insulin_frame' in locals():
            st.success("Insulin report captured!")
            insulin_image = Image.fromarray(cv2.cvtColor(captured_insulin_frame, cv2.COLOR_BGR2RGB))
            st.image(insulin_image, caption="Captured Insulin Report", use_column_width=True)
            extracted_insulin_text = process_image(insulin_image)
            insulin_data = parse_text(extracted_insulin_text, 'insulin')
            if insulin_data['Insulin']:
                insulin_value = insulin_data['Insulin']
                st.success(f"Auto-filled Insulin value: {insulin_value}")
            else:
                st.warning("Could not extract Insulin value.")
