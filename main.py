from flask import Flask, render_template, redirect, url_for, request
import hashlib
import uuid
import os
import requests

app = Flask(__name__)

KEY_FILE = "device_key.txt"  # File to store the unique key

def get_unique_id():
    try:
        # Check if the key is already stored in the file
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, 'r') as f:
                unique_id = f.read().strip()
        else:
            # Generate a new unique key and store it
            unique_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
            with open(KEY_FILE, 'w') as f:
                f.write(unique_id)
        return unique_id
    except Exception as e:
        return f"Error generating unique ID: {e}"

def check_permission(unique_key):
    try:
        response = requests.get("https://pastebin.com/3qYPuSRt")  # URL for permission list
        if response.status_code == 200:
            data = response.text
            permission_list = [line.strip() for line in data.split("\n") if line.strip()]
            
            # Check for an exact match of the unique key in the permission list
            if unique_key in permission_list:
                return True  # Approved
            return False  # Not approved
        else:
            return False  # Failed to fetch permissions list
    except Exception as e:
        return f"Error checking permission: {e}"

@app.route('/')
def index():
    unique_key = get_unique_id()  # Get the stored or newly generated unique key
    return render_template('index.html', unique_key=unique_key)

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
