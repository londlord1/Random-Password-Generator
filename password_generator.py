import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
from datetime import datetime
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        
        # Файл для хранения истории
        self.history_file = "password_history.json"
        self.history = []
        
        # Загружаем историю
        self.load_history()
        
        # Создаем интерфейс
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для настроек
        settings_frame = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        settings_frame.pack(padx=10, pady=10, fill="x")
        
        # Ползунок длины пароля
        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill="x", pady=5)
        
        ttk.Label(length_frame, text="Длина пароля:").pack(side="left")
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(length_frame, from_=4, to=50, variable=self.length_var, 
                                      orient="horizontal", command=self.update_length_label)
        self.length_scale.pack(side="left", fill="x", expand=True, padx=(10, 10))
        
        self.length_label = ttk.Label(length_frame, text="12", width=3)
        self.length_label.pack(side="left")
        
        # Чекбоксы для выбора символов
        checkboxes_frame = ttk.Frame(settings_frame)
        checkboxes_frame.pack(fill="x", pady=10)
        
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_lowercase = tk.BooleanVar(value=True)
        self.include_uppercase = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(checkboxes_frame, text="Цифры (0-9)", variable=self.include_numbers).pack(anchor="w")
        ttk.Checkbutton(checkboxes_frame, text="Строчные буквы (a-z)", variable=self.include_lowercase).pack(anchor="w")
        ttk.Checkbutton(checkboxes_frame, text="Заглавные буквы (A-Z)", variable=self.include_uppercase).pack(anchor="w")
        ttk.Checkbutton(checkboxes_frame, text="Спецсимволы (!@#$%^&*)", variable=self.include_special).pack(anchor="w")
        
        # Кнопка генерации
        self.generate_button = ttk.Button(settings_frame, text="Сгенерировать пароль", 
                                         command=self.generate_password)
        self.generate_button.pack(pady=10)
        
        # Отображение сгенерированного пароля
        password_frame = ttk.Frame(settings_frame)
        password_frame.pack(fill="x", pady=5)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                       font=("Courier", 12), state="readonly")
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        self.copy_button = ttk.Button(password_frame, text="Копировать", command=self.copy_to_clipboard)
        self.copy_button.pack(side="left", padx=(5, 0))
        
        # Фрейм для истории
        history_frame = ttk.LabelFrame(self.root, text="История паролей", padding=10)
        history_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Таблица истории
        columns = ("#", "Пароль", "Длина", "Дата создания")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=10)
        
        self.history_tree.heading("#", text="#")
        self.history_tree.heading("Пароль", text="Пароль")
        self.history_tree.heading("Длина", text="Длина")
        self.history_tree.heading("Дата создания", text="Дата создания")
        
        self.history_tree.column("#", width=40, anchor="center")
        self.history_tree.column("Пароль", width=200, anchor="center")
        self.history_tree.column("Длина", width=80, anchor="center")
        self.history_tree.column("Дата создания", width=150, anchor="center")
        
        # Scrollbar для таблицы
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопки управления историей
        buttons_frame = ttk.Frame(history_frame)
        buttons_frame.pack(fill="x", pady=5)
        
        ttk.Button(buttons_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Обновить", command=self.refresh_history).pack(side="left", padx=5)
        
        # Загружаем историю в таблицу
        self.refresh_history()
    
    def update_length_label(self, value):
        self.length_label.config(text=str(int(float(value))))
    
    def generate_password(self):
        # Проверка выбора символов
        chars = ""
        if self.include_numbers.get():
            chars += string.digits
        if self.include_lowercase.get():
            chars += string.ascii_lowercase
        if self.include_uppercase.get():
            chars += string.ascii_uppercase
        if self.include_special.get():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return
        
        # Генерация пароля
        length = int(self.length_var.get())
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Отображение пароля
        self.password_var.set(password)
        
        # Сохранение в историю
        self.add_to_history(password, length)
    
    def add_to_history(self, password, length):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            "password": password,
            "length": length,
            "timestamp": timestamp
        }
        
        self.history.append(history_entry)
        self.save_history()
        self.refresh_history()
    
    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
                self.history = []
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить историю?"):
            self.history = []
            self.save_history()
            self.refresh_history()
    
    def refresh_history(self):
        # Очищаем таблицу
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Заполняем таблицу
        for i, entry in enumerate(self.history, 1):
            self.history_tree.insert("", "end", values=(
                i,
                entry["password"],
                entry["length"],
                entry["timestamp"]
            ))
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Скопировано", "Пароль скопирован в буфер обмена!")

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()