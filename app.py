import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from database import init_db, DB_PATH
from decorators import login_required

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database. Note: Switching from cs50 library to sqlite3 to learn without 'training wheels'.
# I'm using sqlite so the app won't be able to manage multiple users at the same time. That's fine for the scope of this project.
# If no database file exists, it will be created automatically. 
init_db()
db = sqlite3.connect(DB_PATH)

# Adding cache control to avoid caching issues.
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Welcome page route
@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

# Root route redirects to dashboard if logged in, otherwise to Welcome page.
@app.route("/")
@login_required
def index():
    return render_template("dashboard.html")

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
        
# TODO: Add error handling for duplicate usernames/emails and other potential issues.
            
        # Flash if successful 
        flash("Registered successfully! Please log in.", "success")
        # Redirect to the login page
        return redirect("/login")

# TODO: Create login template.    

    else:
        return render_template("register.html")