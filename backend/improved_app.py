from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np
import psycopg2
import os
import sys
from flask_cors import CORS

# Inisialisasi Flask
app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

# Load improved model dan preprocessing objects
try:
    with open('diabetes_improved_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('diabetes_scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open('diabetes_features.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    
    print("[INFO] Improved model berhasil dimuat.")
    print(f"[INFO] Feature columns: {feature_columns}")
    
except Exception as e:
    print(f"[ERROR] Gagal memuat improved model: {e}")
    exit(1)

# Koneksi database
try:
    conn = psycopg2.connect(
        dbname="diabetesdb",
        user="postgres", 
        password="Rizkydiska26",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    print("[INFO] Koneksi database berhasil.")
except Exception as e:
    print(f"[ERROR] Gagal konek ke database: {e}")
    exit(1)

def create_features(age, glucose, insulin, bmi):
    """Create all required features including engineered ones"""
    
    features = {
        'Pregnancies': 0,
        'Glucose': glucose,
        'BloodPressure': 70,  
        'SkinThickness': 20,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': 0.3,
        'Age': age
    }
    
    # Engineered features
    features['BMI_Category'] = 0 if bmi < 18.5 else (1 if bmi < 25 else (2 if bmi < 30 else 3))
    features['Age_Category'] = 0 if age < 30 else (1 if age < 50 else 2)
    features['Glucose_Category'] = 0 if glucose < 100 else (1 if glucose < 125 else 2)
    features['BMI_Age_Ratio'] = bmi / age if age > 0 else 0
    features['Glucose_BMI_Ratio'] = glucose / bmi if bmi > 0 else 0
    
    return features

# Endpoint untuk root URL (menampilkan halaman awal atau info)
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Diabetes Prediction API",
        "endpoints": [
            "/predict (POST): Predict diabetes based on user input.",
            "/model_info (GET): Information about the model and features.",
            "/predict (GET): Form to input data for prediction."
        ]
    })

# Endpoint untuk menampilkan formulir input data (GET)
@app.route('/predict', methods=['GET'])
def show_form():
    return render_template('predict_form.html')  # Mengarahkan ke formulir input

# Endpoint untuk prediksi (POST)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Menerima data JSON yang dikirim dari frontend
    
    # Validasi dan konversi
    try:
        age = float(data['age'])
        glucose = float(data['glucose']) 
        insulin = float(data['insulin'])
        bmi = float(data['bmi'])
        
        if age < 1 or age > 120:
            return jsonify({'error': 'Age must be between 1 and 120'}), 400
        if glucose < 50 or glucose > 300:
            return jsonify({'error': 'Glucose must be between 50 and 300 mg/dL'}), 400
        if bmi < 10 or bmi > 60:
            return jsonify({'error': 'BMI must be between 10 and 60'}), 400
        if insulin < 0 or insulin > 500:
            return jsonify({'error': 'Insulin must be between 0 and 500 μU/mL'}), 400
            
    except (ValueError, KeyError) as e:
        return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
    
    try:
        if scaler is not None:
            features_dict = create_features(age, glucose, insulin, bmi)
            input_array = np.array([[features_dict[col] for col in feature_columns]])
            input_scaled = scaler.transform(input_array)
            
            # Prediksi
            probabilities = model.predict_proba(input_scaled)
            prediction_int = model.predict(input_scaled)[0]
            
            prob_diabetes = probabilities[0][1]
            
        else:
            input_data = pd.DataFrame([{
                'age': age,
                'bmi': bmi, 
                'glucose': glucose,
                'insulin': insulin
            }])
            
            probabilities = model.predict_proba(input_data)
            prob_diabetes = probabilities[0][1]
            prediction_int = 1 if prob_diabetes > 0.6 else 0
        
        # Menyimpan hasil ke database
        try:
            cursor.execute(
                "INSERT INTO predictions (age, bmi, glucose, insulin, prediction) VALUES (%s, %s, %s, %s, %s)",
                (age, bmi, glucose, insulin, prediction_int)
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        
        return jsonify({
            'prediction': int(prediction_int),
            'probability': float(prob_diabetes),
            'confidence': 'High' if abs(prob_diabetes - 0.5) > 0.3 else 'Medium',
            'model_type': 'improved' if scaler is not None else 'basic'
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Endpoint untuk informasi model"""
    return jsonify({
        'model_type': 'improved' if scaler is not None else 'basic',
        'features': feature_columns,
        'feature_count': len(feature_columns),
        'has_scaler': scaler is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Jalankan Flask di IP lokal agar dapat diakses dari jaringan
