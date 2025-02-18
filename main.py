#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()

#! Удаление пользователя
cursor.execute("DELETE FROM Users WHERE username = ?", ("newuser",))

#! Сохранение изменений и закрытие соединения
con.commit()
con.close()
