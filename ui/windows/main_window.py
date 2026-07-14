"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: main_window.py
Descrição...: Janela principal da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

import customtkinter as ctk

from core.utils.colors import Colors
from core.utils.constants import Constants
from core.utils.ui import UI

from ui.windows.dashboard_page import DashboardPage
from ui.windows.sidebar import Sidebar


class MainWindow(ctk.CTk):
    """Janela principal da aplicação."""

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.title(Constants.APPLICATION_NAME)

        self.geometry(
            f"{UI.WINDOW_WIDTH}x{UI.WINDOW_HEIGHT}"
        )

        self.minsize(
            UI.MIN_WIDTH,
            UI.MIN_HEIGHT
        )

        self.configure(
            fg_color=Colors.BACKGROUND
        )

        self._center_window()

        self._create_layout()

    def _center_window(self) -> None:
        """Centraliza a janela na tela."""

        self.update_idletasks()

        width = UI.WINDOW_WIDTH
        height = UI.WINDOW_HEIGHT

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    def _create_layout(self) -> None:
        """Cria o layout principal."""

        #
        # Sidebar
        #

        self.sidebar = Sidebar(self)

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        #
        # Dashboard
        #

        self.dashboard = DashboardPage(self)

        self.dashboard.pack(
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

    # ==========================================================
    # Métodos Públicos
    # ==========================================================

    def add_log(self, message: str) -> None:
        """
        Adiciona um log à Dashboard.
        """

        self.dashboard.logs.add_log(
            message
        )

    def set_status(self, status: str) -> None:
        """
        Atualiza o status do serviço.
        """

        self.dashboard.set_status(
            status
        )