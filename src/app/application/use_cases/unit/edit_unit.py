from ....domain.entities.unit import Contact, Unit
from ....domain.repositories.unit_repository import UnitRepository


class EditUnitUseCase:
    """Update an existing organizational unit."""

    def __init__(self, unit_repository: UnitRepository) -> None:
        self._repo = unit_repository

    def execute(
        self,
        unit_id: int,
        num_cliente: str,
        name: str,
        poc_name: str = "",
        poc_email: str = "",
    ) -> Unit:
        """
        Update the unit identified by *unit_id*.

        *poc_name* and *poc_email* replace the existing :class:`Contact`; pass
        empty strings to remove the contact.

        Raises :class:`ValueError` when *num_cliente* or *name* are blank.
        Raises :class:`LookupError` when the unit is not found.
        """
        num_cliente = num_cliente.strip()
        name = name.strip()

        if not all([num_cliente, name]):
            raise ValueError("num_cliente and name are required")

        unit = self._repo.get_by_id(unit_id)
        if unit is None:
            raise LookupError(f"Unit with id {unit_id} not found")

        poc_name = poc_name.strip()
        poc_email = poc_email.strip().lower()
        contact = Contact(name=poc_name, email=poc_email) if poc_name or poc_email else None

        unit.num_cliente = num_cliente
        unit.name = name
        unit.contact = contact
        return self._repo.update(unit)
