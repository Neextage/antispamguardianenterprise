"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: splash_window.py
Descrição...: Splash Screen da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

import customtkinter as ctk

from core.utils.colors import Colors
from core.utils.constants import Constants
from core.utils.ui import UI


class SplashWindow(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")

        self.title(Constants.APPLICATION_NAME)

        self.geometry(
            f"{UI.SPLASH_WIDTH}x{UI.SPLASH_HEIGHT}"
        )

        self.resizable(False, False)

        self.configure(
            fg_color=Colors.BACKGROUND
        )

        self._center()

        self._create_widgets()

    def _center(self) -> None:

        self.update_idletasks()

        width = UI.SPLASH_WIDTH
        height = UI.SPLASH_HEIGHT

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self) -> None:

        ctk.CTkLabel(
            self,
            text="🛡",
            font=(UI.FONT, 48)
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self,
            text=Constants.APPLICATION_NAME,
            font=(UI.FONT, UI.FONT_TITLE, "bold"),
            text_color=Colors.TEXT
        ).pack()

        ctk.CTkLabel(
            self,
            text="Inicializando aplicação...",
            font=(UI.FONT, UI.FONT_NORMAL),
            text_color=Colors.SUBTEXT
        ).pack(pady=(10, 15))

        self.progress = ctk.CTkProgressBar(
            self,
            width=350
        )

        self.progress.pack()

        self.progress.set(0)

        ctk.CTkLabel(
            self,
            text=f"Versão {Constants.VERSION}  •  Build {Constants.BUILD}",
            font=(UI.FONT, UI.FONT_SMALL),
            text_color=Colors.SUBTEXT
        ).pack(side="bottom", pady=15)

    def start(self) -> None:

        self._animate()

        self.mainloop()

    def _animate(self) -> None:

        value = self.progress.get()

        if value >= 1:

            self.destroy()

            return

        self.progress.set(value + 0.02)

        self.after(25, self._animate)