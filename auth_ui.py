import streamlit as st
import time
import sqlite3



# DATABASE CONNECTION

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)



# AUTH UI

def auth_ui():

    st.set_page_config(
        page_title="AI Career Coach | Auth",
        layout="centered"
    )

    #  SESSION INIT 
    if "mode" not in st.session_state:
        st.session_state.mode = "login"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = ""

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "user_role" not in st.session_state:
        st.session_state.user_role = "user"   
    


    #  STYLES 
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }

    .auth-card {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(12px);
        width: 420px;
        margin: auto;
        padding: 32px;
        border-radius: 18px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.45);
    }

    .title {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 24px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: white;
        border-radius: 10px;
        height: 44px;
        font-weight: 600;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)


    #  UI CARD 
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)

    st.markdown("<div class='title'>AI Career Coach</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Login to continue your growth 🚀</div>",
        unsafe_allow_html=True
    )

    #  TOGGLE 
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Login", use_container_width=True):
            st.session_state.mode = "login"

    with c2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.mode = "signup"


    #  FORM 
    with st.form("auth_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        confirm = None
        if st.session_state.mode == "signup":
            confirm = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button(
            "Create Account" if st.session_state.mode == "signup" else "Login"
        )

        if submit:
            if not username or not password:
                st.error("⚠️ Username and Password required")
                return

            conn = get_connection()
            cur = conn.cursor()

            #  SIGN UP 
            if st.session_state.mode == "signup":

                if password != confirm:
                    st.error("❌ Passwords do not match")
                    conn.close()
                    return

                try:
                    cur.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, password)
                    )
                    conn.commit()
                    st.success("✅ Account created successfully")
                    time.sleep(1)
                    st.session_state.mode = "login"
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("⚠️ Username already exists")

                finally:
                    conn.close()

            #  LOGIN 
            else:
                cur.execute(
                    "SELECT id, username,role FROM users WHERE username=? AND password=?",
                    (username, password)
                )
                user = cur.fetchone()
                conn.close()

                if user:
                    st.session_state.logged_in = True
                    
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.session_state.user = user[1]
                    st.session_state.user_role = user[2]

                    st.success(f"🎉 Welcome {user[1]} (user[2])")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)
