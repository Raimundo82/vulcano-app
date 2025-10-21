def test_app_import():
    """Verifica se o Flask app é criado corretamente."""
    from app.app import app
    assert app is not None