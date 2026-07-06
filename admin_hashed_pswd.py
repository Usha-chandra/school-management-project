import sqlite3
from werkzeug.security import generate_password_hash

def init_admin():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # check if admin exists
    cursor.execute("SELECT id FROM users WHERE user_name='admin'")
    admin = cursor.fetchone()

    if not admin:
        # only create admin if missing
        hashed_pw = generate_password_hash("admin123")
        cursor.execute("INSERT INTO users (user_name, user_password, role) VALUES (?, ?, ?)",
                       ("admin", hashed_pw, "admin"))
        print("✅ Admin account created.")
    else:
        print("ℹ️ Admin already exists, no changes made.")

    conn.commit()
    conn.close()
