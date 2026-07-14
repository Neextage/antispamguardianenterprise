"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: dependency_container.py
Descrição...: Container de dependências da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from typing import Any


class DependencyContainer:
    """
    Container responsável por registrar e fornecer
    objetos compartilhados da aplicação.
    """

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Registra um serviço no container.

        Args:
            name: Nome do serviço.
            service: Instância do serviço.
        """
        self._services[name] = service

    def resolve(self, name: str) -> Any:
        """
        Obtém um serviço registrado.

        Args:
            name: Nome do serviço.

        Returns:
            Instância registrada.

        Raises:
            KeyError:
                Caso o serviço não exista.
        """
        if name not in self._services:
            raise KeyError(f"Serviço '{name}' não registrado.")

        return self._services[name]

    def contains(self, name: str) -> bool:
        """
        Verifica se um serviço existe.
        """
        return name in self._services

    def clear(self) -> None:
        """
        Remove todos os serviços registrados.
        """
        self._services.clear()