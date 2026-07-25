from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
from repository import repository
from project_service import (
    generate_milestones,
    rebuild_totals,
    register_session
)
from utils import format_duration, calculate_elapsed_minutes

app = Flask(__name__)

DATABASE = "data/database.json"

# DEFAULT_MILESTONES = [
#     25,
#     50,
#     100,
#     200,
#     350,
#     500,
#     750,
#     1000,
#     1250,
#     1500,
#     2000,
#     3000,
#     5000
# ]

# -----------------------------
# Database
# -----------------------------

def load_data():

    if not repository.exists():

        os.makedirs("data", exist_ok=True)

        default_data = {

            "projects":[

                {

                    "name":"English",

                    "goal":1500,

                    "total_hours":0,

                    "today":0,

                    "week":0,

                    "timer_running":False,

                    "timer_start":None,

                    "milestones":[50,100,200,350,500,750,1000,1250,1500],

                    "history":[]

                }

            ]

        }

        repository.save(default_data)

    data = repository.load()

    project = data["projects"][0]

    project.setdefault("timer_running", False)

    project.setdefault("timer_start", None)

    save_data(data)

    return data

def save_data(data):

    repository.save(data)

# def generate_milestones(goal):

#     milestones = []

#     for m in DEFAULT_MILESTONES:

#         if m < goal:
#             milestones.append(m)

#     milestones.append(goal)

#     return milestones

# def rebuild_totals(project):

#     total = 0
#     today = 0
#     week = 0

#     today_str = datetime.now().strftime("%Y-%m-%d")
#     current_week = datetime.now().isocalendar().week
#     current_year = datetime.now().year

#     for item in project["history"]:

#         hours = float(item["hours"])

#         total += hours

#         dt = datetime.strptime(item["date"], "%Y-%m-%d %H:%M")

#         if dt.strftime("%Y-%m-%d") == today_str:

#             today += hours

#         if dt.isocalendar().week == current_week and dt.year == current_year:

#             week += hours

#     project["total_hours"] = round(total, 2)
#     project["today"] = round(today, 2)
#     project["week"] = round(week, 2)

# -----------------------------
# Helpers
# -----------------------------

def prepare_project():

    data, project, current_project = get_project()

    rebuild_totals(project)

    #save_data(data)

    return data, project, current_project

# def add_history(project, end, hours):

#     project["history"].append({

#         "date": end.strftime("%Y-%m-%d %H:%M"),

#         "hours": round(hours, 6),

#         "display": format_hours(hours)

#     })

# def register_session(project, end, hours):

#     add_history(project, end, hours)

#     rebuild_totals(project)

# def calculate_elapsed_hours(start_time, end_time):

#     elapsed = end_time - start_time

#     return elapsed.total_seconds() / 3600

def get_project():

    data = load_data()

    index = request.args.get("project", 0, type=int)

    if index < 0 or index >= len(data["projects"]):
        index = 0

    project = data["projects"][index]

    return data, project, index

# def format_hours(value):

#     total_minutes = round(value * 60)

#     hours = total_minutes // 60

#     minutes = total_minutes % 60

#     if hours == 0:
#         return f"{minutes} m"

#     if minutes == 0:
#         return f"{hours} h"

#     return f"{hours} h {minutes} m"

# -----------------------------
# Home
# -----------------------------

@app.route("/")
def index():

    data, project, current_project = prepare_project()

    progress = round(
        project["total_hours"] / project["goal"] * 100,
        1
    )

    history_for_ui = list(reversed(project["history"]))

    return render_template(

        "index.html",

        data=data,

        current_project=current_project,

        project=project,

        progress=progress,

        total_text=format_duration(project["total_hours"]),

        today_text=format_duration(project["today"]),

        week_text=format_duration(project["week"]),

        history_for_ui=history_for_ui

    )

@app.route("/create_project", methods=["POST"])
def create_project():

    name = request.form["name"].strip()
    goal = int(request.form["goal"])

    data = load_data()

    new_project = {
        "name": name,
        "goal": goal,
        "total_hours": 0,
        "today": 0,
        "week": 0,
        "timer_running": False,
        "timer_start": None,
        "last_day": "",
        "last_week": 0,
        "milestones": generate_milestones(goal),
        "history": []
    }

    data["projects"].append(new_project)

    save_data(data)

    return redirect(url_for("index"))

