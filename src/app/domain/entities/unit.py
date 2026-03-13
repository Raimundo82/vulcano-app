from dataclasses import dataclass
from typing import Optional


@dataclass
class Unit:
    """Domain entity representing an organizational unit (Unidade de Estrutura Organizacional)."""

    num_cliente: str
    unidade: str
    id: Optional[int] = None
    poc: Optional[str] = None
    email_poc: Optional[str] = None
