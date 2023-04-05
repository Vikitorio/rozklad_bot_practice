import sqlite3 as sq

def db_init ():
    global main_db, cur
    main_db = sq.connect('users_data.db')
    cur = main_db.cursor()
    if main_db:
        print("Підєднались до бд")
    main_db.execute('CREATE TABLE IF NOT EXISTS users(tg_id TEXT PRIMARY KEY,faculty,course,groupe)')
    main_db.commit()
def get_user_groupe(user_id):
    return cur.execute(f'SELECT groupe FROM users WHERE tg_id = {user_id}').fetchall()[0]
def check_user(id):
    return cur.execute(f'SELECT * FROM users WHERE tg_id = {id}').fetchall()
async def db_add_user(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO users VALUES (?,?,?,?)', (tuple(data.values())))
        main_db.commit()
async def delete_user(user_id):
    cur.execute(f'DELETE FROM users WHERE tg_id = {user_id}')

