```python
from flask import Flask, render_template, request, jsonify, session
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
from utils.resume_ai_v2 import analyze_resume
from utils.career_ai import career_brain

app = Flask(__name__)

# Use environment variable in production
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Gemini Configuration
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/")
def home():
    if "chat" not in session:
        session["chat"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.form.get("message", "")
        resume_text = request.form.get("resume_text", "")

        if not user_msg:
            return jsonify({"error": "Message is required"}), 400

        chat_history = session.get("chat", [])

        prompt = f"""
You are an expert Career Guidance AI Assistant.

Resume:
{resume_text}

Previous Conversation:
{chat_history}

Current User Question:
{user_msg}

Provide:
1. Direct answer
2. Actionable recommendations
3. Career guidance when relevant
4. Structured formatting
"""

        response = model.generate_content(prompt)

        reply = response.text if hasattr(response, "text") else "No response generated."

        chat_history.append({"role": "user", "msg": user_msg})
        chat_history.append({"role": "assistant", "msg": reply})

        # Keep only latest messages
        session["chat"] = chat_history[-10:]

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        filename = secure_filename(file.filename)

        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        result = analyze_resume(path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/career", methods=["POST"])
def career():
    try:
        data = request.get_json()

        if not data or "resume_text" not in data:
            return jsonify({"error": "resume_text required"}), 400

        result = career_brain(data["resume_text"])

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```
