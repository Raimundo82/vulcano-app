from ....domain.repositories.unit_repository import UnitRepository


class DeleteUnitUseCase:
    """Delete an organizational unit."""

    def __init__(self, unit_repository: UnitRepository) -> None:
        self._repo = unit_repository

    def execute(self, unit_id: int) -> bool:
        """
        Delete the unit identified by *unit_id*.

        Returns True on success, False when the unit was not found.
        """
        return self._repo.delete(unit_id)
