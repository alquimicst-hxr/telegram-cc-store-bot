"""
Gerenciamento de Banco de Dados SQLite
========================================
Classe DatabaseManager para operacoes com usuarios, cartoes e transacoes.
"""

import sqlite3
import random
import logging
from typing import Dict, List, Optional

from app.config import DB_PATH, CARD_LEVELS

logger = logging.getLogger(__name__)


def luhn_checksum(number: str) -> str:
    """Calcula checksum Luhn para validacao de cartao."""
    digits = [int(d) for d in number]
    for i in range(len(digits) - 1, -1, -1):
        if i % 2 == len(digits) % 2:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
    total = sum(digits)
    return str((10 - (total % 10)) % 10)


def generate_luhn_number(prefix: str, length: int = 16) -> str:
    """Gera numero de cartao com checksum Luhn."""
    raw = prefix + "".join(str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1))
    return raw + luhn_checksum(raw)


def random_name() -> str:
    """Gera nome aleatorio para titular do cartao."""
    nomes = [
        "Ana Beatriz", "Pedro Henrique", "Camila Souza", "Rafael Costa", "Julia Martins",
        "Thiago Almeida", "Larissa Santos", "Mateus Lima", "Isabela Rocha", "Lucas Pereira",
        "Gabriela Nunes", "Daniel Ferreira", "Marina Oliveira", "Bruno Carvalho", "Fernanda Gomes",
    ]
    return random.choice(nomes)


def random_cpf() -> str:
    """Gera CPF valido aleatoriamente."""
    n = [str(random.randint(0, 9)) for _ in range(9)]
    cpf = "".join(n)
    for _ in range(2):
        total = 0
        peso = len(cpf) + 1
        for d in cpf:
            total += int(d) * peso
            peso -= 1
        resto = total % 11
        d = 0 if resto < 2 else 11 - resto
        cpf += str(d)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def random_expiry() -> str:
    """Gera validade aleatoria de cartao."""
    month = random.randint(1, 12)
    year = random.randint(26, 35)
    return f"{month:02d}/{year:02d}"


def random_cvv() -> str:
    """Gera CVV aleatorio."""
    return str(random.randint(100, 999))


def generate_credit_card(level: str) -> Dict[str, str]:
    """Gera cartao de credito simulado com dados aleatorios."""
    prefix_map = {
        "Black": ["5169", "5281", "5290", "5330"],
        "Infinite": ["5234", "5410", "5523", "5587"],
        "Corporate": ["6011", "4024", "4557", "4916"],
        "Business": ["6011", "5236", "5110", "4557"],
        "Classic": ["4532", "4916", "4557", "4024"],
        "Platinum": ["4916", "5169", "5390", "6011"],
    }
    prefix = random.choice(prefix_map.get(level, ["4557"]))
    return {
        "number": generate_luhn_number(prefix, 16),
        "expiry": random_expiry(),
        "cvv": random_cvv(),
        "holder_name": random_name(),
        "cpf": random_cpf(),
    }


