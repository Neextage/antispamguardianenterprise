"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: logs_panel.py
Descrição...: Painel de logs da Dashboard.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from datetime import datetime

from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkTextbox
)

from core.utils.colors import Colors
from core.utils.ui import UI


class LogsPanel(CTkFrame):
    """Painel responsável pela exibição dos logs."""

    def __init__(self, master):

        super().__init__(
            master,
            fg_color=Colors.CARD,
            corner_radius=10
        )

        self._create_widgets()

    def _create_widgets(self):

        CTkLabel(
            self,
            text="Logs do Dia",
            font=(UI.FONT, 16, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        self.textbox = CTkTextbox(
            self,
            height=260
        )

        self.textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.clear()

    # ==========================================================
    # Métodos Públicos
    # ==========================================================

    def add_log(self, message: str) -> None:
        """
        Adiciona uma nova mensagem ao painel.
        """

        now = datetime.now().strftime("%H:%M:%S")

        self.textbox.configure(state="normal")

        self.textbox.insert(
            "end",
            f"[{now}] {message}\n"
        )

        self.textbox.see("end")

        self.textbox.configure(state="disabled")

    def clear(self) -> None:
        """
        Limpa o painel.
        """

        self.textbox.configure(state="normal")

        self.textbox.delete(
            "1.0",
            "end"
        )

        self.textbox.configure(state="disabled")