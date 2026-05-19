import streamlit as st

from auth_ui import auth_ui
from resume_analyzer import show_resume_analyzer
from resume_builder import show_resume_builder
from career_roadmap import show_career_roadmap
from chatbot import show_chatbot
from db import create_tables
from admin_panel import show_admin_panel


# PAGE CONFIG

st.set_page_config(
    page_title="AI Career Coach Agent",
    page_icon="🎓",
    layout="wide"
)

create_tables()



# SESSION STATE

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_role" not in st.session_state:
    st.session_state.user_role = "user"

if "feature" not in st.session_state:
    st.session_state.feature = "🏠 Dashboard"

if "next_feature" not in st.session_state:
    st.session_state.next_feature = None



# ROUTER (LOGIN GUARD)

def go_to(feature_name):
    if not st.session_state.logged_in and feature_name != "🏠 Dashboard":
        st.session_state.next_feature = feature_name
        st.session_state.feature = "🔐 Login"
    else:
        st.session_state.feature = feature_name
    

# SIDEBAR

with st.sidebar:
    st.markdown("## 🎓 AI Career Coach Agent")
    st.caption("Placement-Ready Career Guidance System")

    if st.session_state.logged_in:
        st.success(f"👤 {st.session_state.user}")
    else:
        st.info("🔓 Guest Mode")

    st.markdown("---")

    st.button("🏠 Dashboard", on_click=go_to, args=("🏠 Dashboard",))
    st.button("📄 Resume Analyzer", on_click=go_to, args=("📄 Resume Analyzer",))
    st.button("📝 Resume Builder", on_click=go_to, args=("📝 Resume Builder",))
    st.button("🗺️ Career Roadmap", on_click=go_to, args=("🗺️ Career Roadmap",))
    st.button("🤖 Chatbot", on_click=go_to, args=("🤖 Chatbot",))
   
     # 🔐 ADMIN PANEL BUTTON
    if st.session_state.logged_in and st.session_state.user_role == "admin":
        st.markdown("---")
        st.button(
            "🔐 Admin Panel",
            on_click=go_to,
            args=("🔐 Admin Panel",),
            use_container_width=True
        )

    if st.session_state.logged_in:
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.user_id = None
            st.session_state.user_role = "user"
            st.session_state.feature = "🏠 Dashboard"
            st.rerun()


# LOGIN PAGE

if st.session_state.feature == "🔐 Login":

    auth_ui()

    if st.session_state.logged_in:
        target = st.session_state.next_feature or "🏠 Dashboard"
        st.session_state.next_feature = None
        st.session_state.feature = target
        st.rerun()



# DASHBOARD (PUBLIC)

elif st.session_state.feature == "🏠 Dashboard":

    user = st.session_state.user or "Guest"

    st.markdown(f"""
        <div style="
            padding:30px;
            border-radius:15px;
            background:linear-gradient(135deg,#1f4037,#99f2c8);
            color:white;">
            <h1>🎓 Welcome, {user}</h1>
            <h4>Your AI-Powered Career Growth Platform</h4>
            <p>Analyze • Build • Improve • Get Placed</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🚀 Platform Capabilities")

    q1, q2 = st.columns(2)

    with q1:
            st.success("📄 ATS Resume Analysis")
            st.write(
                "• Semantic matching\n"
                "• Skill gap detection\n"
                "• JD alignment\n"
                "• Industry feedback"
            )

            st.success("🗺️ Career Roadmap")
            st.write(
                "• Step-by-step learning\n"
                "• Role-based planning\n"
                "• Placement focus"
            )

    with q2:
            st.success("📝 Smart Resume Builder")
            st.write(
                "• Editable preview\n"
                "• Professional format\n"
                "• One-click PDF"
            )

            st.success("🤖 AI Career Chatbot")
            st.write(
                "• Interview Q&A\n"
                "• Resume help\n"
                "• ML + OpenAI"
            )

    st.markdown("---")

    st.subheader("⚡ Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.button("📄 Analyze Resume", use_container_width=True,
                  on_click=go_to, args=("📄 Resume Analyzer",))

    with c2:
        st.button("📝 Build Resume", use_container_width=True,
                  on_click=go_to, args=("📝 Resume Builder",))

    with c3:
        st.button("🗺️ Generate Roadmap", use_container_width=True,
                  on_click=go_to, args=("🗺️ Career Roadmap",))



# MODULES (PROTECTED)

elif st.session_state.feature == "📄 Resume Analyzer":
    show_resume_analyzer()

elif st.session_state.feature == "📝 Resume Builder":
    show_resume_builder()

elif st.session_state.feature == "🗺️ Career Roadmap":
    show_career_roadmap()

elif st.session_state.feature == "🤖 Chatbot":
    show_chatbot()

elif st.session_state.feature == "🔐 Admin Panel":
    show_admin_panel()