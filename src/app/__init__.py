import os
from datetime import timedelta
from flask import Flask
from flask_wtf.csrf import generate_csrf
from app.extensions.db import db, migrate
from .config import Config, DevelopmentConfig, ProductionConfig
from app.extensions.csrf import csrf
from app.models.user import User
from app.models.unit import Unit
from app.models.invoice import Invoice



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

    db_user = os.getenv("DB_USER", "vulcano")
    db_pass = os.getenv("DB_PASS", "vulcano")
    db_host = os.getenv("DB_HOST", "db")
    db_name = os.getenv("DB_NAME", "vulcano")

    external_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if external_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = external_uri
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"
        )
    

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
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

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(invoices_bp, url_prefix="/invoices")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(units_bp, url_prefix="/units")

    return app

