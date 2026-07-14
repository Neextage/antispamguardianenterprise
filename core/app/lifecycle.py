"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: lifecycle.py
Descrição...: Controla o ciclo de vida da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from enum import Enum, auto


class ApplicationState(Enum):
    """Representa os estados possíveis da aplicação."""

    STARTING = auto()
    RUNNING = auto()
    STOPPING = auto()
    STOPPED = auto()


class ApplicationLifecycle:
    """Gerencia o estado atual da aplicação."""

    def __init__(self) -> None:
        self._state = ApplicationState.STOPPED

    @property
    def state(self) -> ApplicationState:
        """Retorna o estado atual da aplicação."""
        return self._state

    def set_state(self, state: ApplicationState) -> None:
        """Atualiza o estado da aplicação."""
        self._state = state