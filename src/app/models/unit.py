from ..domain.repositories import UnitRepository

_repo = UnitRepository()


def get_units():
    return [u.to_dict() for u in _repo.get_all()]


def add_unit(num_cliente, unidade, poc, email_poc):
    unit = _repo.create(num_cliente, unidade, poc, email_poc)
    return unit.id


def edit_unit(unit_id, num_cliente, unidade, poc, email_poc):
    return (
        _repo.update(
            unit_id,
            num_cliente=num_cliente,
            unidade=unidade,
            poc=poc,
            email_poc=email_poc,
        )
        is not None
    )


def delete_unit(unit_id):
    return _repo.delete(unit_id)
