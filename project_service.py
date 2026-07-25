from datetime import datetime
from utils import format_duration, calculate_elapsed_minutes

DEFAULT_MILESTONES = [
    25,
    50,
    100,
    200,
    350,
    500,
    750,
    1000,
    1250,
    1500,
    2000,
    3000,
    5000
]

def generate_milestones(goal):

    milestones = []

    for m in DEFAULT_MILESTONES:

        if m < goal:
            milestones.append(m)

    milestones.append(goal)

    return milestones

# def format_hours(value):

#     total_minutes = round(value * 60)

#     hours = total_minutes // 60

#     minutes = total_minutes % 60

#     if hours == 0:
#         return f"{minutes} m"

#     if minutes == 0:
#         return f"{hours} h"

#     return f"{hours} h {minutes} m"

# def calculate_elapsed_hours(start_time, end_time):

#     elapsed = end_time - start_time

#     return elapsed.total_seconds() / 3600

def add_history(project, end, hours):

    project["history"].append({

        "date": end.strftime("%Y-%m-%d %H:%M"),

        "hours": round(hours, 6),

        "display": format_duration(hours)

    })

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

def register_session(project, end, hours):

    add_history(project, end, hours)

    rebuild_totals(project)