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
        self.habits[name] = {
            "completed_days": [],
            "streak": 0,
            "last_completed": None
        }
        self.save_data()
        print(f"Added habit: {name}")

    def check_habit(self, name):
        from datetime import date, timedelta

        if name not in self.habits:
            print("Habit not found.")
            return

        today = str(date.today())
        habit = self.habits[name]

        if today in habit["completed_days"]:
            print("You've already completed this today.")
            return

        # add today
        habit["completed_days"].append(today)

        # calculate streak
        if habit["last_completed"]:
            last = date.fromisoformat(habit["last_completed"])
            if last == date.today() - timedelta(days=1):
                habit["streak"] += 1
            else:
                habit["streak"] = 1
        else:
            habit["streak"] = 1

        habit["last_completed"] = today

        self.save_data()
        print(f"Nice work! {name} streak: {habit['streak']}🔥")
    
    def show_habits(self):
        if not self.habits:
            print("No habits yet. Add one!")
            return

        print("\nYour Habits:")
        for habit, data in self.habits.items():
            streak = data.get("streak", 0)
            days = len(data["completed_days"])
            print(f"- {habit} | Completed {days} days | Streak: {streak}🔥")

