import streamlit as st

# ----------------------------
# Risk Score Interpretation
# ----------------------------
def interpret_risk_score(score):
    if 1 <= score <= 3.9:
        return "Low Risk", "🟢 All Clear", "Maintain current lifestyle."
    elif 4 <= score <= 7.9:
        return "Moderate Risk", "🟡 Caution Zone", "Medical review recommended."
    elif 8 <= score <= 10:
        return "High Risk", "🔴 Immediate Alert", "Urgent medical attention required."
    else:
        return "Invalid", "N/A", "Check inputs."

# ----------------------------
# Risk Score Calculation
# ----------------------------
def calculate_rule_based_score(inputs):
    score = 0
    ldl = inputs['LDL']
    if ldl >= 190: score += 2.0
    elif 160 <= ldl < 190: score += 1.5
    elif 130 <= ldl < 160: score += 1.0
    elif 100 <= ldl < 130: score += 0.5

    hdl = inputs['HDL']
    target_hdl = 40 if inputs['Sex'] == "Male" else 50
    deficit = target_hdl - hdl
    if deficit > 20: score += 1.5
    elif 10 < deficit <= 20: score += 1.0
    elif 0 < deficit <= 10: score += 0.5

    tg = inputs['Triglycerides']
    if tg >= 250: score += 1.5
    elif 200 <= tg < 250: score += 1.0
    elif 150 <= tg < 200: score += 0.5

    hba1c = inputs['HbA1c']
    if hba1c >= 8.0: score += 1.0
    elif 6.5 <= hba1c < 8.0: score += 0.75
    elif 5.7 <= hba1c < 6.5: score += 0.5

    sys = inputs['Systolic']
    dia = inputs['Diastolic']
    if sys >= 140 or dia >= 90: score += 1.0
    elif 130 <= sys < 140 or 80 <= dia < 90: score += 0.75
    elif 120 <= sys < 130 and dia < 80: score += 0.5

    fbs = inputs['FBS']
    if fbs >= 126: score += 0.75
    elif 100 <= fbs < 126: score += 0.5

    smoking = inputs['Smoking']
    if smoking >= 10: score += 0.75
    elif 5 <= smoking < 10: score += 0.5
    elif 1 <= smoking < 5: score += 0.25

    bmi = inputs['BMI']
    if bmi >= 30: score += 0.5
    elif 25 <= bmi < 30: score += 0.25

    age = inputs['Age']
    if age >= 60: score += 0.25

    tsh = inputs['TSH']
    if tsh < 0.4 or tsh >= 10: score += 0.25
    elif 4.1 <= tsh < 10: score += 0.1

    rhr = inputs['RestHR']
    if rhr > 100 or rhr < 50: score += 0.25
    elif 91 <= rhr <= 100: score += 0.15
    elif 50 <= rhr < 60: score += 0.1

    return min(score, 10)

# ----------------------------
# STEMI Detection Functions
# ----------------------------
def is_critical_stemi(lead, value, sex, age):
    if lead in ['V2', 'V3']:
        if sex == "Male" and age >= 40 and value >= 2.0:
            return True
        elif sex == "Male" and age < 40 and value >= 2.5:
            return True
        elif sex == "Female" and value >= 1.5:
            return True
    elif lead == 'V4' and value >= 1.5:
        return True
    elif lead in ['II', 'III', 'aVF'] and value >= 1.5:
        return True
    elif lead == 'V1' and value >= 2.0:
        return True
    return False

def interpret_lead(lead, value, sex, age):
    if lead in ['V2', 'V3']:
        if value <= 1.0: return "✅ Normal"
        elif 1.1 <= value <= 1.9: return "⚠️ Moderate Risk – Mild elevation"
        elif is_critical_stemi(lead, value, sex, age): return "🔴 STEMI (Critical)"
        else: return "❓ Above normal – Check criteria"
    elif lead == 'V4':
        if value <= 0.9: return "✅ Normal"
        elif 1.0 <= value <= 1.4: return "⚠️ Borderline – Evaluate context"
        elif value >= 1.5: return "🔴 STEMI (Critical)"
    elif lead in ['II', 'III', 'aVF']:
        if value <= 0.9: return "✅ Normal"
        elif 0 <= value <= 1.4: return "⚠️ Possible early ischemia"
        elif value >= 1.5: return "🔴 Inferior STEMI"
    elif lead == 'V1':
        if value < 2.0: return "✅ Normal"
        elif value >= 2.0: return "🔴 Anterior STEMI"
    return "❓ Unknown"

