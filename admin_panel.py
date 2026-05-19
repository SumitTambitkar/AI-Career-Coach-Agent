import streamlit as st
import sqlite3
from datetime import datetime

# DATABASE CONNECTION

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ADMIN ACCESS CHECK

def is_admin():
    return (
        st.session_state.get("logged_in") and
        st.session_state.get("user_role") == "admin"
    )

# FETCH DATA

def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role, created_at FROM users")
    data = cur.fetchall()
    conn.close()
    return data


def get_resume_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM resume_builder")
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_analysis_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM resume_analysis")
    count = cur.fetchone()[0]
    conn.close()
    return count


# UPDATE USER ROLE

def update_role(user_id, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET role=? WHERE id=?",
        (role, user_id)
    )
    conn.commit()
    conn.close()


# ADMIN PANEL UI

def show_admin_panel():

    if not is_admin():
        st.error("🚫 Access Denied: Admins only")
        return

    st.title("🔐 Admin Dashboard")
    st.caption("Career Coach Agent – System Control Panel")

    # STATS 
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("👥 Total Users", len(get_users()))
    with c2:
        st.metric("📄 Resumes Built", get_resume_count())
    with c3:
        st.metric("📊 Resume Analysis", get_analysis_count())

    st.divider()

    #  USER MANAGEMENT 
    st.subheader("👥 User Management")

    users = get_users()

    for user in users:
        uid, username, role, created_at = user

        with st.expander(f"👤 {username} ({role})"):
            st.write(f"🆔 User ID: {uid}")
            st.write(f"📅 Created At: {created_at}")

            new_role = st.selectbox(
                "Change Role",
                ["user", "admin"],
                index=0 if role == "user" else 1,
                key=f"role_{uid}"
            )

            if st.button("💾 Update Role", key=f"btn_{uid}"):
                update_role(uid, new_role)
                st.success(f"Role updated to {new_role}")
                st.rerun()

    st.divider()

    # SYSTEM INFO 
    st.subheader("⚙️ System Info")

    st.info(f"""
    🖥 App Name: AI Career Coach Agent  
    🕒 Admin Login Time: {datetime.now().strftime('%d %b %Y %H:%M:%S')}  
    🗄 Database: SQLite  
    🔐 Access Level: Admin
    """)

    st.success("✅ Admin panel running successfully")
