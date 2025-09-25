# This script is designed to run locally in VS Code.
import os
import datetime
import jwt
from functools import wraps
import pandas as pd
import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# --- GET THE DIRECTORY OF THE CURRENT SCRIPT ---
# This makes file paths reliable, regardless of where you run the script from.
basedir = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(basedir, 'time_predictor.pkl')
DB_PATH = os.path.join(basedir, 'fastbite.db')


# --- 1. APP AND ML MODEL SETUP ---
app = Flask(__name__)
CORS(app) 

# Load the trained ML model using the absolute path
try:
    model = joblib.load(MODEL_PATH)
    print("✅ ML model loaded successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Model not found at '{MODEL_PATH}'. Please run 'model_trainer.py' first.")
    model = None

# Base preparation times for menu items, used for prediction features
MENU_STATS = { 201: 18, 202: 15, 203: 12, 204: 10, 205: 5, 206: 7, 207: 14, 208: 12, 209: 14, 210: 10, 211: 3 }
# A simple in-memory list to simulate the kitchen's order queue
KITCHEN_QUEUE = []


# --- 2. CONFIGURATION AND DATABASE ---
app.config['SECRET_KEY'] = 'a-super-secret-key-for-jwt-that-is-secure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# --- 3. DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_number = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    items = db.Column(db.String(300), nullable=False)
    estimated_time = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Preparing')
    order_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# --- 4. AUTHENTICATION DECORATOR ---
# This function checks for a valid JWT token in the request header
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token: return jsonify({'error': 'Token is missing!'}), 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user: return jsonify({'error': 'User not found!'}), 404
        except Exception as e:
            return jsonify({'error': 'Token is invalid!', 'details': str(e)}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# --- 5. ROUTES TO SERVE THE FRONTEND ---
@app.route('/')
def serve_index():
    """Serves the main login page (index.html)."""
    return send_from_directory(basedir, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serves other static files like home.html, menu.html, or images."""
    # This is a security measure to prevent users from accessing files 
    # outside the project directory.
    if ".." in path or path.startswith("/"):
        return jsonify({"error": "Invalid path"}), 400
    return send_from_directory(basedir, path)




# --- 6. API ENDPOINTS ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    reg_number = data.get('regNumber')
    password = data.get('password')
    if not reg_number or not password: return jsonify({"error": "Registration number and password are required"}), 400
    if User.query.filter_by(reg_number=reg_number).first(): return jsonify({"error": "That registration number is already taken"}), 409
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(reg_number=reg_number, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": f"User '{reg_number}' registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    reg_number = data.get('regNumber')
    password = data.get('password')
    if not reg_number or not password: return jsonify({"error": "Registration number and password required"}), 400
    
    user = User.query.filter_by(reg_number=reg_number).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid registration number or password"}), 401
        
    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"message": "Login successful", "token": token}), 200

@app.route('/api/order', methods=['POST'])
@token_required # This endpoint is protected and requires a valid token
def place_order(current_user):
    if not model: return jsonify({"error": "The prediction model is not available. Server startup may have failed."}), 503

    order_data = request.get_json()
    item_list = order_data.get('items')
    if not item_list: return jsonify({"error": "Order data is missing or invalid"}), 400
    
    item_ids = [item['id'] for item in item_list]
    prep_times = [MENU_STATS.get(int(id), 5) for id in item_ids]
    num_items = sum(item['quantity'] for item in item_list)
    max_item_time = max(prep_times) if prep_times else 0
    avg_item_time = sum(prep_times) / len(prep_times) if prep_times else 0
    now = datetime.datetime.now()
    time_of_day = now.hour
    is_peak = 1 if time_of_day in [12, 13, 14, 19, 20] else 0
    queue_length = len(KITCHEN_QUEUE)

    features_df = pd.DataFrame([[num_items, max_item_time, avg_item_time, time_of_day, is_peak, queue_length]],
                               columns=['num_items', 'max_item_time', 'avg_item_time', 'time_of_day', 'is_peak', 'queue_length'])
    
    predicted_minutes = model.predict(features_df)[0]
    estimated_time = round(predicted_minutes)

    new_order = Order(user_id=current_user.id, items=str(item_list), estimated_time=estimated_time)
    db.session.add(new_order)
    db.session.commit()
    # Simulate an order being completed to keep the queue realistic
    if len(KITCHEN_QUEUE) > 0: KITCHEN_QUEUE.pop(0)
    KITCHEN_QUEUE.append(new_order.id)

    return jsonify({
        "message": "Order placed successfully!",
        "orderId": new_order.id,
        "status": new_order.status,
        "estimatedPrepTime": f"{estimated_time} minutes"
    }), 201

# --- 7. START THE APP ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)

