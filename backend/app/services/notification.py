import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NotificationService")

class NotificationService:
    @staticmethod
    async def send_sms(phone: str, message: str):
        """
        Simulates sending an SMS. 
        In production, replace this with Twilio, Netgsm, or other SMS gateway.
        """
        logger.info(f"[SMS] Sending to {phone}: {message}")
        # Simulation: In a real app, you'd use a library like 'requests' or 'twilio'
        # Example Twilio:
        # client = Client(account_sid, auth_token)
        # client.messages.create(body=message, from_=from_number, to=phone)
        return True

    @staticmethod
    async def send_appointment_confirmation(phone: str, user_name: str, date: str, time: str, service: str):
        message = f"Sayın {user_name}, {date} tarihinde saat {time}'daki {service} randevunuz onaylanmıştır. Teşekkür ederiz."
        return await NotificationService.send_sms(phone, message)

    @staticmethod
    async def send_reminder(phone: str, user_name: str, date: str, time: str, service: str):
        message = f"Hatırlatma: Sayın {user_name}, bugün saat {time}'da {service} randevunuz bulunmaktadır. Bekliyoruz!"
        return await NotificationService.send_sms(phone, message)
