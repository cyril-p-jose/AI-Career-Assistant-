import PyPDF2

SKILLS_DB = [
    "python","java","javascript","react","node","flask",
    "django","sql","mongodb","html","css","machine learning",
    "ai","data analysis","git","docker"
]

def extract_text(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.lower()


def analyze_resume(path):
    text = extract_text(path)

    skills = [s for s in SKILLS_DB if s in text]

    score = 40
    score += len(skills) * 7

    # EXPERIENCE CHECK
    exp_bonus = 10 if "experience" in text else 0
    project_bonus = 10 if "project" in text else 0
    github_bonus = 10 if "github" in text else 0

    score += exp_bonus + project_bonus + github_bonus
    score = min(score, 100)

    missing = []
    if "project" not in text:
        missing.append("Add real-world projects")
    if "github" not in text:
        missing.append("Add GitHub profile")
    if len(skills) < 5:
        missing.append("Add more technical skills")

    return {
        "skills": skills,
        "score": score,
        "missing": missing,
        "strength": "Good technical foundation" if score > 70 else "Needs improvement"
    }
