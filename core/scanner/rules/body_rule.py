"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: body_rule.py
Descrição...: Regra de análise do corpo do e-mail.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from core.config.scanner_defaults import SUSPICIOUS_WORDS

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis


class BodyRule:
    """
    Analisa o corpo do e-mail.
    """

    def analyze(
        self,
        email: EmailModel,
        analysis: SpamAnalysis
    ) -> None:

        body = email.body.lower()

        for word, score in SUSPICIOUS_WORDS.items():

            if word in body:

                analysis.score += score

                analysis.add_reason(
                    f'Corpo contém "{word}" (+{score})'
                )