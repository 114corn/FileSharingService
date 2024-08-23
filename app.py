from flask import Flask, jsonify, Blueprint, make_response
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/')
def home():
    return jsonify({'message': 'Welcome to the Flask API'})

@data_bp.route('/api/data')
def get_data():
    return jsonify({'data': 'Here is your data'})

app.register_blueprint(data_bp)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    response = jsonify({'message': 'A unexpected error occurred', 'error': str(error)})
    response.status_code = 500 if not hasattr(error, 'code') else error.code
    return response

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)