"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: main.py
Descrição...: Ponto de entrada da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from core.app.application import Application


def main() -> None:
    """
    Ponto de entrada da aplicação.
    """
    app = Application()

    try:
        app.start()

        input("\nPressione ENTER para encerrar...")

    except KeyboardInterrupt:
        print("\nInterrupção solicitada pelo usuário.")

    finally:
        app.stop()


if __name__ == "__main__":
    main()