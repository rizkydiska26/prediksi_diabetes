from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import numpy as np
import pandas as pd
import joblib
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import random
import hashlib
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'diabetesdb',
    'user': 'postgres',
    'password': 'Rizkydiska26',
    'port': '5432'
}

# File paths
FOOD_DATA_URL = "food_data.csv"
DIABETES_MODEL_PATH = 'model.pkl'
DIABETES_SCALER_PATH = 'scaler.pkl'

# Global variables
diabetes_model = None
diabetes_scaler = None
feature_order = None
food_data = None

# Load diabetes model and scaler
def load_models():
    global diabetes_model, diabetes_scaler, feature_order
    try:
        diabetes_model = joblib.load(DIABETES_MODEL_PATH)
        diabetes_scaler = joblib.load(DIABETES_SCALER_PATH)
        
        if hasattr(diabetes_scaler, 'feature_names_in_'):
            feature_order = diabetes_scaler.feature_names_in_
            print(f"[INFO] Diabetes model loaded successfully")
            print(f"[INFO] Feature order: {list(feature_order)}")
        else:
            feature_order = ['Glucose', 'Insulin', 'BMI', 'Age']
            print(f"[INFO] Diabetes model loaded successfully")
            print(f"[INFO] Using default feature order: {feature_order}")
            
    except Exception as e:
        print(f"[ERROR] Failed to load diabetes model: {e}")
        diabetes_model = None
        diabetes_scaler = None
        feature_order = None

# Load food data
def load_food_data():
    global food_data
    try:
        food_data = pd.read_csv(FOOD_DATA_URL)
        if 'Kategori' in food_data.columns:
            food_data['Kategori'] = food_data['Kategori'].str.strip()
        print(f"[INFO] Food data loaded: {len(food_data)} items")
    except Exception as e:
        print(f"[ERROR] Failed to load food data: {e}")
        food_data = None

# Initialize models and data
load_models()
load_food_data()

