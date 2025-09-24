from functools import wraps
from flask import session, jsonify, redirect, url_for, flash, request, current_app
from .ldap_auth import authenticate_user
from ..db import get_connection


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Por favor faça login para aceder esta página", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Por favor faça login", "warning")
            return redirect(url_for("auth.login"))  # Fixed endpoint

        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "SELECT is_admin FROM users WHERE username = %s",
                        (session["username"],),
                    )
                    user = cursor.fetchone()

                    if not user or not user["is_admin"]:
                        flash("Acesso restrito a administradores", "danger")
                        return redirect(url_for("invoices.index"))  # Fixed endpoint

        except Exception as e:
            current_app.logger.error(f"Admin check failed: {str(e)}")
            flash("Erro ao verificar permissões", "danger")
            return redirect(url_for("invoices.index"))

        return f(*args, **kwargs)

    return decorated_function
