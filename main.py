#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


#! Выбор и сортировка по возрасту по убыванию
cursor.execute("""
SELECT username, age, AVG(age)
FROM Users
GROUP BY age
HAVING AVG(age) > ?
ORDER BY age DESC
""", (30,))
res1 = cursor.fetchall()
for row in res1:
    print(row)


#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
