from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/user/add", methods=["POST"])
def add_user():
    try:
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("home"))

    except Exception as e:
        return f"Error adding user: {str(e)}"


@app.route("/user/login", methods=["POST"])
def login_user():
    try:
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return f"Welcome, {user[1]}"
        else:
            return "Invalid credentials"

    except Exception as e:
        return f"Login error: {str(e)}"


app = app