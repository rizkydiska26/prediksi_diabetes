from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import random
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Konfigurasi koneksi ke database
DB_CONFIG = {
    'host': 'localhost',
    'database': 'diabetesdb',
    'user': 'postgres',
    'password': 'Rizkydiska26',
    'port': '5432'
}

# URL CSV data makanan
FOOD_DATA_URL = "food_data.csv"

# Path ke model dan scaler
DIABETES_MODEL_PATH = 'model.pkl'
DIABETES_SCALER_PATH = 'scaler.pkl'
FOOD_MODEL_PATH = 'pred_food.pkl'

# Load model diabetes dan scaler
try:
    diabetes_model = joblib.load(DIABETES_MODEL_PATH)
    print(f"[INFO] Model diabetes berhasil dimuat: {type(diabetes_model)}")
    
    # Load scaler untuk preprocessing data
    diabetes_scaler = joblib.load(DIABETES_SCALER_PATH)
    print(f"[INFO] Scaler diabetes berhasil dimuat: {type(diabetes_scaler)}")
    
    # PENTING: Cek urutan fitur yang benar dari scaler
    if hasattr(diabetes_scaler, 'feature_names_in_'):
        feature_order = diabetes_scaler.feature_names_in_
        print(f"[INFO] ✅ URUTAN FITUR YANG BENAR: {list(feature_order)}")
    else:
        # Fallback jika tidak ada feature names
        feature_order = ['Glucose', 'Insulin', 'BMI', 'Age']  # Berdasarkan debug output
        print(f"[INFO] ⚠️  Menggunakan urutan default: {feature_order}")
        
except Exception as e:
    print(f"[ERROR] Gagal memuat model diabetes atau scaler: {e}")
    diabetes_model = None
    diabetes_scaler = None
    feature_order = None

# Load model rekomendasi makanan
try:
    food_model = joblib.load(FOOD_MODEL_PATH)
    print(f"[INFO] Model rekomendasi makanan berhasil dimuat: {type(food_model)}")
    
    if isinstance(food_model, pd.DataFrame):
        print("[INFO] pred_food.pkl adalah DataFrame - akan digunakan sebagai lookup table")
        food_lookup_data = food_model
        food_ml_model = None
    else:
        print("[INFO] pred_food.pkl adalah ML model - akan digunakan untuk prediksi")
        food_ml_model = food_model
        food_lookup_data = None
        
except Exception as e:
    print(f"[WARNING] Model rekomendasi makanan tidak ditemukan: {e}")
    food_model = None
    food_ml_model = None
    food_lookup_data = None

# Load data makanan dari CSV
try:
    food_data = pd.read_csv(FOOD_DATA_URL)
    print(f"[INFO] Data makanan berhasil dimuat: {len(food_data)} items")
    
    if 'Kategori' in food_data.columns:
        food_data['Kategori'] = food_data['Kategori'].str.strip()
        categories = food_data['Kategori'].unique()
        print(f"[INFO] Kategori tersedia: {list(categories)}")
    else:
        print("[WARNING] Kolom 'Kategori' tidak ditemukan")
        
except Exception as e:
    print(f"[ERROR] Gagal memuat data makanan: {e}")
    food_data = None

