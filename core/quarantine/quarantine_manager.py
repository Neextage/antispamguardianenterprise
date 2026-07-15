"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: quarantine_manager.py
Descrição...: Gerenciador da Quarentena de Spam.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

from core.outlook.outlook_manager import OutlookManager


class QuarantineManager:
    """
    Responsável por mover e-mails
    classificados como Spam para
    a pasta de Quarentena.
    """

    QUARANTINE_FOLDER = "Antispam Guardian Quarantine"

    def __init__(self) -> None:

        self.outlook = OutlookManager()

        self.outlook.connect()

    # ==========================================================
    # Quarentena
    # ==========================================================

    def get_quarantine_folder(
        self,
        account_name: str
    ):
        """
        Localiza ou cria a pasta
        de Quarentena.
        """

        inbox = self.outlook.get_inbox(
            account_name
        )

        if inbox is None:

            return None

        parent = inbox.Parent

        #
        # Procura pasta existente
        #

        for folder in parent.Folders:

            if folder.Name == self.QUARANTINE_FOLDER:

                return folder

        #
        # Cria automaticamente
        #

        return parent.Folders.Add(
            self.QUARANTINE_FOLDER
        )
            # ==========================================================
    # Movimentação
    # ==========================================================

    def move_to_quarantine(
        self,
        mail_item,
        account_name: str
    ) -> bool:
        """
        Move um e-mail para a pasta
        de Quarentena.

        Returns
        -------
        bool
            True quando o e-mail foi movido
            com sucesso.
        """

        folder = self.get_quarantine_folder(
            account_name
        )

        if folder is None:

            return False

        try:

            mail_item.Move(
                folder
            )

            return True

        except Exception:

            return False

    # ==========================================================
    # Verificação
    # ==========================================================

    def quarantine_exists(
        self,
        account_name: str
    ) -> bool:
        """
        Verifica se a pasta de Quarentena
        existe para a conta informada.
        """

        inbox = self.outlook.get_inbox(
            account_name
        )

        if inbox is None:

            return False

        parent = inbox.Parent

        for folder in parent.Folders:

            if folder.Name == self.QUARANTINE_FOLDER:

                return True

        return False
        # ==========================================================
    # Informações
    # ==========================================================

    def get_quarantine_name(self) -> str:
        """
        Retorna o nome da pasta de
        Quarentena.
        """

        return self.QUARANTINE_FOLDER

    def ensure_quarantine(
        self,
        account_name: str
    ):
        """
        Garante que a pasta de Quarentena
        exista e retorna sua referência.
        """

        return self.get_quarantine_folder(
            account_name
        )

    # ==========================================================
    # Conexão
    # ==========================================================

    def connect(self) -> bool:
        """
        Garante conexão com o Outlook.
        """

        if self.outlook.is_connected():

            return True

        return self.outlook.connect()

    def disconnect(self) -> None:
        """
        Encerra a conexão com o Outlook.
        """

        if self.outlook.is_connected():

            self.outlook.disconnect()

    # ==========================================================
    # Utilitário
    # ==========================================================

    def __del__(self):
        """
        Libera a conexão automaticamente
        quando o objeto for destruído.
        """

        try:

            self.disconnect()

        except Exception:

            pass
            # ==========================================================
    # Status
    # ==========================================================

    def is_available(
        self,
        account_name: str
    ) -> bool:
        """
        Verifica se a Quarentena está
        disponível para utilização.
        """

        if not self.connect():

            return False

        folder = self.ensure_quarantine(
            account_name
        )

        return folder is not None

    # ==========================================================
    # Informações
    # ==========================================================

    def __str__(self) -> str:
        """
        Representação textual do Manager.
        """

        return (
            f"QuarantineManager("
            f'folder="{self.QUARANTINE_FOLDER}")'
        )