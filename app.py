from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)

# Secret key from environment variable
app.secret_key = os.environ.get("SECRET_KEY")

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
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

    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vet_appointments")
    total_vet = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pet_records")
    total_pet_records = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vaccinations")
    total_vaccinations = cursor.fetchone()[0]

    return render_template(
        'admin.html',
        appointments=appointments,
        total_appointments=total_appointments,
        total_vet=total_vet,
        total_reports=total_reports,
        total_pet_records=total_pet_records,
        total_vaccinations=total_vaccinations
    )

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

@app.route('/chatbot_response', methods=['POST'])
def chatbot_response():
    user_message = request.form['message'].lower()

    if "fever" in user_message:
        reply = "Drink plenty of water, take rest, and consult a doctor if fever continues."

    elif "cold" in user_message:
        reply = "Drink warm water and take proper rest."

    elif "headache" in user_message:
        reply = "Stay hydrated and avoid screen time."

    elif "cough" in user_message:
        reply = "Use warm fluids and consult a doctor if severe."

    elif "pet vomiting" in user_message:
        reply = "Please consult a veterinarian immediately."

    elif "dog fever" in user_message:
        reply = "Monitor temperature and visit a vet."

    else:
        reply = "Please consult a healthcare professional for accurate advice."

    return f"<h2>{reply}</h2><br><a href='/chatbot'>Go Back</a>"

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/insurance')
def insurance():
    return render_template('insurance.html')

@app.route('/pharmacy')
def pharmacy():
    return render_template('pharmacy.html')

@app.route('/google-login')
def google_login():
    return google.authorize_redirect(
        redirect_uri='http://localhost:5000/authorize'
    )

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()

    user_info = google.get(
        'https://www.googleapis.com/oauth2/v1/userinfo'
    ).json()

    session['user'] = user_info

    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
