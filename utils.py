import os
import aiofiles
import hmac
from hashlib import sha256
from flask import send_file, abort, request
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY").encode()
ACCESS_CONTROL_KEY = os.environ.get("ACCESS_CONTROL_KEY").encode()
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")

async def save_file(file, folder=UPLOAD_FOLDER):
    filename = secure_filename(file.filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, filename)
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(await file.read())
    logging.info(f"File saved: {file_path}")
    return file_path

def generate_secure_url(file_path, key=SECRET_KEY):
    filename = os.path.basename(file_path)
    token = hmac.new(key, msg=filename.encode(), digestmod=sha256).hexdigest()
    url = f"/download?file={filename}&token={token}"
    logging.info(f"Generated secure URL for {filename}")
    return url

def validate_secure_url(filename, token, key=SECRET_KEY):
    expected_token = hmac.new(key, msg=filename.encode(), digestmod=sha256).hexdigest()
    valid = hmac.compare_digest(expected_token, token)
    if valid:
        logging.info(f"Secure URL validation succeeded for {filename}")
    else:
        logging.warning(f"Secure URL validation failed for {filename}")
    return valid

async def serve_secure_file(request, folder=UPLOAD_FOLDER):
    filename = request.args.get('file')
    token = request.args.get('token')
    if not filename or not token or not validate_secure_url(filename, token):
        logging.error("Access denied. Invalid parameters or failed validation.")
        abort(403)
    file_path = os.path.join(folder, secure_filename(filename))
    logging.info(f"Serving file: {file_path}")
    return await send_file(file_path)

def user_has_access(user_id, access_key=ACCESS_CONTROL_KEY):
    access_granted = hmac.compare_digest(user_id.encode(), access_key)
    if access_granted:
        logging.info(f"Access granted to user ID: {user_id}")
    else:
        logging.warning(f"Access denied for user ID: {user_id}")
    return access_granted