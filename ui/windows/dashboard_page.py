"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: dashboard_page.py
Descrição...: Página principal da Dashboard.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkLabel,
)

from core.utils.colors import Colors
from core.utils.constants import Constants
from core.utils.ui import UI

from ui.windows.logs_panel import LogsPanel
from ui.windows.outlook_panel import OutlookPanel
from ui.windows.statistics_cards import StatisticsCards


class DashboardPage(CTkFrame):
    """Página principal da Dashboard."""

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self._create_widgets()

    def _create_widgets(self) -> None:

        #
        # Título
        #

        CTkLabel(
            self,
            text="Dashboard",
            font=(UI.FONT, 28, "bold"),
            text_color=Colors.TEXT
        ).pack(
            anchor="w"
        )

        CTkLabel(
            self,
            text=f"Versão {Constants.VERSION} • Build {Constants.BUILD}",
            font=(UI.FONT, UI.FONT_SMALL),
            text_color=Colors.SUBTEXT
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        #
        # Outlook
        #

        self.outlook_panel = OutlookPanel(self)

        self.outlook_panel.pack(
            fill="x",
            pady=(0, 20)
        )

        #
        # Status
        #

        status = CTkFrame(
            self,
            fg_color=Colors.CARD,
            corner_radius=10
        )

        status.pack(
            fill="x",
            pady=(0, 20)
        )

        CTkLabel(
            status,
            text="Status do Serviço",
            font=(UI.FONT, 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.status_label = CTkLabel(
            status,
            text="🟡 Aguardando início",
            font=(UI.FONT, 14)
        )

        self.status_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        #
        # Cards
        #

        self.statistics = StatisticsCards(self)

        self.statistics.pack(
            anchor="w",
            pady=(0, 20)
        )

        #
        # Botão
        #

        self.start_button = CTkButton(
            self,
            text="▶ Iniciar Análise",
            width=220,
            height=40
        )

        self.start_button.pack(
            anchor="w",
            pady=(0, 20)
        )

        #
        # Logs
        #

        self.logs = LogsPanel(self)

        self.logs.pack(
            fill="both",
            expand=True
        )

        self.logs.add_log(
            "Dashboard carregada com sucesso."
        )

        self.logs.add_log(
            "Aguardando inicialização do serviço."
        )

    # ==========================================================
    # Métodos públicos
    # ==========================================================

    def set_status(self, text: str) -> None:
        """
        Atualiza o status do serviço.
        """

        self.status_label.configure(
            text=text
        )