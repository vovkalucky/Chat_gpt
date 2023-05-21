import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('chatgpt.db')
    cur = base.cursor()
    if base:
        print('Database connect OK')
    base.execute('CREATE TABLE IF NOT EXISTS menu(user_id TEXT, text TEXT)')
    base.commit()


async def sql_add_commit(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?,?)', tuple(data.values()))
        base.commit()