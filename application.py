from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    books = Book.query.limit(6).all()
    return render_template("index.html", books=books)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/validate_login", methods=["POST"])
def validate_login():
    username = request.form.get("username")
    password = request.form.get("password")

    checkUser = User.query.filter_by(username=username, password=password).first()
    if checkUser != None:
        return redirect(url_for('index'))
    else:
        return render_template("error.html", message="Account is invalid")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    username = request.form.get("username")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")

    if password != confirmPassword:
        return render_template("error.html", message="Password and Confirm Password mismatched")

    checkUser = User.query.filter_by(username=username).first()
    if checkUser != None:
        return render_template("error.html", message="User is already registered")

    user = User(username=username, password=password)
    
    User.add_user(user)
    return render_template("success.html", message="Successfully Registered!")
    