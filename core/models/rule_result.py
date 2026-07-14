"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: rule_result.py
Descrição...: Resultado individual de uma regra.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class RuleResult:
    """
    Representa o resultado de uma regra
    aplicada pelo Scanner.
    """

    rule: str

    description: str

    score: int

    matched: bool = True

    def __str__(self) -> str:

        signal = "+" if self.score >= 0 else ""

        return (
            f"{self.rule}: "
            f"{self.description} "
            f"({signal}{self.score})"
        )