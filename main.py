#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


#! Выбираем всех юзера
cursor.execute("""SELECT * FROM Users""")
users = cursor.fetchall()

#! Словарь
users_list = []
for user in users:
    user_dict = {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "age": user[3]
    }
    users_list.append(user_dict)

for user in users_list:
    print(user)

#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
