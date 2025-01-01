import json
from tabulate import tabulate
from datetime import datetime

# File to store tasks
TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if file doesn't exist
    except json.JSONDecodeError:
        return []  # Handle invalid JSON format

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Add a new task
def add_task(tasks):
    title = input("Enter task title: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()
    priority = input("Enter priority (Low, Medium, High): ").strip().lower()

    # Validate date format
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Task not added.")
        return

    if priority not in ["low", "medium", "high"]:
        print("Invalid priority level. Task not added.")
        return

    task_id = len(tasks) + 1
    tasks.append({
        "id": task_id,
        "title": title,
        "due_date": due_date,
        "priority": priority.capitalize()
    })
    print("Task added successfully!")

# View all tasks
def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    headers = ["ID", "Title", "Due Date", "Priority"]
    rows = [[task["id"], task["title"], task["due_date"], task["priority"]] for task in tasks]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

# Update a task
def update_task(tasks):
    try:
        task_id = int(input("Enter the ID of the task to update: "))
        task = next((task for task in tasks if task["id"] == task_id), None)
        if not task:
            print("Task not found.")
            return

        print(f"Updating Task: {task['title']}")
        new_title = input("Enter new title (leave blank to keep current): ").strip()
        new_due_date = input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ").strip()
        new_priority = input("Enter new priority (Low, Medium, High, leave blank to keep current): ").strip().lower()

        if new_title:
            task["title"] = new_title
        if new_due_date:
            try:
                datetime.strptime(new_due_date, "%Y-%m-%d")
                task["due_date"] = new_due_date
            except ValueError:
                print("Invalid date format. Date not updated.")
        if new_priority in ["low", "medium", "high"]:
            task["priority"] = new_priority.capitalize()

        print("Task updated successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")

# Delete a task
def delete_task(tasks):
    try:
        task_id = int(input("Enter the ID of the task to delete: "))
        task = next((task for task in tasks if task["id"] == task_id), None)
        if not task:
            print("Task not found.")
            return

        tasks.remove(task)
        print("Task deleted successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")

# Main menu
def menu():
    tasks = load_tasks()
    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()
