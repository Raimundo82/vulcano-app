from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.user import User


class UserRepository(ABC):
    """Abstract repository interface for User persistence."""

    @abstractmethod
    def get_all(self) -> List[User]:
        """Return all users ordered by role (admins first) then by username."""

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Return a single user by id, or None if not found."""

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Return a single user by username, or None if not found."""

    @abstractmethod
    def save(self, user: User) -> User:
        """Persist a new user and return it with the generated id."""

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user and return it."""

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete a user by id. Return True on success."""

    @abstractmethod
    def update_last_login(self, username: str) -> bool:
        """Set last_login to the current timestamp for the given username.

        Return True on success.
        """
