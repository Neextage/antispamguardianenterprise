"""
===============================================================================
Projeto.....: Antispam Guardian Enterprise
Arquivo.....: paths.py
Descrição...: Caminhos utilizados pela aplicação.
Autor.......: Neextage
Versão......: 0.1.0
===============================================================================
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ASSETS = ROOT / "assets"

CONFIG = ROOT / "config"

DATA = ROOT / "data"

LOGS = ROOT / "logs"

TEMP = ROOT / "temp"

BACKUPS = ROOT / "backups"

CACHE = ROOT / "cache"

RESOURCES = ROOT / "resources"

DOCS = ROOT / "docs"