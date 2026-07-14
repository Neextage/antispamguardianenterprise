"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: teste_scanner.py
Descrição...: Teste do Scanner Antispam.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from core.outlook.outlook_manager import OutlookManager
from core.outlook.email_manager import EmailManager
from core.scanner.spam_scanner import SpamScanner


def main():

    outlook = OutlookManager()

    if not outlook.connect():

        print("Não foi possível conectar ao Outlook.")
        return

    accounts = outlook.get_account_names()

    if not accounts:

        print("Nenhuma conta encontrada.")
        return

    account = accounts[0]

    inbox = outlook.get_inbox(account)

    if inbox is None:

        print("Inbox não encontrada.")
        return

    email_manager = EmailManager()

    scanner = SpamScanner()

    items = inbox.Items

    total = min(items.Count, 10)

    print("=" * 80)
    print("ANTISPAM GUARDIAN ENTERPRISE")
    print("=" * 80)
    print(f"Conta: {account}")
    print(f"E-mails analisados: {total}")
    print("=" * 80)

    for index in range(1, total + 1):

        mail = items.Item(index)

        email = email_manager.convert(
            mail,
            account
        )

        analysis = scanner.scan(
            email
        )

        print()

        print("=" * 80)

        print(f"[{index}]")

        print("- Assunto:")
        print(f"  {email.subject}")

        print("- Remetente:")
        print(f"  {email.sender_name}")

        print(f"  <{email.sender_email}>")

        print("- Score:")
        print(f"  {analysis.score}")

        print("- Spam:")
        print(f"  {analysis.is_spam}")

        print("- Crítico:")
        print(f"  {analysis.is_critical}")

        print("- Motivos:")

        if analysis.reasons:

            for reason in analysis.reasons:

                print(f"   • {reason}")

        else:

            print("   Nenhum.")

    print()

    print("=" * 80)
    print("Fim da análise.")
    print("=" * 80)


if __name__ == "__main__":

    main()