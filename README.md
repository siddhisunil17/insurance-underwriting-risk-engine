# AI-Powered Health Insurance Underwriting Risk Engine

This project predicts high-claim underwriting risk for health insurance policyholders using portfolio, premium, utilization, and policy data.

## Project Components

- Insurance EDA
- Data cleaning
- Feature engineering
- High-claim risk prediction model
- SHAP explainability
- FastAPI inference API
- Streamlit frontend dashboard

## Model Performance

- Accuracy: 82.9%
- ROC AUC: 0.935
- High-risk recall: 92%
- High-risk precision: 60%

## Architecture

Streamlit Frontend → FastAPI Backend → Random Forest Model → Underwriting Decision

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt