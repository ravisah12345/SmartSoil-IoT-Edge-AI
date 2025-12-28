# SmartSoil
## An IoT and Edge AI–Enabled Intelligent Plant Monitoring System

SmartSoil is an IoT-based plant monitoring system developed for the **COM6017M** module.  
It combines real-time sensing, edge AI inference, cloud analytics, and Telegram notifications
to monitor soil and environmental conditions effectively.

---

## System Architecture

Sensors → Arduino UNO R4 WiFi → BLE →  
Raspberry Pi (Edge AI – TensorFlow Lite) →  
ThingSpeak Cloud (MATLAB Analytics) →  
Telegram Bot → User

---

## Key Features

- Real-time soil and environmental monitoring  
- Edge AI classification (GOOD / MODERATE / BAD)  
- Bluetooth Low Energy (BLE) communication  
- Cloud analytics using ThingSpeak & MATLAB  
- Telegram notifications with anti-spam logic  

---

## Hardware Used

- Arduino UNO R4 WiFi  
- Raspberry Pi 4 (8GB)  
- Soil moisture sensor  
- pH sensor  
- Light sensor (LDR)  
- DHT11 temperature & humidity sensor  
- Soil EC / secondary soil sensor  

---

## Software & Technologies

## Software & Technologies

- Arduino IDE  
- Python 3.11  
- TensorFlow Lite  
- MATLAB (ThingSpeak Analytics)  
- ThingSpeak Dashboard (Data Visualisation)  
- Telegram Bot API  
- Bluetooth Low Energy (BLE)  

---

## Repository Structure

SmartSoil-IoT-Edge-AI/
├── Arduino/
├── RaspberryPi/
│ ├── soil_pipeline.py
│ ├── generate_tflite_model.py
│ ├── soil_model.tflite
│ └── requirements.txt
├── MATLAB/
└── README.md


---

## Edge AI Model

The Edge AI model runs locally on the Raspberry Pi using TensorFlow Lite.
It classifies soil condition into:
- GOOD
- MODERATE
- BAD

This enables low-latency decision making without relying fully on the cloud.

---

## Start SmartSoil System (Raspberry Pi)

Run the following commands on the Raspberry Pi terminal:

```bash

cd ~/smartsoil
source ai_env/bin/activate
pip install -r requirements.txt
python soil_pipeline.py

```

-----

## Once running, the system will:

Receive sensor data via BLE
Perform Edge AI inference
Upload data to ThingSpeak
Send Telegram notifications when required

----

## Telegram Notifications

Telegram is used as the user notification layer.
Alerts are sent only when the system state changes
(OK → Warning → Danger or recovery to OK).

----

## HOW React, ThingHTTP & Telegram CONNECT (MENTAL MODEL)

MATLAB Analytics
        ↓
   Alert Level Field
        ↓
ThingSpeak React
        ↓
   ThingHTTP Trigger
        ↓
Telegram Bot API
        ↓
      User

React = decision maker
ThingHTTP = messenger
Telegram = delivery platform  
---

##  Project Screenshots

Screenshots of the ThingSpeak dashboard, Telegram notifications, and the physical system
setup are available in the `Docs/` directory.


---

## Demonstration Video

https://www.youtube.com/watch?v=umyJOh03-Co


---

## Security Note

API keys, Telegram bot tokens, and cloud credentials are not included in this repository.
Users must insert their own credentials using placeholder values before deployment.

---

## 👤 Author

Ravi Sah
BSc Computer Science
York St John University

Module: COM6017M – Internet of Things & Edge Computing

