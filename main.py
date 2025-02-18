#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


#! COUNT
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]
print(total_users)

#! SUM
cursor.execute("SELECT SUM(age) FROM Users")
total_sum = cursor.fetchone()[0]
print(total_sum)

#! MIN
cursor.execute("SELECT MIN(age) FROM Users")
total_min = cursor.fetchone()[0]
print(total_min)

#! MAX
cursor.execute("SELECT MAX(age) FROM Users")
total_max = cursor.fetchone()[0]
print(total_max)


#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
