import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db, config, plans, users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    plans = users.get_users_plans(user_id)
    return render_template("show_user.html", user=user, plans=plans)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = plans.search(query)
    else:
        query = ""
        results = []
    return render_template("search.html",query=query, results=results)

@app.route("/update_plan", methods=["POST"])
def update_plan():
    plan_id = request.form["plan_id"]
    plan = plans.get_plan(plan_id)
    if not plan:
        abort(404)
    if plan["user_id"] != session["user_id"]:
        abort(403)

    plan = request.form["plan"]
    if not plan or len(plan) > 50:
            abort(403)

    hours_per_week = request.form["hours_per_week"]
    try:
        hours_per_week = int(hours_per_week)
    except:
        abort(403)
    if not hours_per_week or (hours_per_week > 99):
        abort(403)

    info = request.form["info"]
    if len(info) > 1000:
            abort(403)

    plans.update_plan(plan_id, plan, hours_per_week, info)

    return redirect("/plan/" + str(plan_id))

@app.route("/edit_plan/<int:plan_id>")
def edit_plan(plan_id):
    require_login()

    plan = plans.get_plan(plan_id)
    if not plan :
        abort(404)
    if plan["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_plan.html", plan=plan)

@app.route("/delete_plan/<int:plan_id>", methods=["GET", "POST"])
def delete_plan(plan_id):
    plan = plans.get_plan(plan_id)

    if not plan:
            abort(404)
    if plan["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_plan.html", plan=plan)

    if request.method == "POST":
        if "delete" in request.form:
            plans.delete_plan(plan_id)
            return redirect("/")
        else:
            return redirect("/plan/" + str(plan_id))

@app.route("/plan/<int:plan_id>")
def show_plan(plan_id):
    plan = plans.get_plan(plan_id)
    if not plan:
        abort(404)
    plan_class = plans.get_plan_class(plan_id)
    return render_template("show_plan.html", plan=plan, plan_class=plan_class)

@app.route("/create_plans", methods=["POST"])
def create_plans():
    require_login()

    plan = request.form["plan"]
    if not plan or len(plan) > 50:
        abort(403)
    hours_per_week = request.form["hours_per_week"]
    try:
        hours_per_week = int(hours_per_week)
    except:
        abort(403)
    if not hours_per_week or (hours_per_week > 99):
        abort(403)
    info = request.form["info"]
    if len(info) > 1000:
        abort(403)
    user_id = session["user_id"]

    plan_class = request.form["plan_class"]

    plans.add_plans(plan, hours_per_week, info, user_id, plan_class)

    return redirect("/")
    
@app.route("/add_plans")
def add_plans():
    require_login()
    return render_template("add_plans.html")

@app.route("/")
def index():
    all_plans = plans.get_plans()
    if "user_id" in session:
        users_plans = plans.get_users_plans("user_id")
    else:
        users_plans = None
    return render_template("index.html", plans = all_plans, users_plans = users_plans)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Error: the passwords do not match"

    try:
        users.create_user(username, password1)
    except slite3.IntegirtyError:
        return "Error: the usename is taken"

    return "Username created :3"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/") 
        else:
            return "Error: incorrect username or password"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")