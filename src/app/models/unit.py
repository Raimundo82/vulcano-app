import mysql.connector
from ..config import Config
from ..db import get_connection
from MySQLdb.cursors import DictCursor


def get_units():
    try:
        conn = get_connection()
        cursor = conn.cursor(DictCursor)
        cursor.execute("SELECT * FROM unidades ORDER BY num_cliente, unidade")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise err


def add_unit(num_cliente, unidade, poc, email_poc):
    try:
        conn = get_connection()
        cursor = conn.cursor(DictCursor)
        cursor.execute(
                    """
                    INSERT INTO unidades (num_cliente, unidade, poc, email_poc)
                    VALUES (%s, %s, %s, %s)
                """,
                    (num_cliente, unidade, poc, email_poc),
                )
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        raise err


def edit_unit(unit_id, num_cliente, unidade, poc, email_poc):
    try:
        conn = get_connection()
        cursor = conn.cursor(DictCursor)
        cursor.execute(
                    """
                    UPDATE unidades
                    SET num_cliente = %s, unidade = %s, poc = %s, email_poc = %s
                    WHERE id = %s
                """,
                    (num_cliente, unidade, poc, email_poc, unit_id),
                )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        raise err


def delete_unit(unit_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(DictCursor)
        cursor.execute("DELETE FROM unidades WHERE id = %s", (unit_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        raise err