# Simple HTML Template for testing
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiabCare Backend Testing</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .status-ok { background: #d4edda; color: #155724; }
        .status-error { background: #f8d7da; color: #721c24; }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-group input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover {
            background: #0056b3;
        }
        .result {
            margin-top: 15px;
            padding: 15px;
            border-radius: 4px;
            background: #d4edda;
            border: 1px solid #c3e6cb;
        }
        .result.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        pre {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 12px;
            max-height: 400px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DiabCare Backend Testing Interface - Enhanced GI Filtering</h1>
        <p>Diabetes prediction and personalized food recommendation system</p>
        
        <h2>System Status</h2>
        <div class="status-grid">
            <div class="status-item">
                <span>Diabetes Model</span>
                <span class="status-{{ 'ok' if diabetes_model_status else 'error' }}">{{ diabetes_model_status }}</span>
            </div>
            <div class="status-item">
                <span>Food Data</span>
                <span class="status-{{ 'ok' if food_data_status else 'error' }}">{{ food_data_status }}</span>
            </div>
            <div class="status-item">
                <span>Database</span>
                <span class="status-{{ 'ok' if db_status else 'error' }}">{{ db_status }}</span>
            </div>
        </div>
        
        <div class="container">
            <h3>Enhanced GI Filtering Rules:</h3>
            <ul>
                <li><strong>Risiko Tinggi:</strong> Hanya makanan GI ≤ 35 (Sangat Rendah)</li>
                <li><strong>Risiko Sedang:</strong> Hanya makanan GI ≤ 50 (Rendah)</li>
                <li><strong>Risiko Rendah:</strong> Hanya makanan GI ≤ 50 (Rendah)</li>
                <li><strong>Personalisasi:</strong> Setiap user mendapat makanan berbeda berdasarkan input unik</li>
            </ul>
        </div>
    </div>

    <div class="container">
        <h2>Diabetes Prediction Test</h2>
        <div class="form-group">
            <label>Age:</label>
            <input type="number" id="age" value="25" min="1" max="120">
        </div>
        <div class="form-group">
            <label>BMI:</label>
            <input type="number" id="bmi" value="22.0" step="0.1" min="10" max="60">
        </div>
        <div class="form-group">
            <label>Glucose:</label>
            <input type="number" id="glucose" value="85" min="50" max="500">
        </div>
        <div class="form-group">
            <label>Insulin:</label>
            <input type="number" id="insulin" value="8" step="0.1" min="0" max="1000">
        </div>
        <button class="btn" onclick="testPrediction()">Test Prediction</button>
        <button class="btn" onclick="testLowRisk()">Test Low Risk</button>
        <button class="btn" onclick="testHighRisk()">Test High Risk</button>
        <div id="predictionResult"></div>
    </div>

    <div class="container">
        <h2>Food Recommendation Test</h2>
        <div class="form-group">
            <label>Category:</label>
            <select id="category">
                <option value="Buah">Buah</option>
                <option value="Sayur">Sayur</option>
                <option value="Karbohidrat">Karbohidrat</option>
                <option value="Protein Hewani">Protein Hewani</option>
                <option value="Protein Nabati">Protein Nabati</option>
                <option value="Biji-bijian">Biji-bijian</option>
                <option value="Kacang-kacangan">Kacang-kacangan</option>
            </select>
        </div>
        <div class="form-group">
            <label>User Age:</label>
            <input type="number" id="userAge" value="45" min="1" max="120">
        </div>
        <div class="form-group">
            <label>User BMI:</label>
            <input type="number" id="userBmi" value="28.5" step="0.1" min="10" max="60">
        </div>
        <div class="form-group">
            <label>User Glucose:</label>
            <input type="number" id="userGlucose" value="120" min="50" max="500">
        </div>
        <div class="form-group">
            <label>User Insulin:</label>
            <input type="number" id="userInsulin" value="15" step="0.1" min="0" max="1000">
        </div>
        <button class="btn" onclick="testFoodRecommendation()">Get Food Recommendations</button>
        <div id="foodResult"></div>
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
                
                let html = `<div class="result">
                    <h3>Prediction Result</h3>
                    <p><strong>Input:</strong> Age=${data.age}, BMI=${data.bmi}, Glucose=${data.glucose}, Insulin=${data.insulin}</p>
                    <p><strong>Prediction:</strong> ${result.prediction_text} (${result.prediction})</p>
                    <p><strong>Risk Level:</strong> ${result.risk_level}</p>`;
                
                if (result.debug_info) {
                    html += `<p><strong>Reordered Features:</strong> ${result.debug_info.reordered_features.join(',')}</p>`;
                }
                
                html += `<pre>${JSON.stringify(result, null, 2)}</pre></div>`;
                
                document.getElementById('predictionResult').innerHTML = html;
            } catch (error) {
                document.getElementById('predictionResult').innerHTML = 
                    `<div class="result error"><h3>Error</h3><p>${error.message}</p></div>`;
            }
        }

        async function testLowRisk() {
            await testSpecificCase({age: 25, bmi: 22, glucose: 85, insulin: 8}, "Low Risk");
        }

        async function testHighRisk() {
            await testSpecificCase({age: 55, bmi: 32, glucose: 140, insulin: 25}, "High Risk");
        }

        async function testSpecificCase(userData, caseName) {
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(userData)
                });
                
                const result = await response.json();
                
                let html = `<div class="result">
                    <h3>${caseName} Test Result</h3>
                    <p><strong>Input:</strong> Age=${userData.age}, BMI=${userData.bmi}, Glucose=${userData.glucose}, Insulin=${userData.insulin}</p>
                    <p><strong>Prediction:</strong> ${result.prediction_text} (${result.prediction})</p>
                    <p><strong>Risk Level:</strong> ${result.risk_level}</p>`;
                
                if (result.debug_info) {
                    html += `<p><strong>Reordered Features:</strong> ${result.debug_info.reordered_features.join(',')}</p>`;
                }
                
                html += `<pre>${JSON.stringify(result, null, 2)}</pre></div>`;
                
                document.getElementById('predictionResult').innerHTML = html;
            } catch (error) {
                document.getElementById('predictionResult').innerHTML = 
                    `<div class="result error"><h3>Error</h3><p>${error.message}</p></div>`;
            }
        }

        async function testFoodRecommendation() {
            const data = {
                category: document.getElementById('category').value,
                user_data: {
                    age: parseFloat(document.getElementById('userAge').value),
                    bmi: parseFloat(document.getElementById('userBmi').value),
                    glucose: parseFloat(document.getElementById('userGlucose').value),
                    insulin: parseFloat(document.getElementById('userInsulin').value)
                }
            };

            try {
                const response = await fetch('/recommend_food', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                let html = `<div class="result">
                    <h3>Food Recommendations</h3>
                    <p><strong>Category:</strong> ${result.category_requested}</p>
                    <p><strong>Risk Level:</strong> ${result.risk_level}</p>
                    <p><strong>GI Filter:</strong> ${result.gi_filter}</p>
                    <p><strong>User Seed:</strong> ${result.debug_info?.user_seed || 'N/A'}</p>
                    <pre>${JSON.stringify(result, null, 2)}</pre>
                </div>`;
                
                document.getElementById('foodResult').innerHTML = html;
            } catch (error) {
                document.getElementById('foodResult').innerHTML = 
                    `<div class="result error"><h3>Error</h3><p>${error.message}</p></div>`;
            }
        }
    </script>
</body>
</html>
"""

@contextmanager
def get_db_connection():
    """Database connection context manager"""
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
    """Initialize database and check tables"""
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
                print("[INFO] Predictions table created")
            else:
                print("[INFO] Predictions table exists")
                    
            return True
                
    except Exception as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        return False

def reorder_features_for_model(age, bmi, glucose, insulin):
    """Reorder features to match model training order"""
    if feature_order is None:
        return [glucose, insulin, bmi, age]
    
    feature_mapping = {
        'Age': age,
        'BMI': bmi, 
        'Glucose': glucose,
        'Insulin': insulin
    }
    
    reordered = []
    for feature_name in feature_order:
        if feature_name in feature_mapping:
            reordered.append(feature_mapping[feature_name])
            
    return reordered

def save_prediction_to_db(age, bmi, glucose, insulin, prediction):
    """Save prediction to database"""
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
            
            return prediction_id
            
    except Exception as e:
        print(f"[ERROR] Failed to save prediction: {e}")
        return None

def determine_diabetes_risk_level(glucose, insulin, bmi, age):
    """Determine diabetes risk level based on health parameters"""
    risk_score = 0
    
    # Glucose scoring (most important factor)
    if glucose >= 126:
        risk_score += 4  # Diabetic range
    elif glucose >= 100:
        risk_score += 2  # Prediabetic range
    elif glucose >= 90:
        risk_score += 1  # Elevated normal
    
    # Insulin scoring
    if insulin >= 25:
        risk_score += 3  # High insulin resistance
    elif insulin >= 15:
        risk_score += 2  # Moderate insulin resistance
    elif insulin >= 10:
        risk_score += 1  # Mild elevation
    
    # BMI scoring
    if bmi >= 30:
        risk_score += 2  # Obese
    elif bmi >= 25:
        risk_score += 1  # Overweight
    
    # Age scoring
    if age >= 60:
        risk_score += 2
    elif age >= 45:
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 7:
        return "Risiko Tinggi"
    elif risk_score >= 4:
        return "Risiko Sedang"
    else:
        return "Risiko Rendah"

def safe_float(value, default=0.0):
    """Safely convert value to float"""
    try:
        if pd.isna(value) or value == '' or value is None:
            return default
        return float(value)
    except (ValueError, TypeError):
        return default

def generate_user_seed(age, bmi, glucose, insulin, category):
    """Generate unique seed for each user input combination"""
    # Create unique string from user data and category with timestamp component
    current_hour = datetime.now().strftime('%Y%m%d%H')  # Changes every hour for variety
    input_string = f"{age}_{bmi}_{glucose}_{insulin}_{category}_{current_hour}"
    
    # Use MD5 hash to create consistent but unique seed
    hash_object = hashlib.md5(input_string.encode())
    seed = int(hash_object.hexdigest()[:8], 16)
    
    return seed

def get_food_recommendations(category, user_data, top_n=5):
    """Enhanced food recommendations with strict GI filtering and personalization"""
    try:
        if food_data is None:
            return [], "LOW_RISK", "No Data", {"error": "Food data not available"}
            
        # Category mapping
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
        category_foods = food_data[food_data['Kategori'].str.strip() == csv_category].copy()
        
        if len(category_foods) == 0:
            category_foods = food_data[food_data['Kategori'].str.strip() == category.strip()].copy()
            
        # Extract user health profile
        age = user_data.get('age', 30)
        bmi = user_data.get('bmi', 25)
        glucose = user_data.get('glucose', 100)
        insulin = user_data.get('insulin', 10)
        
        # Determine diabetes risk level
        risk_level = determine_diabetes_risk_level(glucose, insulin, bmi, age)
        
        # Generate unique seed for this user and category combination
        user_seed = generate_user_seed(age, bmi, glucose, insulin, category)
        
        debug_info = {
            'category_requested': category,
            'csv_category_mapped': csv_category,
            'total_foods_in_category': len(category_foods),
            'user_profile': {'age': age, 'bmi': bmi, 'glucose': glucose, 'insulin': insulin},
            'risk_level': risk_level,
            'user_seed': user_seed
        }
        
        if len(category_foods) == 0:
            debug_info['error'] = 'No foods found in category'
            return [], risk_level, "No GI Filter", debug_info
        
        # ENHANCED GI FILTERING based on risk level
        foods_before_filter = len(category_foods)
        
        if risk_level == "Risiko Tinggi":
            # VERY STRICT: Only foods with GI ≤ 35 (Very Low)
            category_foods = category_foods[
                category_foods['Glycemic Index'].apply(lambda x: safe_float(x, 100) <= 35)
            ].copy()
            gi_filter = "GI ≤ 35 (Sangat Rendah - Untuk Risiko Tinggi)"
            
        elif risk_level == "Risiko Sedang":
            # STRICT: Only foods with GI ≤ 50 (Low)
            category_foods = category_foods[
                category_foods['Glycemic Index'].apply(lambda x: safe_float(x, 100) <= 50)
            ].copy()
            gi_filter = "GI ≤ 50 (Rendah - Untuk Risiko Sedang)"
            
        else:  # LOW_RISK
            # MODERATE: Only foods with GI ≤ 50 (Low)
            category_foods = category_foods[
                category_foods['Glycemic Index'].apply(lambda x: safe_float(x, 100) <= 50)
            ].copy()
            gi_filter = "GI ≤ 50 (Rendah - Untuk Risiko Rendah)"
        
        debug_info['filtering'] = {
            'foods_before_filter': foods_before_filter,
            'foods_after_filter': len(category_foods),
            'gi_filter': gi_filter
        }
        
        if len(category_foods) == 0:
            debug_info['error'] = 'No foods remaining after GI filtering'
            return [], risk_level, gi_filter, debug_info
        
        # Sort by Glycemic Index (lowest first)
        category_foods = category_foods.sort_values('Glycemic Index')
        
        # PERSONALIZATION: Use user seed for consistent but varied selection
        random.seed(user_seed)
        
        # Get more candidates than needed for variety
        available_foods = len(category_foods)
        candidates_count = min(available_foods, top_n * 3)  # Get 3x more candidates
        
        if available_foods <= top_n:
            # If we have fewer foods than requested, return all
            selected_foods = category_foods
        else:
            # Select from top candidates with weighted randomization
            top_candidates = category_foods.head(candidates_count)
            
            # Create weights favoring lower GI foods
            weights = []
            for idx, (_, food_row) in enumerate(top_candidates.iterrows()):
                gi = safe_float(food_row.get('Glycemic Index', 55))
                # Lower GI = higher weight
                weight = max(1, 50 - gi)  # Ensure positive weight
                weights.append(weight)
            
            # Weighted random selection
            selected_indices = random.choices(
                range(len(top_candidates)), 
                weights=weights, 
                k=min(top_n, len(top_candidates))
            )
            
            # Remove duplicates while preserving order
            seen = set()
            unique_indices = []
            for idx in selected_indices:
                if idx not in seen:
                    seen.add(idx)
                    unique_indices.append(idx)
            
            # Get the selected foods
            selected_foods = top_candidates.iloc[unique_indices[:top_n]]
            
            # Sort selected foods by GI again
            selected_foods = selected_foods.sort_values('Glycemic Index')
        
        # Format recommendations
        recommendations = []
        for _, food_row in selected_foods.iterrows():
            gi = safe_float(food_row.get('Glycemic Index', 0))
            
            food_item = {
                'name': str(food_row.get('Food Name', 'Unknown')),
                'category': category,
                'calories': int(safe_float(food_row.get('Calories', 0))),
                'glycemic_index': int(gi),
                'carbohydrates': round(safe_float(food_row.get('Carbohydrates', 0)), 1),
                'protein': round(safe_float(food_row.get('Protein', 0)), 1),
                'fat': round(safe_float(food_row.get('Fat', 0)), 1),
                'fiber': round(safe_float(food_row.get('Fiber Content', 0)), 1),
                'sugar_content': round(safe_float(food_row.get('Sugar Content', 0)), 1),
                'sodium_content': round(safe_float(food_row.get('Sodium Content', 0)), 1),
                'suitable_for_diabetes': int(safe_float(food_row.get('Suitable for Diabetes', 1))),
                'rating': min(5.0, 5.0 - (gi / 10)),  # Rating based on GI
                'personalization_score': round(random.uniform(0.7, 0.95), 3),
                'model_used': 'enhanced_rule_based_algorithm',
                'gi_category': 'Sangat Rendah' if gi <= 35 else 'Rendah' if gi <= 50 else 'Sedang',
                'diabetes_friendly': gi <= 50,
                'recommendation_reason': f'GI {int(gi)} - {"Sangat aman" if gi <= 35 else "Aman" if gi <= 50 else "Terbatas"} untuk diabetes'
            }
            recommendations.append(food_item)
            
        debug_info['final_selection'] = len(recommendations)
        debug_info['gi_range'] = {
            'lowest': int(safe_float(selected_foods['Glycemic Index'].min(), 0)) if len(selected_foods) > 0 else 0,
            'highest': int(safe_float(selected_foods['Glycemic Index'].max(), 0)) if len(selected_foods) > 0 else 0,
            'average': round(safe_float(selected_foods['Glycemic Index'].mean(), 0), 1) if len(selected_foods) > 0 else 0
        }
        
        return recommendations, risk_level, gi_filter, debug_info
        
    except Exception as e:
        debug_info = {'error': f'Exception: {str(e)}'}
        print(f"[ERROR] Error in food recommendation: {e}")
        traceback.print_exc()
        return [], "LOW_RISK", "Error", debug_info

@app.route('/')
def home():
    """Main testing interface"""
    try:
        db_status = init_database()
        
        return render_template_string(HTML_TEMPLATE,
                                    diabetes_model_status="Ready" if diabetes_model is not None else "Not Found",
                                    food_data_status=f"Ready ({len(food_data)} items)" if food_data is not None else "Not Found",
                                    db_status="Connected" if db_status else "Error")
    except Exception as e:
        print(f"[ERROR] Error in home route: {e}")
        traceback.print_exc()
        return f"Error: {str(e)}", 500

@app.route('/predict', methods=['POST'])
def predict():
    """Diabetes prediction endpoint"""
    try:
        if diabetes_model is None or diabetes_scaler is None:
            return jsonify({
                'success': False,
                'error': 'Diabetes model or scaler not available'
            }), 500
            
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
            
        # Validate input
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
        
        # Validate ranges
        if not (0 < age < 150):
            return jsonify({'success': False, 'error': 'Age must be between 1-149'}), 400
        if not (10 < bmi < 60):
            return jsonify({'success': False, 'error': 'BMI must be between 10-60'}), 400
        if not (50 < glucose < 500):
            return jsonify({'success': False, 'error': 'Glucose must be between 50-500'}), 400
        if not (0 < insulin < 1000):
            return jsonify({'success': False, 'error': 'Insulin must be between 1-999'}), 400
        
        # Reorder features to match model training order
        reordered_features = reorder_features_for_model(age, bmi, glucose, insulin)
        
        # Use DataFrame with feature names to avoid sklearn warning
        if feature_order is not None:
            features_df = pd.DataFrame([reordered_features], columns=feature_order)
            features_scaled = diabetes_scaler.transform(features_df)
        else:
            features = np.array([reordered_features])
            features_scaled = diabetes_scaler.transform(features)
        
        prediction = int(diabetes_model.predict(features_scaled)[0])
        prediction_text = 'Risiko Tinggi' if prediction == 1 else 'Risiko Rendah'
        
        # Determine detailed risk level for food recommendations
        risk_level = determine_diabetes_risk_level(glucose, insulin, bmi, age)
        
        # Save to database
        prediction_id = save_prediction_to_db(age, bmi, glucose, insulin, prediction)
        
        # Create debug information
        original_order = [age, bmi, glucose, insulin]
        feature_mapping = {
            'Age': age,
            'BMI': bmi, 
            'Glucose': glucose,
            'Insulin': insulin
        }

        debug_info = {
            'original_order': original_order,
            'reordered_features': reordered_features,
            'expected_order': list(feature_order) if feature_order is not None else ['Glucose', 'Insulin', 'BMI', 'Age'],
            'feature_mapping': feature_mapping
        }

        # Convert prediction text to Indonesian
        prediction_text_id = 'Risiko Tinggi' if prediction == 1 else 'Risiko Rendah'

        return jsonify({
            'success': True,
            'prediction': prediction,
            'prediction_text': prediction_text_id,
            'risk_level': risk_level,
            'prediction_id': prediction_id,
            'input_data': {
                'age': age,
                'bmi': bmi,
                'glucose': glucose,
                'insulin': insulin
            },
            'debug_info': debug_info,
            'scaled_input': features_scaled[0].tolist(),
            'message': f'Prediksi berhasil: {prediction_text_id}',
            'gi_filtering_info': {
                'Risiko_Tinggi': 'Hanya makanan GI ≤ 35 (Sangat Rendah)',
                'Risiko_Sedang': 'Hanya makanan GI ≤ 50 (Rendah)', 
                'Risiko_Rendah': 'Hanya makanan GI ≤ 50 (Rendah)',
                'current_user_filter': f'GI ≤ {35 if risk_level == "HIGH_RISK" else 50}'
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input data: {str(e)}'
        }), 400
    except Exception as e:
        print(f"[ERROR] Error in predict: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/recommend_food', methods=['POST'])
def recommend_food():
    """Enhanced food recommendation endpoint with strict GI filtering"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False, 
                'error': 'No data provided'
            }), 400
            
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
        
        # Validate user_data
        required_user_fields = ['age', 'bmi', 'glucose', 'insulin']
        for field in required_user_fields:
            if field not in user_data:
                return jsonify({
                    'success': False,
                    'error': f'Missing user data field: {field}'
                }), 400
        
        # Get enhanced recommendations with strict GI filtering
        recommendations, risk_level, gi_filter, debug_info = get_food_recommendations(category, user_data)
        
        if not recommendations:
            return jsonify({
                'success': False,
                'error': 'No recommendations found for this category with current GI filtering',
                'debug_info': debug_info,
                'suggestion': 'Try a different category or check if foods in this category meet the GI requirements'
            }), 404
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'source': 'enhanced_rule_based_algorithm',
            'category_requested': category,
            'total_recommendations': len(recommendations),
            'user_profile': user_data,
            'risk_level': risk_level,
            'gi_filter': gi_filter,
            'model_used': 'enhanced_rule_based_algorithm',
            'debug_info': debug_info,
            'personalization_info': {
                'user_seed': debug_info.get('user_seed'),
                'unique_selection': 'Each user gets different foods based on their input',
                'gi_priority': 'Foods sorted by lowest glycemic index first'
            },
            'filtering_rules': {
                'Risiko_Tinggi': 'GI ≤ 35 (Sangat Rendah)',
                'Risiko_Sedang': 'GI ≤ 50 (Rendah)',
                'Risiko_Rendah': 'GI ≤ 50 (Rendah)'
            },
            'timestamp': datetime.now().isoformat()
        })
            
    except Exception as e:
        print(f"[ERROR] Error in recommend_food: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': {
            'diabetes_model': diabetes_model is not None,
            'diabetes_scaler': diabetes_scaler is not None,
            'food_data': food_data is not None
        },
        'enhanced_features': {
            'strict_gi_filtering': True,
            'personalized_recommendations': True,
            'rule_based_algorithm': True,
            'gi_thresholds': {
                'HIGH_RISK': '≤ 35 (Sangat Rendah)',
                'MEDIUM_RISK': '≤ 50 (Rendah)',
                'LOW_RISK': '≤ 50 (Rendah)'
            }
        }
    })

if __name__ == '__main__':
    print("DiabCare Enhanced Backend Server")
    print("=" * 50)
    
    # Initialize database
    db_ready = init_database()
    
    # Status check
    print(f"Diabetes model: {'Ready' if diabetes_model is not None else 'Not Found'}")
    print(f"Diabetes scaler: {'Ready' if diabetes_scaler is not None else 'Not Found'}")
    print(f"Food data (CSV): {'Ready' if food_data is not None else 'Not Found'}")
    print(f"Database: {'Ready' if db_ready else 'Error'}")
    
    print("=" * 50)
    print("ENHANCED GI FILTERING RULES:")
    print(" Risiko Tinggi: Hanya GI ≤ 35 (Sangat Rendah)")
    print(" Risiko Sedang: Hanya GI ≤ 50 (Rendah)")  
    print(" Risiko Rendah: Hanya GI ≤ 50 (Rendah)")
    print(" Rule-based: Tetap menggunakan algoritma rule-based")
    print("=" * 50)
    print("Web Testing Interface: http://127.0.0.1:5000")
    print("Health Check: http://127.0.0.1:5000/health")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}")
        traceback.print_exc()
