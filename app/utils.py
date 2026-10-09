"""
Funcoes Auxiliares
===================
Utilitarios gerais para o bot.
"""

import json
import os
import logging
import re
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def format_money(value: float) -> str:
    """Formata valor em Real."""
    return f"R$ {float(value):.2f}".replace(".", ",")


def read_json(path: str, default: Optional[Dict] = None) -> Dict:
    """Le arquivo JSON com fallback."""
    if default is None:
        default = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.debug(f"Arquivo {path} nao encontrado. Usando default.")
        return default


def write_json(path: str, data: Dict) -> bool:
    """Escreve arquivo JSON."""
    try:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar JSON em {path}: {e}")
        return False


def buscaprox(text: str, cmd: str, ignore_list: list) -> str:
    """Remove comandos do texto."""
    out = text
    for ig in ignore_list:
        out = out.replace(ig, "", 1)
    return out.strip()


def is_valid_bin(bin_value: str) -> bool:
    """Valida se BIN tem formato correto."""
    return bool(re.fullmatch(r"\d{4,6}", bin_value))


def is_valid_value(value_str: str) -> tuple:
    """
    Valida e converte valor em float.
    Retorna (bool, float) - (valido, valor)
    """
    try:
        value = float(value_str.replace(",", "."))
        return True, value
    except ValueError:
        return False, 0.0


def mask_card_number(number: str) -> str:
    """Mascara numero de cartao mostrando apenas ultimos 4 digitos."""
    if len(number) < 4:
        return number
    return f"**** **** **** {number[-4:]}"


def format_card_info(card: Dict) -> str:
    """Formata informacoes do cartao para exibicao."""
    return (
        f"💳 Cartao: {card.get('number', 'N/A')}\n"
        f"📅 Validade: {card.get('expiry', 'N/A')}\n"
        f"🔑 CVV: {card.get('cvv', 'N/A')}\n"
        f"👤 Titular: {card.get('holder_name', 'N/A')}\n"
        f"📄 CPF: {card.get('cpf', 'N/A')}"
    )


def extract_admin_args(text: str) -> list:
    """Extrai argumentos de comando admin."""
    return re.findall(r"[A-Za-z0-9@\.\-_]+", text.lower())


def get_card_emoji(level: str) -> str:
    """Retorna emoji para nivel de cartao."""
    emoji_map = {
        "black": "💎",
        "infinite": "♾️",
        "corporate": "🏢",
        "business": "💼",
        "classic": "📝",
        "platinum": "⭐",
    }
    return emoji_map.get(level.lower(), "💳")