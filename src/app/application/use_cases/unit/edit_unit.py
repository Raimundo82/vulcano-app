from ....domain.entities.unit import Unit
from ....domain.repositories.unit_repository import UnitRepository


class EditUnitUseCase:
    """Update an existing organizational unit."""

    def __init__(self, unit_repository: UnitRepository) -> None:
        self._repo = unit_repository

    def execute(
        self,
        unit_id: int,
        num_cliente: str,
        unidade: str,
        poc: str = "",
        email_poc: str = "",
    ) -> Unit:
        """
        Update the unit identified by *unit_id*.

        Raises :class:`ValueError` when *num_cliente* or *unidade* are blank.
        Raises :class:`LookupError` when the unit is not found.
        """
        num_cliente = num_cliente.strip()
        unidade = unidade.strip()

        if not all([num_cliente, unidade]):
            raise ValueError("num_cliente and unidade are required")

        unit = self._repo.get_by_id(unit_id)
        if unit is None:
            raise LookupError(f"Unit with id {unit_id} not found")

        unit.num_cliente = num_cliente
        unit.unidade = unidade
        unit.poc = poc.strip() or None
        unit.email_poc = email_poc.strip().lower() or None
        return self._repo.update(unit)
