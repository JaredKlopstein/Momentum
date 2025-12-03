from momentum.tracker import HabitTracker
from rich.console import Console
console = Console()

def main():
    tracker = HabitTracker()

    while True:
        console.print("\n[bold blue]=== Momentum Habit Tracker ===[/]")
        console.print("[cyan]1.[/] Add habit")
        console.print("[cyan]2.[/] Check off habit for today")
        console.print("[cyan]3.[/] View habits dashboard")
        console.print("[cyan]4.[/] Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Habit name: ")
            tracker.add_habit(name)
        elif choice == "2":
            name = input("Habit to check off: ")
            tracker.check_habit(name)
        elif choice == "3":
            tracker.show_habits()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
