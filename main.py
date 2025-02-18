#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


#! Наибольший возраст
cursor.execute("""
SELECT username, age
FROM Users
WHERE age = (SELECT MAX(age) FROM Users)
""")
oldtest_users = cursor.fetchall()

for i in oldtest_users:
    print(i)

#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
