from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import joblib
app = FastAPI(title="Diabetes Prediction API")

# =========================
# Load Model (LOCAL EXPORT)
# =========================
try:
    # model = mlflow.pyfunc.load_model("model/diabetes-final_model.pkl")
    model =joblib.load("model/diabetes-final_model.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    raise


# =========================
# Input Schema
# =========================
class DiabetesInput(BaseModel):
    gender: int
    age: float
    hypertension: int
    heart_disease: int
    smoking_history: int
    bmi: float
    HbA1c_level: float
    blood_glucose_level: float


# =========================
# Routes
# =========================
@app.get("/")
def home():
    return {
        "message": "Diabetes & Heart Disease Prediction API is running",
        "predict_endpoint": "/predict",
        "docs": "/docs"
    }


@app.post("/predict")
def predict(data: DiabetesInput):
    try:
        input_df = pd.DataFrame([{
            "gender": data.gender,
            "age": data.age,
            "hypertension": data.hypertension,
            "heart_disease": data.heart_disease,
            "smoking_history": data.smoking_history,
            "bmi": data.bmi,
            "HbA1c_level": data.HbA1c_level,
            "blood_glucose_level": data.blood_glucose_level
        }])

        prediction = model.predict(input_df)[0]

        return {
            "prediction": int(prediction),
            "result": "⚠️ Diabetes Detected" if prediction == 1 else "✅ No Diabetes",
            
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/info")
def info():
    return {
        "model": "Diabetes / Heart Disease Classifier",
        "features": [
            "gender", "age", "hypertension", "heart_disease",
            "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"
        ]
    }
