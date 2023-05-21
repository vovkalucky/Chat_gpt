import sqlite3
import sqlite3 as sq


def sql_start():
    global conn, cur
    conn = sq.connect('chatgpt.db')
    cur = conn.cursor()
    if conn:
        print('Database connect OK')
    conn.execute('CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY, username TEXT, date DATETIME)')
    conn.commit()


async def sql_add_commit(message):
    try:
        print(message.json())
        user_id = message.chat.id
        username = message.chat.username
        date = message.date

        # Проверка наличия пользователя
        cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cur.fetchone()
        if result is None:
            cur.execute('INSERT INTO users VALUES (?,?,?)', (user_id, username, date))
            conn.commit()
        # else:
        #     print("Значение user_id уже существует в таблице.")

    except sqlite3.Error as error:
        print("Error:", error)
    finally:
        if conn:
            conn.close()
