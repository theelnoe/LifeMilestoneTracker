from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
from project_service import (
    get_projects,
    get_project_view,
    get_project_history,
    create_project,
    update_project,
    delete_project,
    create_session,
    update_session,
    delete_session,
    finish_timer,
    format_minutes
)

timer_state = {
    "running": False,
    "start": None
}

app = Flask(__name__)



@app.route("/")
def index():
    index = request.args.get("project", 0, type=int)

    projects = get_projects()
    project = get_project_view(index)
    
    sessions = get_project_history(project["id"])
    
    return render_template(
        "index.html",
        projects=projects,
        project=project,
        sessions=sessions,
        current_project=project["current_project"]
    )

@app.route("/create_project", methods=["POST"])
def create_project_route():

    name = request.form["name"].strip()
    goal = int(request.form["goal"])
    domain_id = int(request.form["domain_id"])

    create_project(name, goal, domain_id)

    return redirect("/")

@app.route("/edit_project", methods=["POST"])
def edit_project_route():

    project_id = int(request.form["project_id"])
    name = request.form["name"].strip()
    goal = int(request.form["goal"])
    domain_id = int(request.form["domain_id"])

    update_project(
        project_id,
        name,
        goal,
        domain_id
    )

    return redirect(
        url_for(
            "index",
            project=request.form["project_index"]
        )
    )

@app.route("/delete_project", methods=["POST"])
def delete_project_route():

    project_id = int(request.form["project_id"])

    delete_project(project_id)

    return redirect("/")

@app.route("/add_time", methods=["POST"])
def add_time_route():

    data = request.get_json()

    project_index = int(data["project_id"])

    projects = get_projects()
    project_id = projects[project_index]["Project_ID"]

    hours = data["hours"]
    minutes = data["minutes"]

    value = hours * 60 + minutes

    new_session = create_session(
        project_id,
        value
    )

    project = get_project_view(project_index)

    new_history = {
        "id": new_session["Session_ID"],
        "date": new_session["StartTime"],
        "value": new_session["Value"],
        "display": format_minutes(new_session["Value"])
    }

    return {
        "success": True,

        "total_hours": project["total"],
        "total_text": project["total_display"],
        "today_text": project["today_display"],
        "week_text": project["week_display"],

        "goal": project["goal"],
        "progress": project["progress"],
        "milestones": project["milestones"],

        "new_history": new_history
    }

@app.route("/edit_session", methods=["POST"])
def edit_session_route():

    data = request.get_json()

    project_index = int(data["project_id"])

    session_id = int(data["session_id"])

    hours = int(data["hours"])

    minutes = int(data["minutes"])

    value = hours * 60 + minutes

    update_session(
        session_id,
        value
    )

    return {
        "success": True,
        "display": format_minutes(value)
    }

@app.route("/delete_session", methods=["POST"])
def delete_session_route():

    data = request.get_json()

    project_id = int(data["project_id"])
    session_id = int(data["session_id"])

    delete_session(session_id)

    return {
        "success": True
    }

@app.route("/start_timer", methods=["POST"])
def start_timer():

    project_index = int(request.args.get("project", 0))

    if not timer_state["running"]:
        timer_state["running"] = True
        timer_state["start"] = datetime.now()

    return {
        "success": True
    }

@app.route("/timer_status")
def timer_status():

    return {
        "running": timer_state["running"],
        "start": str(timer_state["start"])
    }

@app.route("/stop_timer", methods=["POST"])
def stop_timer():

    if not timer_state["running"]:
        return {
            "success": False,
            "message": "Timer is not running"
        }

    start = timer_state["start"]
    end = datetime.now()

    project_index = int(request.args.get("project", 0))
    projects = get_projects()
    project_id = projects[project_index]["Project_ID"]

    minutes = finish_timer(
        start,
        project_id
    )

    if minutes == 0:
        timer_state["running"] = False
        timer_state["start"] = None

        return {
            "success": True,
            "minutes": 0
        }

    timer_state["running"] = False
    timer_state["start"] = None

    return {
        "success": True,
        "minutes": minutes
    }

if __name__ == "__main__":
    app.run(debug=True)