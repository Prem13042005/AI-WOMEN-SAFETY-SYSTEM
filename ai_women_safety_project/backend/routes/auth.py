from flask import Blueprint, request, jsonify
import mysql.connector

auth_routes = Blueprint('auth', __name__)

# DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="WJ28@krhps",
    database="women_safety_db"
)
cursor = db.cursor(dictionary=True)

# Register route
@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # ✅ Expecting JSON
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"status": "error", "message": "Email already exists"}), 409

    cursor.execute(
        "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
        (name, email, phone, password)
    )
    db.commit()
    return jsonify({"status": "success", "message": "Registered successfully"}), 201

# Login route
@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # ✅ Expecting JSON
    email = data.get('email')
    password = data.get('password')

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
