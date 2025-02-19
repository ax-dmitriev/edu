#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


#! Выбираем первого юзера
cursor.execute("""SELECT * FROM Users""")
first_user = cursor.fetchone()
print(first_user)

#! Выбираем первых двух юзера
cursor.execute("""SELECT * FROM Users""")
first_3_user = cursor.fetchmany(3)
print(first_3_user)

#! Выбираем всех юзера
cursor.execute("""SELECT * FROM Users""")
all_users = cursor.fetchall()
print(all_users)



#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
