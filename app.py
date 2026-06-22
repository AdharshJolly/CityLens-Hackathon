import streamlit as st
import cv2
import tempfile
from ultralytics import YOLO
import os

st.set_page_config(page_title="CityShield-AI", page_icon="🛡️", layout="wide")

st.title("🛡️ CityShield-AI Hazard Dashboard")
st.markdown("Select an Intelligence Engine from the sidebar and upload an image or video to see real-time YOLO11n hazard detection.")

# Sidebar
st.sidebar.header("Configuration")
engine_choice = st.sidebar.selectbox(
    "Select Intelligence Engine:",
    ("Fire Engine", "Collapse Engine", "Accident Engine", "Animal Engine", "Streetlight Engine")
)

# Map choices to model paths
model_paths = {
    "Fire Engine": "submission/fire/best.pt",
    "Collapse Engine": "submission/collapse/best.pt",
    "Accident Engine": "submission/accident/best.pt",
    "Animal Engine": "submission/animal/best.pt",
    "Streetlight Engine": "submission/streetlight/best.pt"
}

model_path = model_paths[engine_choice]

@st.cache_resource
def load_model(path):
    if os.path.exists(path):
        return YOLO(path)
    return None

model = load_model(model_path)

if model is None:
    st.error(f"Model weights not found at {model_path}. Please ensure the model is trained.")
else:
    st.sidebar.success(f"{engine_choice} Loaded!")

    uploaded_file = st.file_uploader("Upload Image or Video (jpg, png, mp4)", type=["jpg", "jpeg", "png", "mp4"])

    if uploaded_file is not None:
        if "video" in uploaded_file.type or uploaded_file.name.endswith(".mp4"):
            st.markdown("### 🎥 Live Video Inference")
            run_button = st.button("Start Live Analysis")
            
            if run_button:
                # Save to temp file so OpenCV can read it
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(uploaded_file.read())
                
                cap = cv2.VideoCapture(tfile.name)
                stframe = st.empty() # Placeholder for live video feed
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # Run YOLO Inference
                    results = model.predict(frame, conf=0.25, verbose=False)
                    annotated_frame = results[0].plot()
                    
                    # Convert BGR to RGB for Streamlit rendering
                    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                    
                    # Update placeholder dynamically to create live video effect!
                    stframe.image(annotated_frame, channels="RGB", use_container_width=True)
                    
                cap.release()
                st.success("Video Analysis Complete!")
                
        else:
            st.markdown("### 🖼️ Image Inference")
            run_button = st.button("Run Analysis")
            
            if run_button:
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                tfile.write(uploaded_file.read())
                
                results = model.predict(tfile.name, conf=0.25, verbose=False)
                annotated_img = results[0].plot()
                annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.image(uploaded_file, caption="Original Input", use_container_width=True)
                with col2:
                    st.image(annotated_img, caption="CityShield AI Output", use_container_width=True)

