# logistics/ai_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def build_and_train_model(X_train, y_train):
    """
    建立一個簡單的全連接神經網絡模型來預測高峰時段
    X_train: 特徵矩陣 (例如：時段、運送量、設備狀態等)
    y_train: 標籤 (例如：是否為高峰時段, 0 或 1)
    """
    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),  # 第一層隱藏層
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')  # 輸出層，使用 sigmoid 做二分類
    ])
    
    # 編譯模型
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    # 訓練模型
    model.fit(X_train, y_train, epochs=20, batch_size=16, validation_split=0.2)
    
    return model

def predict_peak_period(model, X_test):
    """
    使用訓練好的模型進行預測
    X_test: 測試資料的特徵矩陣
    回傳預測結果 (機率值)
    """
    predictions = model.predict(X_test)
    return predictions
