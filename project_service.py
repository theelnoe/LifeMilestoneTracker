from datetime import datetime
from repository import JSONRepository, DATABASE_V2_PATH

repository = JSONRepository(DATABASE_V2_PATH)

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

def get_projects():
    data = repository.load()
    return data["projects"]

def get_project(project_index=0):
    projects = get_projects()

    if project_index < 0 or project_index >= len(projects):
        project_index = 0

    return projects[project_index], project_index

def get_project_view(project_index=0):
    data = repository.load()

    projects = data["projects"]

    if project_index < 0 or project_index >= len(projects):
        project_index = 0

    project = projects[project_index]

    project_id = project["Project_ID"]

    total_minutes = calculate_total(data, project_id)
    today_minutes = calculate_today(data, project_id)
    week_minutes = calculate_week(data, project_id)

    total_hours = total_minutes / 60
    
    return {
        "id": project_id,
        "domain_id": project["Domain_ID"],
        "name": project["Name"],
        "goal": project["Goal"],

        "domain": get_domain_name(
            data,
            project["Domain_ID"]
        ),

        "unit": get_unit_name(
            data,
            project["Unit_ID"]
        ),

        # عدد برای محاسبات JS
        "total": total_hours,
        "today": today_minutes,
        "week": week_minutes,

        # متن برای نمایش
        "total_display": format_minutes(total_minutes),
        "today_display": format_minutes(today_minutes),
        "week_display": format_minutes(week_minutes),

        "progress": calculate_progress(
            total_hours,
            project["Goal"]
        ),

        "next_milestone": get_next_milestone(
            total_hours,
            project["Goal"]
        ),

        "milestones": generate_milestones(
            project["Goal"]
        ),

        "current_project": project_index,
    }

def get_domain_name(data, domain_id):
    for domain in data["domains"]:
        if domain["Domain_ID"] == domain_id:
            return domain["Name"]

    return ""

def get_unit_name(data, unit_id):
    for unit in data["units"]:
        if unit["Unit_ID"] == unit_id:
            return unit["Name"]

    return ""

def calculate_total(data, project_id):
    total = 0

    for session in data["sessions"]:
        if session["Project_ID"] == project_id:
            total += session["Value"]

    return total

def get_project_sessions(data, project_id):
    sessions = []

    for session in data["sessions"]:
        if session["Project_ID"] == project_id:
            sessions.append(session)

    return sessions

def calculate_today(data, project_id):
    total = 0
    today = datetime.now().strftime("%Y-%m-%d")

    for session in data["sessions"]:
        if session["Project_ID"] == project_id:
            session_date = session["StartTime"].split(" ")[0]

            if session_date == today:
                total += session["Value"]

    return total

def format_minutes(value):

    hours = value // 60
    minutes = value % 60

    if hours > 0 and minutes > 0:
        return f"{hours} h {minutes} m"

    elif hours > 0:
        return f"{hours} h"

    else:
        return f"{minutes} m"

def get_project_history(project_id):
    data = repository.load()

    history = []

    for session in data["sessions"]:

        if session["Project_ID"] == project_id:
            print("SESSION RAW:", session)
            history.append({
                "id": session["Session_ID"],
                "date": session["StartTime"],
                "value": session["Value"],
                "display": format_minutes(session["Value"])
            })

    history.reverse()

    return history

def calculate_week(data, project_id):
    total = 0

    now = datetime.now()
    current_week = now.isocalendar().week
    current_year = now.year

    for session in data["sessions"]:
        if session["Project_ID"] == project_id:

            dt = datetime.strptime(
                session["StartTime"],
                "%Y-%m-%d %H:%M"
            )

            if (
                dt.isocalendar().week == current_week
                and dt.year == current_year
            ):
                total += session["Value"]

    return total

def calculate_progress(total, goal):
    if goal <= 0:
        return 0

    return round((total / goal) * 100, 1)

def generate_milestones(goal):
    milestones = []

    for milestone in DEFAULT_MILESTONES:
        if milestone < goal:
            milestones.append(milestone)

    milestones.append(goal)

    return milestones

def get_next_milestone(total, goal):
    milestones = generate_milestones(goal)

    for milestone in milestones:
        if total < milestone:
            return milestone

    return goal

def create_project(name, goal, domain_id, unit_id=1):
    data = repository.load()

    projects = data["projects"]

    new_id = 1

    if projects:
        new_id = max(
            p["Project_ID"] for p in projects
        ) + 1

    new_project = {
        "Project_ID": new_id,
        "User_ID": 1,
        "Domain_ID": domain_id,
        "Unit_ID": unit_id,
        "Name": name,
        "Goal": goal,
        "Is_Active": True
    }

    projects.append(new_project)

    repository.save(data)

    return new_project

def update_project(project_id, name, goal, domain_id, unit_id=1):
    data = repository.load()

    for project in data["projects"]:
        if project["Project_ID"] == project_id:

            project["Name"] = name
            project["Goal"] = goal
            project["Domain_ID"] = domain_id
            project["Unit_ID"] = unit_id

            repository.save(data)

            return project

    return None

def delete_project(project_id):
    data = repository.load()

    projects = data["projects"]

    for project in projects:
        if project["Project_ID"] == project_id:
            projects.remove(project)

            repository.save(data)

            return True

    return False

def get_sessions(data, project_id):
    sessions = []

    for session in data["sessions"]:
        if session["Project_ID"] == project_id:
            sessions.append(session)

    return sessions

def create_session(project_id, value):
    data = repository.load()

    sessions = data["sessions"]

    new_id = 1

    if sessions:
        new_id = max(
            s["Session_ID"] for s in sessions
        ) + 1

    new_session = {
        "Session_ID": new_id,
        "Project_ID": project_id,
        "DomainActivity_ID": 0,
        "StartTime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Value": value,
        "Material": "",
        "Notes": ""
    }

    sessions.append(new_session)

    repository.save(data)

    return new_session

def update_session(session_id, value):
    data = repository.load()

    for session in data["sessions"]:
        if session["Session_ID"] == session_id:

            session["Value"] = value

            repository.save(data)

            return session

    return None

def delete_session(session_id):
    data = repository.load()

    sessions = data["sessions"]

    for session in sessions:
        if session["Session_ID"] == session_id:

            sessions.remove(session)

            repository.save(data)

            return True

    return False

def finish_timer(start_time, project_id):

    end_time = datetime.now()
    elapsed_seconds = (end_time - start_time).total_seconds()
    minutes = elapsed_seconds / 60

    if minutes < 1:
        return 0

    minutes = round(minutes)

    create_session(
        project_id=project_id,
        value=minutes
    )

    return minutes


#