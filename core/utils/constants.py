"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: constants.py
Descrição...: Constantes globais da aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from core.version import APP_VERSION


class Constants:
    """Constantes globais da aplicação."""

    APPLICATION_NAME = APP_VERSION.application_name

    VERSION = APP_VERSION.version

    BUILD = APP_VERSION.build

    RELEASE = APP_VERSION.release

    AUTHOR = APP_VERSION.author

    COMPANY = APP_VERSION.company

    PYTHON_VERSION = APP_VERSION.python_version

    COPYRIGHT = "© 2026 Neextage"

    DATABASE_NAME = "antispam_guardian.db"

    QUARANTINE_FOLDER = "Quarentena AntispamGuardian"

    LOG_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

    DATE_FORMAT = "%d/%m/%Y"

    TIME_FORMAT = "%H:%M:%S"