import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import check_password_hash, generate_password_hash
from database import init_db, DB_PATH
from decorators import login_required
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
import re


# Load environment variables from .env file. Remember to create a .env file with needed variables. See the .env.example file for reference.
load_dotenv()

# Configure application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise ValueError("SECRET_KEY is not set in the environment variables (.env file). Please set it to a secure random value.")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure rate limiter to prevent abuse.
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)


# Configure database. 
# Note: Switching from cs50 library to sqlite3 to learn without 'training wheels'.
# I'm using sqlite, the app won't be able to manage multiple users at the same time. That's fine for the scope of this project.
# If no database file exists, it will be created automatically. 
init_db()
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row  # To return rows as dictionaries
    return g.db

# Close the database connection after each request to prevent resource leaks.
@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


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
    return redirect("/dashboard/")


#TODO: @app.route("/dashboard") to show user's transactions and balance.
#TODO: Verify that SECRET_KEY is beign used. Log in, then chance secret key and check


# Register route for new users to create an account.
@app.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")  # Limit registration attempts to prevent abuse. 
def register():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
      
        # Validate form data.
        if not username or not email or not password:
            flash("Please fill out all fields.", "danger")
            return render_template("register.html")
        # Validate username
        if not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9_]{1,16}[a-zA-Z0-9]$", username):
            flash("Username can only contain letters and numbers. It can also have underscores in between but not at the beginning or end.", "danger") 
            return render_template("register.html")
        # Validate email
        try:
            validated_email = validate_email(email, check_deliverability=False) # check_deliverability=False to avoid latency.
            email = validated_email.normalized
        except EmailNotValidError:
            flash("Invalid email address.", "danger")
            return render_template("register.html")    
        # Validate password
        if not re.match(r"^(?=.*[A-Z])(?=.*[0-9]).{8,128}$", password):
            flash("Password must be between 8 and 128 characters.", "danger")
            return render_template("register.html")
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

       # If form is correct, hash the password
        hashed_password = generate_password_hash(password) 

        # Insert the new user into the database
        # Could consider moving query logic to database.py for better separation of concerns, but keeping it here for simplicity for now.
        try:
            get_db().execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", (username, email, hashed_password))
            get_db().commit()
        except sqlite3.IntegrityError:
            flash("Username or email already registered.", "danger")
            return render_template("register.html")

        # Flash if successful 
        flash("Registered successfully! Please log in.", "success")

        # Redirect to the login page
        return redirect("/login")   

# If GET request, just render the registration form.    
    else:
        return render_template("register.html")
    

# Login route for existing users to log in.
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")  # Limit login attempts to prevent abuse.
def login():
    # If POST request, process the login form.
    # Note: Copilot auto completion suggest adding account lockout. Not needed for the scope of this project but it was nice to learn about it.
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate form data
        if not username or not password:
            flash("Please fill out all fields.", "danger")
            return render_template("login.html")
        
        # Check username and password length before hashing to prevent unnecesary computation
        if len(password) > 128 or len(username) > 18:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")
        
        # Query the database for the user
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None or not check_password_hash(user["hash"], password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html")
        
        # Remember the user in the session
        session["user_id"] = user["id"]
        return redirect("/dashboard")
    
    # If GET request, just render the login form.
    else:
        return render_template("login.html")