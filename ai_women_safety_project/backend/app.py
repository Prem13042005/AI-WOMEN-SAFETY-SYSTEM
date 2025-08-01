from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

# Initialize Flask
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Config
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Register backend API blueprints
from routes.auth import auth_routes
from routes.sos import sos_routes
from routes.prediction import prediction_routes

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(sos_routes, url_prefix='/sos')
app.register_blueprint(prediction_routes, url_prefix='/predict')

# Serve static HTML files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def serve_login():
    return send_from_directory(app.static_folder, 'login.html')

@app.route('/register')
def serve_register():
    return send_from_directory(app.static_folder, 'register.html')

@app.route('/dashboard')
def serve_dashboard():
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/about')
def about():
    return send_from_directory(app.static_folder, 'about.html')

# Serve all other static assets (css, js, lottie, images, etc.)
@app.route('/<path:filename>')
def serve_static_files(filename):
    file_path = os.path.join(app.static_folder, filename)
    if os.path.isfile(file_path):
        return send_from_directory(app.static_folder, filename)
    return jsonify({'error': 'File not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
