from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.unit import Unit


class UnitRepository(ABC):
    """Abstract repository interface for Unit persistence."""

    @abstractmethod
    def get_all(self) -> List[Unit]:
        """Return all units ordered by num_cliente then unidade."""

    @abstractmethod
    def get_by_id(self, unit_id: int) -> Optional[Unit]:
        """Return a single unit by id, or None if not found."""

    @abstractmethod
    def save(self, unit: Unit) -> Unit:
        """Persist a new unit and return it with the generated id."""

    @abstractmethod
    def update(self, unit: Unit) -> Unit:
        """Update an existing unit and return it."""

    @abstractmethod
    def delete(self, unit_id: int) -> bool:
        """Delete a unit by id. Return True on success."""
