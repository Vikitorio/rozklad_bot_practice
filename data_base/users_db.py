import sqlite3 as sq

def db_init ():
    global main_db, cur
    main_db = sq.connect('users_data.db')
    cur = main_db.cursor()
    if main_db:
        print("Підєднались до бд")
    main_db.execute('CREATE TABLE IF NOT EXISTS users (tg_id TEXT PRIMARY KEY,faculty,course,groupe,next_notification,notification_time,get_notification DEFAULT 0,get_news DEFAULT 1)')
    main_db.commit()
def get_user_groupe(user_id):
    return cur.execute(f'SELECT groupe FROM users WHERE tg_id = {user_id}').fetchall()[0]
def check_user(id):
    return cur.execute(f'SELECT * FROM users WHERE tg_id = {id}').fetchall()
async def db_add_user(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO  users (tg_id,faculty,course,groupe) VALUES (?,?,?,?)', (tuple(data.values())))
        main_db.commit()
async def delete_user(user_id):
    cur.execute(f'DELETE FROM users WHERE tg_id = {user_id}')


def get_faculty(id):
    user = cur.execute(f'SELECT faculty FROM users WHERE tg_id = {id}').fetchall()[0][0]
    print(user)
    return user
def set_notification(id,time):
    cur.execute(f'UPDATE users SET get_notification = "1", notification_time = {time} WHERE tg_id = {id}')
    main_db.commit()
def remove_notification(id):
    cur.execute(f'UPDATE users SET get_notification = "0" WHERE tg_id = {id}')
    main_db.commit()