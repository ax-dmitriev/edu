##! Подключение модулей
##import sqlite3
##
###! Подключение к базе данных
##con = sqlite3.connect("db.db")
##cursor = con.cursor()
##
##try:
##    # Начало транзакции
##    cursor.execute("BEGIN")
##    # Операция
##    cursor.execute("INSERT INTO Users (username, email) VALUES (?, ?)", ("user6", "user6@gmail.com"))
##    cursor.execute("INSERT INTO Users (username, email) VALUES (?, ?)", ("user7", "user7@gmail.com"))
##    # Подтверждение
##    cursor.execute("COMMIT")
##except:
##    # Отмена
##    cursor.execute("ROLLBACK")
##
##
##
##! Сохранение изменений и закрытие соединения
##con.commit()
##con.close()


import sqlite3

with sqlite3.connect("db.db") as con:
    cursor = con.cursor()
    try:
        with con:
            cursor.execute("INSERT INTO Users (username, email) VALUES (?, ?)", ("user8", "user8@gmail.com"))
            cursor.execute("INSERT INTO Users (username, email) VALUES (?, ?)", ("user9", "user9@gmail.com"))
    except:
        pass
