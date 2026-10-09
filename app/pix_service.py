"""
Servico de Integracao Pix
==========================
Integracao com gateway de pagamento Pix.
Estrutura pronta para conectar com API real.
"""

import logging
import requests
from typing import Dict, Optional

from app.config import PIX_API_URL, PIX_API_TOKEN

logger = logging.getLogger(__name__)


class PixService:
    """Gerenciador de pagamentos via Pix."""

    def __init__(self, api_url: str = PIX_API_URL, api_token: str = PIX_API_TOKEN):
        self.api_url = api_url
        self.api_token = api_token
        self.enabled = bool(api_url and api_token)

    def create_charge(self, user_id: int, value: float, description: str = "") -> Optional[Dict]:
        """
        Cria cobranca Pix.

        Args:
            user_id: ID do usuario
            value: Valor em reais
            description: Descricao da cobranca

        Returns:
            Dicionario com dados da cobranca ou None
        """
        if not self.enabled:
            logger.warning("⚠️ Servico Pix nao configurado.")
            return None

        try:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            payload = {
                "user_id": user_id,
                "value": value,
                "description": description or "Deposito Haxor Store",
            }
            response = requests.post(
                f"{self.api_url}/charge",
                json=payload,
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()
            logger.info(f"✅ Cobranca Pix criada: {user_id} - R$ {value}")
            return response.json()
        except Exception as exc:
            logger.exception(f"❌ Erro ao criar cobranca Pix: {exc}")
            return None

    def check_payment(self, charge_id: str) -> Optional[Dict]:
        """
        Verifica status de pagamento.

        Args:
            charge_id: ID da cobranca

        Returns:
            Dicionario com status ou None
        """
        if not self.enabled:
            return None

        try:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            response = requests.get(
                f"{self.api_url}/charge/{charge_id}",
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            logger.exception(f"❌ Erro ao verificar pagamento: {exc}")
            return None

    def generate_qr_code(self, charge_id: str) -> Optional[str]:
        """
        Gera QR Code para pagamento.

        Args:
            charge_id: ID da cobranca

        Returns:
            String com QR Code ou None
        """
        if not self.enabled:
            return None

        try:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            response = requests.get(
                f"{self.api_url}/charge/{charge_id}/qr_code",
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("qr_code")
        except Exception as exc:
            logger.exception(f"❌ Erro ao gerar QR Code: {exc}")
            return None


# Instancia global do servico Pix
pix_service = PixService()