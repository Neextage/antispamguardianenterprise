"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: account_model.py
Descrição...: Modelo de uma conta do Outlook.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AccountModel:
    """
    Representa uma conta configurada no Microsoft Outlook.
    """

    display_name: str

    store: Any

    inbox: Any | None = None

    is_default: bool = False