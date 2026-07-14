"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: bootstrap.py
Descrição...: Responsável pela inicialização dos componentes da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from core.app.dependency_container import DependencyContainer
from core.app.lifecycle import (
    ApplicationLifecycle,
    ApplicationState,
)


class Bootstrap:
    """
    Inicializa os componentes principais da aplicação.
    """

    def __init__(self) -> None:
        self.container = DependencyContainer()
        self.lifecycle = ApplicationLifecycle()

    def initialize(self) -> DependencyContainer:
        """
        Executa a sequência de inicialização da aplicação.

        Returns:
            DependencyContainer: Container configurado.
        """

        self.lifecycle.set_state(ApplicationState.STARTING)

        # Registra objetos compartilhados
        self.container.register("lifecycle", self.lifecycle)

        self.lifecycle.set_state(ApplicationState.RUNNING)

        return self.container

    def shutdown(self) -> None:
        """
        Finaliza a aplicação.
        """

        self.lifecycle.set_state(ApplicationState.STOPPING)

        self.container.clear()

        self.lifecycle.set_state(ApplicationState.STOPPED)