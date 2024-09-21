from flask import Blueprint
from flask import request, redirect
from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


from main.models import User
from main.database import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = get_user_by_email(email)
        if not user:
            return {"status": "failed", "message": "Invalid email or password"}
        
        if not check_password_hash(user.password, password):
            return {"status": "failed", "message": "Invalid email or password"}
        
        login_user(user)
        
        return {"status": "success", "url": "/"}
    return render_template("login.html")


@auth.route('/sign-out', methods=["GET"])
def sign_out():
    logout_user()
    return redirect("/")

def create_username(email: str) -> str:
    return email.split("@")[0]

def get_user_by_email(email: str) -> User:
    return User.query.filter_by(email=email).first()

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form

        email = data.get("email")
        username = create_username(email)
        password = data.get("password")
        confirm_password = data.get("confirmpassword")

        if get_user_by_email(email):
            return {"status": "failed", "message": "Email already exists"}

        user = User(
            email=email, 
            username=username, 
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return {
            "status": "success", 
            "user": {"email": email, "username": username}
            }
    return render_template("register.html")
