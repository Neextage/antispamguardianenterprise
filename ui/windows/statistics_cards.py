"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: statistics_cards.py
Descrição...: Cards de estatísticas da Dashboard.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from customtkinter import (
    CTkFrame,
    CTkLabel
)

from core.utils.colors import Colors
from core.utils.ui import UI


class StatisticsCards(CTkFrame):
    """Cards de estatísticas da Dashboard."""

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.labels = {}

        self._create_cards()

    def _create_cards(self):

        cards = [
            ("emails", "E-mails\nAnalisados"),
            ("spam", "Spam\nDetectado"),
            ("quarantine", "Quarentena"),
            ("critical", "Spam\nCrítico")
        ]

        for key, title in cards:

            card = CTkFrame(
                self,
                width=170,
                height=100,
                fg_color=Colors.CARD,
                corner_radius=10
            )

            card.pack(
                side="left",
                padx=8
            )

            card.pack_propagate(False)

            CTkLabel(
                card,
                text=title,
                font=(UI.FONT, 13)
            ).pack(
                pady=(15, 5)
            )

            value = CTkLabel(
                card,
                text="0",
                font=(UI.FONT, 28, "bold"),
                text_color=Colors.PRIMARY
            )

            value.pack()

            self.labels[key] = value

    # ==========================================================
    # Atualização dos cards
    # ==========================================================

    def update_statistics(
        self,
        emails: int,
        spam: int,
        quarantine: int,
        critical: int
    ) -> None:

        self.labels["emails"].configure(
            text=str(emails)
        )

        self.labels["spam"].configure(
            text=str(spam)
        )

        self.labels["quarantine"].configure(
            text=str(quarantine)
        )

        self.labels["critical"].configure(
            text=str(critical)
        )