@app.route("/edit_project", methods=["POST"])
def edit_project():

    data = load_data()

    project_index = int(request.form["project"])

    new_name = request.form["name"].strip()

    new_goal = int(request.form["goal"])

    if new_name == "":
        return redirect(url_for("index"))

    if new_goal <= 0:
        return redirect(url_for("index"))

    data["projects"][project_index]["name"] = new_name

    data["projects"][project_index]["goal"] = new_goal

    data["projects"][project_index]["milestones"] = generate_milestones(new_goal)

    save_data(data)

    return redirect(
        url_for(
            "index",
            project=project_index
        )
    )

@app.route("/delete_project", methods=["POST"])
def delete_project():

    data = load_data()

    project_index = int(request.form["project"])

    if len(data["projects"]) <= 1:
        return redirect(url_for("index"))

    data["projects"].pop(project_index)

    save_data(data)

    return redirect(url_for("index"))

# -----------------------------
# Start Timer
# -----------------------------

@app.route("/start_timer", methods=["POST"])
def start_timer():
    print(request.args)
    data, project, _ = get_project()

    if not project["timer_running"]:

        project["timer_running"] = True

        project["timer_start"] = datetime.now().isoformat()

        save_data(data)

    return jsonify({
        "success": True
    })

# -----------------------------
# Timer Status
# -----------------------------

@app.route("/timer_status")
def timer_status():

    _, project, _ = get_project()

    return jsonify({

        "running": project["timer_running"],

        "start": project["timer_start"]

    })

# -----------------------------
# Stop Timer
# -----------------------------

@app.route("/stop_timer", methods=["POST"])
def stop_timer():

    data, project, _ = get_project()

    if not project["timer_running"]:

        return jsonify({
            "success": False
        })

    start = datetime.fromisoformat(project["timer_start"])
    end = datetime.now()
    minutes = calculate_elapsed_minutes(start, end)
    hours = minutes / 60
    # اگر کمتر از 1 دقیقه بود، ثبت نکن
    if hours < (1 / 60):

        project["timer_running"] = False
        project["timer_start"] = None

        save_data(data)

        return jsonify({

            "success": True,

            "hours": 0

        })

    register_session(project, end, hours)

    project["timer_running"] = False
    project["timer_start"] = None

    save_data(data)

    return jsonify({

        "success": True,

        "hours": format_duration(hours)

    })

# -----------------------------
# Add Time
# -----------------------------

@app.route("/add_time", methods=["POST"])
def add_time():

    data, project, _ = get_project()

    body = request.get_json()

    hours = int(body.get("hours", 0))
    minutes = int(body.get("minutes", 0))

    value = hours + minutes / 60

    if value <= 0:

        return jsonify({

            "success": False,

            "message": "Invalid time"

        })

    end_time = datetime.now()

    register_session(
        project,
        end_time,
        value
    )

    save_data(data)
    progress = 0

    if project["goal"] > 0:
        progress = round(
            project["total_hours"] / project["goal"] * 100,
            1
        )
        
    return jsonify({

        "success": True,

        "goal": project["goal"],

        "milestones": project["milestones"],

        "progress": progress,

        "total_hours": round(project["total_hours"], 6),

        "total_text": format_duration(project["total_hours"]),

        "today_text": format_duration(project["today"]),

        "week_text": format_duration(project["week"]),

        "new_history": project["history"][-1]

    })

# -----------------------------
# Edit Session
# -----------------------------

@app.route("/edit_session", methods=["POST"])
def edit_session():

    data, project, _ = get_project()

    body = request.get_json()

    index = body["index"]

    hours = int(body["hours"])

    minutes = int(body["minutes"])

    value = hours + minutes / 60

    real_index = len(project["history"]) - 1 - index

    project["history"][real_index]["hours"] = round(value, 2)

    project["history"][real_index]["display"] = format_duration(value)

    rebuild_totals(project)

    save_data(data)

    progress = 0

    if project["goal"] > 0:
        progress = round(
            project["total_hours"] / project["goal"] * 100,
            1
        )

    return jsonify({

        "success": True,

        "goal": project["goal"],

        "milestones": project["milestones"],

        "total_hours": project["total_hours"],

        "total_text": format_duration(project["total_hours"]),

        "today_text": format_duration(project["today"]),

        "week_text": format_duration(project["week"]),

        "display": format_duration(value),

        "progress": progress

    })

# -----------------------------
# Delete Session
# -----------------------------

@app.route("/delete_session", methods=["POST"])
def delete_session():

    data, project, _ = get_project()

    body = request.get_json()

    index = int(body["index"])

    # تاریخچه در UI برعکس نمایش داده می‌شود
    real_index = len(project["history"]) - 1 - index

    project["history"].pop(real_index)

    rebuild_totals(project)

    save_data(data)

    return jsonify({
        "success": True
    })
    

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

'''if __name__ == "__main__":

    app.run(
        debug=True
    )'''