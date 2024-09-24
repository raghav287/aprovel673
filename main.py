from flask import Flask, render_template, redirect, url_for, request
import hashlib
import os
import requests
import uuid
import json

app = Flask(__name__)

# Path to store the device key
DEVICE_KEY_FILE = 'device_key.json'

def get_or_create_device_key():
    """Get the device key, generate and store it if it doesn't exist."""
    if os.path.exists(DEVICE_KEY_FILE):
        # Load the existing device key
        with open(DEVICE_KEY_FILE, 'r') as f:
            data = json.load(f)
            return data['device_key']
    else:
        # Generate a new device key
        unique_id = uuid.uuid1()  # Generate UUID based on the machine’s network interface and hardware
        device_key = hashlib.sha256(str(unique_id).encode()).hexdigest()
        
        # Save the new device key to a file
        with open(DEVICE_KEY_FILE, 'w') as f:
            json.dump({'device_key': device_key}, f)
        
        return device_key

def check_permission(device_key):
    """Check if the device key has been approved."""
    try:
        response = requests.get("https://pastebin.com/raw/3h2v25aR")
        if response.status_code == 200:
            data = response.text
            permission_list = [line.strip() for line in data.split("\n") if line.strip().find(device_key) != -1]
            if not permission_list:
                return False  # Not approved yet
            return True  # Approved
        else:
            return False  # Failed to fetch permissions list
    except Exception as e:
        return f"Error checking permission: {e}"

@app.route('/')
def index():
    device_key = get_or_create_device_key()  # Get or create the unique device key
    return render_template('index.html', device_key=device_key)

@app.route('/check_approval/<device_key>', methods=['GET'])
def check_approval(device_key):
    if check_permission(device_key):
        return redirect(url_for('approved'))  # Redirect to approval page
    else:
        return render_template('not_approved.html', device_key=device_key)  # Stay on approval check

@app.route('/approved')
def approved():
    return render_template('approved.html')  # Show approved page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