class DatabaseManager:
    """Gerenciador de banco de dados SQLite para o bot."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        """Abre conexao com banco de dados."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Inicializa schema do banco de dados."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    balance REAL DEFAULT 0.0,
                    total_purchases INTEGER DEFAULT 0,
                    is_verified INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    number TEXT NOT NULL,
                    expiry TEXT NOT NULL,
                    cvv TEXT NOT NULL,
                    holder_name TEXT NOT NULL,
                    cpf TEXT NOT NULL,
                    status TEXT DEFAULT 'available',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    valor REAL NOT NULL,
                    descricao TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_cards_level ON cards(level, status)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_users_verified ON users(is_verified)")
            conn.commit()
            logger.info("✅ Banco de dados inicializado.")

    def seed_stock_if_empty(self) -> None:
        """Popula banco de dados com cartoes iniciais se vazio."""
        with self._connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
            if count > 0:
                return

            for level, data in CARD_LEVELS.items():
                for _ in range(data["stock"]):
                    card = generate_credit_card(level)
                    conn.execute(
                        """
                        INSERT INTO cards(level, number, expiry, cvv, holder_name, cpf, status)
                        VALUES (?, ?, ?, ?, ?, ?, 'available')
                        """,
                        (
                            level,
                            card["number"],
                            card["expiry"],
                            card["cvv"],
                            card["holder_name"],
                            card["cpf"],
                        ),
                    )
            conn.commit()
            logger.info("📦 Estoque inicial criado.")

    def add_user(self, user_id: int, username: Optional[str], first_name: str) -> None:
        """Adiciona ou atualiza usuario no banco."""
        with self._connect() as conn:
            existing = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if existing:
                conn.execute(
                    "UPDATE users SET username = ?, first_name = ? WHERE user_id = ?",
                    (username or "", first_name, user_id),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO users(user_id, username, first_name, balance, total_purchases, is_verified)
                    VALUES (?, ?, ?, 0.0, 0, 0)
                    """,
                    (user_id, username or "", first_name),
                )
            conn.commit()

    def get_user(self, user_id: int) -> Optional[sqlite3.Row]:
        """Obtem dados de usuario."""
        with self._connect() as conn:
            return conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()

    def set_verified(self, user_id: int, value: bool = True) -> None:
        """Marca usuario como verificado."""
        with self._connect() as conn:
            conn.execute("UPDATE users SET is_verified = ? WHERE user_id = ?", (1 if value else 0, user_id))
            conn.commit()

    def add_balance(self, user_id: int, amount: float) -> float:
        """Adiciona saldo ao usuario."""
        with self._connect() as conn:
            current = conn.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
            if current is None:
                raise ValueError("Usuario nao encontrado.")
            new_balance = float(current["balance"]) + float(amount)
            conn.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
            conn.commit()
            return new_balance

    def deduct_balance(self, user_id: int, amount: float) -> None:
        """Remove saldo do usuario."""
        current = self.get_user_balance(user_id)
        new_balance = current - amount
        with self._connect() as conn:
            conn.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
            conn.commit()

    def get_user_balance(self, user_id: int) -> float:
        """Obtem saldo do usuario."""
        user = self.get_user(user_id)
        if not user:
            return 0.0
        return float(user["balance"])

    def add_transaction(self, user_id: int, tipo: str, valor: float, descricao: str) -> None:
        """Registra transacao no historico."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO transactions(user_id, tipo, valor, descricao)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, tipo, float(valor), descricao),
            )
            conn.commit()

    def get_history(self, user_id: int, limit: int = 10) -> List[sqlite3.Row]:
        """Obtem historico de transacoes do usuario."""
        with self._connect() as conn:
            return conn.execute(
                """
                SELECT * FROM transactions
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()

    def get_all_users(self) -> List[int]:
        """Obtem lista de todos os usuarios."""
        with self._connect() as conn:
            rows = conn.execute("SELECT user_id FROM users").fetchall()
            return [r["user_id"] for r in rows]

    def get_available_cards(self, level: str) -> List[sqlite3.Row]:
        """Obtem cartoes disponiveis de um nivel."""
        with self._connect() as conn:
            return conn.execute(
                """
                SELECT * FROM cards
                WHERE level = ? AND status = 'available'
                ORDER BY id ASC
                """,
                (level,),
            ).fetchall()

    def mark_card_sold(self, card_id: int) -> None:
        """Marca cartao como vendido."""
        with self._connect() as conn:
            conn.execute("UPDATE cards SET status = 'sold' WHERE id = ?", (card_id,))
            conn.commit()

    def increment_total_purchases(self, user_id: int) -> None:
        """Incrementa contador de compras do usuario."""
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE users SET total_purchases = total_purchases + 1 WHERE user_id = ?
                """,
                (user_id,),
            )
            conn.commit()

    def get_stock_summary(self) -> Dict[str, int]:
        """Obtem resumo de estoque por nivel."""
        summary: Dict[str, int] = {}
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT level, COUNT(*) AS qty
                FROM cards
                WHERE status = 'available'
                GROUP BY level
                """
            ).fetchall()
            for row in rows:
                summary[row["level"]] = int(row["qty"])
        return summary

    def add_card(self, level: str, number: str, expiry: str, cvv: str, holder_name: str, cpf: str) -> None:
        """Adiciona cartao ao banco."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO cards(level, number, expiry, cvv, holder_name, cpf, status)
                VALUES (?, ?, ?, ?, ?, ?, 'available')
                """,
                (level, number, expiry, cvv, holder_name, cpf),
            )
            conn.commit()