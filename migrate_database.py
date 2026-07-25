import json
import os

SOURCE = "data/database.json"
TARGET = "data/database_v2.json"


def load_database():
    with open(SOURCE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_database(data):
    with open(TARGET, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    old = load_database()

    new = {
        "users": [
            {
                "User_ID": 1,
                "Name": "Elnoe"
            }
        ],
        "domains": [],
        "activities": [],
        "domain_activities": [],
        "units": [
            {
                "Unit_ID": 1,
                "Name": "Hours",
                "Measurement_Type": "Time"
            }
        ],
        "projects": [],
        "sessions": []
    }

    next_project_id = 1
    next_session_id = 1

    for project in old["projects"]:

        new["projects"].append({
            "Project_ID": next_project_id,
            "User_ID": 1,
            "Domain_ID": 0,
            "Unit_ID": 1,
            "Name": project["name"],
            "Goal": project["goal"],
            "Is_Active": True
        })

        for item in project["history"]:

            minutes = round(float(item["hours"]) * 60)

            new["sessions"].append({
                "Session_ID": next_session_id,
                "Project_ID": next_project_id,
                "DomainActivity_ID": 0,
                "StartTime": item["date"],
                "Value": minutes,
                "Material": "",
                "Notes": ""
            })

            next_session_id += 1

        next_project_id += 1

    save_database(new)

    print("Migration completed.")
    print(f"Projects : {len(new['projects'])}")
    print(f"Sessions : {len(new['sessions'])}")


if __name__ == "__main__":
    main()