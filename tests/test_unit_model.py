from app.models.unit import Unit, get_units, add_unit, edit_unit, delete_unit
from app.extensions.db import db

def test_unit_model_repr(app):
    """Garante que o modelo Unit guarda dados corretamente e tem __repr__ funcional."""
    with app.app_context():
        unit = Unit(unidade="Base Naval de Lisboa", num_cliente="1001", poc="TestePoc", email_poc="bnl@marinha.pt")
        db.session.add(unit)
        db.session.commit()

        found = Unit.query.filter_by(num_cliente="1001").first()
        assert found is not None
        assert found.unidade == "Base Naval de Lisboa"
        assert "<Unit Base Naval de Lisboa>" == repr(found)

def test_unit_crud_operations(app):
    """Testa as operações CRUD completas do modelo Unit."""
    with app.app_context():
        # 1️⃣ Adicionar uma unidade
        unit_id = add_unit(
            num_cliente="C123",
            unidade="Base Norte",
            poc="Comandante Silva",
            email_poc="silva@marinha.pt"
        )
        assert unit_id is not None

        created = Unit.query.get(unit_id)
        assert created.unidade == "Base Norte"
        assert created.num_cliente == "C123"

        # 2️⃣ Editar a unidade existente
        result = edit_unit(
            unit_id,
            num_cliente="C999",
            unidade="Base Sul",
            poc="Comandante Costa",
            email_poc="costa@marinha.pt"
        )
        assert result is True

        updated = Unit.query.get(unit_id)
        assert updated.unidade == "Base Sul"
        assert updated.poc == "Comandante Costa"

        # 3️⃣ Obter todas as unidades (deve conter a unidade criada)
        units = get_units()
        assert isinstance(units, list)
        assert any(u.id == unit_id for u in units)

        # 4️⃣ Apagar a unidade
        deleted = delete_unit(unit_id)
        assert deleted is True
        assert Unit.query.get(unit_id) is None

def test_edit_and_delete_nonexistent_unit(app):
    """Garante que editar/apagar uma unidade inexistente devolve False."""
    with app.app_context():
        assert edit_unit(9999, "X", "Y", "Z", "email@test.pt") is False
        assert delete_unit(9999) is False

def test_unit_repr():
    """Testa o método __repr__."""
    u = Unit(num_cliente="C001", unidade="Base Atlântica", poc="POC", email_poc="poc@nav.pt")
    assert "<Unit Base Atlântica>" in repr(u)