# ----------------------------
# Streamlit Navigation
# ----------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", ["Risk Scoring", "ECG STEMI Detection", "About"])

# ----------------------------
# Page 1: Risk Scoring
# ----------------------------
if page == "Risk Scoring":
    st.title("🔬 10-Point Hybrid Heart Risk Scoring")

    st.sidebar.header("🩺 Enter Clinical Inputs")
    sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
    age = st.sidebar.number_input("Age", 10, 100)
    ldl = st.sidebar.number_input("LDL (mg/dL)", 0, 300)
    hdl = st.sidebar.number_input("HDL (mg/dL)", 0, 100)
    tg = st.sidebar.number_input("Triglycerides (mg/dL)", 50, 500)
    hba1c = st.sidebar.number_input("HbA1c (%)", 3.0, 15.0)
    sys = st.sidebar.number_input("Systolic BP", 80, 200)
    dia = st.sidebar.number_input("Diastolic BP", 40, 130)
    fbs = st.sidebar.number_input("Fasting Blood Sugar", 50, 300)
    smoking = st.sidebar.number_input("Cigarettes/day", 0, 60)
    bmi = st.sidebar.number_input("BMI", 10.0, 50.0)
    tsh = st.sidebar.number_input("TSH (mIU/L)", 0.01, 100.0)
    rhr = st.sidebar.number_input("Resting Heart Rate", 30, 150)

    if st.sidebar.button("🔍 Calculate Risk"):
        inputs = {
            "Sex": sex, "Age": age, "LDL": ldl, "HDL": hdl, "Triglycerides": tg,
            "HbA1c": hba1c, "Systolic": sys, "Diastolic": dia, "FBS": fbs,
            "Smoking": smoking, "BMI": bmi, "TSH": tsh, "RestHR": rhr
        }
        score = calculate_rule_based_score(inputs)
        category, interpretation, advice = interpret_risk_score(score)

        st.subheader("📊 Risk Scoring Output")
        st.metric("Total Score (1–10)", f"{score:.2f}")
        st.write(f"**Risk Level:** {category}")
        st.write(f"**Interpretation:** {interpretation}")
        st.info(f"**Advice:** {advice}")

# ----------------------------
# Page 2: ECG STEMI Detection
# ----------------------------
elif page == "ECG STEMI Detection":
    st.title("📉 ECG Lead-Based STEMI Detection")

    st.sidebar.header("🔢 Enter ST Elevation (mm)")
    sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
    age = st.sidebar.number_input("Age", 10, 100, step=1)

    v1 = st.sidebar.number_input("Lead V1", 0.0, 10.0, step=0.1)
    v2 = st.sidebar.number_input("Lead V2", 0.0, 10.0, step=0.1)
    v3 = st.sidebar.number_input("Lead V3", 0.0, 10.0, step=0.1)
    v4 = st.sidebar.number_input("Lead V4", 0.0, 10.0, step=0.1)
    ii = st.sidebar.number_input("Lead II", 0.0, 10.0, step=0.1)
    iii = st.sidebar.number_input("Lead III", 0.0, 10.0, step=0.1)
    avf = st.sidebar.number_input("Lead aVF", 0.0, 10.0, step=0.1)

    if st.sidebar.button("🔬 Evaluate ECG"):
        leads = {'V1': v1, 'V2': v2, 'V3': v3, 'V4': v4, 'II': ii, 'III': iii, 'aVF': avf}
        stemi_detected = False

        st.subheader("📄 Lead-by-Lead Interpretation")
        for lead, val in leads.items():
            result = interpret_lead(lead, val, sex, age)
            st.write(f"**{lead}:** {result}")
            if "STEMI" in result:
                stemi_detected = True

        st.markdown("---")
        st.subheader("🧠 Final Prediction")
        if stemi_detected:
            st.error("🔴 Heart Attack Detected (STEMI) — Seek immediate care.")
        else:
            st.success("🟢 No Heart Attack Detected")
        st.caption("🩺 Based on age- and sex-adjusted lead criteria.")

# ----------------------------
# Page 3: About
# ----------------------------
elif page == "About":
    st.title("ℹ️ About This Tool")
    st.markdown("""
This app combines:

1. **10-Point Rule-Based Heart Risk Scoring**
2. **Lead-by-Lead ECG STEMI Detection**

Built using clinical guidelines for early detection of myocardial infarction (MI) and cardiovascular risk factors.
    """)

