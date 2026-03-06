
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Simple conversation memory
conversation_memory = []
MAX_MEMORY = 10

# HuggingFace model
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

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

    conversation_memory.append("User: " + user_message)
    conversation_memory[:] = conversation_memory[-MAX_MEMORY:]

    prompt = "\n".join(conversation_memory)

    payload = {
        "inputs": prompt
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            ai_reply = result[0]["generated_text"]
        else:
            ai_reply = "Model response error"

    except Exception as e:
        ai_reply = "Error: " + str(e)

    conversation_memory.append("AI: " + ai_reply)

    return jsonify({"reply": ai_reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
