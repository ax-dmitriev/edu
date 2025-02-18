#! Подключение модулей
import sqlite3

#! Подключение к базе данных
con = sqlite3.connect("db.db")
cursor = con.cursor()


###! Выбираем имена и возраст юзеров старше 25 лет
##cursor.execute("SELECT username, age FROM Users WHERE age > ?", (25,))
##res = cursor.fetchall()
##for row in res:
##    print(row)
        
###! Средний возраст для каждого возраста
##cursor.execute("SELECT age, AVG(age) FROM Users GROUP BY age")
##res1 = cursor.fetchall()
##for row in res1:
##    print(row)
###! Фильтр по среднему более 30 лет
##cursor.execute("SELECT age, AVG(age) FROM Users GROUP BY age HAVING AVG(age) > ?", (30,))
##res2 = cursor.fetchall()
##for row in res2:
##    print(row)

#! Выбор и сортировка по возрасту по убыванию
cursor.execute("SELECT username, age FROM Users ORDER BY age DESC")
res1 = cursor.fetchall()
for row in res1:
    print(row)


#! Сохранение изменений и закрытие соединения
##con.commit()
con.close()
