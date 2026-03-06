from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from bedrock_client import ask_claude
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Store user sessions
sessions = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get("Body", "").strip()
    sender = request.form.get("From", "")

    resp = MessagingResponse()
    msg = resp.message()

    # Get or create session
    if sender not in sessions:
        sessions[sender] = {
            "history": []
        }
        msg.body("Namaste! 🙏 Main Sarkar Saathi hoon.\nAap kaunsi government scheme ke baare mein jaanna chahte hain?\n\nYou can ask me in Hindi, English, Tamil or any language!")
        return str(resp)

    session = sessions[sender]

    # Ask Claude
    try:
        reply, updated_history = ask_claude(session["history"], incoming_msg)
        session["history"] = updated_history
        msg.body(reply)
    except Exception as e:
        msg.body("Sorry, kuch problem ho gayi. Please try again! 🙏")
        print(f"Error: {e}")

    return str(resp)

@app.route("/")
def home():
    return "Sarkar Saathi is running! 🇮🇳"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)