from flask import Flask, render_template, redirect, url_for, request
import hashlib
import os
import requests
import time

app = Flask(__name__)

def get_unique_id():
    try:
        # Generate unique ID based on system UID and login
        return hashlib.sha256((str(os.getuid()) + os.getlogin()).encode()).hexdigest()
    except Exception as e:
        return f"Error generating unique ID: {e}"

def check_permission(unique_key):
    try:
        response = requests.get("https://github.com/raghav416/Approval/blob/main/Approval.txt")
        if response.status_code == 200:
            data = response.text
            permission_list = [line.strip() for line in data.split("\n") if line.strip().find(unique_key) != -1]
            if not permission_list:
                return False  # Not approved yet
            return True  # Approved
        else:
            return False  # Failed to fetch permissions list
    except Exception as e:
        return f"Error checking permission: {e}"

@app.route('/')
def index():
    unique_key = get_unique_id()  # Generate unique key for the user
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
    
