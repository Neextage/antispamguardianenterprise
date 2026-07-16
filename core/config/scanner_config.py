"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: scanner_config.py
Descrição...: Configurações do Scanner.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path


class ScannerConfig:
    """
    Responsável pelo gerenciamento das
    configurações do Scanner.
    """

    CONFIG_FOLDER = Path("config")

    CONFIG_FILE = CONFIG_FOLDER / "scanner.ini"

    def __init__(self) -> None:

        self.parser = ConfigParser()

        self._load()
            # ==========================================================
    # Inicialização
    # ==========================================================

    def _load(self) -> None:
        """
        Carrega o arquivo de configuração.
        Caso não exista, cria automaticamente.
        """

        self.CONFIG_FOLDER.mkdir(
            exist_ok=True
        )

        if not self.CONFIG_FILE.exists():

            self._create_default()

        self.parser.read(
            self.CONFIG_FILE,
            encoding="utf-8"
        )

    def _create_default(self) -> None:
        """
        Cria o arquivo scanner.ini
        com as configurações padrão.
        """

        self.parser["SCANNER"] = {

            "spam_score": "50",

            "critical_score": "80",

            "max_emails": "100",

            "auto_quarantine": "true"

        }

        self.parser["RULES"] = {

            "sender_rule": "true",

            "subject_rule": "true",

            "body_rule": "true",

            "url_rule": "true",

            "attachment_rule": "true"

        }

        with open(
            self.CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            self.parser.write(
                file
            )
                # ==========================================================
    # Scanner
    # ==========================================================

    def get_spam_score(self) -> int:
        """
        Retorna o score mínimo para
        classificação de Spam.
        """

        return self.parser.getint(
            "SCANNER",
            "spam_score"
        )

    def get_critical_score(self) -> int:
        """
        Retorna o score mínimo para
        Spam Crítico.
        """

        return self.parser.getint(
            "SCANNER",
            "critical_score"
        )

    def get_max_emails(self) -> int:
        """
        Retorna a quantidade máxima
        de e-mails analisados.
        """

        return self.parser.getint(
            "SCANNER",
            "max_emails"
        )

    def auto_quarantine_enabled(self) -> bool:
        """
        Retorna se a Quarentena
        Automática está habilitada.
        """

        return self.parser.getboolean(
            "SCANNER",
            "auto_quarantine"
        )

    # ==========================================================
    # Regras
    # ==========================================================

    def sender_rule_enabled(self) -> bool:

        return self.parser.getboolean(
            "RULES",
            "sender_rule"
        )

    def subject_rule_enabled(self) -> bool:

        return self.parser.getboolean(
            "RULES",
            "subject_rule"
        )

    def body_rule_enabled(self) -> bool:

        return self.parser.getboolean(
            "RULES",
            "body_rule"
        )

    def url_rule_enabled(self) -> bool:

        return self.parser.getboolean(
            "RULES",
            "url_rule"
        )

    def attachment_rule_enabled(self) -> bool:

        return self.parser.getboolean(
            "RULES",
            "attachment_rule"
        )
            # ==========================================================
    # Alteração das Configurações
    # ==========================================================

    def set_spam_score(
        self,
        value: int
    ) -> None:
        """
        Define o score mínimo para Spam.
        """

        self.parser.set(
            "SCANNER",
            "spam_score",
            str(value)
        )

    def set_critical_score(
        self,
        value: int
    ) -> None:
        """
        Define o score mínimo para Spam Crítico.
        """

        self.parser.set(
            "SCANNER",
            "critical_score",
            str(value)
        )

    def set_max_emails(
        self,
        value: int
    ) -> None:
        """
        Define a quantidade máxima
        de e-mails analisados.
        """

        self.parser.set(
            "SCANNER",
            "max_emails",
            str(value)
        )

    def set_auto_quarantine(
        self,
        enabled: bool
    ) -> None:
        """
        Ativa ou desativa
        a Quarentena Automática.
        """

        self.parser.set(
            "SCANNER",
            "auto_quarantine",
            str(enabled).lower()
        )

    # ==========================================================
    # Regras
    # ==========================================================

    def set_sender_rule(
        self,
        enabled: bool
    ) -> None:

        self.parser.set(
            "RULES",
            "sender_rule",
            str(enabled).lower()
        )

    def set_subject_rule(
        self,
        enabled: bool
    ) -> None:

        self.parser.set(
            "RULES",
            "subject_rule",
            str(enabled).lower()
        )

    def set_body_rule(
        self,
        enabled: bool
    ) -> None:

        self.parser.set(
            "RULES",
            "body_rule",
            str(enabled).lower()
        )

    def set_url_rule(
        self,
        enabled: bool
    ) -> None:

        self.parser.set(
            "RULES",
            "url_rule",
            str(enabled).lower()
        )

    def set_attachment_rule(
        self,
        enabled: bool
    ) -> None:

        self.parser.set(
            "RULES",
            "attachment_rule",
            str(enabled).lower()
        )
            # ==========================================================
    # Persistência
    # ==========================================================

    def save(self) -> None:
        """
        Salva as configurações
        no arquivo scanner.ini.
        """

        with open(
            self.CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            self.parser.write(
                file
            )

    def reload(self) -> None:
        """
        Recarrega as configurações
        do arquivo scanner.ini.
        """

        self.parser.read(
            self.CONFIG_FILE,
            encoding="utf-8"
        )

    # ==========================================================
    # Utilitários
    # ==========================================================

    def reset_defaults(self) -> None:
        """
        Restaura todas as configurações
        padrão do Scanner.
        """

        self._create_default()

        self.reload()

    # ==========================================================
    # Informações
    # ==========================================================

    def get_config_path(self) -> Path:
        """
        Retorna o caminho do
        arquivo scanner.ini.
        """

        return self.CONFIG_FILE

    # ==========================================================
    # Finalização
    # ==========================================================

    def __str__(self) -> str:

        return (
            f"ScannerConfig("
            f'file="{self.CONFIG_FILE}")'
        )