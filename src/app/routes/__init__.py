# Import the route blueprints
from .auth import auth_bp
from .invoices import invoices_bp
from .users import users_bp
from .units import units_bp

# Optionally, define what gets imported when using `from app.routes import *`
__all__ = ["auth_bp", "invoices_bp", "users_bp", "units_bp"]
