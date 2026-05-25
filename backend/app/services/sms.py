import os
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        # Gerçek API anahtarları .env dosyasından alınmalıdır
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_number = os.getenv("TWILIO_FROM_NUMBER", "")
        
        self.netgsm_user = os.getenv("NETGSM_USER", "")
        self.netgsm_pass = os.getenv("NETGSM_PASS", "")
        self.netgsm_header = os.getenv("NETGSM_HEADER", "")
        
        # Decide default provider automatically based on what keys are present
        if self.twilio_sid and self.twilio_token:
            self.default_provider = "twilio"
        elif self.netgsm_user and self.netgsm_pass:
            self.default_provider = "netgsm"
        else:
            self.default_provider = "mock"

    async def send_sms(self, phone: str, message: str, provider: Optional[str] = None):
        """
        SMS gönderim proxy motoru. Ortam değişkenlerine göre (AWS/Twilio/Netgsm) gerçek ağ çağrısı başlatır 
        ya da yapılandırma eksikse güvenli mock durumuna düşer.
        """
        active_provider = provider or self.default_provider
        
        logger.info(f"[SMS GATEWAY] Routing message to {phone} via '{active_provider}' engine.")
        
        try:
            if active_provider == "twilio":
                return await self._send_twilio(phone, message)
            elif active_provider == "netgsm":
                return await self._send_netgsm(phone, message)
            else:
                print(f"📦 [MOCK SMS - {phone}] {message}")
                return {"status": "success", "provider": "mock", "delivered": True}
        except Exception as e:
            logger.error(f"[SMS GATEWAY ERROR] Failed to push to {active_provider}. Error: {str(e)}")
            return {"status": "failed", "detail": str(e)}

    async def _send_twilio(self, phone: str, message: str):
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json"
        data = {
            "To": phone,
            "From": self.twilio_number,
            "Body": message
        }
        auth = (self.twilio_sid, self.twilio_token)
        async with httpx.AsyncClient() as client:
            res = await client.post(url, data=data, auth=auth)
            res.raise_for_status()
            return {"status": "success", "provider": "twilio", "response": res.json()}

    async def _send_netgsm(self, phone: str, message: str):
        url = "https://api.netgsm.com.tr/sms/send/get"
        # Dummy structure for NetGSM GET API representation
        params = {
            "usercode": self.netgsm_user,
            "password": self.netgsm_pass,
            "msgheader": self.netgsm_header,
            "mobilenumber": phone,
            "message": message,
            "appkey": os.getenv("NETGSM_APPKEY", "")
        }
        async with httpx.AsyncClient() as client:
            res = await client.get(url, params=params)
            res.raise_for_status()
            return {"status": "success", "provider": "netgsm", "response": res.text}

sms_service = SMSService()
