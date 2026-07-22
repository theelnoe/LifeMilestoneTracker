from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATABASE = "data/database.json"


# -----------------------------
# Database
# -----------------------------

def load_data():

    if not os.path.exists(DATABASE):

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

        with open(DATABASE,"w") as f:

            json.dump(default_data,f,indent=4)

    with open(DATABASE,"r") as f:

        data = json.load(f)
        project = data["projects"][0]
        project.setdefault("timer_running", False)
        project.setdefault("timer_start", None)
        save_data(data)
        return data

def save_data(data):

    with open(DATABASE,"w") as f:

        json.dump(data,f,indent=4,ensure_ascii=False)

def rebuild_totals(project):

    total = 0
    today = 0
    week = 0

    today_str = datetime.now().strftime("%Y-%m-%d")
    current_week = datetime.now().isocalendar().week
    current_year = datetime.now().year

    for item in project["history"]:

        hours = float(item["hours"])

        total += hours

        dt = datetime.strptime(item["date"], "%Y-%m-%d %H:%M")

        if dt.strftime("%Y-%m-%d") == today_str:

            today += hours

        if dt.isocalendar().week == current_week and dt.year == current_year:

            week += hours

    project["total_hours"] = round(total, 2)
    project["today"] = round(today, 2)
    project["week"] = round(week, 2)

# -----------------------------
# Helpers
# -----------------------------

def prepare_project():

    data, project, current_project = get_project()

    reset_counters(project)

    rebuild_totals(project)

    save_data(data)

    return data, project, current_project

def add_history(project, end, hours):

    project["history"].append({

        "date": end.strftime("%Y-%m-%d %H:%M"),

        "hours": round(hours, 2),

        "display": format_hours(hours)

    })

def update_project_hours(project, hours):

    project["total_hours"] += hours

    project["today"] += hours

    project["week"] += hours

def register_session(project, end, hours):

    reset_counters(project)

    update_project_hours(project, hours)

    add_history(project, end, hours)

def calculate_elapsed_hours(start_time, end_time):

    elapsed = end_time - start_time

    return elapsed.total_seconds() / 3600

def get_project():

    data = load_data()

    index = request.args.get("project", 0, type=int)

    if index < 0 or index >= len(data["projects"]):
        index = 0

    project = data["projects"][index]

    return data, project, index

def reset_counters(project):

    today = datetime.now().strftime("%Y-%m-%d")

    week = datetime.now().isocalendar().week

    if project.get("last_day") != today:

        project["today"] = 0
        project["last_day"] = today

    if project.get("last_week") != week:

        project["week"] = 0
        project["last_week"] = week

def format_hours(value):

    total_minutes = round(value * 60)

    hours = total_minutes // 60

    minutes = total_minutes % 60

    if hours == 0:
        return f"{minutes} m"

    if minutes == 0:
        return f"{hours} h"

    return f"{hours} h {minutes} m"

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

    return render_template(

        "index.html",

        data=data,

        current_project=current_project,

        project=project,

        progress=progress,

        total_text=format_hours(project["total_hours"]),

        today_text=format_hours(project["today"]),

        week_text=format_hours(project["week"])

    )

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
    hours = calculate_elapsed_hours(start, end)

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

        "hours": format_hours(hours)

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

    value = hours + (minutes / 60)

    if value <= 0:

        return jsonify({

            "success": False,

            "message": "Invalid time"

        })

    register_session(
        project,
        datetime.now(),
        value
    )

    save_data(data)

    return jsonify({

        "success": True,

        "total": round(project["total_hours"],2)

    })


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )