#include <ArduinoBLE.h>
#include <DHT.h>

// ---------- Pin setup ----------
#define SOIL_MOISTURE_PIN A0
#define PH_PIN            A1
#define LIGHT_PIN         A2
#define SOIL2_PIN         A3

#define DHTPIN   2
#define DHTTYPE  DHT11
DHT dht(DHTPIN, DHTTYPE);

// ---------- BLE setup ----------
#define SERVICE_UUID         "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
#define CHARACTERISTIC_UUID_TX "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

BLEService uartService(SERVICE_UUID);
BLECharacteristic txChar(CHARACTERISTIC_UUID_TX, BLERead | BLENotify, 128);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  dht.begin();

  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("SmartSoil-UNO-R4");
  BLE.setDeviceName("SmartSoil-UNO-R4");

  BLE.setAdvertisedService(uartService);
  uartService.addCharacteristic(txChar);
  BLE.addService(uartService);

  BLE.advertise();
  BLE.setConnectable(true);
  BLE.setAdvertisingInterval(32);

  Serial.println("BLE started. Advertising as SmartSoil-UNO-R4...");
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    while (central.connected()) {
      BLE.poll();  // keep BLE responsive

      // ---- Read sensors ----
      int soilRaw  = analogRead(SOIL_MOISTURE_PIN);
      int phRaw    = analogRead(PH_PIN);
      int lightRaw = analogRead(LIGHT_PIN);
      int soil2Raw = analogRead(SOIL2_PIN);

      float h = dht.readHumidity();
      float t = dht.readTemperature();

      if (isnan(h) || isnan(t)) {
        // DHT failed, skip this cycle
        Serial.println("DHT read failed");
        delay(1000);
        continue;
      }

      // Optional: convert raw pH reading (you can calibrate later)
      float phValue = map(phRaw, 0, 1023, 0, 14);  // rough fake scaling

      // ---- Build JSON ----
      String json = "{";
      json += "\"soil\":"   + String(soilRaw)  + ",";
      json += "\"temp\":"   + String(t)        + ",";
      json += "\"hum\":"    + String(h)        + ",";
      json += "\"light\":"  + String(lightRaw) + ",";
      json += "\"ph\":"     + String(phValue)  + ",";
      json += "\"soil2\":"  + String(soil2Raw);
      json += "}";

      Serial.println("Sending: " + json);

      txChar.writeValue(json.c_str());  // send to Raspberry Pi

      delay(1000);  // 1 second between sends
    }

    Serial.println("Disconnected from central.");
  }
}
