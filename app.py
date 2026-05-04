import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database. Note: Switching from cs50 library to sqlite3 to learn without 'training wheels'.
db = sqlite3.connect("cashflow_tracker.db")

# Adding cache control to avoid caching issues.
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Root route redirects to dashboard if logged in, otherwise to Welcome page.
@app.route("/")
def index():
    if "user_id" in session:
        return render_template("dashboard.html")
    else:
        return render_template("welcome.html")

# Register route for new users to create an account.
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", (username, email, hashed_password))
        db.commit()

        # Redirect to the login page
        return redirect("/login")

    else:
        return render_template("register.html") 
