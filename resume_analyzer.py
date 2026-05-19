import streamlit as st
import PyPDF2
import re
import sqlite3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# DATABASE

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def save_resume_analysis(user_id, ats_score, missing_keywords):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO resume_analysis (user_id, ats_score, missing_keywords)
        VALUES (?, ?, ?)
    """, (
        user_id,
        ats_score,
        ", ".join(missing_keywords)
    ))

    conn.commit()
    conn.close()


# TEXT EXTRACTION

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()


def clean_text(text):
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# JD KEYWORDS

def extract_jd_keywords(jd_text, max_keywords=25):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=max_keywords,
        ngram_range=(1, 2)
    )
    vectorizer.fit([jd_text])
    return vectorizer.get_feature_names_out()


# ATS SCORE

def ats_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)


# AI FEEDBACK

def generate_rewrite_suggestions(missing_keywords):
    suggestions = []
    for kw in missing_keywords[:6]:
        suggestions.append(
            f"Worked on projects involving **{kw}** to improve job-relevant expertise."
        )
    return suggestions


def section_wise_feedback(missing_keywords):
    return {
        "Skills": [f"Add **{kw}** under technical skills" for kw in missing_keywords[:5]],
        "Projects": [f"Create a mini project using **{kw}**" for kw in missing_keywords[:3]],
        "Experience": [f"Mention hands-on experience with **{kw}**" for kw in missing_keywords[:3]],
        "Summary": ["Rewrite summary using JD keywords and role-specific terms"]
    }


# STREAMLIT UI

def show_resume_analyzer():

    # 🔐 LOGIN GUARD
    if not st.session_state.logged_in:
        st.warning("🔐 Please login to analyze your resume")
        return

    st.title("🧠 AI Resume Analyzer")
    st.caption("ATS Optimization • Skill Gap Analysis • AI Feedback")

    resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area(
        "📋 Paste Job Description",
        height=220,
        placeholder="Paste company job description here"
    )

    if st.button("🚀 Analyze & Improve Resume"):
        if not resume_file or not jd_text:
            st.warning("Please upload resume and paste Job Description")
            return

        #  PROCESS 
        resume_text = clean_text(extract_text_from_pdf(resume_file))
        jd_clean = clean_text(jd_text)

        jd_keywords = extract_jd_keywords(jd_clean)
        ats_score = ats_similarity(resume_text, jd_clean)

        matched = [k for k in jd_keywords if k in resume_text]
        missing = list(set(jd_keywords) - set(matched))

        #  OUTPUT 
        st.subheader("📊 ATS Match Score")
        st.progress(int(ats_score))
        st.metric("ATS Compatibility (%)", ats_score)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Keywords")
            st.write(matched if matched else "No strong matches found")

        with col2:
            st.subheader("❌ Missing Keywords")
            st.write(missing if missing else "Great! No major gaps")

        st.subheader("🧠 AI Resume Feedback")

        if ats_score >= 80:
            st.success("Excellent resume. Minor optimization needed.")
        elif ats_score >= 60:
            st.warning("Good resume but missing JD alignment.")
        else:
            st.error("Resume is not ATS optimized.")

        st.subheader("✍️ AI Resume Rewrite Suggestions")
        for r in generate_rewrite_suggestions(missing):
            st.write("•", r)

        st.subheader("🛠 Section-wise Improvement Plan")
        for section, tips in section_wise_feedback(missing).items():
            with st.expander(section):
                for tip in tips:
                    st.write("➕", tip)

        #  SAVE TO DATABASE 
        save_resume_analysis(
            st.session_state.user_id,
            ats_score,
            missing
        )

        st.success("📁 Resume analysis saved successfully")
