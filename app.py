import streamlit as st
import cv2
import numpy as np
from engine import analyze_face, generate_pdf

st.title("🩺 AI-Based Face Health Scanner")
st.write("Upload a face image to generate an approximate health report.")

uploaded_file = st.camera_input("Take a Picture")

if uploaded_file is not None:

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    st.image(image, channels="BGR", caption="Uploaded Image")

    with st.spinner("Analyzing face... Please wait ⏳"):
        age_range, gender, stress, bp, sugar = analyze_face(image)

    st.subheader("🧾 Health Report")
    st.write(f"**Estimated Age Range:** {age_range}")
    st.write(f"**Predicted Gender:** {gender}")
    st.write(f"**Stress Level:** {stress}")
    st.write(f"**Estimated Blood Pressure:** {bp}")
    st.write(f"**Estimated Sugar Level:** {sugar}")

    # Create downloadable PDF
    pdf_path = generate_pdf(age_range, gender, stress, bp, sugar)

    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download Health Report as PDF",
            data=pdf_file,
            file_name="health_report.pdf",
            mime="application/pdf"
        )
