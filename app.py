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

#with open("tasks.json", "r") as tasks_data:
#    tasks = json.loads(tasks_data)

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
    return redirect("/todolist")

@app.route("/todolist")
def todolist():
    tasks = get_tasks()
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
    tasks = get_tasks()
    return render_template("admin.html", tasks=tasks)

@app.route("/log", methods=["POST"])
def log():
    done = True
    # iterate over request.form.keys() dismissing "Abschicken"
    done_tasks = []
    for key in request.form.keys():
        try:
            done_tasks.append(int(key))
        except TypeError:
            continue
    tasks = get_tasks()
    for task in tasks:
        if task["id"] in done_tasks:
            task["done"] = True
        else:
            task["done"] = False
            done = False
    print(json.dumps(tasks))
    with open(f"time", "w") as file:
        file.write(json.dumps(create_log(done)))
    return create_log(done)

@app.route("/addtask", methods=["POST", "GET"])
@login_required
def addtask():
    tasks = get_tasks()
    tasks.append({"id": len(tasks) + 1, "title": request.form["title"], "done": False, "Beschreibung": request.form["description"]})
    set_tasks(tasks)
    return redirect("/")

@app.route("/deletetask", methods=["POST"])
def deletetask():
    tasks = get_tasks()
    to_delete = []
    for key in request.form.keys():
        try:
            to_delete.append(int(key))
        except ValueError:
            continue
    for task in tasks:
        if task["id"] in to_delete:
            tasks.remove(task)
    set_tasks(tasks)
    update_task_ids()
    return redirect("/")


def create_log(done):
    date = datetime.datetime.now()
    return date.strftime("%c"), ", alle Aufgaben erledigt." if done == True else "nicht alles erledigt"

def get_tasks():
    with open("tasks.json", "r") as tasks_data:
        return json.load(tasks_data)

def set_tasks(tasks):
    with open("tasks.json", "w") as tasks_data:
        tasks_data.write(json.dumps(tasks))

def update_task_ids():
    tasks = get_tasks()
    for i in range(0, len(tasks)):
        tasks[i]["id"] = i + 1
#        breakpoint()
    set_tasks(tasks)

if __name__ == "__main__":
    app.run(debug=True)