from flask import Flask, request, redirect, url_for, send_from_directory
import hashlib
import os
import requests
import uuid  # <-- Make sure to import uuid

app = Flask(__name__)

# Route to serve the image
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('/mnt/data', filename)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <style>
            body {
                background-image: url('https://i.ibb.co/f0JCQMM/Screenshot-20240922-100537-Gallery.jpg');
                background-size: cover;
                text-align: center;
                color: yellow;
                font-family: Arial, sans-serif;
            }
            h1 {
                font-size: 4em;
                margin-top: 100px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                font-size: 2em;
                color: green;
                text-decoration: none;
                background: black;
                padding: 10px 20px;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome!</h1>
        <a href="/approval-request">Request Approval</a>
    </body>
    </html>
    '''

@app.route('/approval-request')
def approval_request():
    unique_key = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
    return '''
    <html>
    <head>
        <style>
            body {{
                background-image: url('https://i.ibb.co/f0JCQMM/Screenshot-20240922-100537-Gallery.jpg');
                background-size: cover;
                text-align: center;
                color: yellow;
                font-family: Arial, sans-serif;
            }}
            h1 {{
                font-size: 3em;
                margin-top: 100px;
            }}
            p {{
                font-size: 1.5em;
            }}
            input[type=submit] {{
                font-size: 1.5em;
                padding: 10px 20px;
                background-color: black;
                color: green;
                border: none;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Approval Request</h1>
        <p>Your unique key is: {}</p>
        <form action="/check-permission" method="post">
            <input type="hidden" name="unique_key" value="{}">
            <input type="submit" value="Request Approval">
        </form>

        <a href="https://wa.me/+919354720853" style="font-size: 1.5em; padding: 10px 20px; background-color: black; color: green; border-radius: 10px; text-decoration: none;">Contact Owner</a>
    
   </body>
    </html>
    '''.format(unique_key, unique_key)

@app.route('/check-permission', methods=['POST'])
def check_permission():
    unique_key = request.form['unique_key']
    response = requests.get("https://pastebin.com/raw/3qYPuSRt")
    approved_tokens = [token.strip() for token in response.text.splitlines() if token.strip()]
    if unique_key in approved_tokens:
        return redirect(url_for('approved', key=unique_key))
    else:
        return redirect(url_for('not_approved', key=unique_key))

@app.route('/approved')
def approved():
    key = request.args.get('key')
    return '''
    <html>
    <head>
        <style>
            body {{
                background-image: url('https://i.ibb.co/f0JCQMM/Screenshot-20240922-100537-Gallery.jpg');
                background-size: cover;
                text-align: center;
                color: yellow;
                font-family: Arial, sans-serif;
            }}
            h1 {{
                font-size: 3em;
                margin-top: 100px;
            }}
            p {{
                font-size: 1.5em;
            }}
            a {{
                font-size: 1.5em;
                padding: 10px 20px;
                background-color: black;
                color: green;
                border-radius: 10px;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <h1>Approved!</h1>
        <p>Your unique key is: {}</p>
        <p>You have been approved. You can proceed with the script.</p>
        <a href="https://done-hsuk.onrender.com" target="_blank">Request Approval</a>
    </body>
    </html>
    '''.format(key)

@app.route('/not-approved')
def not_approved():
    key = request.args.get('key')
    return '''
    <html>
    <head>
        <style>
            body {{
                background-image: url('https://i.ibb.co/f0JCQMM/Screenshot-20240922-100537-Gallery.jpg');
                background-size: cover;
                text-align: center;
                color: yellow;
                font-family: Arial, sans-serif;
            }}
            h1 {{
                font-size: 3em;
                margin-top: 100px;
            }}
            p {{
                font-size: 1.5em;
            }}
        </style>
    </head>
    <body>
        <h1>Not Approved</h1>
        <p>Your unique key is: {}</p>
        <p>Sorry, you don't have permission to run this script.</p>
    </body>
    </html>
    '''.format(key)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=10000, debug=True)
