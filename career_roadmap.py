import streamlit as st
import sqlite3
import json

# DATABASE

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def save_career_roadmap(user_id, domain, role, level, roadmap, weeks, months):
    conn = get_connection()
    cur = conn.cursor()

    roadmap_data = {
        "domain": domain,
        "role": role,
        "level": level,
        "steps": roadmap,
        "weeks": weeks,
        "months": months
    }

    cur.execute("""
        INSERT INTO career_roadmap (user_id, roadmap)
        VALUES (?, ?)
    """, (
        user_id,
        json.dumps(roadmap_data)
    ))

    conn.commit()
    conn.close()


# CAREER ROADMAP DATA

CAREER_DOMAINS = {
    "Technology": {
        "Data Scientist": {
            "Beginner": [
                ("Python Basics", 40),
                ("Statistics & Probability", 50),
                ("Pandas & NumPy", 30),
                ("Mini Data Analysis Project", 20)
            ],
            "Intermediate": [
                ("Machine Learning Algorithms", 60),
                ("Data Visualization", 30),
                ("SQL for Data Science", 30),
                ("End-to-End ML Project", 50)
            ],
            "Advanced": [
                ("Deep Learning", 60),
                ("Model Deployment", 40),
                ("Kaggle Competitions", 40),
                ("Portfolio Optimization", 20)
            ]
        },

        "Web Developer": {
            "Beginner": [
                ("HTML, CSS, JavaScript", 40),
                ("Responsive Design", 20),
                ("Git & GitHub", 15),
                ("Mini Website Project", 25)
            ],
            "Intermediate": [
                ("React.js", 50),
                ("Backend (Flask/Django)", 50),
                ("APIs & Database", 30),
                ("Full Stack Project", 40)
            ],
            "Advanced": [
                ("System Design Basics", 30),
                ("Performance Optimization", 25),
                ("Cloud Deployment", 30),
                ("Portfolio & Interview Prep", 25)
            ]
        }
    },

    "Business & Management": {
        "MBA Aspirant": {
            "Beginner": [
                ("Quantitative Aptitude", 40),
                ("Logical Reasoning", 30),
                ("Business Fundamentals", 30)
            ],
            "Intermediate": [
                ("CAT Level Practice", 60),
                ("Case Studies", 40),
                ("Mock Tests", 40)
            ],
            "Advanced": [
                ("GD & PI Preparation", 40),
                ("Advanced Mock Analysis", 30),
                ("B-School Applications", 20)
            ]
        },

        "Digital Marketing": {
            "Beginner": [
                ("Marketing Fundamentals", 30),
                ("SEO Basics", 25),
                ("Social Media Marketing", 25)
            ],
            "Intermediate": [
                ("Google Ads & Analytics", 40),
                ("Content Strategy", 30),
                ("Live Campaign Project", 40)
            ],
            "Advanced": [
                ("Growth Marketing", 30),
                ("Conversion Optimization", 30),
                ("Portfolio & Freelancing", 25)
            ]
        }
    },

    "Creative & Media": {
        "Graphic Designer": {
            "Beginner": [
                ("Design Principles", 30),
                ("Photoshop / Canva", 30),
                ("Color Theory", 20)
            ],
            "Intermediate": [
                ("Illustrator / Figma", 40),
                ("Branding Projects", 40),
                ("UI Design Basics", 30)
            ],
            "Advanced": [
                ("Advanced UI/UX", 40),
                ("Client Projects", 40),
                ("Portfolio & Freelancing", 30)
            ]
        },

        "Video Editor": {
            "Beginner": [
                ("Premiere Pro Basics", 30),
                ("Short Video Editing", 25),
                ("Transitions & Effects", 20)
            ],
            "Intermediate": [
                ("YouTube Editing", 40),
                ("Motion Graphics Basics", 30),
                ("Client Practice", 30)
            ],
            "Advanced": [
                ("Advanced Motion Graphics", 40),
                ("Brand Editing", 30),
                ("Freelancing & Monetization", 30)
            ]
        }
    }
}


# HELPER

def calculate_duration(total_hours, hours_per_day):
    days = total_hours / hours_per_day
    weeks = int(days / 7)
    months = round(weeks / 4, 1)
    return weeks, months


# STREAMLIT UI

def show_career_roadmap():

    # 🔐 LOGIN CHECK
    if not st.session_state.logged_in:
        st.warning("🔐 Please login to generate career roadmap")
        return

    st.title("🧭 AI Career Roadmap Generator")
    st.caption("Personalized roadmap with time estimation")

    col1, col2, col3 = st.columns(3)

    with col1:
        domain = st.selectbox("🌍 Domain", CAREER_DOMAINS.keys())

    with col2:
        role = st.selectbox(
            "🎯 Career Role",
            CAREER_DOMAINS[domain].keys()
        )

    with col3:
        level = st.selectbox(
            "📊 Your Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

    hours_per_day = st.slider(
        "⏱️ Study Hours per Day",
        min_value=1,
        max_value=10,
        value=3
    )

    st.divider()

    if st.button("🚀 Generate Roadmap", use_container_width=True):

        roadmap = CAREER_DOMAINS[domain][role][level]
        total_hours = sum(step[1] for step in roadmap)
        weeks, months = calculate_duration(total_hours, hours_per_day)

        #  SUMMARY 
        st.markdown(f"""
        <div style="
            padding:20px;
            border-radius:15px;
            background:linear-gradient(135deg,#1d2671,#c33764);
            color:white;">
            <h2>🎯 {role}</h2>
            <p><b>Domain:</b> {domain}</p>
            <p><b>Level:</b> {level}</p>
            <p><b>Estimated Time:</b> {weeks} weeks (~{months} months)</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        #  ROADMAP STEPS 
        progress = 0
        step_weight = 100 / len(roadmap)

        for i, (step, hrs) in enumerate(roadmap, start=1):
            progress += step_weight
            st.markdown(f"### ✅ Step {i}: {step}")
            st.progress(int(progress))
            st.write(f"📘 Estimated Effort: **{hrs} hours**")
            st.divider()

        #  SAVE 
        save_career_roadmap(
            st.session_state.user_id,
            domain,
            role,
            level,
            roadmap,
            weeks,
            months
        )

        st.success("💾 Career roadmap saved successfully 🎉")
