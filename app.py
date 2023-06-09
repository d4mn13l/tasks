from flask import Flask, render_template, request, redirect, url_for
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


app = Flask(__name__)
app.secret_key = "q377v5zn8304zn47tiug2du7za4go67843qz58z4rgdhafu3pu68"
app.config["SESSION_TYPE"] = "filesystem"
app.debug = True

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "/login"

edittask_id = 0

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def get_user(user_id):
    return User(user_id)


@app.route("/")
def main():
    print(get_tasks())
    return redirect("/todolist")

@app.route("/todolist")
def todolist():
    tasks = get_tasks()
    return render_template("tasks.html", tasks = tasks)

@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("authentication.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

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

@app.route("/handleadmininput", methods=["POST"])
def handleadmininput():
    tasks = get_tasks()
    if request.form.get("edit"):
        for task in tasks:
            if task["title"] in request.form.get("edit"):
                edittask_id = task["id"]
                return redirect(url_for("edittask", task=task))
    return redirect(url_for("deletetask", keys=request.form.keys()))

@app.route("/deletetask", methods=["POST", "GET"])
def deletetask():
    tasks = get_tasks()
    to_delete = []
    keys = request.args.get("keys")
    for key in keys:
        try:
            to_delete.append(int(key))
        except ValueError:
            continue
    for task in tasks: #doesn't iterate over all tasks
        print(task["id"])
        if task["id"] in to_delete:
            print("removed", task)
            tasks.remove(task)
    set_tasks(tasks)
    update_task_ids()
    return redirect("/")

@app.route("/edittask", methods=["GET", "POST"])
def edittask():
    if request.method == "GET":
        return render_template("edittask.html", task=request.args.get("task"))
    tasks = get_tasks()
    tasks[edittask_id - 1] = {"id": edittask_id, "title": request.form.get("title"), "done": False, "description": request.form.get("description")}
    #there must be a better way to get the id here
    set_tasks(tasks)
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