from flask import Flask, jsonify
import requests
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

DATABASE = 'connectivity.db'

def check_connectivity():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS connectivity
                 (id INTEGER PRIMARY KEY, status TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def log_status(status):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO connectivity (status) VALUES (?)", (status,))
    conn.commit()
    conn.close()

def send_notification():
    sender_email = "your_email@example.com"
    receiver_email = "admin@example.com"
    password = "your_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Internet Connectivity Alert"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = "Internet connection is down!"
    part = MIMEText(text, "plain")
    message.attach(part)

    server = smtplib.SMTP_SSL('smtp.example.com', 465)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

@app.route('/check_connectivity', methods=['GET'])
def connectivity_status():
    status = "up" if check_connectivity() else "down"
    log_status(status)
    if status == "down":
        send_notification()
    return jsonify({"status": status})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
