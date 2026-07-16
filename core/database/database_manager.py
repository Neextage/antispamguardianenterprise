"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: database_manager.py
Descrição...: Gerenciador do banco de dados SQLite.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


class DatabaseManager:
    """
    Responsável pelo gerenciamento
    do banco SQLite do Antispam Guardian Enterprise.
    """

    DATABASE_NAME = "antispam_guardian.db"

    def __init__(self) -> None:

        database_folder = Path("data")

        database_folder.mkdir(
            exist_ok=True
        )

        self.database_path = (
            database_folder /
            self.DATABASE_NAME
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.cursor = self.connection.cursor()

        self._create_tables()
            # ==========================================================
    # Inicialização
    # ==========================================================

    def _create_tables(self) -> None:
        """
        Cria todas as tabelas do banco de dados.
        """

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS email_analysis (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                analysis_date TEXT NOT NULL,

                computer_name TEXT,

                application_version TEXT,

                outlook_account TEXT,

                sender_name TEXT,

                sender_email TEXT,

                subject TEXT,

                spam_score INTEGER,

                is_spam INTEGER,

                is_critical INTEGER,

                moved_to_quarantine INTEGER,

                reasons TEXT

            )
            """
        )

        self.connection.commit()

    # ==========================================================
    # Inserção
    # ==========================================================

    def insert_analysis(
        self,
        *,
        analysis_date: str,
        computer_name: str,
        application_version: str,
        outlook_account: str,
        sender_name: str,
        sender_email: str,
        subject: str,
        spam_score: int,
        is_spam: bool,
        is_critical: bool,
        moved_to_quarantine: bool,
        reasons: str
    ) -> None:
        """
        Registra uma análise no banco.
        """

        self.cursor.execute(
            """
            INSERT INTO email_analysis (

                analysis_date,

                computer_name,

                application_version,

                outlook_account,

                sender_name,

                sender_email,

                subject,

                spam_score,

                is_spam,

                is_critical,

                moved_to_quarantine,

                reasons

            )

            VALUES (

                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?

            )
            """,
            (
                analysis_date,

                computer_name,

                application_version,

                outlook_account,

                sender_name,

                sender_email,

                subject,

                spam_score,

                int(is_spam),

                int(is_critical),

                int(moved_to_quarantine),

                reasons

            )
        )

        self.connection.commit()
            # ==========================================================
    # Consultas
    # ==========================================================

    def get_total_analyses(self) -> int:
        """
        Retorna a quantidade total
        de análises registradas.
        """

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM email_analysis
            """
        )

        result = self.cursor.fetchone()

        return int(result[0])

    def get_total_spam(self) -> int:
        """
        Retorna a quantidade
        de spams detectados.
        """

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM email_analysis
            WHERE is_spam = 1
            """
        )

        result = self.cursor.fetchone()

        return int(result[0])

    def get_total_critical(self) -> int:
        """
        Retorna a quantidade
        de spams críticos.
        """

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM email_analysis
            WHERE is_critical = 1
            """
        )

        result = self.cursor.fetchone()

        return int(result[0])

    def get_total_quarantine(self) -> int:
        """
        Retorna a quantidade de
        mensagens movidas para
        a Quarentena.
        """

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM email_analysis
            WHERE moved_to_quarantine = 1
            """
        )

        result = self.cursor.fetchone()

        return int(result[0])
        # ==========================================================
    # Histórico
    # ==========================================================

    def get_history(
        self,
        limit: int = 100
    ) -> list[tuple]:
        """
        Retorna o histórico das análises
        mais recentes.
        """

        self.cursor.execute(
            """
            SELECT

                analysis_date,

                outlook_account,

                sender_name,

                sender_email,

                subject,

                spam_score,

                is_spam,

                is_critical,

                moved_to_quarantine,

                reasons

            FROM email_analysis

            ORDER BY id DESC

            LIMIT ?
            """,
            (
                limit,
            )
        )

        return self.cursor.fetchall()

    # ==========================================================
    # Manutenção
    # ==========================================================

    def clear_history(self) -> None:
        """
        Remove todo o histórico
        de análises.
        """

        self.cursor.execute(
            """
            DELETE FROM email_analysis
            """
        )

        self.connection.commit()

    # ==========================================================
    # Banco
    # ==========================================================

    def database_exists(self) -> bool:
        """
        Verifica se o banco foi criado.
        """

        return self.database_path.exists()
        # ==========================================================
    # Persistência
    # ==========================================================

    def commit(self) -> None:
        """
        Salva alterações pendentes no banco.
        """

        self.connection.commit()

    # ==========================================================
    # Conexão
    # ==========================================================

    def close(self) -> None:
        """
        Encerra a conexão com o banco de dados.
        """

        try:

            self.connection.close()

        except Exception:

            pass

    # ==========================================================
    # Finalização
    # ==========================================================

    def __del__(self):
        """
        Fecha automaticamente a conexão
        quando o objeto for destruído.
        """

        try:

            self.close()

        except Exception:

            pass