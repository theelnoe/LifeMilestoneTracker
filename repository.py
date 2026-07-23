import os
import json


DATABASE_PATH = "data/database.json"
print("Repository file:", DATABASE_PATH)

class JSONRepository:
    def exists(self):

        return os.path.exists(DATABASE_PATH)

    def load(self):
        print("LOAD:", DATABASE_PATH)
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:

            return json.load(f)

    def save(self, data):
        print("SAVE:", DATABASE_PATH)
        with open(DATABASE_PATH, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )


repository = JSONRepository()