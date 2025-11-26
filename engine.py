import cv2
from deepface import DeepFace
from fer import FER
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ---------------------------------
# AGE RANGE
# ---------------------------------
def age_range_from_value(age):
    low = max(0, age - 5)
    high = age + 5
    return f"{low}-{high}"


# ---------------------------------
# EMOTION DETECTION 
# ---------------------------------
def detect_emotion(image):
    detector = FER()
    emotion, score = detector.top_emotion(image)
    return emotion, score


# ---------------------------------
# CALCULATE STRESS BASED ON EMOTION
# ---------------------------------
def calculate_stress(emotion):
    if emotion is None:
        return 0
    
    
    emotion = emotion.lower()

    if emotion == "happy":
        return "Low (10–30%)"
    elif emotion == "neutral":
        return "Moderate (30–45%)"
    elif emotion == "surprise":
        return "Mild–High (40–55%)"
    elif emotion == "sad":
        return "High (60–75%)"
    elif emotion == "fear":
        return "High (70–85%)"
    elif emotion == "disgust":
        return "Very High (75–90%)"
    elif emotion == "angry":
        return "Extremely High (85–100%)"
    else:
        return "Moderate (30–45%)"


# ---------------------------------
# BP & SUGAR LOGIC
# ---------------------------------
def estimate_bp_and_sugar(age, stress_level, emotion):

    # 1. Base values by age
    if age <= 25:
        base_sys = 115; base_dia = 75; base_sugar = 90
    elif age <= 35:
        base_sys = 120; base_dia = 80; base_sugar = 100
    elif age <= 50:
        base_sys = 130; base_dia = 85; base_sugar = 110
    else:
        base_sys = 145; base_dia = 90; base_sugar = 120

    # 2. Emotion stress contribution
    emotion_stress = {
        "happy": 0, "neutral": 5, "surprise": 8,
        "sad": 12, "fear": 15, "disgust": 18, "angry": 22
    }
    emo_score = emotion_stress.get(emotion.lower(), 5)

    # 3. Stress uplift multipliers
    stress_level_lower = stress_level.lower()

    if "low" in stress_level_lower:
        bp_uplift = 0.02; sugar_uplift = 5
    elif "moderate" in stress_level_lower:
        bp_uplift = 0.05; sugar_uplift = 10
    elif "mild" in stress_level_lower:
        bp_uplift = 0.09; sugar_uplift = 18
    elif "high (60" in stress_level_lower:
        bp_uplift = 0.15; sugar_uplift = 25
    elif "very" in stress_level_lower:
        bp_uplift = 0.22; sugar_uplift = 40
    elif "extremely" in stress_level_lower:
        bp_uplift = 0.30; sugar_uplift = 55
    else:
        bp_uplift = 0.05; sugar_uplift = 10

    # 4. Final values
    final_sys = int(base_sys * (1 + bp_uplift))
    final_dia = int(base_dia * (1 + bp_uplift))
    final_sugar = int(base_sugar + sugar_uplift + emo_score)

    return f"{final_sys}/{final_dia} mmHg", f"{final_sugar} mg/dL"


# ---------------------------------
# MAIN ANALYSIS FUNCTION
# ---------------------------------
def analyze_face(image):

    # AGE + GENDER (stabilized)
    ages, genders = [], []

    for i in range(3):
        res = DeepFace.analyze(
            image,
            actions=['age', 'gender'],
            detector_backend='retinaface',
            enforce_detection=False
        )[0]

        ages.append(res["age"])
        genders.append(res["dominant_gender"])

    avg_age = sum(ages) // len(ages)
    age_range = age_range_from_value(avg_age)
    gender = max(set(genders), key=genders.count)

    # Internal emotion
    emotion, emo_score = detect_emotion(image)

    # Stress level
    stress = calculate_stress(emotion)

    # BP + sugar
    bp, sugar = estimate_bp_and_sugar(avg_age, stress, emotion)

    return age_range, gender, stress, bp, sugar


# ---------------------------------
# PDF GENERATOR
# ---------------------------------
def generate_pdf(age_range, gender, stress, bp, sugar, output_path="health_report.pdf"):

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "Health Report")

    c.setFont("Helvetica", 12)
    y = 700

    c.drawString(50, y, f"Estimated Age Range: {age_range}"); y -= 30
    c.drawString(50, y, f"Predicted Gender: {gender}"); y -= 30
    c.drawString(50, y, f"Stress Level: {stress}"); y -= 30
    c.drawString(50, y, f"Estimated Blood Pressure: {bp}"); y -= 30
    c.drawString(50, y, f"Estimated Sugar Level: {sugar}");

    c.save()
    return output_path
