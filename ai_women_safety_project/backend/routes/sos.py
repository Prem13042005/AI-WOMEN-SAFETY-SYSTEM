from flask import Blueprint, request, jsonify 
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from services.db import db, cursor  

sos_routes = Blueprint('sos_routes', __name__)

# Reusable DB connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="WJ28@krhps",
        database="women_safety_db"
    )

@sos_routes.route('/trigger', methods=['POST'])
def trigger_sos():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Input validation
        if not user_id or not latitude or not longitude:
            return jsonify({"status": "fail", "message": "Missing required fields"}), 400

        # Insert into DB
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO sos_logs (user_id, latitude, longitude, triggered_at)
            VALUES (%s, %s, %s, %s)
        """
        values = (user_id, latitude, longitude, datetime.now())
        cursor.execute(query, values)
        conn.commit()

        # Close connection
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "🚨 SOS logged successfully"}), 200

    except Error as e:
        print("❌ Database error:", e)
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    except Exception as e:
        print("❌ Server error:", e)
        return jsonify({"status": "error", "message": "Unexpected error occurred"}), 500

@sos_routes.route('/add_contact', methods=['POST'])
def add_emergency_contact():
    data = request.json
    cursor.execute("""
        INSERT INTO emergency_contacts (user_id, contact_name, contact_number)
        VALUES (%s, %s, %s)
    """, (data['user_id'], data['name'], data['number']))
    db.commit()
    return jsonify({"status": "success", "message": "Contact saved successfully"}), 200
