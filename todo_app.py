limport tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pickle

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador de tareas pendientes")

        self.tasks_red = []
        self.tasks_yellow = []
        self.tasks_green = []

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.date_label = tk.Label(root, text="Datos:")
        self.date_label.pack()

        self.date_entry = tk.Entry(root, width=40)
        self.date_entry.pack(pady=10)
        self.date_entry.insert(0, self.get_current_date())

        self.add_button = tk.Button(root, text="Agregar una tarea", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(pady=10)

        self.complete_button = tk.Button(root, text="Completado", command=self.complete_task)
        self.complete_button.pack()

        self.delete_button = tk.Button(root, text="Eliminar tarea", command=self.delete_task)
        self.delete_button.pack()

        self.priority_label = tk.Label(root, text="Prioridad:")
        self.priority_label.pack()

        self.priority_var = tk.StringVar()
        self.priority_var.set("Rojo")
        self.priority_radio_red = tk.Radiobutton(root, text="Rojo", variable=self.priority_var, value="Rojo", command=self.update_task_listbox)
        self.priority_radio_yellow = tk.Radiobutton(root, text="Amarillo", variable=self.priority_var, value="Amarillo", command=self.update_task_listbox)
        self.priority_radio_green = tk.Radiobutton(root, text="Verde", variable=self.priority_var, value="Verde", command=self.update_task_listbox)
        self.priority_radio_red.pack()
        self.priority_radio_yellow.pack()
        self.priority_radio_green.pack()

        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Archivo", menu=self.file_menu)
        self.file_menu.add_command(label="Guardar tarea", command=self.save_tasks)
        self.file_menu.add_command(label="Cargar tarea", command=self.load_tasks)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir del programa", command=root.quit)

        self.about_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Acerca del programa", menu=self.about_menu)
        self.about_menu.add_command(label="Información", command=self.show_about_info)

    def get_current_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def add_task(self):
        task = self.task_entry.get()
        date = self.date_entry.get() or self.get_current_date()
        priority = self.priority_var.get()

        if task:
            if priority == "Rojo":
                self.tasks_red.append((task, date))
            elif priority == "Amarillo":
                self.tasks_yellow.append((task, date))
            elif priority == "Verde":
                self.tasks_green.append((task, date))

            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, self.get_current_date())

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        selected_priority = self.priority_var.get()

        if selected_priority == "Rojo":
            tasks = self.tasks_red
        elif selected_priority == "Amarillo":
            tasks = self.tasks_yellow
        elif selected_priority == "Verde":
            tasks = self.tasks_green

        for task, date in tasks:
            self.task_listbox.insert(tk.END, f"({selected_priority}) ({date}) {task}")

    def complete_task(self):
        selected_priority = self.priority_var.get()
        selected_task_index = self.task_listbox.curselection()

        if selected_priority == "Rojo":
            tasks = self.tasks_red
        elif selected_priority == "Amarillo":
            tasks = self.tasks_yellow
        elif selected_priority == "Verde":
            tasks = self.tasks_green

        if selected_task_index:
            completed_task = tasks[selected_task_index[0]]
            tasks.remove(completed_task)
            self.update_task_listbox()

    def delete_task(self):
        selected_priority = self.priority_var.get()
        selected_task_index = self.task_listbox.curselection()

        if selected_priority == "Rojo":
            tasks = self.tasks_red
        elif selected_priority == "Amarillo":
            tasks = self.tasks_yellow
        elif selected_priority == "Verde":
            tasks = self.tasks_green

        if selected_task_index:
            tasks.pop(selected_task_index[0])
            self.update_task_listbox()

    def save_tasks(self):
        tasks_to_save = {
            "tasks_red": self.tasks_red,
            "tasks_yellow": self.tasks_yellow,
            "tasks_green": self.tasks_green
        }
        with open("tasks.pkl", "wb") as f:
            pickle.dump(tasks_to_save, f)
        messagebox.showinfo("Guardado", "Las listas de tareas pendientes se han guardado.")

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as f:
                tasks_to_load = pickle.load(f)
            self.tasks_red = tasks_to_load["tasks_red"]
            self.tasks_yellow = tasks_to_load["tasks_yellow"]
            self.tasks_green = tasks_to_load["tasks_green"]
            self.update_task_listbox()
            messagebox.showinfo("Cargado", "Se han cargado las listas de tareas pendientes.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo no encontrado.")

    def show_about_info(self):
        about_text = "Planificador de tareas pendientes v1.0\n\n"
        about_text += "Это приложение поможет вам организовать ваши дела по приоритетам.\n"
        about_text += "Задачи делятся на три категории по цветам:\n\n"
        about_text += "• Красный список - очень важные дела\n"
        about_text += "• Желтый список - относительно важные дела\n"
        about_text += "• Зеленый список - не очень важные дела\n\n"
        about_text += "Выберите цвет задачи с помощью радиокнопок. Если вы не указываете дату,\n"
        about_text += "то автоматически будет использована текущая дата.\n"
        about_text += "Вы можете сохранить и загрузить списки дел.\n\n"
        about_text += "Автор: Ashot Gimishyan\n"
        about_text += "Дата: " + datetime.now().strftime("%d.%m.%Y")

        messagebox.showinfo("О программе", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
