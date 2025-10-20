from app.models.user import User
from app.extensions.db import db

def test_user_model_repr(app):
    """Garante que o __repr__ devolve o formato esperado."""
    with app.app_context():
        user = User(username="m1000", display_name="ADU", email="m1000@marinha.pt", is_admin=True)
        db.session.add(user)
        db.session.commit()

        assert repr(user) == "<User m1000>"
        assert user.username == "m1000"
        assert user.display_name == "ADU"
        assert user.is_admin is True

def test_user_crud_operations(app):
    """Testa CRUD completo do Modelo User"""
    with app.app_context():
        # Cria utilizador
        user = User(username="m1000", display_name="ADU", email="m1000@marinha.pt", is_admin=True)
        user.save()

        found = User.get_by_username("m1000")
        assert found is not None
        assert found.username == "m1000"
        assert found.is_admin is True

        # Atualizar utilizador
        found.display_name = "ADU Updated"
        found.save()
        refreshed = User.get_by_id(found.id)
        assert refreshed.display_name == "ADU Updated"

        # get_al deve conter pelo menos este utilizador
        all_users = User.get_all()
        assert isinstance(all_users, list)
        assert any(u.username == "m1000" for u in all_users)

        # Remover utilizador
        found.delete()
        assert User.get_by_id(found.id) is None

def test_user_repr(app):
    """Testa o método __repr__."""
    with app.app_context():
        user = User(username="m2000", display_name="ADU", email="m2000@marinha.pt", is_admin=True)
        assert repr(user) == "<User m2000>"