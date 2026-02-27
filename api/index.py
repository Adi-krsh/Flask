from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME")
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/user/add', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, (username, email, password))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('login'))

@app.route('/user/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return f"Welcome, {user[1]}"
    else:
        return "Invalid credentials"

# IMPORTANT for Vercel
app = app