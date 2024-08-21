from flask import Flask, jsonify, Blueprint
import os
from dotenv import load_dotenv

load_dotenv()

# Create a Flask application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Define a Blueprint for your data-related routes
data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/')
def home():
    """Home route returning welcome message."""
    return jsonify({'message': 'Welcome to the Flask API'})

@data_bp.route('/api/data')
def get_data():
    """API route returning dummy data."""
    return jsonify({'data': 'Here is your data'})

# Register the Blueprint with the app
app.register_blueprint(data_bp)

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)