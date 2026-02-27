from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


# Get database URL from Vercel environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


# =========================
# SIGNUP
# =========================
@app.route("/user/add", methods=["POST"])
def add_user():
    try:
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        # Hash password before storing
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(username)=LOWER(%s)",
            (username,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            conn.close()
            return "Username already exists"

        # Insert user
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("home"))

    except Exception as e:
        return f"Error adding user: {str(e)}"


# =========================
# LOGIN
# =========================
@app.route("/user/login", methods=["POST"])
def login_user():
    try:
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Case-insensitive username search
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(username)=LOWER(%s)",
            (username,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user[3], password):
            return f"Welcome, {user[1]}"

        return "Invalid credentials"

    except Exception as e:
        return f"Login error: {str(e)}"


# Required for Vercel
app = app