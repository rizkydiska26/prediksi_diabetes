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
        <h1>DiabCare Backend Testing Interface</h1>
        
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
                    <p><strong>Prediction:</strong> ${result.prediction_text} (${result.prediction})</p>`;
                
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
                    <p><strong>Prediction:</strong> ${result.prediction_text} (${result.prediction})</p>`;
                
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
                    <p><strong>ML Prediction:</strong> ${result.ml_prediction}</p>
                    <p><strong>GI Strategy:</strong> ${result.gi_strategy}</p>
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
    """Get food recommendations using ML model prediction and rule-based selection"""
    try:
        if food_data is None:
            return [], "Risiko Rendah", "No Data", {"error": "Food data not available"}
            
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
        
        # Use ML model to predict diabetes risk
        ml_prediction = 0  # Default to low risk
        ml_prediction_text = "Risiko Rendah"
        
        if diabetes_model is not None and diabetes_scaler is not None:
            try:
                # Reorder features for model
                reordered_features = reorder_features_for_model(age, bmi, glucose, insulin)
                
                # Use DataFrame with feature names to avoid sklearn warning
                if feature_order is not None:
                    features_df = pd.DataFrame([reordered_features], columns=feature_order)
                    features_scaled = diabetes_scaler.transform(features_df)
                else:
                    features = np.array([reordered_features])
                    features_scaled = diabetes_scaler.transform(features)
                
                ml_prediction = int(diabetes_model.predict(features_scaled)[0])
                ml_prediction_text = 'Risiko Tinggi' if ml_prediction == 1 else 'Risiko Rendah'
                
            except Exception as e:
                print(f"[ERROR] ML prediction failed: {e}")
                ml_prediction = 0
                ml_prediction_text = "Risiko Rendah"
        
        # Generate unique seed for this user and category combination
        user_seed = generate_user_seed(age, bmi, glucose, insulin, category)
        
        debug_info = {
            'category_requested': category,
            'csv_category_mapped': csv_category,
            'total_foods_in_category': len(category_foods),
            'user_profile': {'age': age, 'bmi': bmi, 'glucose': glucose, 'insulin': insulin},
            'ml_prediction': ml_prediction,
            'ml_prediction_text': ml_prediction_text,
            'user_seed': user_seed
        }
        
        if len(category_foods) == 0:
            debug_info['error'] = 'No foods found in category'
            return [], ml_prediction_text, "No Strategy", debug_info
        
        # Rule-based food selection strategy based on ML prediction
        if ml_prediction == 1:  # High Risk - prioritize lowest GI foods
            category_foods = category_foods.sort_values('Glycemic Index')
            gi_strategy = "Prioritas GI Terendah (Risiko Tinggi)"
        else:  # Low Risk - can include higher GI foods
            # Sort by GI but allow higher values
            category_foods = category_foods.sort_values('Glycemic Index')
            gi_strategy = "GI Fleksibel (Risiko Rendah)"
        
        debug_info['gi_strategy'] = gi_strategy
        debug_info['foods_available'] = len(category_foods)
        
        # PERSONALIZATION: Use user seed for consistent but varied selection
        random.seed(user_seed)
        
        # Get more candidates than needed for variety
        available_foods = len(category_foods)
        
        if available_foods <= top_n:
            # If we have fewer foods than requested, return all
            selected_foods = category_foods
        else:
            if ml_prediction == 1:  # High Risk - focus on lowest GI
                # Take top 50% lowest GI foods and randomize within that
                low_gi_count = max(top_n, len(category_foods) // 2)
                candidates = category_foods.head(low_gi_count)
            else:  # Low Risk - more variety allowed
                # Can select from broader range
                candidates = category_foods
            
            # Random selection from candidates
            if len(candidates) <= top_n:
                selected_foods = candidates
            else:
                selected_indices = random.sample(range(len(candidates)), top_n)
                selected_foods = candidates.iloc[selected_indices]
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
                'rating': min(5.0, 5.0 - (gi / 20)),  # Rating based on GI
                'personalization_score': round(random.uniform(0.7, 0.95), 3),
                'model_used': 'rule_based_with_ml_prediction',
                'gi_category': 'Sangat Rendah' if gi <= 35 else 'Rendah' if gi <= 50 else 'Sedang' if gi <= 70 else 'Tinggi',
                'diabetes_friendly': gi <= 50,
                'recommendation_reason': f'GI {int(gi)} - {"Sangat aman" if gi <= 35 else "Aman" if gi <= 50 else "Perhatikan" if gi <= 70 else "Hindari"} untuk diabetes'
            }
            recommendations.append(food_item)
            
        debug_info['final_selection'] = len(recommendations)
        debug_info['gi_range'] = {
            'lowest': int(safe_float(selected_foods['Glycemic Index'].min(), 0)) if len(selected_foods) > 0 else 0,
            'highest': int(safe_float(selected_foods['Glycemic Index'].max(), 0)) if len(selected_foods) > 0 else 0,
            'average': round(safe_float(selected_foods['Glycemic Index'].mean(), 0), 1) if len(selected_foods) > 0 else 0
        }
        
        return recommendations, ml_prediction_text, gi_strategy, debug_info
        
    except Exception as e:
        debug_info = {'error': f'Exception: {str(e)}'}
        print(f"[ERROR] Error in food recommendation: {e}")
        traceback.print_exc()
        return [], "Risiko Rendah", "Error", debug_info

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
    """Diabetes prediction endpoint using ML model only"""
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
            'debug_info': debug_info,
            'scaled_input': features_scaled[0].tolist(),
            'message': f'Prediksi berhasil: {prediction_text}',
            'model_info': {
                'type': 'ML_Model_Only',
                'categories': ['Risiko Tinggi', 'Risiko Rendah'],
                'note': 'Menggunakan model ML untuk kategorisasi diabetes'
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
    """Food recommendation endpoint using ML prediction and rule-based selection"""
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
        
        # Get recommendations using ML prediction and rule-based selection
        recommendations, ml_prediction, gi_strategy, debug_info = get_food_recommendations(category, user_data)
        
        if not recommendations:
            return jsonify({
                'success': False,
                'error': 'No recommendations found for this category',
                'debug_info': debug_info,
                'suggestion': 'Try a different category'
            }), 404
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'source': 'rule_based_with_ml_prediction',
            'category_requested': category,
            'total_recommendations': len(recommendations),
            'user_profile': user_data,
            'ml_prediction': ml_prediction,
            'gi_strategy': gi_strategy,
            'model_used': 'rule_based_with_ml_prediction',
            'debug_info': debug_info,
            'personalization_info': {
                'user_seed': debug_info.get('user_seed'),
                'unique_selection': 'Each user gets different foods based on their input',
                'strategy': 'ML prediction determines GI prioritization'
            },
            'algorithm_info': {
                'prediction_method': 'ML Model Only',
                'food_selection': 'Rule-based Algorithm',
                'categories': ['Risiko Tinggi', 'Risiko Rendah'],
                'gi_strategy_high_risk': 'Prioritas GI terendah',
                'gi_strategy_low_risk': 'GI fleksibel'
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
        'system_features': {
            'ml_prediction_only': True,
            'categories': ['Risiko Tinggi', 'Risiko Rendah'],
            'food_algorithm': 'rule_based',
            'personalized_recommendations': True,
            'gi_strategy': {
                'high_risk': 'Prioritas GI terendah',
                'low_risk': 'GI fleksibel'
            }
        }
    })

