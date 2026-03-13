from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Contact:
    """
    Value object representing a point-of-contact person.

    Used by :class:`Unit` to store the name and e-mail of the responsible
    officer (POC) for the organisational unit.
    """

    name: str
    email: str


@dataclass
class Unit:
    """
    Domain entity representing an Organisational Unit (Unidade de Estrutura
    Organizacional — UEO).

    Each unit is identified by a ``num_cliente`` which corresponds to the
    MEO telecommunications account/contract number used in invoice data.
    The :attr:`contact` value object holds the responsible officer details.
    """

    num_cliente: str
    name: str

    id: Optional[int] = None
    contact: Optional[Contact] = None
