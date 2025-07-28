from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Gemini API setup
GEMINI_API_KEY = "AIzaSyDrP45CJUOupgyjTQ-J6hzR4YTaT2iwBdg"  # Replace with your actual Gemini API key
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

# WhatsApp webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')

    # Call Gemini
    gemini_response = requests.post(
        GEMINI_URL,
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": incoming_msg}]}]}
    )

    reply = gemini_response.json()['candidates'][0]['content']['parts'][0]['text']

    # Return TwiML reply
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

# Run the app on public URL
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
