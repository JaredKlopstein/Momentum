import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

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
            console.print("[bold yellow]No habits yet. Add one![/]")
            return

        table = Table(title="Momentum Habit Dashboard")

        table.add_column("Habit", style="cyan", no_wrap=True)
        table.add_column("Total Days", style="green")
        table.add_column("Streak 🔥", style="magenta")

        for habit, data in self.habits.items():
            total = len(data.get("completed_days", []))
            streak = data.get("streak", 0)
            table.add_row(habit, str(total), str(streak))

        console.print(table)

    def weekly_stats(self):
        from datetime import date, timedelta

        if not self.habits:
            console.print("[yellow]No habits to analyze yet.[/]")
            return

        table = Table(title="Last 7 Days Progress")
        table.add_column("Habit", style="cyan")
        table.add_column("Completed (7d)", style="green")

        today = date.today()

        for habit, data in self.habits.items():
            completions = 0
            for day in data["completed_days"]:
                d = date.fromisoformat(day)
                if (today - d).days < 7:
                    completions += 1

            table.add_row(habit, f"{completions}/7")

        console.print(table)

    def delete_habit(self, name):
        if name not in self.habits:
            console.print("[red]Habit not found.[/]")
            return
        
        confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
        if confirm == "y":
            del self.habits[name]
            self.save_data()
            console.print(f"[bold red]Deleted habit:[/] {name}")
        else:
            console.print("[yellow]Delete canceled.[/]")
