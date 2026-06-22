def career_brain(resume_text):
    text = resume_text.lower()

    roles = []
    roadmap = []

    if "python" in text:
        roles += ["Backend Developer", "Data Analyst"]

    if "react" in text:
        roles += ["Frontend Developer"]

    if "machine learning" in text:
        roles += ["AI Engineer"]

    if "sql" in text:
        roles += ["Data Engineer"]

    roadmap = [
        "Master Data Structures & Algorithms",
        "Build 5 real-world projects",
        "Learn system design basics",
        "Contribute to open source",
        "Apply for internships"
    ]

    return {
        "recommended_roles": roles,
        "skill_gap_analysis": "Focus on DSA + Projects + System Design",
        "roadmap": roadmap
    }
