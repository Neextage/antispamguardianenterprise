"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: outlook_panel.py
Descrição...: Painel de informações do Outlook.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

import platform

from customtkinter import (
    CTkCheckBox,
    CTkComboBox,
    CTkEntry,
    CTkFrame,
    CTkLabel
)

from core.utils.colors import Colors
from core.utils.ui import UI


class OutlookPanel(CTkFrame):
    """Painel de seleção da conta Outlook."""

    def __init__(self, master):

        super().__init__(
            master,
            fg_color=Colors.CARD,
            corner_radius=10
        )

        #
        # Callback da Dashboard
        #

        self.on_account_changed = None

        self._create_widgets()

    def _create_widgets(self):

        #
        # Conta Outlook
        #

        CTkLabel(
            self,
            text="Conta Outlook",
            font=(UI.FONT, 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.combo_accounts = CTkComboBox(
            self,
            values=[
                "Carregando contas..."
            ],
            width=350,
            command=self._on_account_changed
        )

        self.combo_accounts.pack(
            anchor="w",
            padx=20
        )

        #
        # Checkbox
        #

        self.check_all_accounts = CTkCheckBox(
            self,
            text="Analisar todas as contas do Outlook",
            command=self._on_toggle_all_accounts
        )

        self.check_all_accounts.pack(
            anchor="w",
            padx=20,
            pady=(10, 0)
        )

        #
        # Nome da máquina
        #

        CTkLabel(
            self,
            text="Nome da Máquina",
            font=(UI.FONT, 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.entry_machine = CTkEntry(
            self,
            width=350
        )

        self.entry_machine.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        self.entry_machine.insert(
            0,
            platform.node()
        )

    # ==========================================================
    # Eventos
    # ==========================================================

    def _on_account_changed(self, value: str):

        if callable(self.on_account_changed):

            self.on_account_changed()

    def _on_toggle_all_accounts(self):

        if self.check_all_accounts.get():

            self.combo_accounts.configure(
                state="disabled"
            )

        else:

            self.combo_accounts.configure(
                state="normal"
            )

        if callable(self.on_account_changed):

            self.on_account_changed()

    # ==========================================================
    # Métodos públicos
    # ==========================================================

    def set_accounts(self, accounts: list[str]):

        if not accounts:

            accounts = [
                "Nenhuma conta encontrada"
            ]

        self.combo_accounts.configure(
            values=accounts
        )

        self.combo_accounts.set(
            accounts[0]
        )

    def analyze_all_accounts(self) -> bool:

        return bool(
            self.check_all_accounts.get()
        )

    def get_selected_account(self) -> str:

        return self.combo_accounts.get()

    def get_machine_name(self) -> str:

        return self.entry_machine.get()