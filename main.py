#! Модуль
import sqlite3

#! Подключение, курсор
con = sqlite3.connect("db_2.db")
cursor = con.cursor()


#! Создание таблицы - Tasks
cursor.execute("""
CREATE TABLE IF NOT EXISTS Tasks (
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
status TEXT DEFAULT 'Not started'
)
""")

#! Добавление новой задачи
def add_task(title):
    cursor.execute("INSERT INTO  Tasks (title) VALUES (?)", (title,))
    con.commit()

#! Обновление статуса задачи
def update_task_status(task_id, status):
    cursor.execute("UPDATE Tasks SET status = ? WHERE id = ?", (status, task_id))
    con.commit()
    
#! Вывод списка задач
def list_tasks():
    cursor.execute("SELECT * FROM Tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)
    
#! Добавление новых задач
add_task("Подготовить презентацию")
add_task("Закончить отчёт")
add_task("Приготовить ужин")

#! Обновление статуса задач
update_task_status(2, "In progress")

#! Вывод списка задач
list_tasks()

#! Отключение
con.close()
