"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: dashboard_controller.py
Descrição...: Controller principal da Dashboard.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis

from core.outlook.email_manager import EmailManager
from core.outlook.outlook_manager import OutlookManager

from core.scanner.spam_scanner import SpamScanner


class DashboardController:
    """
    Controller responsável pela comunicação
    entre a Dashboard e o Scanner.
    """

    def __init__(self) -> None:

        self.outlook = OutlookManager()

        self.email_manager = EmailManager()

        self.scanner = SpamScanner()

    # ==========================================================
    # Outlook
    # ==========================================================

    def connect(self) -> bool:
        """
        Conecta ao Microsoft Outlook.
        """

        return self.outlook.connect()

    def disconnect(self) -> None:
        """
        Finaliza a conexão.
        """

        self.outlook.disconnect()

    def is_connected(self) -> bool:
        """
        Verifica se existe conexão ativa.
        """

        return self.outlook.is_connected()

    def get_accounts(self) -> list[str]:
        """
        Retorna os nomes das contas
        disponíveis no Outlook.
        """

        return self.outlook.get_account_names()

    def get_inbox_count(
        self,
        account_name: str
    ) -> int:
        """
        Retorna a quantidade de mensagens
        da Caixa de Entrada.
        """

        return self.outlook.get_inbox_message_count(
            account_name
        )

    def get_inbox(
        self,
        account_name: str
    ):
        """
        Retorna o objeto Inbox da conta.
        """

        return self.outlook.get_inbox(
            account_name
        )
            # ==========================================================
    # Conversão
    # ==========================================================

    def convert_mail(
        self,
        mail_item,
        account_name: str
    ) -> EmailModel:
        """
        Converte um MailItem do Outlook
        em EmailModel.
        """

        return self.email_manager.convert(
            mail_item,
            account_name
        )

    # ==========================================================
    # Scanner
    # ==========================================================

    def analyze_mail(
        self,
        mail_item,
        account_name: str
    ) -> SpamAnalysis:
        """
        Analisa um único e-mail.
        """

        email = self.convert_mail(
            mail_item,
            account_name
        )

        return self.scanner.scan(
            email
        )

    def analyze_inbox(
        self,
        account_name: str,
        limit: int | None = None
    ) -> list[SpamAnalysis]:
        """
        Analisa os e-mails da Caixa de Entrada.

        Parameters
        ----------
        account_name:
            Conta do Outlook.

        limit:
            Limite de mensagens a analisar.
            Quando None, analisa todas.
        """

        inbox = self.get_inbox(
            account_name
        )

        if inbox is None:

            return []

        items = inbox.Items

        total = items.Count

        if limit is not None:

            total = min(
                total,
                limit
            )

        analyses: list[SpamAnalysis] = []

        for index in range(1, total + 1):

            try:

                mail_item = items.Item(index)

                analysis = self.analyze_mail(
                    mail_item,
                    account_name
                )

                analyses.append(
                    analysis
                )

            except Exception:

                #
                # Continua a análise mesmo
                # quando um e-mail falhar.
                #

                continue

        return analyses
        # ==========================================================
    # Estatísticas
    # ==========================================================

    @staticmethod
    def build_statistics(
        analyses: list[SpamAnalysis]
    ) -> dict[str, int]:
        """
        Gera as estatísticas da análise.
        """

        emails = len(analyses)

        spam = sum(
            1
            for analysis in analyses
            if analysis.is_spam
        )

        critical = sum(
            1
            for analysis in analyses
            if analysis.is_critical
        )

        #
        # A quarentena será implementada
        # na Sprint 10.
        #

        quarantine = 0

        return {

            "emails": emails,

            "spam": spam,

            "critical": critical,

            "quarantine": quarantine

        }

    # ==========================================================
    # Logs
    # ==========================================================

    @staticmethod
    def build_logs(
        analyses: list[SpamAnalysis]
    ) -> list[str]:
        """
        Gera as mensagens para o painel
        de logs da Dashboard.
        """

        logs: list[str] = []

        logs.append(
            "======================================"
        )

        logs.append(
            f"E-mails analisados: {len(analyses)}"
        )

        spam = sum(

            1

            for analysis in analyses

            if analysis.is_spam

        )

        critical = sum(

            1

            for analysis in analyses

            if analysis.is_critical

        )

        logs.append(
            f"Spam detectado: {spam}"
        )

        logs.append(
            f"Spam crítico: {critical}"
        )

        logs.append(
            "======================================"
        )

        return logs
        # ==========================================================
    # Execução
    # ==========================================================

    def start_scan(
        self,
        account_name: str,
        limit: int | None = None
    ) -> dict:
        """
        Executa a análise completa da Caixa de Entrada.

        Retorna um dicionário contendo as
        estatísticas e os logs da análise.
        """

        analyses = self.analyze_inbox(
            account_name,
            limit
        )

        statistics = self.build_statistics(
            analyses
        )

        logs = self.build_logs(
            analyses
        )

        return {

            "success": True,

            "analyses": analyses,

            "statistics": statistics,

            "logs": logs

        }

    # ==========================================================
    # Dashboard
    # ==========================================================

    def initialize(self) -> dict:
        """
        Inicializa a Dashboard.

        Retorna as informações necessárias
        para carregar a interface.
        """

        if not self.connect():

            return {

                "success": False,

                "accounts": [],

                "status": "🔴 Outlook não encontrado"

            }

        accounts = self.get_accounts()

        return {

            "success": True,

            "accounts": accounts,

            "status": "🟢 Outlook conectado"

        }
            # ==========================================================
    # Utilitários
    # ==========================================================

    def get_total_messages(
        self,
        account_name: str
    ) -> int:
        """
        Retorna a quantidade de mensagens
        da Caixa de Entrada.
        """

        return self.get_inbox_count(
            account_name
        )

    def reload_accounts(self) -> list[str]:
        """
        Atualiza a lista de contas do Outlook.
        """

        if not self.is_connected():

            if not self.connect():

                return []

        return self.get_accounts()

    def close(self) -> None:
        """
        Encerra a conexão com o Outlook.
        """

        try:

            self.disconnect()

        except Exception:

            pass