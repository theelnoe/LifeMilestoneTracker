import os
import requests


REMOTE_LOAD_URL = "https://elnoe.com/tracker_api/load.php"
REMOTE_SAVE_URL = "https://elnoe.com/tracker_api/save.php"

API_KEY = os.environ.get("TRACKER_API_KEY")
USE_REMOTE_DATABASE = os.environ.get("TRACKER_API_KEY") is not None

class JSONRepository:

    def __init__(self, database_path=None):
        self.database_path = database_path


    def exists(self):
        return True


    def load(self):
        if USE_REMOTE_DATABASE:
            response = requests.get(
                REMOTE_LOAD_URL,
                headers={
                    "X-Api-Key": API_KEY
                }
            )
            response.raise_for_status()
            return response.json()
        else:
            import json
            with open(
                "data/database.json",
                "r",
                encoding="utf-8"
            ) as f:
                return json.load(f)


    def save(self, data):
        if USE_REMOTE_DATABASE:
            response = requests.post(
                REMOTE_SAVE_URL,
                headers={
                    "X-Api-Key": API_KEY,
                    "Content-Type": "application/json"
                },
                json=data
            )
            response.raise_for_status()
        else:
            import json
            with open(
                "data/database.json",
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=4
                )


repository = JSONRepository()