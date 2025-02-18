#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()

#! Добавление нового пользователя
cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", ("newuser", "us1@ya.ru", 28))

#! Сохранение изменений и закрытие соединения
con.commit()
con.close()
