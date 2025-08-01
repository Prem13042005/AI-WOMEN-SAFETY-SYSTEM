import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="WJ28@krhps",  # Use environment variables in production!
    database="women_safety_db"
)

cursor = db.cursor(dictionary=True)
