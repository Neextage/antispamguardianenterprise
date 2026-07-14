"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: application.py
Descrição...: Classe principal responsável pela execução da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from core.app.bootstrap import Bootstrap
from core.app.lifecycle import ApplicationLifecycle
from core.version import APP_VERSION


class Application:
    """
    Classe principal da aplicação.
    """

    def __init__(self) -> None:
        self.bootstrap = Bootstrap()
        self.container = None
        self.lifecycle: ApplicationLifecycle | None = None

    def start(self) -> None:
        """
        Inicializa a aplicação.
        """

        print("=" * 60)
        print(APP_VERSION.application_name)
        print(f"Versão : {APP_VERSION.version}")
        print(f"Build   : {APP_VERSION.build}")
        print(f"Release : {APP_VERSION.release}")
        print("=" * 60)
        print()

        print("Inicializando aplicação...")

        self.container = self.bootstrap.initialize()

        self.lifecycle = self.container.resolve("lifecycle")

        print("Aplicação inicializada com sucesso.")

    def stop(self) -> None:
        """
        Finaliza a aplicação.
        """

        print()
        print("Encerrando aplicação...")

        self.bootstrap.shutdown()

        print("Aplicação encerrada.")