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

from core.outlook.outlook_manager import OutlookManager
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

        self.outlook_manager = OutlookManager()

        self._create_widgets()

        #
        # Callback do OutlookPanel
        #

        self.outlook_panel.on_account_changed = (
            self._update_statistics
        )

        self._load_outlook_accounts()

    # ==========================================================
    # Interface
    # ==========================================================

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
        # Painel Outlook
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
            "Inicializando Outlook..."
        )

    # ==========================================================
    # Outlook
    # ==========================================================

    def _load_outlook_accounts(self) -> None:
        """
        Carrega automaticamente as contas do Outlook.
        """

        if not self.outlook_manager.connect():

            self.logs.add_log(
                "Falha ao conectar ao Outlook."
            )

            self.set_status(
                "🔴 Outlook não encontrado"
            )

            return

        accounts = self.outlook_manager.get_account_names()

        self.outlook_panel.set_accounts(
            accounts
        )

        self.logs.add_log(
            "Outlook conectado."
        )

        self.logs.add_log(
            f"{len(accounts)} conta(s) encontrada(s)."
        )

        self.set_status(
            "🟢 Outlook conectado"
        )

        #
        # Atualiza os cards
        #

        self._update_statistics()
            # ==========================================================
    # Atualização da Dashboard
    # ==========================================================

    def _update_statistics(self) -> None:
        """
        Atualiza os cards da Dashboard de acordo
        com a conta selecionada.
        """

        accounts = self.outlook_manager.get_account_names()

        if not accounts:

            self.statistics.set_emails_analyzed(0)

            return

        #
        # Todas as contas
        #

        if self.outlook_panel.analyze_all_accounts():

            total_messages = 0

            for account in accounts:

                total_messages += (
                    self.outlook_manager.get_inbox_message_count(
                        account
                    )
                )

            self.statistics.set_emails_analyzed(
                total_messages
            )

            self.logs.add_log(
                f"Modo: Todas as contas ({total_messages} e-mails)."
            )

            return

        #
        # Conta selecionada
        #

        account = self.outlook_panel.get_selected_account()

        total_messages = (
            self.outlook_manager.get_inbox_message_count(
                account
            )
        )

        self.statistics.set_emails_analyzed(
            total_messages
        )

        self.logs.add_log(
            f"Conta selecionada: {account}"
        )

        self.logs.add_log(
            f"E-mails encontrados: {total_messages}"
        )
            # ==========================================================
    # Métodos públicos
    # ==========================================================

    def refresh(self) -> None:
        """
        Atualiza as estatísticas da Dashboard.
        """

        self._update_statistics()

    def set_status(self, text: str) -> None:
        """
        Atualiza o status do serviço.
        """

        self.status_label.configure(
            text=text
        )