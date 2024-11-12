import tkinter as ttk
from tkinter import messagebox
import mysql.connector
import tkinter.ttk as tttk

# Настройки подключения к MySQL
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # Ваше имя пользователя MySQL
        password='12543hRGB2001',  # Ваш пароль MySQL
        database='clinic_db'  # Имя вашей базы данных
    )

# Создание таблицы
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция добавления пациента в БД
def add_user():
    name = entry_name.get()
    age = entry_age.get()

    if name and age:
        try:
            age = int(age)
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
            conn.commit()
            conn.close()
            messagebox.showinfo("Информация", "Пациент добавлен")
            entry_name.delete(0, ttk.END)
            entry_age.delete(0, ttk.END)
            display_users()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    else:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")

def delete_user():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите пользователя для удаления")
        return
    user_id = tree.item(selected_item)['values'][0]
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Информация", "Пациент успешно удален")
    display_users()

def display_users():
    for row in tree.get_children():
        tree.delete(row)

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", ttk.END, values=row)

create_table()

root = ttk.Tk()
root.title("Пациенты клиники")

ttk.Label(root, text='Имя:').grid(row=0, column=0)
entry_name = ttk.Entry(root)
entry_name.grid(row=0, column=1)

ttk.Label(root, text='Возраст:').grid(row=1, column=0)
entry_age = ttk.Entry(root)
entry_age.grid(row=1, column=1)

button_add = ttk.Button(root, text='Добавить', command=add_user)
button_add.grid(row=2, column=0, columnspan=2)

button_delete = ttk.Button(root, text='Удалить', command=delete_user)
button_delete.grid(row=4, column=0, columnspan=2)

columns = ("ID", "Имя", "Возраст")
tree = tttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=3, column=0, columnspan=2)

display_users()  # Показать пользователей при запуске

root.mainloop()
