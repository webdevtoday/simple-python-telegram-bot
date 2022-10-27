import sqlite3
from pathlib import Path


__BASE_DIR = Path(__file__).resolve().parent


def ensure_connection(func):

    def inner(*args, **kwargs):
        with sqlite3.connect(__BASE_DIR.joinpath('questionnaire.db')) as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Check that the required tables exist, otherwise create them

        Important: You must perform migrations to such tables yourself

        :param conn: connection to DBMS
        :param force: explicitly recreate all tables
    """
    c = conn.cursor()

    # User information
    # TODO: create if necessary...

    # Messages from users
    if force:
        c.execute('DROP TABLE IF EXISTS user_message')

    c.execute('''
        CREATE TABLE IF NOT EXISTS user_message (
            id          INTEGER PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            text        TEXT NOT NULL
        )
    ''')

    # Save Changes
    conn.commit()


@ensure_connection
def add_message(conn, user_id: int, text: str):
    c = conn.cursor()
    c.execute(
        'INSERT INTO user_message (user_id, text) VALUES (?, ?)', (user_id, text))
    conn.commit()


@ensure_connection
def count_messages(conn, user_id: int):
    c = conn.cursor()
    c.execute(
        'SELECT COUNT(*) FROM user_message WHERE user_id = ? LIMIT 1', (user_id,))
    (res, ) = c.fetchone()
    return res


@ensure_connection
def list_messages(conn, user_id: int, limit: int = 10):
    c = conn.cursor()
    c.execute(
        'SELECT id, text FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ?', (user_id, limit))
    return c.fetchall()
