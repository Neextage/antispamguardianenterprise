from core.config.scanner_config import ScannerConfig

config = ScannerConfig()

print("=" * 60)
print("SCANNER CONFIG")
print("=" * 60)

print("Spam Score:", config.get_spam_score())
print("Critical Score:", config.get_critical_score())
print("Max Emails:", config.get_max_emails())
print("Auto Quarantine:", config.auto_quarantine_enabled())

print("=" * 60)
