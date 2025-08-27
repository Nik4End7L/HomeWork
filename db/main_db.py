import sqlite3
from db import queries
from config import db_path
import datetime


def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TASKS)
    print('База данных подключена!')
    conn.commit()
    conn.close()


def add_task(task):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat(timespec="seconds")
    cursor.execute(queries.INSERT_TASK, (task, now))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_task(filter_type='all'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if filter_type == 'completed':
        cursor.execute(queries.SELECT_TASK_COMPLETED)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.SELECT_TASK_UNCOMPLETED)
    else:
        cursor.execute(queries.SELECT_TASK)

    tasks = cursor.fetchall()
    conn.close()
    return tasks 


def delete_task(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()


def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if new_task is not None and completed is not None:
        cursor.execute("UPDATE tasks SET task = ?, completed = ? WHERE id = ?", (new_task, completed, task_id))
    elif new_task is not None:
        cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
    elif completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))

    conn.commit()
    conn.close()

