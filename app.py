from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    doctor TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vet_appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_name TEXT,
    doctor TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pet_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vaccinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_name TEXT,
    vaccine_date TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/human')
def human():
    return render_template('human.html')

@app.route('/vet')
def vet():
    return render_template('vet.html')

@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()

    return render_template('admin.html', appointments=appointments)

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        name = request.form['name']
        doctor = request.form['doctor']
        date = request.form['date']
        time = request.form['time']

        cursor.execute(
            "INSERT INTO appointments (name, doctor, date, time) VALUES (?, ?, ?, ?)",
            (name, doctor, date, time)
        )
        conn.commit()

        return "Appointment Booked Successfully!"

    return render_template('appointment.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        file = request.files['report_file']

        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            cursor.execute(
                "INSERT INTO reports (report_name) VALUES (?)",
                (file.filename,)
            )
            conn.commit()

            return "Medical Report Uploaded Successfully!"

    return render_template('report.html')
@app.route('/symptom')
def symptom():
    return render_template('symptom.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/remedies')
def remedies():
    return render_template('remedies.html')

@app.route('/vet_appointment', methods=['GET', 'POST'])
def vet_appointment():
    if request.method == 'POST':
        pet_name = request.form['pet_name']
        doctor = request.form['doctor']
        date = request.form['date']
        time = request.form['time']

        cursor.execute(
            "INSERT INTO vet_appointments (pet_name, doctor, date, time) VALUES (?, ?, ?, ?)",
            (pet_name, doctor, date, time)
        )
        conn.commit()

        return "Vet Appointment Booked Successfully!"

    return render_template('vet_appointment.html')

@app.route('/pet_records', methods=['GET', 'POST'])
def pet_records():
    if request.method == 'POST':
        file = request.files['pet_file']

        if file:
            filepath = os.path.join(
                app.config['UPLOAD_FOLDER'],
                file.filename
            )
            file.save(filepath)

            cursor.execute(
                "INSERT INTO pet_records (file_name) VALUES (?)",
                (file.filename,)
            )
            conn.commit()

            return "Pet Record Uploaded Successfully!"

    return render_template('pet_records.html')

@app.route('/pet_symptom', methods=['GET', 'POST'])
def pet_symptom():
    if request.method == 'POST':
        symptom = request.form['symptom']

        if "vomiting" in symptom.lower():
            result = "Possible issue: Digestive problem"

        elif "fever" in symptom.lower():
            result = "Possible issue: Infection"

        elif "skin" in symptom.lower():
            result = "Possible issue: Skin allergy"

        else:
            result = "Please consult a veterinarian"

        return result

    return render_template('pet_symptom.html')

@app.route('/vaccination', methods=['GET', 'POST'])
def vaccination():
    if request.method == 'POST':
        pet_name = request.form['pet_name']
        vaccine_date = request.form['vaccine_date']

        cursor.execute(
            "INSERT INTO vaccinations (pet_name, vaccine_date) VALUES (?, ?)",
            (pet_name, vaccine_date)
        )
        conn.commit()

        return "Vaccination Reminder Set Successfully!"

    return render_template('vaccination.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template("forgot_password.html")

@app.route('/reset', methods=['POST'])
def reset():
    email = request.form['email']
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)