"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: scanner_rules.py
Descrição...: Regras padrão do Scanner Antispam.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

#
# Palavras suspeitas
#

SUSPICIOUS_WORDS = {

    "pix": 20,

    "urgente": 15,

    "promoção": 15,

    "promoção!": 15,

    "bitcoin": 20,

    "criptomoeda": 20,

    "ganhe dinheiro": 30,

    "clique aqui": 25,

    "confirme sua conta": 30,

    "senha": 10

}

#
# Domínios confiáveis
#

TRUSTED_DOMAINS = {

    "microsoft.com",

    "google.com",

    "office.com",

    "outlook.com",

    "hotmail.com",

    "admgto.com.br",

    "locaweb.com.br"

}

#
# Domínios públicos
#

PUBLIC_DOMAINS = {

    "gmail.com",

    "live.com",

    "icloud.com",

    "yahoo.com",

    "terra.com.br",

    "uol.com.br",

    "bol.com.br",

    "proton.me",

    "protonmail.com"

}

#
# Extensões bloqueadas
#

BLOCKED_EXTENSIONS = {

    ".exe",

    ".bat",

    ".cmd",

    ".scr",

    ".vbs",

    ".ps1"

}