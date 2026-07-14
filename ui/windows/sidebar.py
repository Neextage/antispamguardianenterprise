"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: sidebar.py
Descrição...: Menu lateral da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from customtkinter import CTkButton, CTkFrame, CTkLabel

from core.utils.colors import Colors
from core.utils.ui import UI


class Sidebar(CTkFrame):
    """Menu lateral da aplicação."""

    def __init__(self, master):

        super().__init__(
            master,
            width=220,
            fg_color=Colors.SIDEBAR,
            corner_radius=0
        )

        self.pack_propagate(False)

        self._create_widgets()

    def _create_widgets(self):

        CTkLabel(
            self,
            text="🛡",
            font=(UI.FONT, 34)
        ).pack(
            pady=(30, 5)
        )

        CTkLabel(
            self,
            text="Antispam\nGuardian",
            font=(UI.FONT, 19, "bold"),
            text_color="white",
            justify="center"
        ).pack(
            pady=(0, 30)
        )

        self.buttons = {}

        menu = [
            "Dashboard",
            "Outlook",
            "Quarentena",
            "IA Guardian",
            "SMTP",
            "Blacklist",
            "Whitelist",
            "Logs",
            "Configurações"
        ]

        for item in menu:

            button = CTkButton(
                self,
                text=item,
                height=40,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#0D47A1",
                anchor="w"
            )

            button.pack(
                fill="x",
                padx=10,
                pady=3
            )

            self.buttons[item] = button

        CTkLabel(
            self,
            text="Versão 0.1.0",
            text_color="white",
            font=(UI.FONT, 11)
        ).pack(
            side="bottom",
            pady=15
        )