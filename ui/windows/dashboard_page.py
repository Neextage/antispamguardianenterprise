"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: dashboard_page.py
Descrição...: Página principal da Dashboard.
Autor.......: Neextage
Versão......: 0.3.0
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

        self.outlook_panel = OutlookPanel(self)

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

        self.logs = LogsPanel(self)

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

        #
        # Carrega as contas
        #

        self.outlook_panel.set_accounts(
            result["accounts"]
        )

        #
        # Atualiza o status
        #

        self.set_status(
            result["status"]
        )

        #
        # Logs
        #

        self.logs.add_log(
            "Outlook conectado."
        )

        self.logs.add_log(
            f"{len(result['accounts'])} conta(s) encontrada(s)."
        )

        #
        # Atualiza os cards ao iniciar
        #

        self._update_statistics()

    # ==========================================================
    # Dashboard
    # ==========================================================

    def _update_statistics(self) -> None:
        """
        Atualiza os cards conforme
        a conta atualmente selecionada.
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
        Inicia a análise dos e-mails.
        """

        #
        # Descobre quais contas serão analisadas
        #

        if self.outlook_panel.analyze_all_accounts():

            accounts = self.controller.get_accounts()

            self.logs.add_log(
                "Modo: analisar todas as contas."
            )

        else:

            account = self.outlook_panel.get_selected_account()

            if not account:

                self.logs.add_log(
                    "Nenhuma conta selecionada."
                )

                return

            accounts = [account]

        #
        # Atualiza o status
        #

        self.set_status(
            "🟡 Analisando e-mails..."
        )

        #
        # Zera os acumuladores
        #

        total_emails = 0
        total_spam = 0
        total_quarantine = 0
        total_critical = 0

        #
        # Analisa cada conta
        #

        for account in accounts:

            self.logs.add_log("")

            self.logs.add_log(
                f"Conta selecionada: {account}"
            )

            result = self.controller.start_scan(

                account_name=account,

                limit=100

            )

            statistics = result["statistics"]

            total_emails += statistics["emails"]
            total_spam += statistics["spam"]
            total_quarantine += statistics["quarantine"]
            total_critical += statistics["critical"]

            for message in result["logs"]:

                self.logs.add_log(
                    message
                )

        #
        # Atualiza os cards apenas uma vez
        #

        self.statistics.update_statistics(

            emails=total_emails,

            spam=total_spam,

            quarantine=total_quarantine,

            critical=total_critical

        )

        self.logs.add_log("")

        self.logs.add_log(
            "======================================"
        )

        self.logs.add_log(
            "Resumo Geral"
        )

        self.logs.add_log(
            f"E-mails analisados: {total_emails}"
        )

        self.logs.add_log(
            f"Spam detectado: {total_spam}"
        )

        self.logs.add_log(
            f"Quarentena: {total_quarantine}"
        )

        self.logs.add_log(
            f"Spam crítico: {total_critical}"
        )

        self.logs.add_log(
            "======================================"
        )

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
        Atualiza o texto do Status do Serviço.
        """

        if self.status_label is not None:

            self.status_label.configure(
                text=text
            )

    def clear_logs(self) -> None:
        """
        Limpa o painel de logs.
        """

        if self.logs is not None:

            try:

                self.logs.clear()

            except AttributeError:

                #
                # Caso o LogsPanel ainda não possua
                # o método clear(), apenas ignora.
                #

                pass

    def destroy(self) -> None:
        """
        Finaliza a Dashboard.
        """

        try:

            self.controller.close()

        except Exception:

            pass

        super().destroy()