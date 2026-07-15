"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: email_manager.py
Descrição...: Conversão de objetos Outlook para EmailModel.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

import re

from core.models.email_model import EmailModel


class EmailManager:
    """
    Responsável por converter objetos do Outlook
    em objetos EmailModel.
    """

    URL_PATTERN = re.compile(
        r"https?://[^\s<>\"']+",
        re.IGNORECASE
    )

    # ==========================================================
    # Conversão
    # ==========================================================

    def convert(
        self,
        mail_item,
        account_name: str = ""
    ) -> EmailModel:
        """
        Converte um MailItem do Outlook
        para EmailModel.
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

        #
        # Tamanho
        #

        email.size = self._safe_get(
            mail_item,
            "Size",
            0
        )

        #
        # Anexos
        #

        self._load_attachments(
            mail_item,
            email
        )

        #
        # URLs
        #

        self._load_urls(
            email
        )

        return email

    # ==========================================================
    # Anexos
    # ==========================================================

    def _load_attachments(
        self,
        mail_item,
        email: EmailModel
    ) -> None:
        """
        Carrega os anexos do e-mail.
        """

        try:

            attachments = mail_item.Attachments

            for index in range(
                1,
                attachments.Count + 1
            ):

                attachment = attachments.Item(index)

                email.add_attachment(
                    attachment.FileName
                )

        except Exception:

            pass

    # ==========================================================
    # URLs
    # ==========================================================

    def _load_urls(
        self,
        email: EmailModel
    ) -> None:
        """
        Procura URLs no corpo do e-mail.
        """

        text = (
            email.body
            + "\n"
            + email.html_body
        )

        for url in self.URL_PATTERN.findall(text):

            email.add_url(url)

    # ==========================================================
    # Utilitário
    # ==========================================================

    @staticmethod
    def _safe_get(
        obj,
        attribute,
        default=""
    ):
        """
        Obtém um atributo do Outlook
        de forma segura.
        """

        try:

            return getattr(
                obj,
                attribute
            )

        except Exception:

            return default