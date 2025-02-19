###! Модуль
##import sqlite3
##
###! Подключение, курсор
##con = sqlite3.connect("db.db")
##cursor = con.cursor()
##
###! Запрос
##query = f"SELECT * FROM Users WHERE age > ?"
##cursor.execute(query, (25,))
##users = cursor.fetchall()
##print(users)
##
##con.close()


#! Модуль
##import sqlite3
##
#! Подключение, курсор
##con = sqlite3.connect("db.db")
##cursor = con.cursor()
##
#! Запрос
####query = f"SELECT * FROM Users WHERE age > ?"
####cursor.execute(query, (25,))
####users = cursor.fetchall()
####print(users)
##
### Представление
##cursor.execute("CREATE VIEW ActiveUsers AS SELECT * FROM Users WHERE is_active = 1")
##cursor.execute("SELECT * FROM ActiveUsers")
##active_users = cursor.fetchall()
##print(active_users)
##
##con.close()


#! Модуль
import sqlite3

#! Подключение, курсор
con = sqlite3.connect("db_2.db")
cursor = con.cursor()

###! Запрос
##cursor.execute("""
##CREATE TABLE IF NOT EXISTS Users (
##id INTEGER PRIMARY KEY,
##username TEXT NOT NULL,
##email TEXT NOT NULL,
##age INTEGER NOT NULL,
##created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
##)
##""")
##
###! Триггер
##cursor.execute("""
##CREATE TRIGGER IF NOT EXISTS update_created_at
##AFTER INSERT ON Users
##BEGIN
##UPDATE Users SET created_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
##END
##""")

#! Индекс
cursor.execute("CREATE INDEX idx_username ON Users (username)")

con.commit()
con.close()
