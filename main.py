#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


#! Наибольший возраст
cursor.execute("SELECT * FROM Users")
users = cursor.fetchall()
for i in users:
    print(i)


#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
