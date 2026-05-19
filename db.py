import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    #  USERS 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
         role TEXT DEFAULT 'user',        
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
     #  SAFE ROLE COLUMN ADD 
    cur.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cur.fetchall()]
    if "role" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")

    #  RESUME ANALYSIS 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resume_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        ats_score REAL,
        missing_keywords TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    #  RESUME BUILDER 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resume_builder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        email TEXT,
        phone TEXT,
        linkedin TEXT,
        objective TEXT,
        skills TEXT,
        education TEXT,
        projects TEXT,
        certifications TEXT,
        template TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    #  CAREER ROADMAP 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS career_roadmap (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        roadmap TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
