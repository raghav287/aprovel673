import logging
from flask import Flask, render_template, redirect, url_for, request
import hashlib
import os
import requests
import json

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Your constants and functions
KEY_FILE = 'device_keys.json'
APPROVED_FILE = 'approved_phones.json'
MAX_KEYS = 10  # Limit the number of unique keys to 10

# Example usage of logging in a function
def get_unique_key():
    public_ip = get_public_ip()
    if not public_ip:
        logging.error("Failed to retrieve public IP address")
        return "Error retrieving IP address"

    keys = load_keys()

    # Check if the IP already has a key
    if public_ip in keys:
        logging.info(f"Device with IP {public_ip} already has a key.")
        return keys[public_ip]

    # If we have 10 keys already
    if len(keys) >= MAX_KEYS:
        logging.warning(f"Limit of {MAX_KEYS} unique keys reached.")
        return "Limit of 10 unique keys reached"

    # Generate a new key
    random_bytes = os.urandom(16)
    unique_key = hashlib.sha256(random_bytes + public_ip.encode()).hexdigest()

    # Save the new key and log the event
    keys[public_ip] = unique_key
    save_keys(keys)
    logging.info(f"New key generated for IP {public_ip}: {unique_key}")
    return unique_key

@app.route('/check_approval/<unique_key>', methods=['GET'])
def check_approval(unique_key):
    logging.info(f"Checking approval for key: {unique_key}")
    approved_keys = check_permission(unique_key)
    if not isinstance(approved_keys, list):
        return approved_keys  # Return error if any

    keys = load_keys()
    approved_phones = load_approved_phones()

    if unique_key in approved_keys and unique_key not in approved_phones:
        logging.info(f"Approving phone for key: {unique_key}")
        approved_phones.append(unique_key)
        save_approved_phones(approved_phones)

    # Check how many devices are now approved and allow corresponding number of phones
    approved_count = len(approved_phones)
    total_keys = len(keys)

    logging.info(f"Approved {approved_count}/{total_keys} phones")

    if approved_count == total_keys:
        return render_template('all_approved.html')  # All devices approved
    else:
        return render_template('some_approved.html', approved_count=approved_count, total_keys=total_keys)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
