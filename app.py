from flask import Flask, render_template, request, redirect, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
)
import json
import time
import datetime


tasks = [
    {"id": 1, "title": "Kaffeemaschine reinigen", "done": False, "description": "Beschreibung"},
    {"id": 2, "title": "Licht ausschalten", "done": False, "description": "Lichtschlater umlegen"}
]

app = Flask(__name__)
app.secret_key = "q377v5zn8304zn47tiug2du7za4go67843qz58z4rgdhafu3pu68"
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def get_user(user_id):
    return User(user_id)


@app.route("/")
def main():
#    return render_template("index.html")
    return render_template("tasks.html", tasks = tasks)

@app.route("/login", methods=["POST"])
def login():
    return render_template("authentication.html")

@app.route("/logout")
def logout():
    pass

@app.route("/dologin", methods=["POST"])
def dologin():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "sicherespasswort":
        login_user(User(username))
        return redirect("/admin")
    else:
        return redirect("/loginfailed")

@app.route("/loginfailed")
def loginfailed():
    return render_template("loginfailed.html")

@app.route("/admin")
@login_required
def admin():
    return "admin"

@app.route("/log", methods=["POST"])
def log():
    done = True
    aufgaben = [int(i) for i in request.form.get("Aufgabe", [])]
    for task in tasks:
        if task["id"] in aufgaben:
            task["done"] = True
        else:
            task["done"] = False
            done = False
    print(json.dumps(tasks))
    with open(f"time", "w") as file:
        file.write(json.dumps(create_log(done)))
    return "ok"

def create_log(done):
    date = datetime.datetime.now()
    if done == True:
        return date.strftime("%c"), ", alle Aufgaben erledigt."

if __name__ == "__main__":
    app.run(debug=True)