#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()

#! Создание таблицы - Users
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER
)
""")

#! Сохранение изменений и закрытие соединения
con.commit()
con.close()
