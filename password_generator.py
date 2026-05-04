import tkinter as tk
from tkinter import ttk
import random
import string
import json
import os
from datetime import datetime

def generate_password():
    length = length_var.get()
    if length < 4:
        status_var.set("Минимальная длина пароля: 4 символа")
        return
    if length > 64:
        status_var.set("Максимальная длина пароля: 64 символа")
        return
    
    chars = ""
    if digits_var.get():
        chars += string.digits
    if letters_var.get():
        chars += string.ascii_letters
    if special_var.get():
        chars += string.punctuation
    
    if not chars:
        status_var.set("Выберите хотя бы один тип символов")
        return
    
    password = ''.join(random.choice(chars) for _ in range(length))
    password_var.set(password)
    status_var.set(f"Пароль сгенерирован: {len(password)} символов")
    
    history_list.insert(0, {
        'password': password,
        'length': length,
        'digits': digits_var.get(),
        'letters': letters_var.get(),
        'special': special_var.get(),
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    update_history_table()
    save_history()

def update_history_table():
    for item in history_table.get_children():
        history_table.delete(item)
    
    for entry in history_list[:10]:
        types = []
        if entry['digits']:
            types.append("Цифры")
        if entry['letters']:
            types.append("Буквы")
        if entry['special']:
            types.append("Спец.")
        
        history_table.insert("", 0, values=(
            entry['password'],
            entry['length'],
            ", ".join(types) if types else "Нет",
            entry['time']
        ))

def save_history():
    history_data = []
    for entry in history_list[:20]:
        history_data.append(entry)
    
    with open('password_history.json', 'w', encoding='utf-8') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)

def load_history():
    global history_list
    if os.path.exists('password_history.json'):
        try:
            with open('password_history.json', 'r', encoding='utf-8') as f:
                history_list = json.load(f)
            update_history_table()
        except:
            history_list = []

def copy_to_clipboard():
    password = password_var.get()
    if password:
        window.clipboard_clear()
        window.clipboard_append(password)
        status_var.set("Пароль скопирован в буфер обмена")

def clear_history():
    global history_list
    history_list = []
    update_history_table()
    if os.path.exists('password_history.json'):
        os.remove('password_history.json')
    status_var.set("История очищена")

window = tk.Tk()
window.title("Генератор паролей")
window.geometry("700x600")
window.resizable(False, False)

history_list = []

control_frame = ttk.LabelFrame(window, text="Параметры пароля", padding="15")
control_frame.pack(fill="x", padx=15, pady=10)

ttk.Label(control_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
length_var = tk.IntVar(value=12)
length_slider = ttk.Scale(control_frame, from_=4, to=64, variable=length_var, orient="horizontal")
length_slider.grid(row=0, column=1, sticky="ew", padx=10)
length_label = ttk.Label(control_frame, textvariable=length_var, width=5)
length_label.grid(row=0, column=2)

digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=False)

ttk.Checkbutton(control_frame, text="Цифры (0-9)", variable=digits_var).grid(row=1, column=0, sticky="w", pady=3)
ttk.Checkbutton(control_frame, text="Буквы (A-Z, a-z)", variable=letters_var).grid(row=1, column=1, sticky="w", pady=3)
ttk.Checkbutton(control_frame, text="Спецсимволы (!@#$)", variable=special_var).grid(row=1, column=2, sticky="w", pady=3)

button_frame = ttk.Frame(control_frame)
button_frame.grid(row=2, column=0, columnspan=3, pady=10)

generate_btn = ttk.Button(button_frame, text="Сгенерировать пароль", command=generate_password)
generate_btn.pack(side="left", padx=5)

copy_btn = ttk.Button(button_frame, text="Копировать", command=copy_to_clipboard)
copy_btn.pack(side="left", padx=5)

clear_btn = ttk.Button(button_frame, text="Очистить историю", command=clear_history)
clear_btn.pack(side="left", padx=5)

result_frame = ttk.LabelFrame(window, text="Результат", padding="10")
result_frame.pack(fill="x", padx=15, pady=5)

password_var = tk.StringVar(value="")
password_entry = ttk.Entry(result_frame, textvariable=password_var, font=("Courier", 14), state="readonly", justify="center")
password_entry.pack(fill="x", padx=5)

status_var = tk.StringVar(value="Готов к работе")
status_bar = ttk.Label(window, textvariable=status_var, relief="sunken", anchor="w", padding=(10, 5))
status_bar.pack(fill="x", padx=15, pady=(0, 5))

history_frame = ttk.LabelFrame(window, text="История паролей", padding="10")
history_frame.pack(fill="both", expand=True, padx=15, pady=5)

columns = ("Пароль", "Длина", "Типы символов", "Время создания")
history_table = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)

for col in columns:
    history_table.heading(col, text=col)
    history_table.column(col, width=150)

history_table.column("Пароль", width=200)
history_table.column("Типы символов", width=120)
history_table.column("Время создания", width=150)

history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=history_table.yview)
history_table.configure(yscrollcommand=history_scroll.set)

history_table.pack(side="left", fill="both", expand=True)
history_scroll.pack(side="right", fill="y")

load_history()
window.mainloop()
