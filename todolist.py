import tkinter as tk
from tkinter import messagebox
import json
import os


# The tasks will be saved in this file
TASK_FILE = "tasks.json"


# -----------------------------
# FUNCTIONS
# -----------------------------

def load_tasks():
    """Load tasks from the saved file."""

    if os.path.exists(TASK_FILE):

        try:
            with open(TASK_FILE, "r") as file:
                saved_tasks = json.load(file)

                for task in saved_tasks:
                    task_listbox.insert(tk.END, task)

        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "File Error",
                "The saved task file could not be opened."
            )

    update_task_count()


def save_tasks():
    """Save all tasks to a file."""

    all_tasks = task_listbox.get(0, tk.END)

    with open(TASK_FILE, "w") as file:
        json.dump(list(all_tasks), file, indent=4)


def add_task():
    """Add a new task to the list."""

    task = task_entry.get().strip()

    if task == "":
        messagebox.showwarning(
            "Empty Task",
            "Please type a task first."
        )
        return

    task_listbox.insert(tk.END, "☐ " + task)

    task_entry.delete(0, tk.END)
    task_entry.focus()

    save_tasks()
    update_task_count()


def mark_task_done():
    """Mark the selected task as completed."""

    selected_task = task_listbox.curselection()

    if not selected_task:
        messagebox.showwarning(
            "No Task Selected",
            "Please click a task first."
        )
        return

    task_position = selected_task[0]
    task_text = task_listbox.get(task_position)

    if task_text.startswith("☐ "):
        new_text = "✓ " + task_text[2:]

    else:
        new_text = "☐ " + task_text[2:]

    task_listbox.delete(task_position)
    task_listbox.insert(task_position, new_text)
    task_listbox.selection_set(task_position)

    save_tasks()
    update_task_count()


def delete_task():
    """Delete the selected task."""

    selected_task = task_listbox.curselection()

    if not selected_task:
        messagebox.showwarning(
            "No Task Selected",
            "Please click the task you want to delete."
        )
        return

    task_listbox.delete(selected_task[0])

    save_tasks()
    update_task_count()


def delete_all_tasks():
    """Delete every task after asking the user."""

    if task_listbox.size() == 0:
        messagebox.showinfo(
            "No Tasks",
            "Your to-do list is already empty."
        )
        return

    answer = messagebox.askyesno(
        "Delete All Tasks",
        "Are you sure you want to delete all tasks?"
    )

    if answer:
        task_listbox.delete(0, tk.END)

        save_tasks()
        update_task_count()


def update_task_count():
    """Count all tasks and completed tasks."""

    total_tasks = task_listbox.size()
    completed_tasks = 0

    for position in range(total_tasks):
        task = task_listbox.get(position)

        if task.startswith("✓ "):
            completed_tasks += 1

    task_count_label.config(
        text=f"Total: {total_tasks}   |   Completed: {completed_tasks}"
    )


def add_task_with_enter(event):
    """Add a task when the Enter key is pressed."""

    add_task()


# -----------------------------
# MAIN WINDOW
# -----------------------------

window = tk.Tk()

window.title("Rain's To-Do List")
window.geometry("650x720")
window.resizable(False, False)
window.configure(bg="#F5F3FF")


# -----------------------------
# HEADER
# -----------------------------

header = tk.Frame(window, bg="#7C3AED", height=120)
header.pack(fill="x")

title_label = tk.Label(
    header,
    text="My To-Do List",
    font=("Arial", 27, "bold"),
    bg="#7C3AED",
    fg="white"
)

title_label.pack(pady=(22, 5))

subtitle_label = tk.Label(
    header,
    text="Plan your tasks and finish them one by one",
    font=("Arial", 11),
    bg="#7C3AED",
    fg="#EDE9FE"
)

subtitle_label.pack()


# -----------------------------
# MAIN CARD
# -----------------------------

card = tk.Frame(
    window,
    bg="white",
    padx=30,
    pady=25,
    highlightbackground="#DDD6FE",
    highlightthickness=1
)

card.pack(padx=40, pady=30, fill="both", expand=True)


# -----------------------------
# ADD TASK AREA
# -----------------------------

input_label = tk.Label(
    card,
    text="What do you need to do?",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#374151"
)

input_label.pack(anchor="w")

input_frame = tk.Frame(card, bg="white")
input_frame.pack(fill="x", pady=(8, 18))

task_entry = tk.Entry(
    input_frame,
    font=("Arial", 13),
    bd=1,
    relief="solid"
)

task_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=9
)

add_button = tk.Button(
    input_frame,
    text="Add Task",
    font=("Arial", 11, "bold"),
    bg="#7C3AED",
    fg="white",
    activebackground="#6D28D9",
    cursor="hand2",
    command=add_task
)

add_button.pack(
    side="left",
    padx=(10, 0),
    ipadx=12,
    ipady=7
)


# -----------------------------
# TASK LIST
# -----------------------------

list_frame = tk.Frame(card, bg="white")
list_frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

task_listbox = tk.Listbox(
    list_frame,
    font=("Arial", 13),
    bg="#FAFAFA",
    fg="#374151",
    selectbackground="#DDD6FE",
    selectforeground="#4C1D95",
    activestyle="none",
    bd=1,
    relief="solid",
    yscrollcommand=scrollbar.set
)

task_listbox.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.config(command=task_listbox.yview)


# -----------------------------
# TASK COUNT
# -----------------------------

task_count_label = tk.Label(
    card,
    text="Total: 0   |   Completed: 0",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#6B7280"
)

task_count_label.pack(pady=12)


# -----------------------------
# ACTION BUTTONS
# -----------------------------

button_frame = tk.Frame(card, bg="white")
button_frame.pack(fill="x")

done_button = tk.Button(
    button_frame,
    text="Mark Done",
    font=("Arial", 11, "bold"),
    bg="#22C55E",
    fg="white",
    activebackground="#16A34A",
    cursor="hand2",
    command=mark_task_done
)

done_button.grid(
    row=0,
    column=0,
    padx=4,
    ipadx=12,
    ipady=8,
    sticky="ew"
)

delete_button = tk.Button(
    button_frame,
    text="Delete Selected",
    font=("Arial", 11, "bold"),
    bg="#F59E0B",
    fg="white",
    activebackground="#D97706",
    cursor="hand2",
    command=delete_task
)

delete_button.grid(
    row=0,
    column=1,
    padx=4,
    ipadx=12,
    ipady=8,
    sticky="ew"
)

delete_all_button = tk.Button(
    button_frame,
    text="Delete All",
    font=("Arial", 11, "bold"),
    bg="#EF4444",
    fg="white",
    activebackground="#DC2626",
    cursor="hand2",
    command=delete_all_tasks
)

delete_all_button.grid(
    row=0,
    column=2,
    padx=4,
    ipadx=12,
    ipady=8,
    sticky="ew"
)

button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)
button_frame.columnconfigure(2, weight=1)


# Pressing Enter will add the task
task_entry.bind("<Return>", add_task_with_enter)

# Load saved tasks when the app starts
load_tasks()

task_entry.focus()

window.mainloop()