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
from core.quarantine.quarantine_manager import QuarantineManager
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

        #
        # Quarentena
        #

        self.quarantine = QuarantineManager()

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
    ) -> tuple[list[SpamAnalysis], int, list[str]]:
        """
        Analisa a Caixa de Entrada.

        Retorna:
            análises,
            quantidade movida,
            logs da quarentena.
        """

        inbox = self.get_inbox(
            account_name
        )

        if inbox is None:

            return [], 0, []

        items = inbox.Items

        total = items.Count

        if limit is not None:

            total = min(
                total,
                limit
            )

        analyses: list[SpamAnalysis] = []

        quarantine_logs: list[str] = []

        quarantine_count = 0

        for index in range(1, total + 1):

            try:

                mail_item = items.Item(index)

                email = self.convert_mail(
                    mail_item,
                    account_name
                )

                analysis = self.scanner.scan(
                    email
                )

                analyses.append(
                    analysis
                )

                if analysis.is_spam:

                    moved = self.quarantine.move_to_quarantine(

                        mail_item,

                        account_name

                    )

                    if moved:

                        quarantine_count += 1

                        quarantine_logs.append(
                            f'Spam movido: "{email.subject}"'
                        )

                        quarantine_logs.append(
                            f"Remetente: {email.sender_email}"
                        )

            except Exception:

                continue

        return (

            analyses,

            quarantine_count,

            quarantine_logs

        )
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

        return {

            "emails": emails,

            "spam": spam,

            "critical": critical,

            #
            # Será atualizado
            # pelo start_scan()
            #

            "quarantine": 0

        }

    # ==========================================================
    # Logs
    # ==========================================================

    @staticmethod
    def build_logs(
        analyses: list[SpamAnalysis]
    ) -> list[str]:
        """
        Gera os logs da análise.
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
            "Análise concluída com sucesso."
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
        Executa a análise completa da Caixa
        de Entrada.

        Retorna os resultados para a Dashboard.
        """

        analyses, quarantine_count, quarantine_logs = (
            self.analyze_inbox(
              account_name,
              limit
            )
        )

        statistics = self.build_statistics(
            analyses
        )

        #
        # Atualiza quantidade da quarentena
        #

        statistics["quarantine"] = quarantine_count

        logs = self.build_logs(
            analyses
        )
                #
        # Logs da Quarentena
        #

        logs.extend(
            quarantine_logs
        )

        if quarantine_count > 0:

            logs.append(
                f"{quarantine_count} e-mail(s) movido(s) para a Quarentena."
            )

        else:

            logs.append(
                "Nenhum e-mail foi movido para a Quarentena."
            )

        return {

            "success": True,

            "statistics": statistics,

            "analyses": analyses,

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

    # ==========================================================
    # Finalização
    # ==========================================================

    def close(self) -> None:
        """
        Encerra a conexão com o Outlook.
        """

        try:

            self.disconnect()

        except Exception:

            pass