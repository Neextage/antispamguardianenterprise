"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: attachment_rule.py
Descrição...: Regra de análise de anexos.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis


class AttachmentRule:
    """
    Analisa anexos do e-mail.

    (Implementação inicial)
    """

    def analyze(
        self,
        email: EmailModel,
        analysis: SpamAnalysis
    ) -> None:

        #
        # Implementaremos esta regra
        # nas próximas Sprints.
        #

        return