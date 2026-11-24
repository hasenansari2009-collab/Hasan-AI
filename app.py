from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

@app.route("/")
def home():
    return "HASAN AI SERVER ONLINE"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message required"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"You are HASAN AI. Reply naturally and briefly. User: {message}"
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
