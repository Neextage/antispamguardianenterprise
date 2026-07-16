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

from datetime import datetime
import platform

from core.config.scanner_config import ScannerConfig
from core.database.database_manager import DatabaseManager

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis

from core.outlook.email_manager import EmailManager
from core.outlook.outlook_manager import OutlookManager

from core.quarantine.quarantine_manager import QuarantineManager

from core.scanner.spam_scanner import SpamScanner

from core.utils.constants import Constants


class DashboardController:
    """
    Controller responsável pela comunicação
    entre a Dashboard e toda a camada
    de negócio da aplicação.
    """

    def __init__(self) -> None:
        """
        Inicializa todos os componentes
        utilizados pela Dashboard.
        """

        #
        # Outlook
        #

        self.outlook = OutlookManager()

        self.email_manager = EmailManager()

        #
        # Scanner
        #

        self.scanner = SpamScanner()

        #
        # Quarentena
        #

        self.quarantine = QuarantineManager()

        #
        # Banco SQLite
        #

        self.database = DatabaseManager()

        #
        # Configurações
        #

        self.config = ScannerConfig()
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
        Finaliza a conexão com o Outlook.
        """

        self.outlook.disconnect()

    def is_connected(self) -> bool:
        """
        Verifica se existe conexão ativa.
        """

        return self.outlook.is_connected()

    def initialize(self) -> dict:
        """
        Inicializa a Dashboard.

        Realiza a conexão com o Outlook e
        retorna as informações necessárias
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

    def get_accounts(self) -> list[str]:
        """
        Retorna todas as contas
        disponíveis no Outlook.
        """

        return self.outlook.get_account_names()

    def reload_accounts(self) -> list[str]:
        """
        Atualiza a lista de contas.
        """

        if not self.is_connected():

            if not self.connect():

                return []

        return self.get_accounts()

    def get_inbox(
        self,
        account_name: str
    ):
        """
        Retorna a Caixa de Entrada
        da conta selecionada.
        """

        return self.outlook.get_inbox(
            account_name
        )

    def get_total_messages(
        self,
        account_name: str
    ) -> int:
        """
        Retorna a quantidade de mensagens
        existentes na Caixa de Entrada.
        """

        return self.outlook.get_inbox_message_count(
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
        para um objeto EmailModel.
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

    # ==========================================================
    # Quarentena
    # ==========================================================

    def quarantine_available(
        self,
        account_name: str
    ) -> bool:
        """
        Verifica se a Quarentena está
        disponível para a conta.
        """

        return self.quarantine.is_available(
            account_name
        )
            # ==========================================================
    # Análise da Caixa de Entrada
    # ==========================================================

    def analyze_inbox(
        self,
        account_name: str,
        limit: int | None = None
    ) -> tuple[list[SpamAnalysis], int, list[str]]:
        """
        Analisa os e-mails da Caixa de Entrada.

        Retorna:
            - Lista de análises
            - Quantidade de e-mails enviados
              para a Quarentena
            - Logs da Quarentena
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

        for index in range(
            1,
            total + 1
        ):

            try:

                mail_item = items.Item(
                    index
                )

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
                                #
                # Salva a análise no banco SQLite
                #

                reasons = "\n".join(

                    rule.description

                    for rule in analysis.rules

                )

                self.database.insert_analysis(

                    analysis_date=datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),

                    computer_name=platform.node(),

                    application_version=Constants.VERSION,

                    outlook_account=account_name,

                    sender_name=email.sender_name,

                    sender_email=email.sender_email,

                    subject=email.subject,

                    spam_score=analysis.score,

                    is_spam=analysis.is_spam,

                    is_critical=analysis.is_critical,

                    moved_to_quarantine=(
                        analysis.is_spam
                        and
                        self.config.auto_quarantine_enabled()
                    ),

                    reasons=reasons

                )

                #
                # Quarentena
                #

                if (
                    analysis.is_spam
                    and
                    self.config.auto_quarantine_enabled()
                ):

                    moved = self.quarantine.move_to_quarantine(

                        mail_item,

                        account_name

                    )

                    if moved:

                        quarantine_count += 1

                        quarantine_logs.append(

                            f'Spam movido para Quarentena: "{email.subject}"'

                        )

                        quarantine_logs.append(

                            f"Remetente: {email.sender_email}"

                        )

                elif analysis.is_spam:

                    quarantine_logs.append(

                        "Quarentena automática desabilitada."

                    )

                    quarantine_logs.append(

                        f'Spam detectado: "{email.subject}"'

                    )

            except Exception as error:

                quarantine_logs.append(

                    f"Erro ao analisar mensagem {index}: {error}"

                )

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

        total_emails = len(
            analyses
        )

        spam_count = sum(

            1

            for analysis in analyses

            if analysis.is_spam

        )

        critical_count = sum(

            1

            for analysis in analyses

            if analysis.is_critical

        )

        return {

            "emails": total_emails,

            "spam": spam_count,

            "critical": critical_count,

            #
            # Atualizado posteriormente
            # pelo método start_scan()
            #

            "quarantine": 0

        }

    # ==========================================================
    # Banco de Dados
    # ==========================================================

    def get_database_statistics(
        self
    ) -> dict[str, int]:
        """
        Retorna estatísticas persistidas
        no banco SQLite.
        """

        return {

            "analyses": self.database.get_total_analyses(),

            "spam": self.database.get_total_spam(),

            "critical": self.database.get_total_critical(),

            "quarantine": self.database.get_total_quarantine()

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
            "ANTISPAM GUARDIAN ENTERPRISE"
        )

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

        safe = len(
            analyses
        ) - spam

        logs.append(
            f"E-mails seguros: {safe}"
        )

        logs.append(
            "Análise concluída com sucesso."
        )

        logs.append(
            f"Registros adicionados: {len(analyses)}"
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
        Executa a análise completa da
        Caixa de Entrada.
        """

        #
        # Utiliza o limite configurado
        #

        if limit is None:

            limit = self.config.get_max_emails()

        #
        # Executa Scanner
        #

        analyses, quarantine_count, quarantine_logs = (

            self.analyze_inbox(

                account_name,

                limit

            )

        )

        #
        # Estatísticas
        #

        statistics = self.build_statistics(

            analyses

        )

        statistics["quarantine"] = (

            quarantine_count

        )

        #
        # Logs
        #

        logs = self.build_logs(

            analyses

        )

        logs.append(

            "Resultados gravados no banco SQLite."

        )

        #
        # Logs da Quarentena
        #

        if quarantine_logs:

            logs.append("")

            logs.append(
                "===== QUARENTENA ====="
            )

            logs.extend(

                quarantine_logs

            )

        #
        # Resumo
        #

        if quarantine_count > 0:

            logs.append("")

            logs.append(

                f"{quarantine_count} e-mail(s) movido(s) para a Quarentena."

            )

        else:

            logs.append("")

            logs.append(

                "Nenhum e-mail foi movido para a Quarentena."

            )

        #
        # Resultado
        #

        return {

            "success": True,

            "statistics": statistics,

            "analyses": analyses,

            "logs": logs

        }
            # ==========================================================
    # Dashboard
    # ==========================================================

    def refresh_dashboard(
        self,
        account_name: str
    ) -> dict:
        """
        Atualiza as informações exibidas
        na Dashboard.
        """

        return {

            "connected": self.is_connected(),

            "account": account_name,

            "messages": self.get_total_messages(
                account_name
            ),

            "database": self.get_database_statistics()

        }

    # ==========================================================
    # Utilitários
    # ==========================================================

    def get_configuration(self) -> ScannerConfig:
        """
        Retorna a configuração atual
        do Scanner.
        """

        return self.config

    def get_database(self) -> DatabaseManager:
        """
        Retorna o gerenciador
        do banco SQLite.
        """

        return self.database

    def get_scanner(self) -> SpamScanner:
        """
        Retorna a instância
        do Scanner.
        """

        return self.scanner

    def get_outlook(self) -> OutlookManager:
        """
        Retorna a instância do
        OutlookManager.
        """

        return self.outlook

    def get_email_manager(self) -> EmailManager:
        """
        Retorna o EmailManager.
        """

        return self.email_manager

    def get_quarantine(self) -> QuarantineManager:
        """
        Retorna o gerenciador
        de Quarentena.
        """

        return self.quarantine
        # ==========================================================
    # Estado
    # ==========================================================

    def is_quarantine_enabled(self) -> bool:
        """
        Retorna se a Quarentena
        Automática está habilitada.
        """

        return self.config.auto_quarantine_enabled()

    def get_max_scan_limit(self) -> int:
        """
        Retorna a quantidade máxima
        de e-mails configurada.
        """

        return self.config.get_max_emails()

    def get_spam_score(self) -> int:
        """
        Retorna o score mínimo
        para Spam.
        """

        return self.config.get_spam_score()

    def get_critical_score(self) -> int:
        """
        Retorna o score mínimo
        para Spam Crítico.
        """

        return self.config.get_critical_score()

    # ==========================================================
    # Finalização
    # ==========================================================

    def close(self) -> None:
        """
        Finaliza todos os recursos
        utilizados pelo Controller.
        """

        try:

            self.database.close()

        except Exception:

            pass

        try:

            self.outlook.disconnect()

        except Exception:

            pass

    def __del__(self):
        """
        Garante a liberação dos recursos
        quando o objeto for destruído.
        """

        try:

            self.close()

        except Exception:

            pass
            # ==========================================================
    # Informações
    # ==========================================================

    def get_application_information(self) -> dict:
        """
        Retorna informações da aplicação.
        """

        return {

            "application": "Antispam Guardian Enterprise",

            "version": Constants.VERSION,

            "database": self.database.database_exists(),

            "connected": self.is_connected(),

            "quarantine": self.config.auto_quarantine_enabled()

        }

    def get_runtime_information(self) -> dict:
        """
        Retorna informações da sessão atual.
        """

        return {

            "computer": platform.node(),

            "analysis_date": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

        }

    # ==========================================================
    # Diagnóstico
    # ==========================================================

    def health_check(self) -> dict:
        """
        Executa uma verificação simples
        dos principais componentes.
        """

        return {

            "outlook": self.is_connected(),

            "database": self.database.database_exists(),

            "scanner": self.scanner is not None,

            "email_manager": self.email_manager is not None,

            "quarantine": self.quarantine is not None,

            "configuration": self.config is not None

        }
            # ==========================================================
    # Representação
    # ==========================================================

    def __repr__(self) -> str:
        """
        Representação do objeto.
        """

        return (

            f"{self.__class__.__name__}("

            f"connected={self.is_connected()}, "

            f"accounts={len(self.get_accounts()) if self.is_connected() else 0})"

        )

    def __str__(self) -> str:
        """
        Representação amigável.
        """

        return (

            "DashboardController"

        )