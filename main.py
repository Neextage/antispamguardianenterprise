"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: main.py
===============================================================================
"""

from core.app.application import Application


def main() -> None:

    app = Application()

    try:

        app.start()

    finally:

        app.stop()


if __name__ == "__main__":

    main()