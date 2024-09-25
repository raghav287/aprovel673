from flask import Flask, render_template, redirect, url_for, request, make_response
import hashlib
import uuid
import os
import requests

app = Flask(__name__)

KEY_FILE = "device_key.txt"  # File to store the unique key (fallback mechanism)

def generate_unique_id():
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

def get_unique_id_from_cookie_or_generate(request):
    unique_id = request.cookies.get('device_key')
    if not unique_id:
        unique_id = generate_unique_id()
    return unique_id

def check_permission(unique_key):
    try:
        response = requests.get("https://pastebin.com/raw/3qYPuSRt")  # URL for permission list
        if response.status_code == 200:
            # Ensure to strip spaces and newline characters from the permission list
            permission_list = [line.strip() for line in response.text.split("\n") if line.strip()]

            # Check for an **exact** match with the unique key in the permission list
            if unique_key in permission_list:
                return True  # Key is approved
            return False  # Key is not approved
        else:
            return False  # Failed to fetch the permissions list
    except Exception as e:
        return f"Error checking permission: {e}"

@app.route('/')
def index():
    unique_key = get_unique_id_from_cookie_or_generate(request)  # Get the key from cookies or generate new
    response = make_response(render_template('index.html', unique_key=unique_key))

    # Store the unique key in a cookie to maintain uniqueness across sessions per device
    response.set_cookie('device_key', unique_key)
    return response

@app.route('/check_approval/<unique_key>', methods=['GET'])
def check_approval(unique_key):
    if check_permission(unique_key):
        return redirect(url_for('approved'))  # Redirect to approval page
    else:
        return render_template('not_approved.html', unique_key=unique_key)  # Stay on approval check

@app.route('/approved')
def approved():
    return render_template('approved.html')  # Show approved page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
