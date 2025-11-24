import os
from datetime import timedelta

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import Config, DevelopmentConfig, ProductionConfig
from .routes.auth import auth_bp
from .routes.invoices import invoices_bp
from .routes.units import units_bp
from .routes.users import users_bp

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.config.from_object(
    ProductionConfig if os.getenv("FLASK_ENV") == "production" else DevelopmentConfig
)

# For production:
app.config.update(
    SECRET_KEY=Config.SECRET_KEY,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
)

# Import routes

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(users_bp)
app.register_blueprint(units_bp)
