"""
Teste do EmailManager.
"""

from core.outlook.outlook_manager import OutlookManager
from core.outlook.email_manager import EmailManager


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

    print("=" * 70)
    print("Conta:", account)
    print("=" * 70)

    inbox = outlook.get_inbox(account)

    if inbox is None:

        print("Inbox não encontrada.")
        return

    manager = EmailManager()

    items = inbox.Items

    total = min(items.Count, 10)

    print(f"{total} e-mails encontrados.\n")

    for index in range(1, total + 1):

        mail = items.Item(index)

        email = manager.convert(
            mail,
            account
        )

        print(f"[{index}]")
        print("Assunto :", email.subject)
        print("Remetente:", email.sender_name)
        print("Email    :", email.sender_email)
        print("Data     :", email.received_time)
        print("-" * 70)


if __name__ == "__main__":

    main()