{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import numpy as np\
import pandas as pd\
from sklearn.model_selection import train_test_split\
from tensorflow.keras.models import Sequential\
from tensorflow.keras.layers import Dense\
from tensorflow.keras.utils import to_categorical\
import tensorflow as tf\
\
# -----------------------------------------\
# 1. Generate synthetic dataset\
# -----------------------------------------\
\
def generate_sample():\
    soil = np.random.randint(0, 1024)\
    light = np.random.randint(0, 1024)\
    ph = np.random.uniform(5.0, 8.0)\
    temp = np.random.uniform(18, 38)\
    hum = np.random.uniform(20, 95)\
\
    # Label logic\
    if soil < 300 or hum < 30:\
        label = 0  # BAD\
    elif 300 <= soil <= 600:\
        label = 1  # MODERATE\
    else:\
        label = 2  # GOOD\
\
    return soil, temp, hum, light, ph, label\
\
samples = 2000\
data = [generate_sample() for _ in range(samples)]\
df = pd.DataFrame(data, columns=["soil", "temp", "hum", "light", "ph", "label"])\
\
# -----------------------------------------\
# 2. Prepare dataset\
# -----------------------------------------\
\
X = df[["soil", "temp", "hum", "light", "ph"]].values\
y = to_categorical(df["label"], 3)  # 3 classes\
\
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\
\
# -----------------------------------------\
# 3. Build and train neural network\
# -----------------------------------------\
\
model = Sequential([\
    Dense(32, activation="relu", input_shape=(5,)),\
    Dense(32, activation="relu"),\
    Dense(3, activation="softmax")\
])\
\
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])\
model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=1)\
\
loss, acc = model.evaluate(X_test, y_test, verbose=0)\
print("Model accuracy:", acc)\
\
# -----------------------------------------\
# 4. Convert to TFLite\
# -----------------------------------------\
\
converter = tf.lite.TFLiteConverter.from_keras_model(model)\
tflite_model = converter.convert()\
\
with open("soil_model.tflite", "wb") as f:\
    f.write(tflite_model)\
\
print("TFLite model saved as soil_model.tflite")\
}