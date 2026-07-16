"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: rules_engine.py
Descrição...: Motor de regras para pontuação de spam.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

from core.config.scanner_config import ScannerConfig

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis

from core.scanner.rules.sender_rule import SenderRule
from core.scanner.rules.subject_rule import SubjectRule
from core.scanner.rules.body_rule import BodyRule
from core.scanner.rules.url_rule import UrlRule
from core.scanner.rules.attachment_rule import AttachmentRule


class RulesEngine:
    """
    Executa todas as regras cadastradas
    para análise de spam.
    """

    def __init__(self) -> None:
        """
        Inicializa o motor de regras.
        """

        #
        # Configurações
        #

        self.config = ScannerConfig()

        #
        # Lista de regras
        #

        self.rules = []

        #
        # Sender
        #

        if self.config.sender_rule_enabled():

            self.rules.append(
                SenderRule()
            )

        #
        # Subject
        #

        if self.config.subject_rule_enabled():

            self.rules.append(
                SubjectRule()
            )

        #
        # Body
        #

        if self.config.body_rule_enabled():

            self.rules.append(
                BodyRule()
            )

        #
        # URL
        #

        if self.config.url_rule_enabled():

            self.rules.append(
                UrlRule()
            )

        #
        # Attachment
        #

        if self.config.attachment_rule_enabled():

            self.rules.append(
                AttachmentRule()
            )

    # ==========================================================
    # Scanner
    # ==========================================================

    def analyze(
        self,
        email: EmailModel
    ) -> SpamAnalysis:
        """
        Executa todas as regras
        sobre um e-mail.
        """

        analysis = SpamAnalysis()

        #
        # Executa regras
        #

        for rule in self.rules:

            rule.analyze(
                email,
                analysis
            )

        #
        # Resultado
        #

        analysis.is_spam = (
            analysis.score >=
            self.config.get_spam_score()
        )

        analysis.is_critical = (
            analysis.score >=
            self.config.get_critical_score()
        )

        return analysis