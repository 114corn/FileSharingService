import os
import json
from urllib.parse import urlencode
from hashlib import sha256
import hmac
from flask import send_file, abort
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ACCESS_CONTROL_KEY = os.environ.get("ACCESS_CONTROL_KEY")
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")

def save_file(file, folder=UPLOAD_FOLDER):
    filename = secure_filename(file.filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, filename)
    file.save(file_path)
    return file_path

def generate_secure_url(file_path, key=SECRET_KEY):
    filename = os.path.basename(file_path)
    token = hmac.new(key.encode(), msg=filename.encode(), digestmod=sha256).hexdigest()
    url = f"/download?file={filename}&token={token}"
    return url

def validate_secure_url(filename, token, key=SECRET_KEY):
    expected_token = hmac.new(key.encode(), msg=filename.encode(), digestmod=sha256).hexdigest()
    return hmac.compare_digest(expected_token, token)

def serve_secure_file(request, folder=UPLOAD_FOLDER):
    filename = request.args.get('file')
    token = request.args.get('token')
    if not filename or not token or not validate_secure_url(filename, token):
        abort(403)
    file_path = os.path.join(folder, secure_filename(filename))
    return send_file(file_path)

def user_has_access(user_id, access_key=ACCESS_CONTROL_KEY):
    return hmac.compare_digest(user_id, access_key)