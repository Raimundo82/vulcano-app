import os
from datetime import timedelta
from flask import Flask
from flask_mysqldb import MySQL
from flask_wtf.csrf import generate_csrf
from flask_wtf.csrf import generate_csrf
from .config import Config, DevelopmentConfig, ProductionConfig
from app.extensions.csrf import csrf

# Initialize extensions globally
mysql = MySQL()

def create_app():
    """Application factory for Flask app."""
    app = Flask(__name__)

    # Configurations based on enviroment
    config_class = (
        ProductionConfig
        if os.getenv("FLASK_ENV") == "production"
        else DevelopmentConfig
    )
    app.config.from_object(config_class)

    # Common production/session configs
    app.config.update(
        SECRET_KEY=Config.SECRET_KEY,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
    )

    app.config["MYSQL_AUTOCOMMIT"] = True

    # Initialize extensions
    mysql.init_app(app)
    csrf.init_app(app)

    @app.context_processor
    def inject_csrf_token():
        return {"csrf_token": lambda: generate_csrf()}

    @app.context_processor
    def inject_csrf_token():
        return {"csrf_token": lambda: generate_csrf()}

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.invoices import invoices_bp
    from .routes.users import users_bp
    from .routes.units import units_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(units_bp)

    return app


