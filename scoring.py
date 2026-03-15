# scoring.py

def keyword_coverage(job_desc, resume_text):
    """
    % of job keywords appearing in resume
    """
    jd_words = set(job_desc.lower().split())
    resume_words = set(resume_text.lower().split())

    if not jd_words:
        return 0

    matched = jd_words.intersection(resume_words)
    return round((len(matched) / len(jd_words)) * 100, 2)


def explainable_score(similarity, skill_score, keyword_score):
    """
    Final weighted score
    """
    final = (
        0.5 * similarity +
        0.4 * skill_score +
        0.1 * keyword_score
    )

    return round(final, 2)