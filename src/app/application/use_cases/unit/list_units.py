from typing import List

from ....domain.entities.unit import Unit
from ....domain.repositories.unit_repository import UnitRepository


class ListUnitsUseCase:
    """Return all units ordered by client number then unit name."""

    def __init__(self, unit_repository: UnitRepository) -> None:
        self._repo = unit_repository

    def execute(self) -> List[Unit]:
        return self._repo.get_all()
