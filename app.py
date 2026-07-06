from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask,session, redirect,url_for, render_template,request
import sqlite3
from datetime import datetime 
app = Flask(__name__)
# Secret key is required for sessions
app.secret_key = "usha_secret_key"
@app.route("/")
def index():
    return redirect("/login")   # 🚀 First page is login
@app.route("/home")
def home():
    if "user_name" not in session:
        return redirect("/login")
    if "user_name" in session:   # ✅ Check if user is logged in
        return render_template("home.html", user_name=session["user_name"])
    else:
        return redirect("/login")   # 🚫 If not logged in, send back to login
@app.route("/add_student",methods=["GET", "POST"])
def add_student():
    if "user_name" not in session:
        return redirect("/login")
    
    if request.method == "POST":
        errors = []
        student_name = request.form["student_name"]
        clean_name = student_name.replace(" ","")
        if not clean_name.isalpha():
            errors.append("Student name should contain only letters")
            
        DOB = request.form["DOB"]
        dob_date = datetime.strptime(DOB, "%Y-%m-%d").date()
        todaydate= datetime.now().date()
        if dob_date> todaydate:
            errors.append("Date of Birth cannot be a future date")
            
        grade = request.form["grade"]
        if grade=="Select Grade":
            errors.append("Please select the grade")
            
    
        gender = request.form["gender"]
        
        if gender not in ["Male", "Female", "Other"]:
            errors.append("Please select the valid gender")
            
        address = request.form["address"]
        clean_address = address.strip()
        if not clean_address:
            errors.append("Address cannot be empty")
            
        phone_number = request.form["phone"]
        if not phone_number.isdigit() or len(phone_number)!=10:
            errors.append("Please enter a valid phone number")
            
        email = request.form["email"]
        if email:
             if "@" not in email or "." not in email:
                errors.append("Please enter a valid email address")
                
             
#option1            
# Advanced Email Validation using Regex
# first import re
# email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

# if email and not re.match(email_pattern, email):
#     message6 = "Please enter a valid email address"
#     return render_template("add_student.html", message6=message6)



#Option 2: Library-Based Validation
#pip install email-validator
# from email_validator import validate_email, EmailNotValidError

# try:
#     validate_email(email)
# except EmailNotValidError:
#     message6 = "Please enter a valid email address"
#     return render_template("add_student.html", message6=message6)
        conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
        cursor = conn.cursor()
        # cursor.execute('''INSERT INTO students (student_name, dob, grade, gender, email, phone_number, address) VALUES (?, ?, ?, ?, ?, ?, ?)''', (student_name, DOB, grade, gender, email, phone_number, address))
        # cursor.execute("SELECT * FROM students")
        # rows = cursor.fetchall()
        # print(rows)
        # conn.commit()
        # conn.close()
        # return render_template("success.html" , student_name=student_name, DOB=DOB, grade=grade, gender=gender,  email=email, phone_number=phone_number, address=address)
        if errors:
            return render_template("add_student.html", errors=errors)  
        
        try:
            cursor.execute('''INSERT INTO students
            (student_name, dob, grade, gender, email, phone_number, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (student_name, DOB, grade, gender, email, phone_number, address))

            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            print(rows)

            conn.commit()
            return redirect("/view_students")

        #return render_template("success.html",student_name=student_name,DOB=DOB,grade=grade,gender=gender,email=email,phone_number=phone_number,address=address)

        except sqlite3.IntegrityError:
            error_message = "Database validation failed. Please check your inputs."

            return render_template("add_student.html",error_message=error_message)

        except Exception as e:
            return f"Error: {e}"
        
        finally:
            conn.close()
    return render_template("add_student.html")
@app.route("/view_students",methods=["GET", "POST"])
def view_students():
    if "user_name" not in session:
        return redirect("/login")
    conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
    cursor = conn.cursor()
    if request.method == "POST":
        student_name = request.form["student_name"]
        grade = request.form["grade"]
        search_name = student_name + "%"
        if not student_name and not grade :
            message = "Please fill the search criteria"
            return render_template("view_students.html", message=message)
        elif student_name and not grade :
            cursor.execute("SELECT * FROM students WHERE student_name LIKE?",(search_name,))
            students=cursor.fetchall()   
        elif not student_name and grade:
            cursor.execute("SELECT * FROM students WHERE grade = ?",(grade,))
            students=cursor.fetchall() 
        else :
            cursor.execute("SELECT * FROM students WHERE student_name LIKE ? AND grade = ?",(search_name,grade,))
            students=cursor.fetchall()
            if not students:
               message1 ="No student found"
               return render_template("view_students.html", message1=message1)
    else :
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        #print(students)
    conn.close()
    return render_template("view_students.html", students=students)
@app.route("/edit_student/<int:id>" , methods=["GET", "POST"])
def edit_student(id):
    conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
    cursor = conn.cursor()
    if request.method == "POST":
        student_name = request.form["student_name"]
        DOB = request.form["DOB"]
        grade = request.form["grade"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone_number = request.form["phone"]
        address = request.form["address"]
        cursor.execute("""UPDATE students SET student_name=?, dob=?, grade=?, gender=?, email=?, phone_number=?, address=? WHERE id=?""", (student_name, DOB, grade, gender, email, phone_number, address, id))
        conn.commit()
        conn.close()
        return redirect("/view_students")
    else:
        cursor.execute("SELECT * FROM students WHERE id=?", (id,))
        student = cursor.fetchone()
        conn.close()
        return render_template("edit_student.html", student=student)
@app.route("/delete_student/<int:id>")
def delete_student(id):
    conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/view_students")

@app.route("/register",methods= ["GET","POST"])
def register():
    if request.method == "POST":
        user_name=request.form["user_name"]
        user_password=request.form["user_password"]
        hashed_password=generate_password_hash(user_password)
    
        conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users(user_name,user_password,role) values(?,?,?)''',(user_name,hashed_password,"user"))
        conn.commit()
        conn.close()
        return render_template("register.html", success=True, user_name=user_name)
    return render_template("register.html")   
@app.route("/login",methods= ["GET","POST"])
def login():
    if request.method == "POST":
        user_name=request.form["user_name"]
        user_password=request.form["user_password"]
        conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_password, role from users WHERE user_name = ?",(user_name,))
        row = cursor.fetchone()
        if row is None:
            # No such user
            conn.close()
            return render_template("login.html", error="User not found")
        stored_hash = row[0] 
        role=row[1]  # the hashed password string
        if check_password_hash(stored_hash, user_password,):
            session["user_name"] = user_name
            session["role"]=role
            conn.close()
            if role=="admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return render_template("home.html")
        else:
            conn.close()
            return render_template("login.html", error="Invalid Credentials")
    return render_template("login.html")
@app.route("/logout")
def logout():
    session.pop("user_name", None) 
    session.pop("role",None)  # ✅ Remove user from session
    return redirect("/login")    
@app.route("/admin_dashboard")
def admin_dashboard():
        conn = sqlite3.connect("F:/Usha Projects/SchoolManagementProject/student_web_app/students.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) from students''')
        total_students=cursor.fetchone()[0]
        cursor.execute('''SELECT gender, COUNT(*) from students GROUP BY gender''')
        gender_counts=cursor.fetchall()
        cursor.execute('''SELECT grade, COUNT(*) from students GROUP BY grade''')
        grade_counts=cursor.fetchall()
        conn.close()
        print(total_students)
        print(gender_counts)
        print(grade_counts)
        return render_template("admin_dashboard.html",total_students=total_students,gender_counts=gender_counts,grade_counts=grade_counts)
if __name__ == "__main__":
    app.run(debug=True)