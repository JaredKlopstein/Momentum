from momentum.tracker import HabitTracker

def main():
    tracker = HabitTracker()

    while True:
        print("\n=== Momentum Habit Tracker ===")
        print("1. Add habit")
        print("2. Check off habit for today")
        print("3. View habits")
        print("4. Quit")

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
