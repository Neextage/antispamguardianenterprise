"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: main_window.py
Descrição...: Dashboard principal da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

import customtkinter as ctk

from core.utils.colors import Colors
from core.utils.constants import Constants
from core.utils.ui import UI


class MainWindow(ctk.CTk):
    """Dashboard principal."""

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.title(Constants.APPLICATION_NAME)

        self.geometry(
            f"{UI.WINDOW_WIDTH}x{UI.WINDOW_HEIGHT}"
        )

        self.minsize(
            UI.MIN_WIDTH,
            UI.MIN_HEIGHT
        )

        self.configure(
            fg_color=Colors.BACKGROUND
        )

        self._center()

        self._build_layout()

    def _center(self) -> None:

        self.update_idletasks()

        x = (self.winfo_screenwidth() // 2) - (UI.WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (UI.WINDOW_HEIGHT // 2)

        self.geometry(
            f"{UI.WINDOW_WIDTH}x{UI.WINDOW_HEIGHT}+{x}+{y}"
        )

    def _build_layout(self) -> None:

        # ==========================================================
        # SIDEBAR
        # ==========================================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=210,
            fg_color=Colors.SIDEBAR,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            self.sidebar,
            text="🛡",
            font=(UI.FONT, 34)
        ).pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            self.sidebar,
            text="Antispam\nGuardian",
            font=(UI.FONT, 18, "bold"),
            text_color="white",
            justify="center"
        ).pack(
            pady=(0, 25)
        )

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

            ctk.CTkButton(
                self.sidebar,
                text=item,
                height=40,
                fg_color="transparent",
                hover_color="#0D47A1",
                anchor="w"
            ).pack(
                fill="x",
                padx=10,
                pady=3
            )

        # ==========================================================
        # CONTEÚDO
        # ==========================================================

        self.content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.content.pack(
            expand=True,
            fill="both",
            padx=25,
            pady=20
        )

        ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=(UI.FONT, 28, "bold"),
            text_color=Colors.TEXT
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            self.content,
            text=f"Versão {Constants.VERSION}  •  Build {Constants.BUILD}",
            font=(UI.FONT, 12),
            text_color=Colors.SUBTEXT
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # ==========================================================
        # STATUS
        # ==========================================================

        status = ctk.CTkFrame(
            self.content,
            fg_color=Colors.CARD,
            corner_radius=10
        )

        status.pack(
            fill="x",
            pady=(0, 15)
        )

        ctk.CTkLabel(
            status,
            text="Status do Serviço",
            font=(UI.FONT, 15, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 2)
        )

        ctk.CTkLabel(
            status,
            text="🟢 Em desenvolvimento",
            font=(UI.FONT, 14)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        # ==========================================================
        # LOGS
        # ==========================================================

        logs = ctk.CTkTextbox(
            self.content,
            height=260
        )

        logs.pack(
            expand=True,
            fill="both"
        )

        logs.insert(
            "end",
            "Antispam Guardian Enterprise iniciado.\n\n"
            "Dashboard criada com sucesso.\n\n"
            "Aguardando integração dos módulos..."
        )

        logs.configure(
            state="disabled"
        )