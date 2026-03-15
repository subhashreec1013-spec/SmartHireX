import streamlit as st
import pandas as pd

# ===== Core Imports =====
from core.resume_parser import extract_resume_text
from core.preprocessing import preprocess_text
from skill_gap import skill_gap_analysis
from scoring import explainable_score, keyword_coverage
from semantic_matching import semantic_similarity   # ⭐ NEW (BERT)

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="SmartHireX - Intelligent AI Hiring & Resume Screening Platform",
    page_icon="📊",
    layout="wide"
)

# ================= HERO =================
st.title("SmartHireX - Intelligent AI Hiring & Resume Screening Platform")
st.write(
    "An intelligent hiring platform that uses BERT-based semantic matching, "
    "skill gap analysis, and explainable AI to automatically analyze, rank, "
    "and shortlist candidates for recruiters."
)

# ================= INPUT =================
job_description = st.text_area(
    "📝 Job Description",
    height=200,
    placeholder="Paste job description here..."
)

uploaded_files = st.file_uploader(
    "📂 Upload Resumes (PDF / DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

analyze = st.button("✨ Analyze & Rank Candidates")

# ================= MAIN LOGIC =================
if analyze:

    if not job_description:
        st.warning("Please enter job description")
        st.stop()

    if not uploaded_files:
        st.warning("Please upload resumes")
        st.stop()

    names = []
    cleaned_texts = []

    skill_scores = []
    keyword_scores = []
    final_scores = []

    matched_list = []
    missing_list = []

    # ========= STEP 1: EXTRACT TEXTS =========
    for file in uploaded_files:

        names.append(file.name)

        raw_text = extract_resume_text(file)
        clean_text = preprocess_text(raw_text)

        cleaned_texts.append(clean_text)

        # ===== Skill Gap =====
        matched, missing, skill_score = skill_gap_analysis(
            job_description,
            raw_text
        )

        matched_list.append(", ".join(matched))
        missing_list.append(", ".join(missing))
        skill_scores.append(skill_score)

        # ===== Keyword Coverage =====
        keyword_score = keyword_coverage(job_description, raw_text)
        keyword_scores.append(keyword_score)

    # ========= STEP 2: SEMANTIC MATCHING (BERT) =========
    st.info("⚡ Running semantic similarity using BERT embeddings...")

    semantic_scores = semantic_similarity(job_description, cleaned_texts)
    similarity_scores = [round(s * 100, 2) for s in semantic_scores]

    # ========= STEP 3: EXPLAINABLE FINAL SCORE =========
    for sim, skill, keyword in zip(similarity_scores, skill_scores, keyword_scores):
        final = explainable_score(sim, skill, keyword)
        final_scores.append(final)

    # ========= CREATE TABLE =========
    df = pd.DataFrame({
        "Candidate": names,
        "Final Score %": final_scores,
        "Semantic Similarity %": similarity_scores,
        "Skill Score %": skill_scores,
        "Keyword Score %": keyword_scores,
        "Matched Skills": matched_list,
        "Missing Skills": missing_list
    })

    # Sort by FINAL SCORE
    df = df.sort_values("Final Score %", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", df.index + 1)

    # ========= SUMMARY =========
    st.subheader("📊 Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Candidates", len(df))
    c2.metric("Top Final Score %", df["Final Score %"].max())
    c3.metric("Best Skill Score %", df["Skill Score %"].max())

    # ========= BEST CANDIDATE =========
    best = df.iloc[0]

    st.success(
        f"🏆 Best Candidate: {best['Candidate']} "
        f"(Final Score: {best['Final Score %']}%)"
    )

    st.write("Semantic Similarity:", best["Semantic Similarity %"], "%")
    st.write("Skill Score:", best["Skill Score %"], "%")
    st.write("Keyword Score:", best["Keyword Score %"], "%")
    st.write("✅ Matched Skills:", best["Matched Skills"])
    st.write("❌ Missing Skills:", best["Missing Skills"])

    # ========= TABLE =========
    st.subheader("📋 Candidate Ranking")
    st.dataframe(df, use_container_width=True)

    # ========= CHART =========
    st.subheader("📈 Final Score Comparison")
    st.bar_chart(df.set_index("Candidate")["Final Score %"])

    # ========= DEBUG =========
    with st.expander("View extracted text"):
        for n, t in zip(names, cleaned_texts):
            st.markdown(f"**{n}**")
            st.write(t[:600])