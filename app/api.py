from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import joblib

app = FastAPI(
    title="Insurance Underwriting Risk API"
)

model = joblib.load(
    "models/underwriting_risk_model.pkl"
)

model_features = joblib.load(
    "models/model_features.pkl"
)


class UnderwritingInput(BaseModel):

    age: int
    premium: float
    n_medical_services: int
    exposure_time: float

    gender: str
    type_policy: str
    type_product: str
    distribution_channel: str
    reimbursement: str
    new_business: str

    seniority_insured: int
    seniority_policy: int

    n_insured_pc: int
    n_insured_mun: int
    n_insured_prov: int


@app.get("/")
def home():

    return {
        "message": "Insurance Underwriting Risk API Running"
    }


@app.post("/predict")
def predict_risk(data: UnderwritingInput):
    
    if data.exposure_time <= 0:
        return {
            "error": "exposure_time must be greater than 0"
        }

    claim_frequency = (
        data.n_medical_services
        / data.exposure_time
    )

    age_group = pd.cut(
        [data.age],
        bins=[-1,18,30,45,60,75,100],
        labels=[
            "Child",
            "Young Adult",
            "Adult",
            "Middle Age",
            "Senior",
            "Elderly"
        ]
    )[0]

    input_data = pd.DataFrame([{

        "age": data.age,
        "premium": data.premium,
        "n_medical_services": data.n_medical_services,
        "claim_frequency": claim_frequency,

        "seniority_insured": data.seniority_insured,
        "seniority_policy": data.seniority_policy,

        "n_insured_pc": data.n_insured_pc,
        "n_insured_mun": data.n_insured_mun,
        "n_insured_prov": data.n_insured_prov,

        "policy_lapsed_flag": 0,
        "insured_lapsed_flag": 0,

        "gender": data.gender,
        "type_policy": data.type_policy,
        "type_product": data.type_product,
        "distribution_channel": data.distribution_channel,
        "reimbursement": data.reimbursement,
        "new_business": data.new_business,

        "age_group": age_group
    }])

    input_encoded = pd.get_dummies(
        input_data,
        drop_first=True
    )

    input_encoded = input_encoded.reindex(
        columns=model_features,
        fill_value=0
    )

    probability = (
        model.predict_proba(input_encoded)[0][1]
    )

    prediction = (
        model.predict(input_encoded)[0]
    )

    decision = (
        "Manual Review"
        if prediction == 1
        else "Auto Approve"
    )

    
    risk_score = round(float(probability) * 100, 2)
    if risk_score >= 75:
        risk_tier = "High Risk"
    elif risk_score >= 40:
        risk_tier = "Medium Risk"
    else:
        risk_tier = "Low Risk"
        
        
    return {

        "risk_probability": round(
            float(probability),
            4
        ),
        
        "risk_score": risk_score,
        
        "risk_tier": risk_tier,

        "prediction": int(prediction),

        "underwriting_decision": decision
    }