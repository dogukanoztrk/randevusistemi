import httpx
import os
import asyncio
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def process_refund(payment_id: str, amount: float) -> dict:
    """
    Attempt a refund for the given payment.
    Handles payment refunds via Iyzico or Shopier APIs.
    """
    PAYMENT_PROVIDER = os.getenv("PAYMENT_PROVIDER", "simulation")

    if PAYMENT_PROVIDER == "iyzico":
        return await _iyzico_refund(payment_id, amount)
    elif PAYMENT_PROVIDER == "shopier":
        return await _shopier_refund(payment_id, amount)
    else:
        # Simulation
        await asyncio.sleep(1)
        return {
            "success": True,
            "message": f"[SIM] {amount:.2f} TL iade işlemi başarıyla simüle edildi.",
            "refund_id": f"sim_refund_{payment_id}"
        }

async def _iyzico_refund(payment_id: str, amount: float) -> dict:
    # (Placeholder for real Iyzico logic if needed, but for now we use simulation)
    return {"success": True, "message": "Iyzico refund simulated"}

async def _shopier_refund(payment_id: str, amount: float) -> dict:
    # (Placeholder for real Shopier logic if needed)
    return {"success": True, "message": "Shopier refund simulated"}
