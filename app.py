
from flask import Flask, request, jsonify
from google import genai
from google.genai import types
import os

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
    http_options=types.HttpOptions(timeout=20000)
)

@app.route("/")
def home():
    return "HASAN AI SERVER ONLINE"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Message required"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "You are HASAN AI. Reply naturally, briefly, "
                "with an attitude and savage style while staying respectful. "
                "User: " + message.strip()
            )
        )

        return jsonify({
            "reply": response.text or "Please try again."
        })

    except Exception:
        app.logger.exception("Gemini request failed")
        return jsonify({
            "error": "HASAN AI is temporarily busy. Try again shortly."
        }), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
