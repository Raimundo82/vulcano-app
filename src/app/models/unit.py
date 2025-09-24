import mysql.connector
from ..config import Config
from ..db import get_connection


def get_units():
    try:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM unidades ORDER BY num_cliente, unidade")
                return cursor.fetchall()
    except mysql.connector.Error as err:
        raise err


def add_unit(num_cliente, unidade, poc, email_poc):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
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
        with get_connection() as conn:
            with conn.cursor() as cursor:
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
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM unidades WHERE id = %s", (unit_id,))
                conn.commit()
                return True
    except mysql.connector.Error as err:
        raise err
