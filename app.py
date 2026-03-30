import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db, config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/create_plans", methods=["POST"])
def create_plans():
    plan = request.form["plan"]
    hours_per_week = request.form["hours_per_week"]
    info = request.form["info"]
    user_id = session["user_id"]

    sql = "INSERT INTO plans (plan, hours_per_week, info, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [plan, hours_per_week, info, user_id])

    return redirect("/")
    

@app.route("/add_plans")
def add_plans():
    return render_template("add_plans.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
