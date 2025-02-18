#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()

##cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", ("newuser1", "us1@ya.ru", 28))
##cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", ("newuser2", "us2@ya.ru", 29))
##cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", ("newuser3", "us3@ya.ru", 30))
##cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", ("newuser4", "us4@ya.ru", 31))
##cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", ("newuser5", "us5@ya.ru", 32))

#! Запрос
cursor.execute("SELECT * FROM Users")
users = cursor.fetchall()

for user in users:
    print(user)

#! Сохранение изменений и закрытие соединения
con.commit()
con.close()
