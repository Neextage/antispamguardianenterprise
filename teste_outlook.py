from core.outlook.outlook_manager import OutlookManager

manager = OutlookManager()

if manager.connect():

    account = manager.get_account_names()[0]

    print("Conta:", account)

    print(
        "Mensagens:",
        manager.get_inbox_message_count(account)
    )

else:

    print("Falha.")