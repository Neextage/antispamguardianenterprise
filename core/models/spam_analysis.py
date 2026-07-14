"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: spam_analysis.py
Descrição...: Resultado da análise de spam.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.models.rule_result import RuleResult


@dataclass(slots=True)
class SpamAnalysis:
    """
    Representa o resultado completo da
    análise de um e-mail.
    """

    #
    # Resultado
    #

    score: int = 0

    is_spam: bool = False

    is_critical: bool = False

    #
    # Compatibilidade
    #

    reasons: list[str] = field(
        default_factory=list
    )

    #
    # Resultado detalhado
    #

    rules: list[RuleResult] = field(
        default_factory=list
    )

    # ==========================================================
    # Métodos
    # ==========================================================

    def add_reason(self, reason: str) -> None:
        """
        Mantido por compatibilidade.
        """

        self.reasons.append(reason)

    def add_rule(
        self,
        rule: RuleResult
    ) -> None:
        """
        Adiciona o resultado de uma regra.
        """

        self.rules.append(rule)

        self.score += rule.score

        self.reasons.append(
            rule.description
        )

    @property
    def total_rules(self) -> int:

        return len(self.rules)

    def __str__(self) -> str:

        return (
            f"Score={self.score} | "
            f"Spam={self.is_spam}"
        )