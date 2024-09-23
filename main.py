from flask import Flask, render_template, redirect, url_for, request
import hashlib
import os
import requests
import json

app = Flask(__name__)

# File to store the unique keys and their approval status
KEY_FILE = 'device_keys.json'
MAX_KEYS = 10  # Limit the number of unique keys to 10

def load_keys():
    """Load the keys and approval status from the JSON file."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_keys(keys):
    """Save the keys and their approval status to the JSON file."""
    with open(KEY_FILE, 'w') as f:
        json.dump(keys, f)

def get_public_ip():
    """Get the public IP address of the device."""
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        return None
    except Exception as e:
        return f"Error getting public IP: {e}"

def get_unique_key():
    """Generate or retrieve the unique key for the current device."""
    public_ip = get_public_ip()  # Get the device's public IP
    if not public_ip:
        return "Error retrieving IP address"

    keys = load_keys()  # Load the existing keys

    # If the device already has a key, return it
    if public_ip in keys:
        return keys[public_ip]['key']
    
    # If we already have 10 unique keys, do not generate more
    if len(keys) >= MAX_KEYS:
        return "Limit of 10 unique keys reached"

    # Generate a new unique key
    random_bytes = os.urandom(16)  # Random 16 bytes for uniqueness
    unique_key = hashlib.sha256(random_bytes + public_ip.encode()).hexdigest()
    
    # Save the new key and its approval status (False by default)
    keys[public_ip] = {'key': unique_key, 'approved': False}
    save_keys(keys)

    return unique_key

def check_permission(unique_key):
    """Check if the unique key has been approved locally."""
    keys = load_keys()
    for ip, data in keys.items():
        if data['key'] == unique_key:
            return data['approved']
    return False

def approve_key(unique_key):
    """Approve a specific unique key."""
    keys = load_keys()
    for ip, data in keys.items():
        if data['key'] == unique_key:
            keys[ip]['approved'] = True
            save_keys(keys)
            return True
    return False

@app.route('/')
def index():
    unique_key = get_unique_key()  # Generate or retrieve the unique key for the device
    if "Error" in unique_key:
        return unique_key  # Display error message if any
    return render_template('index.html', unique_key=unique_key)

@app.route('/check_approval/<unique_key>', methods=['GET'])
def check_approval(unique_key):
    if check_permission(unique_key):
        return redirect(url_for('approved'))  # Redirect to approval page
    else:
        return render_template('not_approved.html', unique_key=unique_key)  # Stay on approval check

@app.route('/approve/<unique_key>', methods=['POST'])
def approve(unique_key):
    if approve_key(unique_key):
        return redirect(url_for('approved'))
    else:
        return "Error approving key", 400

@app.route('/approved')
def approved():
    return render_template('approved.html')  # Show approved page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
