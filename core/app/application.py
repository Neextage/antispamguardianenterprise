"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: application.py
Descrição...: Classe principal da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from core.app.bootstrap import Bootstrap
from ui.windows.main_window import MainWindow
from ui.windows.splash_window import SplashWindow


class Application:
    """Classe principal da aplicação."""

    def __init__(self) -> None:

        self.bootstrap = Bootstrap()

    def start(self) -> None:

        self.bootstrap.initialize()

        splash = SplashWindow()

        splash.after(
            2600,
            lambda: self._open_main(splash)
        )

        splash.start()

    def _open_main(
        self,
        splash: SplashWindow
    ) -> None:

        splash.destroy()

        window = MainWindow()

        window.mainloop()

    def stop(self) -> None:

        self.bootstrap.shutdown()

        print("Aplicação encerrada.")