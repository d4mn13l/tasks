import json
with open("tasks.json", "w") as tasks_data:
    tasks_data.write(json.dumps([{"id": 1, "title": "Licht ausschalten", "done": False, "description": "Schalter betätigen."}]))