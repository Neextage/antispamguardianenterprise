"""
Projeto : Antispam Guardian Enterprise
Arquivo : version.py
Autor   : Neextage
Versão  : 0.1.0

Responsabilidade:
Centralizar todas as informações de versão da aplicação.
Este será o único local onde os dados de versão deverão ser alterados.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ApplicationVersion:
    """Representa as informações oficiais da versão da aplicação."""

    application_name: str = "Antispam Guardian Enterprise"
    version: str = "0.1.0"
    build: int = 1
    release: str = "Development"
    author: str = "Neextage"
    company: str = "Neextage"
    python_version: str = "3.13"


APP_VERSION = ApplicationVersion()