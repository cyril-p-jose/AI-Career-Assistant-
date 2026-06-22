from flask import Flask, render_template, request, jsonify, session
import os
import google.generativeai as genai
from werkzeug.utils import secure_filename
from utils.resume_ai_v2 import analyze_resume
from utils.career_ai import career_brain

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- HOME ----------
@app.route("/")
def home():
    if "chat" not in session:
        session["chat"] = []
    return render_template("index.html")


# ---------- CHAT (TOP 1%) ----------
@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.form.get("message")
    resume_text = request.form.get("resume_text", "")

    chat = session.get("chat", [])
    chat.append({"role": "user", "msg": user_msg})

    prompt = f"""
You are an elite FAANG-level Career Coach AI.

Conversation:
{chat}

Resume:
{resume_text}

User:
{user_msg}

Give:
- precise answer
- actionable steps
- career advice if relevant
- keep response structured and professional
"""

    response = model.generate_content(prompt)

    chat.append({"role": "ai", "msg": response.text})
    session["chat"] = chat

    return jsonify({"reply": response.text})


# ---------- RESUME ANALYSIS ----------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    filename = secure_filename(file.filename)

    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    result = analyze_resume(path)

    return jsonify(result)


# ---------- CAREER BRAIN ----------
@app.route("/career", methods=["POST"])
def career():
    data = request.json
    return jsonify(career_brain(data["resume_text"]))


if __name__ == "__main__":
    app.run(debug=True)
