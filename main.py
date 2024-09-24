from flask import Flask, render_template_string
import os
import requests
import sys

app = Flask(__name__)

# Define your logo (assuming it's a string)
logo = "APPROVAL SYSTEM"

# Function to get and validate token
def get_token():
    try:
        uuid = str(os.geteuid()) + str(os.getlogin())
        id = "-".join(uuid)
        httpCaht = requests.get('https://github.com/S4H1L9/Sahilwa900/blob/main/Txt').text
        if id in httpCaht:
            return "approved", id
        else:
            return "unapproved", id
    except:
        sys.exit()

@app.route('/')
def approval():
    status, id = get_token()
    
    if status == "approved":
        # If approved, redirect to the provided link
        return render_template_string("""
        <html>
            <head>
                <title>Approval Page</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: white;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        text-align: center;
                    }}
                    .message {{
                        text-align: center;
                        font-size: 1.2em;
                    }}
                </style>
                <script type="text/javascript">
                    // Automatically redirect after 3 seconds
                    setTimeout(function() {{
                        window.location.href = "https://done-hsuk.onrender.com";
                    }}, 3000);
                </script>
            </head>
            <body>
                <div class="container">
                    <h1>{{ logo }}</h1>
                    <p class="message">Your Token is Successfully Approved. You will be redirected shortly.</p>
                    <p class="message">If you are not redirected, <a href="https://done-hsuk.onrender.com">click here</a>.</p>
                </div>
            </body>
        </html>
        """, logo=logo)

    else:
        # If not approved, show the token and instructions
        key_message = f"Your Token: {id}"
        return render_template_string("""
        <html>
            <head>
                <title>Approval Page</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: white;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        text-align: center;
                        font-size: 2.5em;
                    }}
                    p {{
                        text-align: center;
                        font-size: 1.2em;
                    }}
                    a {{
                        display: block;
                        text-align: center;
                        margin-top: 20px;
                        font-size: 1.2em;
                        color: #007BFF;
                        text-decoration: none;
                    }}
                    a:hover {{
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>{{ logo }}</h1>
                    <p>{{ key_message }}</p>
                    <hr/>
                    <p><b>Important Note</b></p>
                    <p>Approval Price 400 Life Time</p>
                    <p>Free Wale Gand Mara Sakte he</p>
                    <p>Key Copy Krke Owner Ko send karo</p>
                    <a href="https://wa.me/+919354720853?text=Hello%20Sir%20!%20Please%20Approve%20My%20Token%20The%20Token%20Is%20{{ id }}">
                        Contact on WhatsApp
                    </a>
                </div>
            </body>
        </html>
        """, logo=logo, key_message=key_message, id=id)

if __name__ == '__main__':
    app.run(debug=True)
