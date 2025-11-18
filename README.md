# AI Face Health Scanner  
An AI-powered facial analysis system that estimates **Age Range, Gender, Stress Level, Blood Pressure**, and **Sugar Level** from a single face image.

This project was built using **DeepFace**, **FER**, **Streamlit**, and **custom AI logic**.  
It’s designed for demonstration purposes to showcase how facial cues can be used to generate **approximate** wellness insights.

> ⚠️ Not a medical tool — all values are *approximate estimations*, meant only for learning and experimentation.

---

# Project Overview

This system takes a face image and performs:

1. **Face Analysis (DeepFace)**
   - Predicts age  
   - Predicts gender  

2. **Emotion Detection (FER)**
   - Detects dominant emotion  
   - Emotion is *not shown to the user*  
   - Emotion is used internally to calculate stress, BP, sugar  

3. **Stress Level Calculation**
   - Converts emotion → stress levels such as:  
     *Low, Moderate, High, Very High, Extremely High*

4. **Blood Pressure & Sugar Estimation**
   - Age-based physiological baselines  
   - Stress-based multipliers  
   - Emotion-based adjustments  
   - Produces realistic values like:  
     - `118/78 mmHg`  
     - `142/95 mmHg`  
     - `108 mg/dL`  
     - `132 mg/dL`  

5. **Streamlit Frontend**
   - Clean, dark UI  
   - Upload image  
   - See instant health report  
   - Download PDF report  

6. **PDF Report Generation**
   - Auto-generated downloadable report  
   - Uses ReportLab library  

---

# ⚙️ How the Project Was Built

This project is built using a **clean architecture approach**:

## 1. **Backend (engine.py)**
Handles all AI computations:

- Age detection → DeepFace  
- Gender detection → DeepFace  
- Emotion detection → FER  
- Stress logic → Custom mapping  
- BP & Sugar estimation → Custom physiological model  
- PDF generation → ReportLab  

The backend is isolated, so it can be reused with:

- Flask  
- Django  
- Mobile apps  
- Other UIs  

---

## 2. **Frontend (app.py)**
Built using **Streamlit**, which provides:

- File uploader  
- Image preview  
- Loading animation  
- Results display  
- Download PDF button  
- Dark mode UI (via config.toml)  

UI is intentionally simple for a smooth user experience.

---

## 3. **Features**
✔ Facial age estimation  
✔ Gender detection  
✔ Emotion-based stress model  
✔ BP & Sugar estimation (approximate)  
✔ PDF report generation 

---

# 🧠 How It Works (Step-by-Step)

## 🔹 1. User uploads a face image  
Streamlit receives the file and converts to a NumPy array.

## 🔹 2. Age & gender are predicted  
Using DeepFace’s RetinaFace model.

## 🔹 3. Emotion is detected internally  
Emotion affects stress, BP, sugar calculations — but is NOT shown to user.

## 🔹 4. Stress level is computed  
Based on emotion category.

## 🔹 5. BP & Sugar are estimated  
Using a custom physiologically-inspired formula:
- Age → baseline values  
- Stress → percentage uplift  
- Emotion → glucose influence  

## 🔹 6. Output is displayed  
User sees:
- Age Range  
- Gender  
- Stress  
- BP  
- Sugar  

## 🔹 7. PDF is generated  
User can download the report.

---

# ▶️ How to Run the Project

## **1. Clone the repository**
```bash
git clone https://github.com/<your-username>/AI-Face-Health-Scanner.git
cd AI-Face-Health-Scanner
```
## **2. Create a virtual environment**
```bash
python -m venv faceenv
```
## **3. Activate Environment**
```bash
faceenv\Scripts\activate.bat
```
## **4. Install Dependencies**
```bash
pip install -r requirements.txt
```
## **5. Run the Streamlit app**
```bash
streamlit run app.py
```
## **6. Upload a face image and get the report**

---

# ⚠️ Disclaimer
This project is not intended for medical diagnosis.
Values are approximations based on emotions and age heuristics.
Use for learning and demonstration only.
