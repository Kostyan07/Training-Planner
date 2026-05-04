import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

DATA_FILE = 'trainings.json'

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ДД.ММ.ГГГГ)").grid(row=0, column=0)
        self.entry_date = tk.Entry(self.root)
        self.entry_date.grid(row=0, column=1)

        tk.Label(self.root, text="Тип тренировки").grid(row=1, column=0)
        self.entry_type = tk.Entry(self.root)
        self.entry_type.grid(row=1, column=1)

        tk.Label(self.root, text="Длительность (минут)").grid(row=2, column=0)
        self.entry_duration = tk.Entry(self.root)
        self.entry_duration.grid(row=2, column=1)

        # Кнопки
        btn_add = tk.Button(self.root, text="Добавить тренировку", command=self.add_training)
        btn_add.grid(row=3, column=0, pady=5)

        btn_save = tk.Button(self.root, text="Сохранить", command=self.save_data)
        btn_save.grid(row=3, column=1, pady=5)

        btn_load = tk.Button(self.root, text="Загрузить", command=self.load_data)
        btn_load.grid(row=3, column=2, pady=5)

        # Таблица
        columns = ('date', 'type', 'duration')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.title())
        self.tree.grid(row=4, column=0, columnspan=3, pady=10)

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу").grid(row=5, column=0)
        self.filter_type = tk.Entry(self.root)
        self.filter_type.grid(row=5, column=1)
        tk.Button(self.root, text="Фильтр", command=self.filter_by_type).grid(row=5, column=2)

        tk.Label(self.root, text="Фильтр по дате (ДД.ММ.ГГГГ)").grid(row=6, column=0)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1)
        tk.Button(self.root, text="Фильтр", command=self.filter_by_date).grid(row=6, column=2)

    def add_training(self):
        date_str = self.entry_date.get().strip()
        t_type = self.entry_type.get().strip()
        duration_str = self.entry_duration.get().strip()

        # Проверка
        if not date_str or not t_type or not duration_str:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        # Проверка формата даты
        try:
            datetime.datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ДД.ММ.ГГГГ")
            return
        # Проверка длительности
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        training = {
            'date': date_str,
            'type': t_type,
            'duration': int(duration_str)
        }
        self.trainings.append(training)
        self.refresh_tree()
        self.clear_entries()

    def refresh_tree(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data_to_show = data if data is not None else self.trainings
        for t in data_to_show:
            self.tree.insert('', 'end', values=(t['date'], t['type'], t['duration']))

    def clear_entries(self):
        self.entry_date.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранение", "Данные сохранены")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)
            self.refresh_tree()

    def filter_by_type(self):
        t_type = self.filter_type.get().strip()
        if not t_type:
            self.refresh_tree()
            return
        filtered = [t for t in self.trainings if t['type'].lower() == t_type.lower()]
        self.refresh_tree(filtered)

    def filter_by_date(self):
        date_filter = self.filter_date.get().strip()
        if not date_filter:
            self.refresh_tree()
            return
        # Проверка формата даты
        try:
            datetime.datetime.strptime(date_filter, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ДД.ММ.ГГГГ")
            return
        filtered = [t for t in self.trainings if t['date'] == date_filter]
        self.refresh_tree(filtered)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()