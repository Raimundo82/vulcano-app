# src/app/utils/auth_decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash, current_app
from .ldap_auth import authenticate_user


def login_required(f):
    """Ensure the user is logged in (session-based)."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Por favor faça login para aceder a esta página", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Simulated admin check for migration phase."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip DB check during migration
        if "username" not in session:
            flash("Por favor faça login", "warning")
            return redirect(url_for("auth.login"))

        # ⚠️ Temporary placeholder logic
        # username = session.get("username")
        is_admin = session.get("is_admin", True)  # assume admin during migration

        if not is_admin:
            flash("Acesso restrito a administradores (modo simulado)", "danger")
            return redirect(url_for("invoices.index"))

        return f(*args, **kwargs)
    return decorated_function