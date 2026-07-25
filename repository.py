import os
import json


DATABASE_V1 = "data/database.json"
DATABASE_V2 = "data/database_v2.json"
print("Repository file:", DATABASE_V1)

class JSONRepository:
    
    def exists(self):

        return os.path.exists(DATABASE_V1)

    def load(self):
        
        with open(DATABASE_V1, "r", encoding="utf-8") as f:

            return json.load(f)

    def save(self, data):
        
        with open(DATABASE_V1, "w", encoding="utf-8") as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    def load_v2(self):
        with open(DATABASE_V2, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_v2(self, data):
        with open(DATABASE_V2, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

repository = JSONRepository()