if __name__ == '__main__':
    print("DiabCare Backend Server - ML Model Only")
    print("=" * 50)
    
    # Initialize database
    db_ready = init_database()
    
    # Status check
    print(f"Diabetes model: {'Ready' if diabetes_model is not None else 'Not Found'}")
    print(f"Diabetes scaler: {'Ready' if diabetes_scaler is not None else 'Not Found'}")
    print(f"Food data (CSV): {'Ready' if food_data is not None else 'Not Found'}")
    print(f"Database: {'Ready' if db_ready else 'Error'}")
    
    print("=" * 50)
    print("UPDATED SYSTEM RULES:")
    print(" - Menggunakan HANYA model ML untuk kategorisasi diabetes")
    print(" - Kategori: Risiko Tinggi (1) atau Risiko Rendah (0)")
    print(" - Risiko Tinggi: Prioritas makanan GI terendah")
    print(" - Risiko Rendah: Boleh makanan GI lebih tinggi")
    print(" - Rekomendasi makanan: Tetap rule-based algorithm")
    print(" - Personalisasi: Setiap input user berbeda rekomendasinya")
    print("=" * 50)
    print("Web Testing Interface: http://127.0.0.1:5000")
    print("Health Check: http://127.0.0.1:5000/health")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}")
        traceback.print_exc()
