import json
from pathlib import Path

DATA_FILE = Path("data/habits.json")

class HabitTracker:
    def __init__(self):
        self.habits = self.load_data()

    def load_data(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_data(self):
        DATA_FILE.parent.mkdir(exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(self.habits, f, indent=4)

    def add_habit(self, name):
        if name in self.habits:
            print("Habit already exists.")
            return
        self.habits[name] = {"completed_days": []}
        self.save_data()
        print(f"Added habit: {name}")

    def check_habit(self, name):
        from datetime import date
        
        if name not in self.habits:
            print("Habit not found.")
            return
        today = str(date.today())
        if today not in self.habits[name]["completed_days"]:
            self.habits[name]["completed_days"].append(today)
            self.save_data()
            print(f"Checked off {name} for today!")
        else:
            print("You've already completed this today.")

    def show_habits(self):
        if not self.habits:
            print("No habits yet. Add one!")
            return
        for habit, data in self.habits.items():
            print(f"- {habit} (days completed: {len(data['completed_days'])})")
