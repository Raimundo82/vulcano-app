from ....domain.entities.unit import Unit
from ....domain.repositories.unit_repository import UnitRepository


class AddUnitUseCase:
    """Add a new organizational unit."""

    def __init__(self, unit_repository: UnitRepository) -> None:
        self._repo = unit_repository

    def execute(
        self, num_cliente: str, unidade: str, poc: str = "", email_poc: str = ""
    ) -> Unit:
        """
        Create and persist a new :class:`Unit`.

        Raises :class:`ValueError` when *num_cliente* or *unidade* are blank.
        """
        num_cliente = num_cliente.strip()
        unidade = unidade.strip()

        if not all([num_cliente, unidade]):
            raise ValueError("num_cliente and unidade are required")

        unit = Unit(
            num_cliente=num_cliente,
            unidade=unidade,
            poc=poc.strip() or None,
            email_poc=email_poc.strip().lower() or None,
        )
        return self._repo.save(unit)
