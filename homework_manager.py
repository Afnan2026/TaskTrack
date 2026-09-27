from openai import OpenAI
from plyer import notification

# Initialize OpenRouter Client
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

homework_list = []


def show_menu():
    print("\n=== HOMEWORK MANAGER & AI TUTOR ===")
    print("1. View Homework")
    print("2. Add Homework")
    print("3. Mark Homework as Done")
    print("4. Ask AI Tutor for Homework Help")
    print("5. Send Desktop Reminder")
    print("6. Exit")


def view_homework():
    if not homework_list:
        print("\nYour homework list is empty!")
        return

    print("\n--- Current Homework ---")
    for index, task in enumerate(homework_list, 1):
        status = "Done" if task["completed"] else "Pending"
        print(f"{index}. [{status}] {task['title']} (Due: {task['due_date']})")


def add_homework():
    title = input("Enter assignment name: ")
    due_date = input("Enter due date (e.g., Tomorrow, Friday): ")

    task = {
        "title": title,
        "due_date": due_date,
        "completed": False
    }

    homework_list.append(task)
    print(f"Added '{title}' to your list!")


def mark_done():
    view_homework()
    if not homework_list:
        return

    try:
        task_num = int(input("\nEnter task number to complete: "))
        if 1 <= task_num <= len(homework_list):
            homework_list[task_num - 1]["completed"] = True
            print("Task marked as completed!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def ask_ai_tutor():
    print("\n--- AI Study Tutor ---")
    question = input("What question or problem do you need help with? ")

    system_prompt = (
        "You are an encouraging Socratic tutor. "
        "Do NOT write direct essay drafts or solve math problems completely. "
        "Explain the core concept, provide hints, and guide the student step-by-step."
    )

    print("\nAsking AI Tutor...")
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        print("\n--- AI Tutor Hint ---")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error connecting to AI: {e}")


def send_desktop_reminder():
    pending_tasks = [task['title'] for task in homework_list if not task['completed']]

    if not pending_tasks:
        print("\nNo pending homework to notify you about!")
        return

    task_summary = ", ".join(pending_tasks)

    # Trigger Windows Desktop Pop-Up Notification
    notification.notify(
        title="Homework Reminder!",
        message=f"Pending tasks: {task_summary}",
        app_name="TaskTrack",
        timeout=10
    )
    print("\nDesktop notification sent!")


# Main program loop
while True:
    show_menu()
    choice = input("\nChoose an option (1-6): ")

    if choice == "1":
        view_homework()
    elif choice == "2":
        add_homework()
    elif choice == "3":
        mark_done()
    elif choice == "4":
        ask_ai_tutor()
    elif choice == "5":
        send_desktop_reminder()
    elif choice == "6":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please select 1-6.")