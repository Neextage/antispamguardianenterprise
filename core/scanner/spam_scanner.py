"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: spam_scanner.py
Descrição...: Scanner principal de spam.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis
from core.scanner.rules_engine import RulesEngine


class SpamScanner:
    """
    Scanner principal responsável por analisar
    um e-mail utilizando todos os detectores.
    """

    def __init__(self) -> None:

        self.rules_engine = RulesEngine()

    # ==========================================================
    # Scanner
    # ==========================================================

    def scan(
        self,
        email: EmailModel
    ) -> SpamAnalysis:
        """
        Analisa um e-mail e retorna
        o resultado da análise.
        """

        analysis = self.rules_engine.analyze(
            email
        )

        #
        # Futuramente
        #
        # analysis = self.url_detector.analyze(...)
        # analysis = self.attachment_detector(...)
        # analysis = self.ai_guardian(...)
        #

        return analysis