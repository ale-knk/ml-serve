import requests
import random
import time

API_URL = "http://localhost:8000"  # Cambia a "http://api:8000" si lo lanzas desde otro contenedor


def generate_input():
    return {
        "MedInc": round(random.uniform(1.0, 15.0), 2),
        "HouseAge": round(random.uniform(1, 50), 1),
        "AveRooms": round(random.uniform(2, 10), 2),
        "AveBedrms": round(random.uniform(1, 5), 2),
        "Population": round(random.uniform(100, 5000), 1),
        "AveOccup": round(random.uniform(1, 6), 2),
        "Latitude": round(random.uniform(32.0, 42.0), 5),
        "Longitude": round(random.uniform(-124.0, -114.0), 5),
    }


def check_model_info():
    resp = requests.get(f"{API_URL}/model-info")
    if resp.status_code == 200:
        print("✅ Model info:", resp.json())
    else:
        print("⚠️ No model info available:", resp.text)


def simulate_prediction_and_feedback(n: int = 10):
    input_data = generate_input()

    pred_resp = requests.post(f"{API_URL}/predict", json=input_data)
    if pred_resp.status_code != 200:
        print("❌ Prediction failed:", pred_resp.text)
        return

    prediction = pred_resp.json()

    for _ in range(n):
        feedback_value = round(prediction["prediction"] + random.uniform(0.5, 1.5), 2)
        feedback_payload = {"feedback": feedback_value, "prediction_id": prediction["prediction_id"]}

        fb_resp = requests.post(f"{API_URL}/feedback", json=feedback_payload)
        if fb_resp.status_code == 200:
            print(
                f"📨 Feedback sent (value: {feedback_value}) for prediction_id {prediction['prediction_id']}"
            )
        else:
            print("❌ Feedback failed:", fb_resp.text)



if __name__ == "__main__":
    check_model_info()
    for _ in range(10):
        simulate_prediction_and_feedback()
