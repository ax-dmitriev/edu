#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()

#! Добавление нового пользователя
cursor.execute("UPDATE Users SET age = ? WHERE username = ?", (29, "newuser"))

#! Сохранение изменений и закрытие соединения
con.commit()
con.close()
