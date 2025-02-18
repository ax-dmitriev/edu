#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()

#! Создание индекса для столбца email
cursor.execute("CREATE INDEX idx_email ON Users (email)")

#! Сохранение изменений и закрытие соединения
con.commit()
con.close()
