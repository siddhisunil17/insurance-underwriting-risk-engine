import streamlit as st
import requests




st.title("Health Insurance Underwriting Risk Engine")

st.write("Enter policyholder details to predict high-claim underwriting risk.")

age = st.number_input("Age", min_value=0, max_value=100, value=45)
premium = st.number_input("Premium", min_value=0.0, value=850.0)
n_medical_services = st.number_input("Number of Medical Services", min_value=0, value=10)
exposure_time = st.number_input("Exposure Time", min_value=0.01, max_value=1.0, value=1.0)

gender = st.selectbox("Gender", ["F", "M"])
type_policy = st.selectbox("Policy Type", ["C", "I"])
type_product = st.selectbox("Product Type", ["D", "I", "P", "S"])
distribution_channel = st.selectbox("Distribution Channel", ["A", "D", "I"])
reimbursement = st.selectbox("Reimbursement", ["No", "Yes"])
new_business = st.selectbox("New Business", ["No", "Yes"])

seniority_insured = st.number_input("Seniority Insured", min_value=0, value=10)
seniority_policy = st.number_input("Seniority Policy", min_value=0, value=10)
n_insured_pc = st.number_input("Insured Count PC", min_value=0, value=100)
n_insured_mun = st.number_input("Insured Count Municipality", min_value=0, value=1000)
n_insured_prov = st.number_input("Insured Count Province", min_value=0, value=7000)



if st.button("Predict Underwriting Risk"):
    
    payload = {

        "age": age,
        "premium": premium,
        "n_medical_services": n_medical_services,
        "exposure_time": exposure_time,

        "gender": gender,
        "type_policy": type_policy,
        "type_product": type_product,
        "distribution_channel": distribution_channel,
        "reimbursement": reimbursement,
        "new_business": new_business,

        "seniority_insured": seniority_insured,
        "seniority_policy": seniority_policy,

        "n_insured_pc": n_insured_pc,
        "n_insured_mun": n_insured_mun,
        "n_insured_prov": n_insured_prov
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    result = response.json()

    st.subheader("Prediction Result")

    st.write(
        f"Risk Score: {result['risk_score']}/100"
    )

    st.write(
        f"Risk Tier: {result['risk_tier']}"
    )

    st.write(
        f"High-Claim Probability: {result['risk_probability']}"
    )

    if result["prediction"] == 1:

        st.error(
            f"Underwriting Decision: {result['underwriting_decision']}"
        )

    else:

        st.success(
            f"Underwriting Decision: {result['underwriting_decision']}"
        )