from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Gemini API setup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDrP45CJUOupgyjTQ-J6hzR4YTaT2iwBdg")  # Use environment variable or fallback
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# WhatsApp webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')

    # Call Gemini API
    response = requests.post(
        GEMINI_URL,
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": incoming_msg}]}]}
    )

    # Parse Gemini response
    try:
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        reply = "Oops! Something went wrong while generating a response."

    # TwiML response for Twilio
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""

# Start the Flask app (Render requires dynamic PORT)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

