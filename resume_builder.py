import streamlit as st
from fpdf import FPDF
import sqlite3

#  DATABASE 

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def save_resume(user_id, data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO resume_builder (
            user_id, name, email, phone, linkedin,
            objective, skills, education, projects,
            certifications, template
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        data["name"],
        data["email"],
        data["phone"],
        data["linkedin"],
        data["objective"],
        data["skills"],
        data["education"],
        data["projects"],
        data["certifications"],
        data["template"]
    ))

    conn.commit()
    conn.close()


#  PDF GENERATOR 

def generate_resume_pdf(data, filename="resume.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    template = data["template"]

    if template == "Classic":
        title_size, heading_size, body_size = 18, 13, 11
    elif template == "Modern":
        title_size, heading_size, body_size = 20, 14, 11
    else:
        title_size, heading_size, body_size = 17, 12, 10

    pdf.set_font("Arial", "B", title_size)
    pdf.cell(0, 10, data["name"], ln=True, align="C")

    pdf.set_font("Arial", "", body_size)
    contact = " | ".join(filter(None, [data["email"], data["phone"]]))
    if contact:
        pdf.cell(0, 8, contact, ln=True, align="C")
    if data["linkedin"]:
        pdf.cell(0, 8, data["linkedin"], ln=True, align="C")

    pdf.ln(6)

    def section(title, content):
        if content.strip():
            pdf.set_font("Arial", "B", heading_size)
            pdf.cell(0, 8, title, ln=True)
            pdf.set_font("Arial", "", body_size)
            pdf.multi_cell(0, 7, content)
            pdf.ln(3)

    section("Career Objective", data["objective"])
    section("Technical Skills", data["skills"])
    section("Education", data["education"])
    section("Projects / Internship", data["projects"])
    section("Certifications", data["certifications"])

    pdf.output(filename)
    return filename


#  STREAMLIT UI 

def show_resume_builder():

    # 🔐 Login check
    if not st.session_state.logged_in:
        st.warning("🔐 Please login to build resume")
        return

    st.title("📝 Smart Resume Builder")

    if "preview" not in st.session_state:
        st.session_state.preview = False
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = {}

    template = st.radio(
        "🎨 Select Template",
        ["Classic", "Modern", "Professional"],
        horizontal=True
    )

    name = st.text_input("Full Name *")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    linkedin = st.text_input("LinkedIn / GitHub")

    objective = st.text_area("Career Objective")
    skills = st.text_area("Skills")
    education = st.text_area("Education")
    projects = st.text_area("Projects / Internship")
    certifications = st.text_area("Certifications")

    if st.button("👀 Generate Preview"):
        if not name:
            st.warning("Name is mandatory")
            return

        st.session_state.resume_data = {
            "template": template,
            "name": name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "objective": objective,
            "skills": skills,
            "education": education,
            "projects": projects,
            "certifications": certifications,
        }
        st.session_state.preview = True

    if st.session_state.preview:
        st.divider()
        st.subheader("📄 Resume Preview")

        d = st.session_state.resume_data

        st.markdown(f"## {d['name']}")
        st.markdown(f"**{d['email']} | {d['phone']}**")
        st.markdown(d["linkedin"])

        if d["objective"]:
            st.markdown("### 🎯 Career Objective")
            st.write(d["objective"])

        if d["skills"]:
            st.markdown("### 🧠 Skills")
            st.write(d["skills"])

        if d["education"]:
            st.markdown("### 🎓 Education")
            st.write(d["education"])

        if d["projects"]:
            st.markdown("### 💼 Projects")
            st.write(d["projects"])

        if d["certifications"]:
            st.markdown("### 📜 Certifications")
            st.write(d["certifications"])

        if st.button("💾 Save Resume & Download PDF"):
            save_resume(st.session_state.user_id, d)
            filename = generate_resume_pdf(d)

            st.success("✅ Resume saved to database")

            with open(filename, "rb") as f:
                st.download_button(
                    "⬇️ Download Resume PDF",
                    f,
                    file_name="Resume.pdf",
                    mime="application/pdf"
                )
