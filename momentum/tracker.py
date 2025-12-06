import json
import uuid
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table

console = Console()
DATA_FILE = "data/habits.json"


class HabitTracker:
    def __init__(self):
        self.habits = self.load_data()  # {id: habit_data}

    # ---------------- Data Handling ---------------- #

    def load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            return {habit["id"]: habit for habit in data.get("habits", [])}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump({"habits": list(self.habits.values())}, f, indent=2)

    # ---------------- Habit Ops ---------------- #

    def add_habit(self, name, notes=""):
        habit_id = str(uuid.uuid4())
        self.habits[habit_id] = {
            "id": habit_id,
            "name": name,
            "completed_days": [],
            "streak": 0,
            "last_completed": None,
            "notes": notes,
        }
        self.save_data()
        console.print(f"[green]Habit added:[/] {name} ({habit_id[:6]})")
        return habit_id

    def check_habit(self, name):
        # Find habit by name (user friendly)
        habit_id = next((hid for hid, h in self.habits.items() if h["name"] == name), None)
        if not habit_id:
            console.print("[red]Habit not found.[/]")
            return

        habit = self.habits[habit_id]
        today = str(date.today())

        if today in habit["completed_days"]:
            console.print("[yellow]Already checked off today.[/]")
            return

        habit["completed_days"].append(today)

        # streak logic
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

        console.print(f"🔥 Nice work! {habit['name']} streak: {habit['streak']}")

    def show_habits(self):
        if not self.habits:
            console.print("[bold yellow]No habits yet. Add one![/]")
            return

        table = Table(title="Momentum Habit Dashboard")
        table.add_column("Habit", style="cyan", no_wrap=True)
        table.add_column("Total Days", style="green")
        table.add_column("Streak 🔥", style="magenta")

        for habit in self.habits.values():
            total = len(habit["completed_days"])
            streak = habit["streak"]
            table.add_row(habit["name"], str(total), str(streak))

        console.print(table)

    def weekly_stats(self):
        if not self.habits:
            console.print("[yellow]No habits to analyze yet.[/]")
            return

        table = Table(title="Last 7 Days Progress")
        table.add_column("Habit", style="cyan")
        table.add_column("Completed (7d)", style="green")

        today = date.today()

        for habit in self.habits.values():
            completions = sum(
                (today - date.fromisoformat(day)).days < 7
                for day in habit["completed_days"]
            )
            table.add_row(habit["name"], f"{completions}/7")

        console.print(table)

    def delete_habit(self, name):
        habit_id = next((hid for hid, h in self.habits.items() if h["name"] == name), None)
        if not habit_id:
            console.print("[red]Habit not found.[/]")
            return
        
        confirm = input(f"Delete '{name}'? (y/n): ").lower()
        if confirm == "y":
            del self.habits[habit_id]
            self.save_data()
            console.print(f"[red bold]Deleted:[/] {name}")
        else:
            console.print("[yellow]Canceling delete.[/]")
