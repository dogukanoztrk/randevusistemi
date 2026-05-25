from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.appointment import Appointment, AppointmentStatus
from app.core.database import SessionLocal
from app.services.sms import sms_service
import asyncio

async def scan_and_send_reminders():
    """
    Veritabanını tarar ve 24 saatten az kalmış, daha önce hatırlatılmamış 
    'Kesinleşti' randevuları bulup SMS gönderir.
    """
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        target_time = now + timedelta(days=1)
        
        print(f"[REMINDER TASK] Tarama Başladı: {now.strftime('%d %B %Y %H:%M')} (UTC)")

        # Sadece onaylanmış ve henüz hatırlatılmamış olanları getir
        appointments = db.query(Appointment).filter(
            Appointment.status == AppointmentStatus.CONFIRMED.value,
            Appointment.reminded_at == None
        ).all()

        for app in appointments:
            try:
                # Tarihi "2026-04-20T21:00:00.000Z" gibi formatlardan izole et
                date_str = str(app.appointment_date).split('T')[0]
                appointment_dt = datetime.fromisoformat(
                    f"{date_str}T{app.appointment_time}:00"
                )
                
                # Eğer randevu geçmişte değilse ve 24 saat penceresine girdiyse
                if now < appointment_dt <= target_time:
                    # SMS İçeriği
                    time_formatted = appointment_dt.strftime("%d/%m/%Y saat %H:%M")
                    message = f"Sayın {app.user_name}, {time_formatted} tarihindeki randevunuzu hatırlatırız. DiTA"
                    
                    # SMS Gönder
                    await sms_service.send_sms(app.user_email, message)
                    
                    # Hatırlatıldığını kaydet
                    app.reminded_at = datetime.utcnow()
                    db.commit()
            except Exception as e:
                print(f"[REMINDER TASK] App ID {app.id} için hata: {str(e)}")
                
    except Exception as e:
        print(f"[REMINDER TASK] Genel Hata: {str(e)}")
    finally:
        db.close()
