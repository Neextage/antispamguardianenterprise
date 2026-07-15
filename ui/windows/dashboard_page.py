"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: dashboard_page.py
Descrição...: Página principal da Dashboard.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

from customtkinter import (
    CTkButton,
    CTkFrame,
    CTkLabel
)

from core.utils.colors import Colors
from core.utils.constants import Constants
from core.utils.ui import UI

from ui.windows.dashboard_controller import DashboardController
from ui.windows.logs_panel import LogsPanel
from ui.windows.outlook_panel import OutlookPanel
from ui.windows.statistics_cards import StatisticsCards


class DashboardPage(CTkFrame):
    """
    Página principal da Dashboard.
    """

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        #
        # Controller
        #

        self.controller = DashboardController()

        #
        # Componentes
        #

        self.outlook_panel: OutlookPanel | None = None

        self.statistics: StatisticsCards | None = None

        self.logs: LogsPanel | None = None

        self.status_label: CTkLabel | None = None

        self.start_button: CTkButton | None = None

        #
        # Interface
        #

        self._create_widgets()

        #
        # Inicialização
        #

        self._initialize_dashboard()

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
        # Outlook
        #

        self.outlook_panel = OutlookPanel(
            self
        )

        self.outlook_panel.pack(
            fill="x",
            pady=(0, 20)
        )

        #
        # Status
        #

        status_frame = CTkFrame(
            self,
            fg_color=Colors.CARD,
            corner_radius=10
        )

        status_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        CTkLabel(
            status_frame,
            text="Status do Serviço",
            font=(UI.FONT, 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.status_label = CTkLabel(
            status_frame,
            text="🟡 Inicializando...",
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

        self.statistics = StatisticsCards(
            self
        )

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
            height=40,
            command=self._start_scan
        )

        self.start_button.pack(
            anchor="w",
            pady=(0, 20)
        )

        #
        # Logs
        #

        self.logs = LogsPanel(
            self
        )

        self.logs.pack(
            fill="both",
            expand=True
        )

    # ==========================================================
    # Inicialização
    # ==========================================================

    def _initialize_dashboard(self) -> None:
        """
        Inicializa a Dashboard.
        """

        self.logs.add_log(
            "Inicializando Dashboard..."
        )

        result = self.controller.initialize()

        if not result["success"]:

            self.set_status(
                result["status"]
            )

            self.logs.add_log(
                "Falha ao conectar ao Outlook."
            )

            return

        self.outlook_panel.set_accounts(
            result["accounts"]
        )

        self.set_status(
            result["status"]
        )

        self.logs.add_log(
            "Outlook conectado."
        )

        self.logs.add_log(
            f"{len(result['accounts'])} conta(s) encontrada(s)."
        )

        #
        # Atualiza os cards logo na abertura
        #

        self._update_statistics()
            # ==========================================================
    # Scanner
    # ==========================================================

    def _start_scan(self) -> None:
        """
        Inicia a análise dos e-mails.
        """

        account = self.outlook_panel.get_selected_account()

        if not account:

            self.logs.add_log(
                "Nenhuma conta selecionada."
            )

            return

        self.set_status(
            "🟡 Analisando e-mails..."
        )

        self.logs.add_log(
            f"Iniciando análise da conta: {account}"
        )

        #
        # Nesta primeira versão vamos analisar
        # toda a Caixa de Entrada.
        #

        result = self.controller.start_scan(
            account_name=account
        )

        #
        # Atualiza os cards
        #

        statistics = result["statistics"]

        self.statistics.update_statistics(

            emails=statistics["emails"],

            spam=statistics["spam"],

            quarantine=statistics["quarantine"],

            critical=statistics["critical"]

        )

        #
        # Atualiza os logs
        #

        for message in result["logs"]:

            self.logs.add_log(
                message
            )

        self.set_status(
            "🟢 Análise concluída."
        )
            # ==========================================================
    # Dashboard
    # ==========================================================

    def _update_statistics(self) -> None:
        """
        Atualiza os cards da Dashboard de acordo
        com a conta selecionada.
        """

        account = self.outlook_panel.get_selected_account()

        if not account:

            self.statistics.update_statistics(
                emails=0,
                spam=0,
                quarantine=0,
                critical=0
            )

            return

        total = self.controller.get_total_messages(
            account
        )

        self.statistics.update_statistics(
            emails=total,
            spam=0,
            quarantine=0,
            critical=0
        )

    # ==========================================================
    # Scanner
    # ==========================================================

    def _start_scan(self) -> None:
        """
        Inicia a análise dos últimos e-mails
        da conta selecionada.
        """

        account = self.outlook_panel.get_selected_account()

        if not account:

            self.logs.add_log(
                "Nenhuma conta selecionada."
            )

            return

        self.set_status(
            "🟡 Analisando os últimos 100 e-mails..."
        )

        self.logs.add_log(
            f"Conta selecionada: {account}"
        )

        #
        # Nesta versão analisaremos apenas
        # os 100 e-mails mais recentes.
        #

        result = self.controller.start_scan(

            account_name=account,

            limit=100

        )

        statistics = result["statistics"]

        self.statistics.update_statistics(

            emails=statistics["emails"],

            spam=statistics["spam"],

            quarantine=statistics["quarantine"],

            critical=statistics["critical"]

        )

        for log in result["logs"]:

            self.logs.add_log(log)

        self.logs.add_log(
            "Análise finalizada."
        )

        self.set_status(
            "🟢 Scanner finalizado"
        )

    # ==========================================================
    # Métodos Públicos
    # ==========================================================

    def refresh(self) -> None:
        """
        Atualiza os dados da Dashboard.
        """

        self._update_statistics()

    def set_status(
        self,
        text: str
    ) -> None:
        """
        Atualiza o texto do Status.
        """

        self.status_label.configure(
            text=text
        )

    def destroy(self) -> None:
        """
        Finaliza a Dashboard.
        """

        try:

            self.controller.close()

        except Exception:

            pass

        super().destroy()