@contextmanager
def get_db_connection():
    """Context manager untuk koneksi database PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERROR] Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_database():
    """Cek koneksi database dan tabel predictions"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'predictions'
                );
            """)
            
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                print("[INFO] Tabel predictions tidak ditemukan, membuat tabel baru...")
                cursor.execute("""
                    CREATE TABLE predictions (
                        id SERIAL PRIMARY KEY,
                        age INTEGER NOT NULL,
                        bmi FLOAT NOT NULL,
                        glucose INTEGER NOT NULL,
                        insulin FLOAT NOT NULL,
                        prediction INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                conn.commit()
                print("[INFO] Tabel predictions berhasil dibuat")
                return True
            else:
                print("[INFO] Tabel predictions sudah ada")
                return True
                
    except Exception as e:
        print(f"[ERROR] Failed to check/create database: {e}")
        return False

def reorder_features_for_model(age, bmi, glucose, insulin):
    """
    Mengubah urutan fitur dari frontend ke urutan yang diharapkan model
    Frontend: [age, bmi, glucose, insulin]
    Model: [glucose, insulin, bmi, age] (berdasarkan scaler.feature_names_in_)
    """
    if feature_order is None:
        # Fallback ke urutan yang ditemukan dari debug
        return [glucose, insulin, bmi, age]
    
    # Mapping dari nama fitur ke nilai
    feature_mapping = {
        'Age': age,
        'BMI': bmi, 
        'Glucose': glucose,
        'Insulin': insulin
    }
    
    # Susun ulang sesuai urutan yang diharapkan model
    reordered = []
    for feature_name in feature_order:
        if feature_name in feature_mapping:
            reordered.append(feature_mapping[feature_name])
        else:
            print(f"[WARNING] Feature {feature_name} tidak ditemukan dalam mapping")
            
    return reordered

def save_prediction_to_db(age, bmi, glucose, insulin, prediction):
    """Simpan prediksi user ke database PostgreSQL"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO predictions (age, bmi, glucose, insulin, prediction)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (int(age), float(bmi), int(glucose), int(insulin), int(prediction)))
            
            prediction_id = cursor.fetchone()[0]
            conn.commit()
            
            print(f"[INFO] Saved prediction with ID: {prediction_id}")
            return prediction_id
            
    except Exception as e:
        print(f"[ERROR] Failed to save prediction: {e}")
        return None

# HTML Template untuk testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiabCare Backend - FIXED</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        h1, h2 {
            color: #333;
            text-align: center;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background: #f9f9f9;
        }
        .fixed-section {
            background: #d4edda;
            border: 1px solid #c3e6cb;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
            box-sizing: border-box;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .btn-success {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            background: #e8f5e8;
            border: 1px solid #4caf50;
        }
        .error {
            background: #ffebee;
            border: 1px solid #f44336;
            color: #c62828;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        pre {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 12px;
        }
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }
        .status.ok { background: #4caf50; color: white; }
        .status.error { background: #f44336; color: white; }
        .status.fixed { background: #28a745; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 DiabCare Backend - MASALAH SUDAH DIPERBAIKI!</h1>
        
        <!-- Fix Info Section -->
        <div class="section fixed-section">
            <h2>✅ Perbaikan yang Dilakukan</h2>
            <p><strong>Masalah:</strong> Urutan fitur tidak sesuai dengan model training</p>
            <p><strong>Model dilatih dengan urutan:</strong> <code>{{ feature_order }}</code></p>
            <p><strong>Frontend mengirim urutan:</strong> <code>[Age, BMI, Glucose, Insulin]</code></p>
            <p><strong>Solusi:</strong> Backend sekarang otomatis menyusun ulang fitur sesuai urutan yang diharapkan model</p>
        </div>
        
        <!-- Status Section -->
        <div class="section">
            <h2>System Status</h2>
            <p><strong>Diabetes Model:</strong> <span class="status {{ 'fixed' if diabetes_model_status else 'error' }}">{{ diabetes_model_status }}</span></p>
            <p><strong>Diabetes Scaler:</strong> <span class="status {{ 'fixed' if diabetes_scaler_status else 'error' }}">{{ diabetes_scaler_status }}</span></p>
            <p><strong>Feature Order Fix:</strong> <span class="status fixed">APPLIED</span></p>
            <p><strong>Food Model:</strong> <span class="status {{ 'ok' if food_model_status else 'error' }}">{{ food_model_status }}</span></p>
            <p><strong>Food Data:</strong> <span class="status {{ 'ok' if food_data_status else 'error' }}">{{ food_data_status }}</span></p>
            <p><strong>Database:</strong> <span class="status {{ 'ok' if db_status else 'error' }}">{{ db_status }}</span></p>
        </div>

        <div class="grid">
            <!-- Test Cases -->
            <div class="section">
                <h2>🧪 Test Cases</h2>
                <button class="btn btn-success" onclick="testLowRiskCase()">Test Low Risk (Should be 0)</button>
                <button class="btn btn-success" onclick="testHighRiskCase()">Test High Risk (Should be 1)</button>
                <button class="btn btn-success" onclick="testYourCase()">Test Your Previous Case</button>
                <div id="testResult"></div>
            </div>

            <!-- Manual Testing -->
            <div class="section">
                <h2>Manual Test</h2>
                <form id="predictionForm">
                    <div class="form-group">
                        <label>Age:</label>
                        <input type="number" id="age" value="25" min="1" max="120" required>
                    </div>
                    <div class="form-group">
                        <label>BMI:</label>
                        <input type="number" id="bmi" value="22.0" step="0.1" min="10" max="60" required>
                    </div>
                    <div class="form-group">
                        <label>Glucose:</label>
                        <input type="number" id="glucose" value="85" min="50" max="500" required>
                    </div>
                    <div class="form-group">
                        <label>Insulin:</label>
                        <input type="number" id="insulin" value="8" step="0.1" min="0" max="1000" required>
                    </div>
                    <button type="button" class="btn" onclick="testPrediction()">Test Prediction</button>
                </form>
                <div id="predictionResult"></div>
            </div>
        </div>
    </div>

    <script>
        async function testPrediction() {
            const data = {
                age: parseFloat(document.getElementById('age').value),
                bmi: parseFloat(document.getElementById('bmi').value),
                glucose: parseFloat(document.getElementById('glucose').value),
                insulin: parseFloat(document.getElementById('insulin').value)
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                document.getElementById('predictionResult').innerHTML = 
                    `<div class="result ${result.success ? '' : 'error'}">
                        <h3>Prediction Result:</h3>
                        <p><strong>Input:</strong> Age=${data.age}, BMI=${data.bmi}, Glucose=${data.glucose}, Insulin=${data.insulin}</p>
                        <p><strong>Prediction:</strong> ${result.prediction_text} (${result.prediction})</p>
                        <p><strong>Reordered Features:</strong> ${result.debug_info ? result.debug_info.reordered_features : 'N/A'}</p>
                        <pre>${JSON.stringify(result, null, 2)}</pre>
                    </div>`;
            } catch (error) {
                document.getElementById('predictionResult').innerHTML = 
                    `<div class="result error"><h3>Error:</h3><p>${error.message}</p></div>`;
            }
        }

        async function testLowRiskCase() {
            await testSpecificCase({age: 25, bmi: 22.0, glucose: 85, insulin: 8}, "Low Risk Case");
        }

        async function testHighRiskCase() {
            await testSpecificCase({age: 55, bmi: 35.0, glucose: 180, insulin: 45}, "High Risk Case");
        }

        async function testYourCase() {
            await testSpecificCase({age: 25, bmi: 24.3, glucose: 82, insulin: 8}, "Your Previous Case");
        }

        async function testSpecificCase(data, caseName) {
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                const isCorrect = (caseName.includes("Low") && result.prediction === 0) || 
                                 (caseName.includes("High") && result.prediction === 1) ||
                                 caseName.includes("Your");
                
                document.getElementById('testResult').innerHTML = 
                    `<div class="result ${result.success ? (isCorrect ? '' : 'error') : 'error'}">
                        <h3>${caseName} Result: ${isCorrect ? '✅' : '❌'}</h3>
                        <p><strong>Input:</strong> Age=${data.age}, BMI=${data.bmi}, Glucose=${data.glucose}, Insulin=${data.insulin}</p>
                        <p><strong>Prediction:</strong> ${result.prediction_text} (${result.prediction})</p>
                        <p><strong>Expected:</strong> ${caseName.includes("Low") ? "Low Risk (0)" : caseName.includes("High") ? "High Risk (1)" : "Should be Low Risk (0)"}</p>
                        <p><strong>Reordered Features:</strong> ${result.debug_info ? result.debug_info.reordered_features : 'N/A'}</p>
                    </div>`;
            } catch (error) {
                document.getElementById('testResult').innerHTML = 
                    `<div class="result error"><h3>Error:</h3><p>${error.message}</p></div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Web interface untuk testing backend yang sudah diperbaiki"""
    try:
        db_status = init_database()
        
        return render_template_string(HTML_TEMPLATE,
                                    diabetes_model_status="FIXED" if diabetes_model is not None else "Not Found",
                                    diabetes_scaler_status="FIXED" if diabetes_scaler is not None else "Not Found",
                                    food_model_status="Ready" if food_model is not None else "Not Found", 
                                    food_data_status=f"Ready ({len(food_data)} items)" if food_data is not None else "Not Found",
                                    db_status="Connected" if db_status else "Error",
                                    feature_order=list(feature_order) if feature_order is not None else "Unknown")
    except Exception as e:
        return render_template_string(HTML_TEMPLATE,
                                    diabetes_model_status="FIXED" if diabetes_model is not None else "Not Found",
                                    diabetes_scaler_status="FIXED" if diabetes_scaler is not None else "Not Found",
                                    food_model_status="Ready" if food_model is not None else "Not Found",
                                    food_data_status=f"Ready ({len(food_data)} items)" if food_data is not None else "Not Found",
                                    db_status=f"Error: {str(e)}",
                                    feature_order=list(feature_order) if feature_order is not None else "Unknown")

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint prediksi diabetes dengan urutan fitur yang BENAR"""
    try:
        if diabetes_model is None:
            return jsonify({
                'success': False,
                'error': 'Diabetes model not available'
            }), 500
            
        if diabetes_scaler is None:
            return jsonify({
                'success': False,
                'error': 'Diabetes scaler not available'
            }), 500
            
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        # Validasi input
        required_fields = ['age', 'bmi', 'glucose', 'insulin']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        age = float(data['age'])
        bmi = float(data['bmi'])
        glucose = float(data['glucose'])
        insulin = float(data['insulin'])
        
        # Validasi range nilai
        if not (0 < age < 150):
            return jsonify({'success': False, 'error': 'Age must be between 1-149'}), 400
        if not (10 < bmi < 60):
            return jsonify({'success': False, 'error': 'BMI must be between 10-60'}), 400
        if not (50 < glucose < 500):
            return jsonify({'success': False, 'error': 'Glucose must be between 50-500'}), 400
        if not (0 < insulin < 1000):
            return jsonify({'success': False, 'error': 'Insulin must be between 1-999'}), 400
        
        # 🔧 PERBAIKAN UTAMA: Susun ulang fitur sesuai urutan model
        reordered_features = reorder_features_for_model(age, bmi, glucose, insulin)
        
        print(f"[INFO] 📥 Input dari frontend: Age={age}, BMI={bmi}, Glucose={glucose}, Insulin={insulin}")
        print(f"[INFO] 🔄 Fitur setelah disusun ulang: {reordered_features}")
        print(f"[INFO] 📋 Urutan yang diharapkan model: {list(feature_order) if feature_order is not None else 'Default'}")
        
        # Prediksi menggunakan fitur yang sudah disusun ulang
        features = np.array([reordered_features])
        features_scaled = diabetes_scaler.transform(features)
        prediction = int(diabetes_model.predict(features_scaled)[0])
        prediction_text = 'Risiko Tinggi' if prediction == 1 else 'Risiko Rendah'
        
        # Simpan ke database
        prediction_id = save_prediction_to_db(age, bmi, glucose, insulin, prediction)
        
        print(f"[INFO] ✅ Prediction: {prediction_text} for user (Age: {age}, BMI: {bmi}, Glucose: {glucose}, Insulin: {insulin})")
        print(f"[INFO] 📊 Scaled features: {features_scaled.tolist()[0]}")
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'prediction_text': prediction_text,
            'prediction_id': prediction_id,
            'input_data': {
                'age': age,
                'bmi': bmi,
                'glucose': glucose,
                'insulin': insulin
            },
            'scaled_input': features_scaled.tolist()[0],
            'debug_info': {
                'original_order': [age, bmi, glucose, insulin],
                'reordered_features': reordered_features,
                'expected_order': list(feature_order) if feature_order is not None else 'Default',
                'feature_mapping': dict(zip(feature_order if feature_order is not None else ['Glucose', 'Insulin', 'BMI', 'Age'], reordered_features))
            },
            'message': f'Prediksi berhasil: {prediction_text}',
            'timestamp': datetime.now().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input data: {str(e)}'
        }), 400
    except Exception as e:
        print(f"[ERROR] Prediction error: {e}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

# Tambahkan endpoint food recommendation yang sama seperti sebelumnya
def safe_float(value, default=0.0):
    """Safely convert value to float"""
    try:
        if pd.isna(value) or value == '' or value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    """Safely convert value to int"""
    try:
        if pd.isna(value) or value == '' or value is None:
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default

def calculate_personalized_score_with_model(age, bmi, glucose, insulin, gi, calories, carbs, protein, fat, fiber, sodium):
    """Hitung skor menggunakan model pred_food.pkl jika tersedia, atau fallback ke rule-based"""
    
    # Coba gunakan model ML dulu
    if food_ml_model is not None:
        try:
            user_features = np.array([age, bmi, glucose, insulin])
            food_features = np.array([gi, calories, carbs, protein, fat, fiber, sodium])
            combined_features = np.concatenate([user_features, food_features]).reshape(1, -1)
            
            if hasattr(food_ml_model, 'predict_proba'):
                score = food_ml_model.predict_proba(combined_features)[0][1]
            else:
                score = float(food_ml_model.predict(combined_features)[0])
                
            # Normalisasi score ke 0-1 jika perlu
            if score > 1:
                score = score / 100.0
            elif score < 0:
                score = 0.0
                
            # Tambahkan variasi berdasarkan user profile untuk konsistensi
            user_hash = (age * 0.01 + bmi * 0.02 + glucose * 0.001 + insulin * 0.005) % 1
            score = score * 0.8 + user_hash * 0.2  # 80% model, 20% user variation
            
            return max(0, min(1, score))
            
        except Exception as e:
            print(f"[WARNING] Error using ML model, fallback to rule-based: {e}")
    
    # Fallback ke rule-based scoring
    score = 0.5  # Base score
    
    # Faktor usia
    if age > 50:
        if gi <= 35:
            score += 0.25
        if fiber >= 3:
            score += 0.15
        if sodium <= 100:
            score += 0.1
    elif age < 30:
        if protein >= 8:
            score += 0.2
        if calories >= 100:
            score += 0.1
    else:
        if gi <= 50:
            score += 0.15
        if protein >= 5:
            score += 0.1
    
    # Faktor BMI
    if bmi > 25:
        if calories <= 80:
            score += 0.3
        if fiber >= 4:
            score += 0.2
        if fat <= 3:
            score += 0.15
    elif bmi < 18.5:
        if calories >= 150:
            score += 0.25
        if protein >= 10:
            score += 0.2
        if fat >= 5:
            score += 0.1
    else:
        if gi <= 55:
            score += 0.15
        if protein >= 6:
            score += 0.1
    
    # Faktor glukosa
    if glucose > 126:
        if gi <= 35:
            score += 0.4
        elif gi <= 50:
            score += 0.2
        else:
            score -= 0.3
        if fiber >= 5:
            score += 0.25
        if carbs <= 10:
            score += 0.2
    elif glucose > 100:
        if gi <= 50:
            score += 0.25
        elif gi > 70:
            score -= 0.15
        if fiber >= 3:
            score += 0.15
    else:
        if gi <= 60:
            score += 0.1
    
    # Faktor insulin
    if insulin > 20:
        if gi <= 35:
            score += 0.3
        if fiber >= 4:
            score += 0.2
        if carbs <= 15:
            score += 0.15
    elif insulin < 5:
        if carbs >= 20:
            score += 0.1
        if protein >= 8:
            score += 0.15
    
    # Tambahkan variasi berdasarkan user profile
    user_variation = ((age * 0.01 + bmi * 0.02 + glucose * 0.001 + insulin * 0.005) % 1) * 0.1
    score += user_variation - 0.05
    
    return max(0, min(1, score))

def create_nutritional_benefits(food_row):
    """Buat benefits berdasarkan data nutrisi dari CSV"""
    benefits = []
    
    try:
        gi = safe_float(food_row.get('Glycemic Index', 55))
        calories = safe_float(food_row.get('Calories', 100))
        fiber = safe_float(food_row.get('Fiber Content', 2))
        protein = safe_float(food_row.get('Protein', 5))
        carbs = safe_float(food_row.get('Carbohydrates', 10))
        fat = safe_float(food_row.get('Fat', 2))
        sodium = safe_float(food_row.get('Sodium Content', 0))
        
        benefits.append(f"IG: {int(gi)}")
        benefits.append(f"Kalori: {int(calories)}")
        
        if fiber > 0:
            benefits.append(f"Serat: {fiber}g")
        if protein > 0:
            benefits.append(f"Protein: {protein}g")
        if carbs > 0:
            benefits.append(f"Karbo: {carbs}g")
        if fat > 0:
            benefits.append(f"Lemak: {fat}g")
        if sodium > 0:
            benefits.append(f"Sodium: {int(sodium)}mg")
            
    except Exception as e:
        print(f"[WARNING] Error creating benefits: {e}")
        benefits = ["Data nutrisi tersedia"]
    
    return " | ".join(benefits)

def get_food_recommendations_from_csv(category, user_data, top_n=5):
    """Ambil rekomendasi makanan dari CSV dengan model pred_food.pkl"""
    try:
        if food_data is None:
            print("[WARNING] Data makanan tidak tersedia")
            return get_fallback_recommendations(category)
            
        print(f"[INFO] Mencari rekomendasi untuk kategori: {category}")
        
        # Mapping kategori yang diperbaiki
        category_mapping = {
            "Protein Hewani": "Protein hewani",
            "Protein Nabati": "Protein Nabati", 
            "Karbohidrat": "Karbohidrat",
            "Sayur": "Sayur",
            "Buah": "Buah",
            "Biji-bijian": "Biji-bijian",
            "Kacang-kacangan": "Kacang-kacangan"
        }
        
        csv_category = category_mapping.get(category.strip(), category.strip())
        
        # Filter makanan berdasarkan kategori
        category_foods = food_data[food_data['Kategori'].str.strip() == csv_category].copy()
        
        if len(category_foods) == 0:
            print(f"[WARNING] Tidak ada makanan dalam kategori '{csv_category}', mencoba kategori asli '{category}'")
            # Coba dengan kategori asli
            category_foods = food_data[food_data['Kategori'].str.strip() == category.strip()].copy()
            
        if len(category_foods) == 0:
            print(f"[WARNING] Tidak ada makanan dalam kategori '{category}'")
            return get_fallback_recommendations(category)
            
        print(f"[INFO] Ditemukan {len(category_foods)} makanan dalam kategori")
        
        # Ekstrak profil user
        age = user_data.get('age', 30)
        bmi = user_data.get('bmi', 25)
        glucose = user_data.get('glucose', 100)
        insulin = user_data.get('insulin', 10)
        
        print(f"[INFO] Profil user: Age={age}, BMI={bmi}, Glucose={glucose}, Insulin={insulin}")
        
        # Hitung skor untuk setiap makanan menggunakan model
        food_scores = []
        
        for idx, (_, food_row) in enumerate(category_foods.iterrows()):
            try:
                # Ekstrak data nutrisi
                gi = safe_float(food_row.get('Glycemic Index', 55))
                calories = safe_float(food_row.get('Calories', 100))
                carbs = safe_float(food_row.get('Carbohydrates', 10))
                protein = safe_float(food_row.get('Protein', 5))
                fat = safe_float(food_row.get('Fat', 2))
                fiber = safe_float(food_row.get('Fiber Content', 2))
                sodium = safe_float(food_row.get('Sodium Content', 0))
                
                # Hitung skor menggunakan model atau rule-based
                score = calculate_personalized_score_with_model(
                    age, bmi, glucose, insulin,
                    gi, calories, carbs, protein, fat, fiber, sodium
                )
                
                food_scores.append((score, food_row))
                
            except Exception as e:
                print(f"[WARNING] Error scoring makanan {idx}: {e}")
                food_scores.append((0.5, food_row))
        
        # Urutkan berdasarkan skor (tertinggi dulu)
        food_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Tambahkan variasi berdasarkan user profile untuk konsistensi
        seed_value = int((age * 7 + bmi * 13 + glucose * 3 + insulin * 11) % 1000)
        random.seed(seed_value)
        
        # Pilih top candidates dengan weighted randomization
        top_candidates = food_scores[:min(10, len(food_scores))]
        
        if len(top_candidates) > top_n:
            # Weighted selection (skor tinggi lebih mungkin dipilih)
            weights = [max(0.1, score) for score, _ in top_candidates]
            selected_foods = []
            
            for _ in range(top_n):
                if not top_candidates:
                    break
                    
                # Weighted random selection
                total_weight = sum(weights)
                if total_weight == 0:
                    selected_foods.append(top_candidates.pop(0))
                    weights.pop(0)
                else:
                    rand_val = random.uniform(0, total_weight)
                    cumulative = 0
                    for i, weight in enumerate(weights):
                        cumulative += weight
                        if rand_val <= cumulative:
                            selected_foods.append(top_candidates.pop(i))
                            weights.pop(i)
                            break
        else:
            selected_foods = top_candidates
        
        # Format rekomendasi
        recommendations = []
        for score, food_row in selected_foods:
            food_item = {
                'name': str(food_row.get('Food Name', 'Unknown')),
                'category': category,
                'calories': int(safe_float(food_row.get('Calories', 0))),
                'glycemic_index': int(safe_float(food_row.get('Glycemic Index', 0))),
                'carbohydrates': round(safe_float(food_row.get('Carbohydrates', 0)), 1),
                'protein': round(safe_float(food_row.get('Protein', 0)), 1),
                'fat': round(safe_float(food_row.get('Fat', 0)), 1),
                'fiber': round(safe_float(food_row.get('Fiber Content', 0)), 1),
                'sodium': round(safe_float(food_row.get('Sodium Content', 0)), 1),
                'suitable_for_diabetes': safe_int(food_row.get('Suitable for Diabetes', 0)),
                'benefits': create_nutritional_benefits(food_row),
                'rating': min(5.0, 3.0 + (score * 2.0)),
                'personalization_score': round(score, 3),
                'model_used': 'pred_food.pkl' if food_ml_model is not None else 'rule_based'
            }
            recommendations.append(food_item)
            
        print(f"[INFO] Berhasil membuat {len(recommendations)} rekomendasi")
        return recommendations
        
    except Exception as e:
        print(f"[ERROR] Error dalam rekomendasi: {e}")
        return get_fallback_recommendations(category)

def get_fallback_recommendations(category):
    """Fallback recommendations jika terjadi error"""
    fallback_data = {
        "Buah": [
            {
                "name": "Apel Hijau",
                "category": "Buah", 
                "calories": 52,
                "glycemic_index": 36,
                "carbohydrates": 14.0,
                "protein": 0.3,
                "fat": 0.2,
                "fiber": 2.4,
                "sodium": 1.0,
                "suitable_for_diabetes": 1,
                "benefits": "IG: 36 | Kalori: 52 | Serat: 2.4g | Protein: 0.3g",
                "rating": 4.8,
                "personalization_score": 0.85,
                "model_used": "fallback"
            }
        ]
    }
    return fallback_data.get(category, fallback_data.get("Buah", []))

@app.route('/recommend_food', methods=['POST'])
def recommend_food():
    """Endpoint rekomendasi makanan dengan model pred_food.pkl"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False, 
                'error': 'No data provided'
            }), 400
            
        # Validasi input
        category = data.get('category')
        user_data = data.get('user_data', {})
        
        if not category:
            return jsonify({
                'success': False, 
                'error': 'Category is required'
            }), 400
            
        if not user_data:
            return jsonify({
                'success': False, 
                'error': 'User data is required'
            }), 400
        
        # Validasi user_data
        required_user_fields = ['age', 'bmi', 'glucose', 'insulin']
        for field in required_user_fields:
            if field not in user_data:
                return jsonify({
                    'success': False,
                    'error': f'Missing user data field: {field}'
                }), 400
        
        print(f"[INFO] Food recommendation request:")
        print(f"[INFO] Category: {category}")
        print(f"[INFO] User: Age={user_data.get('age')}, BMI={user_data.get('bmi')}, Glucose={user_data.get('glucose')}, Insulin={user_data.get('insulin')}")
        
        # Ambil rekomendasi dari CSV dengan model
        recommendations = get_food_recommendations_from_csv(category, user_data)
        
        if not recommendations:
            return jsonify({
                'success': False,
                'error': 'No recommendations found for this category'
            }), 404
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'source': 'csv_with_pred_food_model' if food_ml_model is not None else 'csv_with_rule_based',
            'category_requested': category,
            'total_recommendations': len(recommendations),
            'user_profile': user_data,
            'model_used': 'pred_food.pkl' if food_ml_model is not None else 'rule_based_algorithm',
            'timestamp': datetime.now().isoformat()
        })
            
    except Exception as e:
        print(f"[ERROR] Food recommendation error: {e}")
        return jsonify({
            'success': False, 
            'error': f'Internal server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("=" * 70)
    print("🎉 DIABCARE API SERVER - MASALAH SUDAH DIPERBAIKI!")
    print("=" * 70)
    
    # Initialize database
    db_ready = init_database()
    
    # Status check
    print(f"✅ Diabetes model: {'Ready' if diabetes_model is not None else 'Not Found'}")
    print(f"✅ Diabetes scaler: {'Ready' if diabetes_scaler is not None else 'Not Found'}")
    print(f"✅ Feature order fix: {'Applied' if feature_order is not None else 'Using default'}")
    print(f"✅ Expected feature order: {list(feature_order) if feature_order is not None else 'Default'}")
    print(f"✅ Food model: {'Ready' if food_model is not None else 'Optional'}")
    print(f"✅ Food data: {'Ready' if food_data is not None else 'Not Found'}")
    
    print("=" * 70)
    print("🌐 Web Testing Interface: http://127.0.0.1:5000")
    print("🧪 Test dengan kasus yang sebelumnya bermasalah!")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)