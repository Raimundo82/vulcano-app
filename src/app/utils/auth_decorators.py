from functools import wraps

from flask import current_app, flash, redirect, session, url_for

from ..domain.repositories import UserRepository


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
            return redirect(url_for("auth.login"))

        try:
            user = UserRepository().get_by_username(session["username"])
            if not user or not user.is_admin:
                flash("Acesso restrito a administradores", "danger")
                return redirect(url_for("invoices.index"))
        except Exception as e:
            current_app.logger.error(f"Admin check failed: {str(e)}")
            flash("Erro ao verificar permissões", "danger")
            return redirect(url_for("invoices.index"))

        return f(*args, **kwargs)

    return decorated_function
