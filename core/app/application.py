"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: application.py
===============================================================================
"""

from core.app.bootstrap import Bootstrap
from core.version import APP_VERSION
from ui.windows.splash_window import SplashWindow


class Application:

    def __init__(self) -> None:

        self.bootstrap = Bootstrap()

    def start(self) -> None:

        print("=" * 60)
        print(APP_VERSION.application_name)
        print("=" * 60)

        self.bootstrap.initialize()

        splash = SplashWindow()

        splash.start()

    def stop(self) -> None:

        self.bootstrap.shutdown()

        print("Aplicação encerrada.")