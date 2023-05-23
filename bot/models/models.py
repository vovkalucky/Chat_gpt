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


async def sql_add_user(message):
    try:
        user_id = message.chat.id
        username = message.chat.username
        date = message.date

        # Проверка наличия пользователя
        cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        result = cur.fetchone()
        if result is None:
            cur.execute('INSERT INTO users VALUES (?,?,?)', (user_id, username, date))
            conn.commit()
            print('Пользователь добавлен в базу')
        # else:
        #     print("Значение user_id уже существует в таблице.")

    except sqlite3.Error as error:
        print("Error:", error)
    finally:
        if conn:
            conn.close()


async def remove_user_from_database(user_id: int):
    query = "DELETE FROM users WHERE user_id = ?"
    cur.execute(query, (user_id,))
    conn.commit()
    print('Пользователь удален из базы')
    conn.close()
