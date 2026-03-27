import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Keeping the DB path configurable makes the project easier to run
# both locally and inside Docker.
DEFAULT_DB_NAME = 'task_manager.db'
DB_PATH = os.getenv('DB_PATH', DEFAULT_DB_NAME)


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with rows accessible like dictionaries."""
    db_file = Path(DB_PATH)
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


@contextmanager
def get_db_cursor():
    """
    Small helper so each route does not have to repeat the same
    commit / rollback / close logic every time.
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        yield connection, cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
