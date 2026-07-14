"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: email_manager.py
Descrição...: Conversão de objetos Outlook para EmailModel.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from core.models.email_model import EmailModel


class EmailManager:
    """
    Responsável por converter objetos do Outlook
    em objetos EmailModel.
    """

    def convert(self, mail_item, account_name: str = "") -> EmailModel:
        """
        Converte um MailItem do Outlook em EmailModel.
        """

        email = EmailModel()

        #
        # Identificação
        #

        email.entry_id = self._safe_get(
            mail_item,
            "EntryID"
        )

        email.conversation_id = self._safe_get(
            mail_item,
            "ConversationID"
        )

        #
        # Pessoas
        #

        email.sender_name = self._safe_get(
            mail_item,
            "SenderName"
        )

        email.sender_email = self._safe_get(
            mail_item,
            "SenderEmailAddress"
        )

        email.to = self._safe_get(
            mail_item,
            "To"
        )

        email.cc = self._safe_get(
            mail_item,
            "CC"
        )

        email.bcc = self._safe_get(
            mail_item,
            "BCC"
        )

        #
        # Conteúdo
        #

        email.subject = self._safe_get(
            mail_item,
            "Subject"
        )

        email.body = self._safe_get(
            mail_item,
            "Body"
        )

        email.html_body = self._safe_get(
            mail_item,
            "HTMLBody"
        )

        #
        # Data
        #

        email.received_time = self._safe_get(
            mail_item,
            "ReceivedTime"
        )

        #
        # Outlook
        #

        email.account = account_name

        return email

    # ==========================================================
    # Utilitário
    # ==========================================================

    @staticmethod
    def _safe_get(obj, attribute, default=""):
        """
        Obtém um atributo do Outlook de forma segura.
        """

        try:
            return getattr(obj, attribute)

        except Exception:
            return default