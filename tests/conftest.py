import pytest
from app import create_app
from app.extensions.db import db
from app.routes.invoices import invoices_bp  # 1. Importar o blueprint

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # DB temporário
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test_secret_key"
    })
       # 2. Registrar o blueprint na app de teste
    # Use um try-except para evitar erros se outro teste já o registrou
    try:
        app.register_blueprint(invoices_bp, url_prefix="/invoices")
    except ValueError:
        # Blueprint já foi registrado, ignora o erro.
        pass
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
