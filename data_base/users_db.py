import sqlite3 as sq
from datetime import date, timedelta
from handlers import other
def db_init ():
    global main_db, cur
    main_db = sq.connect('users_data.db')
    cur = main_db.cursor()
    if main_db:
        print("Підєднались до бд")
    main_db.execute('CREATE TABLE IF NOT EXISTS users (tg_id TEXT PRIMARY KEY,faculty,course,groupe,next_notification,notification_time,get_notification DEFAULT 0,get_news DEFAULT 1)')
    main_db.execute('CREATE TABLE IF NOT EXISTS admins (tg_id TEXT PRIMARY KEY)')
    main_db.commit()
def get_user_groupe(user_id):
    return cur.execute(f'SELECT groupe FROM users WHERE tg_id = {user_id}').fetchall()[0][0]
def check_user(id):
    return cur.execute(f'SELECT * FROM users WHERE tg_id = {id}').fetchall()
def get_users_id_list(faculty,course,groupe):
    filter = 'SELECT tg_id FROM users '
    if faculty != 'False' and faculty != False:
        filter = filter + f"WHERE faculty = '{faculty}'"
    if course != 'False' and course != False:
        filter = filter + f" AND course = '{course}'"
    if groupe != 'False' and groupe != False:
        filter = filter + f" AND groupe = '{groupe}'"
    return cur.execute(filter).fetchall()
def check_admin(id):
    #cur.execute(f'INSERT INTO  admins (tg_id) VALUES ({id})')
    #main_db.commit()
    return cur.execute(f'SELECT * FROM admins WHERE tg_id={id}').fetchall()
"""def add_admin(id):
    if !(cur.execute(f'SELECT * FROM admins WHERE tg_id={id}').fetchall())"""
async def db_add_user(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO  users (tg_id,faculty,course,groupe) VALUES (?,?,?,?)', (tuple(data.values())))
        main_db.commit()
async def delete_user(user_id):
    cur.execute(f'DELETE FROM users WHERE tg_id = {user_id}')
    main_db.commit()
def get_notification_list():
    users = cur.execute(f'SELECT tg_id FROM users WHERE get_notification = "1"').fetchall()
    print(users)
    if users:
        print(users[0][0])
        return users[0]
def get_notification_day():
    users = cur.execute(f'SELECT tg_id FROM users WHERE next_notification = "{date.today()}"').fetchall()
    print(users)
    if users:
        print(users[0][0])
        return users[0]
    return users
def update_notification_day(id):
    day = date.today()+timedelta(days=1)
    print(day)
    cur.execute(f'UPDATE users SET next_notification = "{day}" WHERE tg_id = {id}')
    main_db.commit()
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
def set_news(id):
    cur.execute(f'UPDATE users SET get_news = "1" WHERE tg_id = {id}')
    main_db.commit()
def remove_news(id):
    cur.execute(f'UPDATE users SET get_news = "0" WHERE tg_id = {id}')
    main_db.commit()

