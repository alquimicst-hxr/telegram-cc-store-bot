"""
Configurations Globais do Bot
=============================
Centraliza todas as constantes, tokens e URLs do bot.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# TELEGRAM
# ============================================================
BOT_TOKEN = os.getenv("8843258561:AAE5KjeWx5syJJ3DvPyOX_O0nUrttIytzZU", "")
OWNER_ID = int(os.getenv("OWNER_ID", "7848571699"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@haxorstorecc")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1004292730971")
SUPPORT_URL = os.getenv("SUPPORT_URL", "https://t.me/haxorsuporte")

# ============================================================
# API CHECKER
# ============================================================
CHECKER_URL = os.getenv("CHECKER_URL", "https://jokercchk.squareweb.app/api/check")
CHECKER_GATE = os.getenv("CHECKER_GATE", "haikaz_apizxic")
CHECKER_TOKEN = os.getenv("CHECKER_TOKEN", "8f237e49178645a06678e4dd67e5af0a")

# ============================================================
# BANCO DE DADOS
# ============================================================
DB_PATH = os.getenv("DB_PATH", "store.db")

# ============================================================
# DEPOSITO E CARTAO
# ============================================================
DEPOSIT_MINIMUM = float(os.getenv("DEPOSIT_MINIMUM", "10.0"))
PRAZO_DEVOLUCAO_MINUTOS = int(os.getenv("PRAZO_DEVOLUCAO_MINUTOS", "5"))

# ============================================================
# PIX
# ============================================================
PIX_API_URL = os.getenv("PIX_API_URL", "")
PIX_API_TOKEN = os.getenv("PIX_API_TOKEN", "")

# ============================================================
# NIVEIS DE CARTOES
# ============================================================
CARD_LEVELS = {
    "Black": {"price": 45.00, "stock": 25, "emoji": "💎"},
    "Infinite": {"price": 35.00, "stock": 25, "emoji": "♾️"},
    "Corporate": {"price": 30.00, "stock": 25, "emoji": "🏢"},
    "Business": {"price": 25.00, "stock": 25, "emoji": "💼"},
    "Classic": {"price": 18.00, "stock": 25, "emoji": "📝"},
    "Platinum": {"price": 22.00, "stock": 25, "emoji": "⭐"},
}

# ============================================================
# LOGGING
# ============================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "bot.log"