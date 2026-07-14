"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: subject_rule.py
Descrição...: Regra de análise do assunto.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from core.config.scanner_defaults import SUSPICIOUS_WORDS

from core.models.email_model import EmailModel
from core.models.rule_result import RuleResult
from core.models.spam_analysis import SpamAnalysis


class SubjectRule:
    """
    Analisa o assunto do e-mail.
    """

    def analyze(
        self,
        email: EmailModel,
        analysis: SpamAnalysis
    ) -> None:

        subject = email.subject.lower()

        for word, score in SUSPICIOUS_WORDS.items():

            if word in subject:

                analysis.add_rule(

                    RuleResult(

                        rule="SubjectRule",

                        description=f'Assunto contém "{word}"',

                        score=score

                    )

                )