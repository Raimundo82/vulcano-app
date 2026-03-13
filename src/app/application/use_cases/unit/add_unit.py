from ....domain.entities.unit import Contact, Unit
from ....domain.repositories.unit_repository import UnitRepository


class AddUnitUseCase:
    """Add a new organizational unit."""

    def __init__(self, unit_repository: UnitRepository) -> None:
        self._repo = unit_repository

    def execute(
        self, num_cliente: str, name: str, poc_name: str = "", poc_email: str = ""
    ) -> Unit:
        """
        Create and persist a new :class:`Unit`.

        *poc_name* and *poc_email* are combined into a :class:`Contact` value
        object.  Both are optional; a unit may have no designated contact.

        Raises :class:`ValueError` when *num_cliente* or *name* are blank.
        """
        num_cliente = num_cliente.strip()
        name = name.strip()

        if not all([num_cliente, name]):
            raise ValueError("num_cliente and name are required")

        poc_name = poc_name.strip()
        poc_email = poc_email.strip().lower()
        contact = Contact(name=poc_name, email=poc_email) if poc_name or poc_email else None

        unit = Unit(
            num_cliente=num_cliente,
            name=name,
            contact=contact,
        )
        return self._repo.save(unit)
