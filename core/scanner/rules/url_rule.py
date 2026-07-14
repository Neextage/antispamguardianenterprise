"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: url_rule.py
Descrição...: Regra de análise de URLs.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from core.models.email_model import EmailModel
from core.models.spam_analysis import SpamAnalysis


class UrlRule:
    """
    Analisa URLs encontradas no e-mail.

    (Implementação inicial)
    """

    def analyze(
        self,
        email: EmailModel,
        analysis: SpamAnalysis
    ) -> None:

        #
        # Implementaremos a análise de URLs
        # nas próximas Sprints.
        #

        return