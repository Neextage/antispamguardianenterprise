"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: spam_scanner.py
Descrição...: Scanner principal de spam.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis
from core.scanner.rules_engine import RulesEngine


class SpamScanner:
    """
    Scanner principal responsável pela análise
    dos e-mails utilizando todas as regras
    cadastradas no RulesEngine.
    """

    def __init__(self) -> None:

        self._rules_engine = RulesEngine()

    # ==================================================================
    # Scanner
    # ==================================================================

    def scan(
        self,
        email: EmailModel
    ) -> SpamAnalysis:
        """
        Analisa um único e-mail.
        """

        return self._rules_engine.analyze(email)

    def scan_many(
        self,
        emails: list[EmailModel]
    ) -> list[SpamAnalysis]:
        """
        Analisa uma lista de e-mails.
        """

        results: list[SpamAnalysis] = []

        for email in emails:

            results.append(
                self.scan(email)
            )

        return results

    # ==================================================================
    # Informações
    # ==================================================================

    @property
    def rules_engine(self) -> RulesEngine:
        """
        Retorna a instância do RulesEngine.
        """

        return self._rules_engine