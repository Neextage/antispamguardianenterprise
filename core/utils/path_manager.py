"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: path_manager.py
Descrição...: Gerencia os diretórios utilizados pela aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from pathlib import Path

from core.utils import paths


class PathManager:
    """Responsável por criar e fornecer os diretórios da aplicação."""

    @staticmethod
    def initialize() -> None:
        """
        Cria automaticamente os diretórios necessários.
        """

        directories = [
            paths.LOGS,
            paths.TEMP,
            paths.DATA,
            paths.CONFIG,
            paths.BACKUPS,
            paths.CACHE,
        ]

        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)