from flask import Flask, request, redirect, url_for, render_template, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)

# Step 1: Basic Flask Setup with Flask-Login
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Change this to something secure

# Step 2: Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Route to redirect to if not logged in

# Step 3: User Model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Step 4: Mock User Database
# This is a simple user database for demonstration purposes
users = {"user1": "password1", "user2": "password2"}

# Step 5: User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)  # Return the User object based on the user ID

# Step 6: Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate credentials
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)  # Log in the user
            return redirect(url_for("protected"))  # Redirect to protected route
        else:
            error = "Invalid username or password"  # Error message for invalid login

    return render_template("login.html", error=locals().get("error", None))

# Step 7: Logout Route
@app.route("/logout")
@login_required  # Ensure only logged-in users can access this route
def logout():
    logout_user()  # Log the user out
    return redirect(url_for("login"))  # Redirect to login page after logout

# Step 8: Protected Route
@app.route("/protected")
@login_required  # Only accessible if logged in
def protected():
    return f"Hello, {current_user.id}! You are logged in."

# Step 9: Home Page
@app.route("/")
def home():
    if current_user.is_authenticated:  # Check if the user is logged in
        return redirect(url_for("protected"))  # Redirect to protected route
    else:
        return redirect(url_for("login"))  # Redirect to login page if not logged in

# Step 10: Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)  # Start Flask app with debug mode enabled