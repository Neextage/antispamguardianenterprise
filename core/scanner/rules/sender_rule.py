"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: sender_rule.py
Descrição...: Regra de análise do remetente.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from core.config.scanner_defaults import (
    PUBLIC_DOMAINS,
    TRUSTED_DOMAINS
)

from core.models.email_model import EmailModel
from core.models.rule_result import RuleResult
from core.models.spam_analysis import SpamAnalysis


class SenderRule:
    """
    Analisa o domínio do remetente.
    """

    def analyze(
        self,
        email: EmailModel,
        analysis: SpamAnalysis
    ) -> None:

        sender = email.sender_email.lower().strip()

        if "@" not in sender:
            return

        domain = sender.split("@")[-1]

        #
        # Domínio confiável
        #

        if domain in TRUSTED_DOMAINS:

            analysis.add_rule(

                RuleResult(

                    rule="SenderRule",

                    description=f"Domínio confiável ({domain})",

                    score=-20

                )

            )

            return

        #
        # Domínio público
        #

        if domain in PUBLIC_DOMAINS:

            analysis.add_rule(

                RuleResult(

                    rule="SenderRule",

                    description=f"Domínio público ({domain})",

                    score=0

                )

            )

            return

        #
        # Domínio desconhecido
        #

        analysis.add_rule(

            RuleResult(

                rule="SenderRule",

                description=f"Domínio desconhecido ({domain})",

                score=15

            )

        )