#from werkzeug.security import generate_password_hash
import sqlite3

conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
cursor = conn.cursor()

# Drop old table
#cursor.execute("DROP TABLE IF EXISTS students")

# Create students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT NOT NULL,

    dob TEXT NOT NULL,

    grade TEXT NOT NULL
        CHECK (grade IN ('1','2','3','4','5','6','7','8','9','10')),

    gender TEXT NOT NULL
        CHECK (gender IN ('Male','Female','Other')),

    email TEXT,

    phone_number TEXT NOT NULL,

    address TEXT NOT NULL
)
''')

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_name TEXT NOT NULL,

    user_password TEXT NOT NULL
)
''')
# cursor.execute('''ALTER TABLE users ADD COLUMN role TEXT''')

#cursor.execute(
    #"INSERT INTO users (user_name, user_password,role) VALUES (?, ?,?)",
   # ("admin", "admin123","admin"))
#cursor.execute('''UPDATE users SET role='admin' WHERE id=1''')
#cursor.execute('''UPDATE users SET role='user' WHERE role IS NULL''')
#cursor.execute('''UPDATE users 
#SET user_password='pbkdf2:sha256:260000$DuHloILlnEgegaBc$7b5d1fdf1c6113347cb9b7c336d023d735c6691a12845810d6a48e85596c5abd',role='admin' 
#WHERE user_name='admin' ''')


#hashed_pw = generate_password_hash("admin123")
#cursor.execute("UPDATE users SET user_password=?, role='admin' WHERE user_name='admin'", (hashed_pw,))



conn.commit()

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print(rows)
conn.close()

#print("Tables created successfully")

