import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class EditTaskWindow(tk.Toplevel):
    def __init__(self, parent, task, update_callback):
        super().__init__(parent)
        self.title("Edit Task")
        self.parent = parent
        self.task = task
        self.update_callback = update_callback

        self.task_name_label = ttk.Label(self, text="Task Name:")
        self.task_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.task_name_entry = ttk.Entry(self, width=40)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.task_description_label = ttk.Label(self, text="Description:")
        self.task_description_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.task_description_entry = ttk.Entry(self, width=40)
        self.task_description_entry.grid(row=1, column=1, padx=5, pady=5)

        self.task_due_label = ttk.Label(self, text="Due Date:")
        self.task_due_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.task_due_entry = DateEntry(self)
        self.task_due_entry.grid(row=2, column=1, padx=5, pady=5)

        self.completed_var = tk.BooleanVar()
        self.completed_check = ttk.Checkbutton(self, text="Completed", variable=self.completed_var)
        self.completed_check.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.update_button = ttk.Button(self, text="Update", command=self.update_task)
        self.update_button.grid(row=4, column=1, padx=5, pady=5, sticky='e')

        self.task_name_entry.insert(0, task['task'])
        self.task_description_entry.insert(0, task['description'])
        self.task_due_entry.set_date(datetime.strptime(task['due_date'], '%Y-%m-%d'))
        self.completed_var.set(task['completed'])

    def update_task(self):
        new_task_name = self.task_name_entry.get()
        new_description = self.task_description_entry.get()
        new_due_date = self.task_due_entry.get_date().strftime('%Y-%m-%d')
        new_completed = self.completed_var.get()

        if new_task_name.strip() == "":
            messagebox.showerror("Error", "Task name cannot be empty.")
            return

        self.task['task'] = new_task_name
        self.task['description'] = new_description
        self.task['due_date'] = new_due_date
        self.task['completed'] = new_completed
        self.update_callback()
        self.destroy()

class TodoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Bold.TLabel', font=('Helvetica', 10, 'bold'))

        self.tasks = []

        ttk.Label(master, text="Create Task", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(master, text="Task Name:", style='Bold.TLabel').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.task_entry = ttk.Entry(master, width=40)
        self.task_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Description:", style='Bold.TLabel').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.description_entry = ttk.Entry(master, width=40)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Due Date:", style='Bold.TLabel').grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.due_date_entry = DateEntry(master, width=15)
        self.due_date_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=4, column=1, padx=5, pady=10, sticky='e')

        ttk.Separator(master, orient='horizontal').grid(row=5, column=0, columnspan=2, sticky='ew', padx=5, pady=10)

        ttk.Label(master, text="Tasks", font=('Helvetica', 12, 'bold')).grid(row=6, column=0, columnspan=2)
        self.task_listbox = tk.Listbox(master, width=70, height=15)
        self.task_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        self.task_listbox.bind("<<ListboxSelect>>", self.enable_update_button)

        self.remove_button = ttk.Button(master, text="Remove Task", command=self.remove_task)
        self.remove_button.grid(row=8, column=0, padx=5, pady=10, sticky='w')

        self.update_button = ttk.Button(master, text="Update Task", command=self.edit_selected_task)
        self.update_button.grid(row=8, column=1, padx=5, pady=10, sticky='e')
        self.update_button.configure(state="disabled")

    def add_task(self):
        task_name = self.task_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date_entry.get_date().strftime('%Y-%m-%d')

        if task_name.strip() == "":
            messagebox.showerror("Error", "Task name cannot be empty.")
            return

        self.tasks.append({'task': task_name, 'description': description, 'due_date': due_date, 'completed': False})
        self.update_task_listbox()
        self.task_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

    def remove_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def edit_selected_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_index]
            edit_window = EditTaskWindow(self.master, task, self.update_task_listbox)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    def enable_update_button(self, event):
        if self.task_listbox.curselection():
            self.update_button.configure(state="normal")
        else:
            self.update_button.configure(state="disabled")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task_data in enumerate(self.tasks, start=1):
            task_info = f"Task {idx}:\n"
            task_info += f"  Task Name: {task_data['task']}\n"
            task_info += f"  Description: {task_data['description']}\n"
            task_info += f"  Due Date: {task_data['due_date']}\n"
            task_info += f"  Completed: {'Yes' if task_data['completed'] else 'No'}\n"
            self.task_listbox.insert(tk.END, task_info)

def main():
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
