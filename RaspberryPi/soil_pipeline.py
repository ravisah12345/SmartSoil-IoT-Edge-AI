import asyncio
import json
import numpy as np
from bleak import BleakScanner, BleakClient
from tflite_runtime.interpreter import Interpreter
import requests

# -------------------------------
# BLE CONFIG (match Arduino)
# -------------------------------
DEVICE_NAME = "SmartSoil-UNO-R4"
SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# -------------------------------
# ThingSpeak CONFIG
# -------------------------------
THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_WRITE_KEY"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# ThingSpeak field mapping:
# field1 = soil
# field2 = temp
# field3 = hum
# field4 = light
# field5 = ph
# field6 = AI prediction (0/1/2)
# field7 = soil2

# -------------------------------
# TFLite MODEL
# -------------------------------
MODEL_PATH = "soil_model.tflite"

interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

LABELS = {0: "BAD", 1: "MODERATE", 2: "GOOD"}
PRED_TO_NUM = {"BAD": 0, "MODERATE": 1, "GOOD": 2}

print("✅ TFLite model loaded")

# -------------------------------
# AI Prediction
# -------------------------------
def predict_soil(soil, temp, hum, light, ph):
    data = np.array([[soil, temp, hum, light, ph]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]["index"], data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]["index"])[0]

    label = LABELS[int(np.argmax(output))]
    confidence = float(np.max(output))
    return label, confidence

# -------------------------------
# ThingSpeak Upload
# -------------------------------
def send_to_thingspeak(soil, soil2, temp, hum, light, ph, status, confidence):
    payload = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": soil,
        "field2": temp,
        "field3": hum,
        "field4": light,
        "field5": ph,
        "field6": PRED_TO_NUM[status],
        "field7": soil2
    }

    try:
        r = requests.post(THINGSPEAK_URL, data=payload, timeout=6)
        if r.status_code == 200:
            print("☁️ Uploaded to ThingSpeak ✅")
        else:
            print(f"⚠️ ThingSpeak error: {r.status_code} {r.text}")
    except Exception as e:
        print("❌ ThingSpeak upload failed:", e)

# -------------------------------
# BLE Notification Handler
# -------------------------------
def handle_notification(sender, data):
    try:
        payload = json.loads(data.decode(errors="ignore"))
        print("\n📡 Received:", payload)

        soil = float(payload["soil"])
        soil2 = float(payload.get("soil2", 0))
        temp = float(payload["temp"])
        hum = float(payload["hum"])
        light = float(payload["light"])
        ph = float(payload["ph"])

        status, conf = predict_soil(soil, temp, hum, light, ph)
        print(f"🌱 AI Prediction: {status} (confidence={conf:.2f})")

        # Upload to ThingSpeak
        send_to_thingspeak(
            soil=soil,
            soil2=soil2,
            temp=temp,
            hum=hum,
            light=light,
            ph=ph,
            status=status,
            confidence=conf
        )

    except Exception as e:
        print("❌ Error parsing BLE data:", e)

# -------------------------------
# BLE Main Loop (stable reconnect)
# -------------------------------
async def main():
    print("🔍 Scanning for BLE device...")
    devices = await BleakScanner.discover(timeout=10)

    target = None
    for d in devices:
        if d.name == DEVICE_NAME:
            target = d
            break

    if not target:
        print("❌ Arduino not found. Make sure it's powered and advertising.")
        return

    print(f"✅ Found {DEVICE_NAME}, address={target.address}")

    while True:
        try:
            print("🔗 Connecting...")
            async with BleakClient(target.address, timeout=15) as client:

                # wait to make service discovery stable
                await asyncio.sleep(2)

                print("📡 Subscribing to notifications...")
                await client.start_notify(CHAR_UUID, handle_notification)

                print("✅ Connected & listening for BLE data...\n")

                while client.is_connected:
                    await asyncio.sleep(1)

                print("⚠️ Device disconnected.")

        except Exception as e:
            print("⚠️ BLE error, retrying in 3 seconds:", e)
            await asyncio.sleep(3)

# -------------------------------
# Run
# -------------------------------
if __name__ == "__main__":
    asyncio.run(main())
