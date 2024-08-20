from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Flask API'})

@app.route('/api/data')
def get_data():
    return jsonify({'data': 'Here is your data'})

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)