from flask import current_app, g
from app import mysql

def get_connection():
    """
    Returns connection from the Flask-MySQLdb extension
    This connection is tied to the Flask app context.
    """
    if "db_conn" not in g:
        g.db_conn = mysql.connection
    return g.db_conn

def close_connection():
    """
    Closes the database connection at the end of the request.
    """
    db_conn = g.pop("db_conn", None)
    if db_conn is not None:
        db_conn.close()
