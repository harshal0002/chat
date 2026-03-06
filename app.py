
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# HuggingFace API
API_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"reply": "No message received"})

    payload = {"inputs": user_message}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            ai_reply = result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            ai_reply = "Model is loading. Please try again in a few seconds."
        else:
            ai_reply = "AI response error"

    except Exception as e:
        ai_reply = "Server error: " + str(e)

    return jsonify({"reply": ai_reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
