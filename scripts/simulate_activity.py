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


def simulate_prediction_and_feedback():
    input_data = generate_input()

    # Enviar predicción
    pred_resp = requests.post(f"{API_URL}/predict", json=input_data)
    if pred_resp.status_code != 200:
        print("❌ Prediction failed:", pred_resp.text)
        return

    prediction = pred_resp.json()
    print(
        f"🔮 Prediction: {prediction['prediction']:.2f} | model: {prediction['model_name']} v{prediction['model_version']}"
    )

    # 🧠 Simula que el usuario envía feedback
    # ⚠️ Necesitamos conocer el ID de la predicción. Este script asume que puedes recuperarlo de algún modo.
    # Simulación: esperar unos segundos y suponer que se ha loggeado la última predicción con id incremental
    time.sleep(2)  # Espera a que se escriba en la DB

    # 👉 Aquí deberías tener un endpoint como `/last-prediction-id` o similar.
    # Lo simulo con un valor incremental artificial para el ejemplo:
    latest_id = get_latest_prediction_id()

    if latest_id is None:
        print("❌ No prediction_id available for feedback.")
        return

    feedback_value = round(random.uniform(0.5, 5.0), 2)
    feedback_payload = {"feedback": feedback_value, "prediction_id": latest_id}

    fb_resp = requests.post(f"{API_URL}/feedback", json=feedback_payload)
    if fb_resp.status_code == 200:
        print(
            f"📨 Feedback sent (value: {feedback_value}) for prediction_id {latest_id}"
        )
    else:
        print("❌ Feedback failed:", fb_resp.text)


# 🔧 Simula un contador simple por ahora (o adáptalo si tienes endpoint real)
def get_latest_prediction_id():
    # Simulación: asume que el ID va creciendo con cada predicción
    # ❗ Reemplaza esto con una consulta real si tienes acceso
    try:
        with open("last_id.txt", "r") as f:
            last_id = int(f.read().strip())
    except FileNotFoundError:
        last_id = 0

    new_id = last_id + 1
    with open("last_id.txt", "w") as f:
        f.write(str(new_id))

    return new_id


if __name__ == "__main__":
    check_model_info()
    for _ in range(5):
        simulate_prediction_and_feedback()
        time.sleep(1)
