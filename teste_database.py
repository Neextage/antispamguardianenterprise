"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: teste_database.py
Descrição...: Teste do banco SQLite.
Autor.......: Neextage
Versão......: 0.2.0
===============================================================================
"""

from core.database.database_manager import DatabaseManager


def main():

    database = DatabaseManager()

    print("=" * 80)
    print("ANTISPAM GUARDIAN ENTERPRISE")
    print("Teste do Banco SQLite")
    print("=" * 80)

    print()

    print(
        f"Banco criado: {database.database_exists()}"
    )

    print()

    print(
        f"Total de análises: {database.get_total_analyses()}"
    )

    print(
        f"Spam detectado: {database.get_total_spam()}"
    )

    print(
        f"Spam crítico: {database.get_total_critical()}"
    )

    print(
        f"Quarentena: {database.get_total_quarantine()}"
    )

    print()

    print("=" * 80)

    history = database.get_history()

    print(
        f"Histórico retornado: {len(history)} registro(s)"
    )

    print("=" * 80)

    database.close()


if __name__ == "__main__":

    main()