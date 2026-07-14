"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: outlook_manager.py
Descrição...: Gerenciador de integração com Microsoft Outlook.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from __future__ import annotations

from typing import List

import pythoncom
import win32com.client

from core.models.account_model import AccountModel


class OutlookManager:
    """
    Responsável pela comunicação com o Microsoft Outlook.
    """

    INBOX_FOLDER = 6

    def __init__(self) -> None:

        self._namespace = None
        self._accounts: List[AccountModel] = []

    # ======================================================================
    # Inicialização
    # ======================================================================

    def connect(self) -> bool:
        """
        Conecta ao Microsoft Outlook.
        """

        try:

            pythoncom.CoInitialize()

            application = win32com.client.Dispatch(
                "Outlook.Application"
            )

            self._namespace = application.GetNamespace(
                "MAPI"
            )

            self._load_accounts()

            return True

        except Exception:

            self.disconnect()

            return False

    # ======================================================================
    # Contas
    # ======================================================================

    def _load_accounts(self) -> None:
        """
        Carrega todas as contas configuradas no Outlook.
        """

        self._accounts.clear()

        if self._namespace is None:
            return

        try:

            stores = self._namespace.Stores

            default_store = None

            try:
                default_store = stores.DefaultStore
            except Exception:
                pass

            for store in stores:

                is_default = False

                if default_store is not None:

                    try:
                        is_default = (
                            store.StoreID == default_store.StoreID
                        )

                    except Exception:
                        pass

                account = AccountModel(
                    display_name=str(store.DisplayName).strip(),
                    store=store,
                    is_default=is_default
                )

                self._accounts.append(account)

        except Exception:

            self._accounts.clear()

    def get_accounts(self) -> List[AccountModel]:
        """
        Retorna todas as contas carregadas.
        """

        return list(self._accounts)

    def get_account_names(self) -> List[str]:
        """
        Retorna somente os nomes das contas.
        """

        return [
            account.display_name
            for account in self._accounts
        ]

    def get_account(
        self,
        display_name: str
    ) -> AccountModel | None:
        """
        Localiza uma conta pelo nome.
        """

        for account in self._accounts:

            if account.display_name == display_name:

                return account

        return None

    # ======================================================================
    # Caixa de Entrada
    # ======================================================================

    def get_inbox(
        self,
        display_name: str
    ):
        """
        Retorna a Caixa de Entrada da conta.
        """

        account = self.get_account(
            display_name
        )

        if account is None:

            return None

        try:

            return account.store.GetDefaultFolder(
                self.INBOX_FOLDER
            )

        except Exception:

            return None

    def get_inbox_message_count(
        self,
        display_name: str
    ) -> int:
        """
        Retorna a quantidade de mensagens
        da Caixa de Entrada.
        """

        inbox = self.get_inbox(
            display_name
        )

        if inbox is None:

            return 0

        try:

            return int(
                inbox.Items.Count
            )

        except Exception:

            return 0

    # ======================================================================
    # Estado
    # ======================================================================

    def is_connected(self) -> bool:
        """
        Verifica se existe conexão ativa.
        """

        return self._namespace is not None

    def disconnect(self) -> None:
        """
        Finaliza a conexão.
        """

        self._accounts.clear()

        self._namespace = None

        try:

            pythoncom.CoUninitialize()

        except Exception:

            pass