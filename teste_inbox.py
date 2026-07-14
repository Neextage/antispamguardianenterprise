import pythoncom
import win32com.client

pythoncom.CoInitialize()

outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")

print("=" * 60)

for store in namespace.Stores:

    print(f"Store: {store.DisplayName}")

    try:
        inbox = store.GetDefaultFolder(6)

        print("Inbox:", inbox.Name)
        print("Mensagens:", inbox.Items.Count)

    except Exception as e:
        print("Erro:", e)

    print("-" * 60)

pythoncom.CoUninitialize()