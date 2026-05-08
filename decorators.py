from functools import wraps
from flask import session, redirect

# Decorator to require login.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/welcome")
        return f(*args, **kwargs)
    return decorated_function
