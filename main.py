#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


#! Выбираем всех юзера
cursor.execute("""SELECT * FROM Users WHERE age IS NULL""")
users = cursor.fetchall()

for user in users:
    print(user)


#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
