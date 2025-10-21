from app.extensions.db import db

class Unit(db.Model):
    __tablename__ = "unidades"
    id = db.Column(db.Integer, primary_key=True)
    num_cliente = db.Column(db.String(50), nullable=False)
    unidade = db.Column(db.String(100), nullable=False)
    poc = db.Column(db.String(100))
    email_poc = db.Column(db.String(120))

    def __repr__(self):
        return f"<Unit {self.unidade}>"


# Funções ORM CRUD
def get_units():
    """Retorna todas as unidades, sorted by client and unit name"""
    return Unit.query.order_by(Unit.num_cliente, Unit.unidade).all()

def add_unit(num_cliente, unidade, poc, email_poc):
    """Insere um registo de uma nova unidade"""
    new_unit = Unit(
        num_cliente=num_cliente,
        unidade=unidade,
        poc=poc,
        email_poc=email_poc
    )
    db.session.add(new_unit)
    db.session.commit()
    return new_unit.id

def edit_unit(unit_id, num_cliente, unidade, poc, email_poc):
    """Edita um registo de uma unidade existente"""
    unit = Unit.query.get(unit_id)
    if not unit:
        return False
    unit.num_cliente = num_cliente
    unit.unidade = unidade
    unit.poc = poc
    unit.email_poc = email_poc
    db.session.commit()
    return True

def delete_unit(unit_id):
    """Remove a unidade existente"""
    unit = Unit.query.get(unit_id)
    if not unit:
        return False
    db.session.delete(unit)
    db.session.commit()
    return True

