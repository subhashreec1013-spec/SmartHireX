# skill_gap.py
# Lightweight version (NO spaCy needed)

SKILL_DB = [
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "pandas", "numpy", "excel", "tableau", "power bi",
    "aws", "docker", "flask", "django", "react"
]


def extract_skills(text):
    """
    Extract skills using simple keyword matching
    """
    text = text.lower()
    skills_found = []

    for skill in SKILL_DB:
        if skill in text:
            skills_found.append(skill)

    return list(set(skills_found))


def skill_gap_analysis(job_desc, resume_text):
    """
    Compare job skills with resume skills
    """
    job_skills = extract_skills(job_desc)
    resume_skills = extract_skills(resume_text)

    matched = list(set(job_skills) & set(resume_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = 0
    if job_skills:
        score = round((len(matched) / len(job_skills)) * 100, 2)

    return matched, missing, score