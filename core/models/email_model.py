"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: email_model.py
Descrição...: Modelo de dados de um e-mail.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class EmailModel:
    """
    Representa um e-mail lido pelo Outlook.

    Esta classe desacopla toda a aplicação da API COM
    do Microsoft Outlook. Todas as demais camadas
    (Scanner, Dashboard, Banco de Dados, Quarentena e IA)
    trabalham exclusivamente com este modelo.
    """

    # ==========================================================
    # Identificação
    # ==========================================================

    entry_id: str = ""
    conversation_id: str = ""

    # ==========================================================
    # Remetente / Destinatários
    # ==========================================================

    sender_name: str = ""
    sender_email: str = ""

    to: str = ""
    cc: str = ""
    bcc: str = ""

    # ==========================================================
    # Conteúdo
    # ==========================================================

    subject: str = ""
    body: str = ""
    html_body: str = ""

    # ==========================================================
    # Datas
    # ==========================================================

    received_time: datetime | None = None

    # ==========================================================
    # Outlook
    # ==========================================================

    account: str = ""
    folder: str = ""

    # ==========================================================
    # Anexos
    # ==========================================================

    attachments: list[str] = field(default_factory=list)

    # Quantidade de anexos
    attachment_count: int = 0

    # ==========================================================
    # Links encontrados
    # ==========================================================

    urls: list[str] = field(default_factory=list)

    # ==========================================================
    # Estatísticas
    # ==========================================================

    # Tamanho aproximado do e-mail (bytes)
    size: int = 0

    # ==========================================================
    # Resultado do Scanner
    # ==========================================================

    spam_score: int = 0

    is_spam: bool = False

    is_quarantined: bool = False

    # ==========================================================
    # Métodos utilitários
    # ==========================================================

    def has_attachments(self) -> bool:
        """
        Retorna True quando o e-mail possui anexos.
        """

        return self.attachment_count > 0

    def has_urls(self) -> bool:
        """
        Retorna True quando o e-mail possui URLs.
        """

        return len(self.urls) > 0

    def add_attachment(self, filename: str) -> None:
        """
        Adiciona um anexo ao modelo.
        """

        self.attachments.append(filename)
        self.attachment_count = len(self.attachments)

    def add_url(self, url: str) -> None:
        """
        Adiciona uma URL encontrada.
        """

        self.urls.append(url)

    def __str__(self) -> str:

        return (
            f"{self.sender_email} -> "
            f"{self.subject}"
        )