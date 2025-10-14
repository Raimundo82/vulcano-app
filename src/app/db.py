from app import mysql
from MySQLdb.cursors import DictCursor

def get_connection():
    """Return the Flask-MySQLdb connection (context managed automatically)."""
    return mysql.connection

def get_dict_cursor():
    """Convenience helper that returns a dictionary-style cursor."""
    conn = get_connection()
    return conn.cursor(DictCursor)