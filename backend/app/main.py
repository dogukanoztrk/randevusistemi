from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional, List
import uuid
import uvicorn
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.models.appointment import Appointment, AppointmentStatus, Base, Review, User, AuditLog, hash_password

from app.core.database import engine, get_db
from app.services.reminder import scan_and_send_reminders
from app.services.refund import process_refund

def log_action(db: Session, admin: dict, action: str, detail: str):
    log = AuditLog(
        company_id=admin.get("company_id"),
        admin_name=admin.get("company_name", "Admin"),
        action=action,
        detail=detail
    )
    db.add(log)
    db.commit()

# Initialize Database
# TODO: Once Alembic migrations are actively used, remove this line.
# Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

class PaymentIntentRequest(BaseModel):
    service_name: str
    service_price: float
    deposit_amount: float
    staff_name: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    company_id: Optional[str] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start Scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scan_and_send_reminders, 'interval', hours=1)
    scheduler.start()
    print("[BACKEND] Scheduler started (Hourly Scan)")
    yield
    # Shutdown: Stop Scheduler
    scheduler.shutdown()
    print("[BACKEND] Scheduler stopped")

app = FastAPI(title="DiTA Appointment Backend", version="1.0.0", lifespan=lifespan)

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"[DEBUG] Incoming {request.method} to {request.url.path}")
    response = await call_next(request)
    print(f"[DEBUG] Response status: {response.status_code}")
    return response

security = HTTPBearer()
import os
SECRET_KEY = os.getenv("SECRET_KEY", "dita_admin_secret_key")

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        if payload.get("role") not in ["admin", "company_admin"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_customer(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        if payload.get("role") != "customer":
            raise HTTPException(status_code=403, detail="Not authorized")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

class ReviewRequest(BaseModel):
    appointment_id: int
    rating: int
    comment: Optional[str] = None

class UserRegister(BaseModel):
    name: str
    phone: str
    password: str

class UserLogin(BaseModel):
    phone: str
    password: str

class CompanyLoginRequest(BaseModel):
    dashboard_code: str
    password: str

# ── Customer Auth ──────────────────────────────────────────────────────────
@app.post("/api/auth/register")
@limiter.limit("5/minute")
def register_user(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.phone == data.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu telefon numarası zaten kayıtlı.")
    user = User(name=data.name, phone=data.phone, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = jwt.encode({"role": "customer", "user_id": user.id, "name": user.name, "phone": user.phone, "exp": datetime.utcnow() + timedelta(days=30)}, SECRET_KEY, algorithm="HS256")
    return {"status": "success", "token": token, "user": {"id": user.id, "name": user.name, "phone": user.phone}}

@app.post("/api/auth/login")
@limiter.limit("10/minute")
def login_user(request: Request, data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == data.phone).first()
    if not user or user.password_hash != hash_password(data.password):
        raise HTTPException(status_code=401, detail="Telefon veya şifre hatalı.")
    token = jwt.encode({"role": "customer", "user_id": user.id, "name": user.name, "phone": user.phone, "exp": datetime.utcnow() + timedelta(days=30)}, SECRET_KEY, algorithm="HS256")
    return {"status": "success", "token": token, "user": {"id": user.id, "name": user.name, "phone": user.phone}}

@app.get("/api/auth/me")
def get_me(payload: dict = Depends(get_current_customer)):
    return {"user_id": payload.get("user_id"), "name": payload.get("name"), "phone": payload.get("phone")}

# ── Company Dashboard Login ────────────────────────────────────────────────
@app.post("/api/company/login")
@limiter.limit("5/minute")
def company_login(request: Request, data: CompanyLoginRequest):
    companies = get_companies_from_file()
    sectors = get_sectors_from_file()
    for comp in companies:
        if comp.get("dashboard_code") == data.dashboard_code:
            if comp.get("dashboard_password_hash") == hash_password(data.password):
                sector = next((s for s in sectors if s["id"] == comp["sector_id"]), None)
                token = jwt.encode({"role": "company_admin", "company_id": comp["id"], "company_name": comp["name"], "sector_id": comp["sector_id"], "exp": datetime.utcnow() + timedelta(hours=24)}, SECRET_KEY, algorithm="HS256")
                return {"status": "success", "token": token, "company": comp, "sector": sector}
            raise HTTPException(status_code=401, detail="Şifre hatalı.")
    raise HTTPException(status_code=404, detail="Şirket kodu bulunamadı.")

def get_current_staff(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        if payload.get("role") != "staff":
            raise HTTPException(status_code=403, detail="Not authorized")
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

class StaffLoginRequest(BaseModel):
    staff_code: str
    password: str

@app.post("/api/staff/login")
@limiter.limit("5/minute")
def staff_login(request: Request, data: StaffLoginRequest):
    staff_list = get_staff_from_file()
    for s in staff_list:
        if s.get("staff_code") == data.staff_code:
            if s.get("password_hash") == hash_password(data.password):
                token = jwt.encode({
                    "role": "staff", 
                    "staff_id": s["id"], 
                    "staff_name": s["name"],
                    "company_id": s["company_id"],
                    "exp": datetime.utcnow() + timedelta(hours=24)
                }, SECRET_KEY, algorithm="HS256")
                return {"status": "success", "token": token, "staff": s}
            raise HTTPException(status_code=401, detail="Şifre hatalı.")
    raise HTTPException(status_code=404, detail="Personel kodu bulunamadı.")

@app.get("/api/staff/appointments")
def get_staff_appointments(db: Session = Depends(get_db), staff: dict = Depends(get_current_staff)):
    # Staff name based filtering is usually safer since company IDs might overlap
    appts = db.query(Appointment).filter(
        Appointment.staff_name == staff["staff_name"],
        Appointment.company_id == staff["company_id"]
    ).order_by(Appointment.appointment_date.desc(), Appointment.appointment_time.desc()).all()
    return appts

@app.get("/")
async def root():
    return {"message": "Welcome to DiTA Backend API"}

@app.post("/api/create-payment-intent")
async def create_payment_intent(request: PaymentIntentRequest, db: Session = Depends(get_db)):
    """
    Ödeme oturumu oluşturur ve bir checkout URL döner.
    """
    actual_price = request.deposit_amount
    companies = get_companies_from_file()
    sectors = get_sectors_from_file()
    
    company = next((c for c in companies if c["id"] == request.company_id), None)
    sector = next((s for s in sectors if company and s["id"] == company.get("sector_id")), None)
    
    if sector and company:
        srv = next((sv for sv in sector.get("services", []) if sv["name"] == request.service_name), None)
        if srv:
            srv_id = str(srv["id"])
            if "custom_prices" in company and srv_id in company["custom_prices"] and company["custom_prices"][srv_id]:
                actual_price = float(company["custom_prices"][srv_id])
            else:
                actual_price = float(srv["price"])

    payment_id = str(uuid.uuid4())
    db_appointment = Appointment(
        external_id=payment_id,
        service_name=request.service_name,
        staff_name=request.staff_name,
        company_id=request.company_id,
        user_name=request.customer_name,
        user_email=request.customer_phone,
        appointment_date=request.appointment_date,
        appointment_time=request.appointment_time,
        amount=actual_price,
        status=AppointmentStatus.PENDING.value
    )
    db.add(db_appointment)
    db.commit()

    # Simulation URL
    checkout_url = f"http://127.0.0.1:5173/checkout-sim?id={payment_id}"
    
    return {
        "status": "success",
        "id": payment_id,
        "token": f"sim_token_{payment_id}",
        "checkout_url": checkout_url
    }

@app.get("/api/available-hours")
async def get_available_hours(date: str, staff_name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Belirli bir gündeki (ve isteğe bağlı olarak personele ait) dolu saatleri döndürür.
    """
    query = db.query(Appointment).filter(
        Appointment.appointment_date == date,
        Appointment.status == AppointmentStatus.CONFIRMED.value
    )
    
    if staff_name:
        query = query.filter(Appointment.staff_name == staff_name)
        
    booked_appointments = query.all()
    booked_hours = [app.appointment_time for app in booked_appointments]
    return booked_hours

@app.post("/api/payment-callback")
async def payment_callback(id: str, status: str, payment_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Ödeme başarılı olduğunda tetiklenen webhook.
    Randevu onaylanır, benzersiz bir cancel_token üretilir.
    """
    appointment = db.query(Appointment).filter(Appointment.external_id == id).first()

    if not appointment:
        return {"status": "error", "message": "Appointment not found"}

    if status == "SUCCESS":
        cancel_token = str(uuid.uuid4())
        appointment.status = AppointmentStatus.CONFIRMED.value
        appointment.cancel_token = cancel_token
        # Store Iyzico/Shopier payment ID for refund later (passed via callback)
        if payment_id:
            appointment.payment_id = payment_id
        db.commit()

        # Send SMS Confirmation
        try:
            from app.services.sms import sms_service
            msg = f"Merhaba {appointment.user_name}, {appointment.appointment_date} {appointment.appointment_time} tarihindeki randevunuz onaylanmıştır. Referans: {appointment.external_id}"
            import asyncio
            asyncio.create_task(sms_service.send_sms(appointment.user_email, msg))
        except Exception as e:
            print(f"SMS Confirmation error: {e}")

        return {
            "status": "success",
            "message": "Appointment confirmed",
            "cancel_token": cancel_token
        }
    
    return {"status": "pending", "message": "Payment not completed"}


@app.get("/api/cancel-appointment/{cancel_token}")
async def cancel_appointment(cancel_token: str, db: Session = Depends(get_db)):
    """
    İptal endpoint'i.
    - cancel_token geçerliyse ve randevuya 24 saatten fazla varsa: iptal eder + iade başlatır.
    - 24 saatten az kaldıysa: 400 hatası döner.
    - Token bulunamazsa: 404 hatası döner.
    """
    appointment = db.query(Appointment).filter(
        Appointment.cancel_token == cancel_token
    ).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Geçersiz veya kullanılmış iptal bağlantısı.")

    if appointment.status == AppointmentStatus.CANCELLED.value:
        raise HTTPException(status_code=400, detail="Bu randevu zaten iptal edilmiş.")

    if appointment.status != AppointmentStatus.CONFIRMED.value:
        raise HTTPException(status_code=400, detail="Yalnızca onaylanmış randevular iptal edilebilir.")

    # ── 24 saatlik iptal süresi kontrolü ──────────────────────────────────────
    try:
        date_str = str(appointment.appointment_date).split('T')[0]
        appointment_dt = datetime.fromisoformat(
            f"{date_str}T{appointment.appointment_time}:00"
        )
    except (ValueError, TypeError):
        raise HTTPException(status_code=500, detail="Randevu tarihi/saati okunamadı.")

    now = datetime.utcnow()
    time_until_appointment = appointment_dt - now

    if time_until_appointment <= timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail=(
                f"İptal süresi dolmuştur. Randevunuza "
                f"{int(time_until_appointment.total_seconds() // 3600)} saat {int((time_until_appointment.total_seconds() % 3600) // 60)} dakika kalmıştır. "
                "İptal işlemi yalnızca 24 saat öncesine kadar yapılabilir."
            )
        )

    # ── İptal & İade ──────────────────────────────────────────────────────────
    appointment.status = AppointmentStatus.CANCELLED.value
    appointment.cancel_token = None  # Token'ı geçersiz kıl (tek kullanımlık)
    db.commit()

    # Iyzico / Shopier üzerinden iade başlat
    refund_result = await process_refund(
        payment_id=appointment.payment_id or appointment.external_id,
        amount=appointment.amount
    )

    return {
        "status": "cancelled",
        "message": "Randevunuz başarıyla iptal edildi.",
        "refund": refund_result,
        "appointment": {
            "service_name": appointment.service_name,
            "date": appointment.appointment_date,
            "time": appointment.appointment_time,
            "refund_amount": appointment.amount
        }
    }

# ── Admin & Sync Endpoints ────────────────────────────────────────────────
import json
import os

# Global BUSINESS_SETTINGS removed, moved to company specific settings

# Persistent Configuration for Sectors
SECTORS_FILE = "dita_sectors.json"
DEFAULT_SECTORS_DATA = [
    {
        "id": "tattoo", "name": "Dövme Stüdyosu", "emoji": "🖋️", "tagline": "Sanatı ten üzerine taşı",
        "theme": {"accent": "#8B5CF6", "accentRgb": "139, 92, 246", "accentDark": "#6D28D9", "accentLight": "#C4B5FD", "bg": "rgba(139, 92, 246, 0.05)", "cardBg": "rgba(139, 92, 246, 0.04)", "name": "Violet"},
        "services": [
            {"id": 1, "name": "Mini Dövme", "category": "Temel İşlemler", "price": 800, "duration": "60 dk", "description": "Küçük, detaylı çizgi çalışması.", "features": ["Konsültasyon", "Steril...", "Bakım", "Ücretsiz Rötuş"]},
            {"id": 2, "name": "Orta Boy", "category": "Sanatsal", "price": 2000, "duration": "2-3 sa", "description": "Renk veya tek renk.", "features": ["Tasarım", "Tek Seans", "Bakım", "Rötuş"]},
            {"id": 3, "name": "Large Piece", "category": "Premium", "price": 4500, "duration": "4+ sa", "description": "Kol, sırt veya bacak komple.", "features": ["Özel Tasarım", "Çoklu Seans", "Premium Mürekkep", "Geniş Bakım"]},
            {"id": 4, "name": "Cover Up", "category": "Düzeltme", "price": 3000, "duration": "3-4 sa", "description": "Eski dövmenin üstünü kapatma.", "features": ["Analiz", "Özel Teknik", "Renk Düzeltme", "Garanti"]}
        ]
    },
    {
        "id": "psikolog", "name": "Psikolog", "emoji": "🧠", "tagline": "Zihnini keşfet, kendini bul",
        "theme": {"accent": "#10B981", "accentRgb": "16, 185, 129", "accentDark": "#059669", "accentLight": "#6EE7B7", "bg": "rgba(16, 185, 129, 0.05)", "cardBg": "rgba(16, 185, 129, 0.04)", "name": "Emerald"},
        "services": [
            {"id": 1, "name": "İlk Görüşme", "price": 600, "duration": "50 dk", "description": "Tanışma ve değerlendirme seansı.", "features": ["Ücretsiz Tanışma", "Anamnez", "Hedef Belirleme", "Plan"]},
            {"id": 2, "name": "Bireysel Terapi", "price": 900, "duration": "50 dk", "description": "Haftalık uzman desteği.", "features": ["Özel Mekan", "Yüz Yüze", "Gizlilik", "Not Tutma"]},
            {"id": 3, "name": "Çift Terapisi", "price": 1500, "duration": "90 dk", "description": "İlişki ve evlilik danışmanlığı.", "features": ["Eşli Katılım", "Empati Çalışması", "Çatışma Çözümü", "Uyum"]},
            {"id": 4, "name": "EMDR Terapisi", "price": 1200, "duration": "60 dk", "description": "Travma odaklı teknik.", "features": ["Göz Hareketleri", "Duygusal Boşalım", "Kalıcı Çözüm", "Yoğun Seans"]}
        ]
    },
    {
        "id": "guzellik", "name": "Güzellik Merkezi", "emoji": "✨", "tagline": "Güzelliğini öne çıkar",
        "theme": {"accent": "#EC4899", "accentRgb": "236, 72, 153", "accentDark": "#BE185D", "accentLight": "#F9A8D4", "bg": "rgba(236, 72, 153, 0.05)", "cardBg": "rgba(236, 72, 153, 0.04)", "name": "Rose"},
        "services": [
            {"id": 1, "name": "Cilt Bakımı", "price": 700, "duration": "60 dk", "description": "Derin temizlik ve maske.", "features": ["Peeling", "Maske", "Mesoterapi", "Masaj"]},
            {"id": 2, "name": "Lazer Epilasyon", "price": 2000, "duration": "45 dk", "description": "Tüm vücut kalıcı çözüm.", "features": ["Buz Başlık", "Acısız", "Garantili", "Hızlı İşlem"]},
            {"id": 3, "name": "Kalıcı Makyaj", "price": 1500, "duration": "120 dk", "description": "Microblading ve dudak renklendirme.", "features": ["Altın Oran", "Kişiye Özel", "Doğal Pigment", "Rötuş"]},
            {"id": 4, "name": "Bölgesel İncelme", "price": 1200, "duration": "40 dk", "description": "Radyofrekans ve kavitasyon.", "features": ["Sıkılaşma", "Ölçüm", "Diyet Desteği", "Makine Bazlı"]}
        ]
    }
]

DEFAULT_SETTINGS = {
    "startTime": "09:00",
    "endTime": "19:00",
    "intervalMinutes": 60,
    "closedDays": [0],
    "breakStartTime": "12:00",
    "breakEndTime": "13:00",
    "hasBreak": True
}

COMPANIES_FILE = "dita_companies.json"
DEFAULT_COMPANIES = [
    {"id": "c1", "sector_id": "tattoo", "name": "Ink Art Studio", "rating": 4.8, "dashboard_code": "INK001", "dashboard_password_hash": hash_password("ink2026"), "brand_color": "#C5A059", "logo_url": "", "settings": DEFAULT_SETTINGS.copy()},
    {"id": "c2", "sector_id": "tattoo", "name": "Tattoo Masters", "rating": 4.9, "dashboard_code": "TAT001", "dashboard_password_hash": hash_password("tat2026"), "brand_color": "#8B5CF6", "logo_url": "", "settings": DEFAULT_SETTINGS.copy()},
    {"id": "c3", "sector_id": "psikolog", "name": "Zihin Psikoloji", "rating": 4.7, "dashboard_code": "ZHN001", "dashboard_password_hash": hash_password("zhn2026"), "brand_color": "#10B981", "logo_url": "", "settings": DEFAULT_SETTINGS.copy()},
    {"id": "c4", "sector_id": "psikolog", "name": "Empati Kliniği", "rating": 4.9, "dashboard_code": "EMP001", "dashboard_password_hash": hash_password("emp2026"), "brand_color": "#3B82F6", "logo_url": "", "settings": DEFAULT_SETTINGS.copy()},
    {"id": "c5", "sector_id": "guzellik", "name": "Estetik Güzellik Merkezi", "rating": 4.8, "dashboard_code": "EST001", "dashboard_password_hash": hash_password("est2026"), "brand_color": "#EC4899", "logo_url": "", "settings": DEFAULT_SETTINGS.copy()},
    {"id": "c6", "sector_id": "guzellik", "name": "Pure Glow Beauty", "rating": 4.6, "dashboard_code": "PGL001", "dashboard_password_hash": hash_password("pgl2026"), "brand_color": "#F59E0B", "logo_url": "", "settings": DEFAULT_SETTINGS.copy()}
]

STAFF_FILE = "dita_staff.json"
DEFAULT_STAFF = [
    {"id": "s1_c1", "name": "Kaan Yılmaz", "title": "Realizm Uzmanı", "avatar": "👨🏻‍🎤", "company_id": "c1", "service_ids": [1, 2], "working_hours": {"startTime": "09:00", "endTime": "18:00"}, "breaks": {"startTime": "12:00", "endTime": "13:00"}},
    {"id": "s2_c1", "name": "Ege Demir", "title": "Minimalist Artist", "avatar": "👨🏼‍🎤", "company_id": "c1", "service_ids": [1], "working_hours": {"startTime": "10:00", "endTime": "19:00"}, "breaks": {"startTime": "13:00", "endTime": "14:00"}},
    {"id": "s3_c1", "name": "Selin Şahin", "title": "Cover Up Ustası", "avatar": "👩🏻‍🎤", "company_id": "c1", "service_ids": [4], "working_hours": {"startTime": "09:00", "endTime": "17:00"}, "breaks": {"startTime": "12:30", "endTime": "13:30"}},
    {"id": "s4_c1", "name": "Ceren Ak", "title": "Geleneksel Dövme", "avatar": "👩🏼‍🎤", "company_id": "c1", "service_ids": [2, 3], "working_hours": {"startTime": "11:00", "endTime": "20:00"}, "breaks": {"startTime": "14:00", "endTime": "15:00"}},
    
    {"id": "s1_c2", "name": "Barış Can", "title": "Portre Uzmanı", "avatar": "👨🏻‍🎤", "company_id": "c2", "service_ids": [2, 3], "working_hours": {"startTime": "09:00", "endTime": "18:00"}, "breaks": {"startTime": "12:00", "endTime": "13:00"}},
    {"id": "s2_c2", "name": "Mert Sönmez", "title": "Line Art Artist", "avatar": "👨🏽‍🎤", "company_id": "c2", "service_ids": [1, 2], "working_hours": {"startTime": "10:00", "endTime": "19:00"}, "breaks": {"startTime": "13:00", "endTime": "14:00"}},
    {"id": "s3_c2", "name": "Zeynep Bal", "title": "Büyük Boy Uzmanı", "avatar": "👩🏻‍🎤", "company_id": "c2", "service_ids": [3], "working_hours": {"startTime": "09:00", "endTime": "17:00"}, "breaks": {"startTime": "12:30", "endTime": "13:30"}},
    {"id": "s4_c2", "name": "Elif Dağ", "title": "Cover Up Uzmanı", "avatar": "👩🏽‍🎤", "company_id": "c2", "service_ids": [2, 4], "working_hours": {"startTime": "11:00", "endTime": "20:00"}, "breaks": {"startTime": "14:00", "endTime": "15:00"}},

    {"id": "s1_c3", "name": "Dr. Berk Can", "title": "Klinik Psikolog", "avatar": "👨🏻‍⚕️", "company_id": "c3", "service_ids": [1, 2], "working_hours": {"startTime": "09:00", "endTime": "18:00"}, "breaks": {"startTime": "12:00", "endTime": "13:00"}},
    {"id": "s2_c3", "name": "Psk. Ozan Koç", "title": "Çift Terapisti", "avatar": "👨🏼‍⚕️", "company_id": "c3", "service_ids": [1, 3], "working_hours": {"startTime": "10:00", "endTime": "19:00"}, "breaks": {"startTime": "13:00", "endTime": "14:00"}},
    {"id": "s3_c3", "name": "Psk. Melis Kaya", "title": "Bireysel Terapist", "avatar": "👩🏼‍⚕️", "company_id": "c3", "service_ids": [1, 2], "working_hours": {"startTime": "09:00", "endTime": "17:00"}, "breaks": {"startTime": "12:30", "endTime": "13:30"}},
    {"id": "s4_c3", "name": "Uzman Psk. Aslı Türk", "title": "EMDR Uzmanı", "avatar": "👩🏻‍⚕️", "company_id": "c3", "service_ids": [1, 4], "working_hours": {"startTime": "11:00", "endTime": "20:00"}, "breaks": {"startTime": "14:00", "endTime": "15:00"}},

    {"id": "s1_c4", "name": "Psk. Caner Aydın", "title": "Travma Uzmanı", "avatar": "👨🏽‍⚕️", "company_id": "c4", "service_ids": [1, 4], "working_hours": {"startTime": "09:00", "endTime": "18:00"}, "breaks": {"startTime": "12:00", "endTime": "13:00"}},
    {"id": "s2_c4", "name": "Psk. Gökhan Erol", "title": "Klinik Terapist", "avatar": "👨🏻‍⚕️", "company_id": "c4", "service_ids": [1, 2], "working_hours": {"startTime": "10:00", "endTime": "19:00"}, "breaks": {"startTime": "13:00", "endTime": "14:00"}},
    {"id": "s3_c4", "name": "Dr. Ece Işık", "title": "Aile ve Çift Terapisti", "avatar": "👩🏻‍⚕️", "company_id": "c4", "service_ids": [1, 3], "working_hours": {"startTime": "09:00", "endTime": "17:00"}, "breaks": {"startTime": "12:30", "endTime": "13:30"}},
    {"id": "s4_c4", "name": "Psk. Burcu Çetin", "title": "Bireysel Terapist", "avatar": "👩🏼‍⚕️", "company_id": "c4", "service_ids": [1, 2], "working_hours": {"startTime": "11:00", "endTime": "20:00"}, "breaks": {"startTime": "14:00", "endTime": "15:00"}},

    {"id": "s1_c5", "name": "Ali Korkmaz", "title": "Cilt Bakım Uzmanı", "avatar": "👨🏻‍⚕️", "company_id": "c5", "service_ids": [1], "working_hours": {"startTime": "09:00", "endTime": "18:00"}, "breaks": {"startTime": "12:00", "endTime": "13:00"}},
    {"id": "s2_c5", "name": "Koray Yıldız", "title": "Kalıcı Makyaj", "avatar": "👨🏼‍⚕️", "company_id": "c5", "service_ids": [3], "working_hours": {"startTime": "10:00", "endTime": "19:00"}, "breaks": {"startTime": "13:00", "endTime": "14:00"}},
    {"id": "s3_c5", "name": "Ayşe Hanım", "title": "Lazer Uzmanı", "avatar": "👩🏼‍🦰", "company_id": "c5", "service_ids": [2], "working_hours": {"startTime": "09:00", "endTime": "17:00"}, "breaks": {"startTime": "12:30", "endTime": "13:30"}},
    {"id": "s4_c5", "name": "Merve Kılıç", "title": "Kavitasyon Uzmanı", "avatar": "👱🏻‍♀️", "company_id": "c5", "service_ids": [4], "working_hours": {"startTime": "11:00", "endTime": "20:00"}, "breaks": {"startTime": "14:00", "endTime": "15:00"}},

    {"id": "s1_c6", "name": "Cem Tekin", "title": "Medikal Estetisyen", "avatar": "👨🏽‍⚕️", "company_id": "c6", "service_ids": [1, 4], "working_hours": {"startTime": "09:00", "endTime": "18:00"}, "breaks": {"startTime": "12:00", "endTime": "13:00"}},
    {"id": "s2_c6", "name": "Sinan Gül", "title": "Lazer & Epilasyon", "avatar": "👨🏻‍⚕️", "company_id": "c6", "service_ids": [2], "working_hours": {"startTime": "10:00", "endTime": "19:00"}, "breaks": {"startTime": "13:00", "endTime": "14:00"}},
    {"id": "s3_c6", "name": "Buse Çelik", "title": "Cilt Bakım Baş Uzmanı", "avatar": "👩🏻‍🦱", "company_id": "c6", "service_ids": [1, 3], "working_hours": {"startTime": "09:00", "endTime": "17:00"}, "breaks": {"startTime": "12:30", "endTime": "13:30"}},
    {"id": "s4_c6", "name": "Gizem Şen", "title": "Zayıflama ve Estetik", "avatar": "👩🏽‍🦳", "company_id": "c6", "service_ids": [2, 4], "working_hours": {"startTime": "11:00", "endTime": "20:00"}, "breaks": {"startTime": "14:00", "endTime": "15:00"}}
]

import shutil

for f_path, default_data in [(STAFF_FILE, DEFAULT_STAFF), (SECTORS_FILE, DEFAULT_SECTORS_DATA), (COMPANIES_FILE, DEFAULT_COMPANIES)]:
    if os.path.isdir(f_path):
        shutil.rmtree(f_path)
    if not os.path.exists(f_path) or os.path.getsize(f_path) < 5:
        with open(f_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)

# Migrate existing companies JSON to include dashboard credentials
def _migrate_company_credentials():
    companies = get_companies_from_file()
    changed = False
    code_map = {"c1": ("INK001", "ink2026"), "c2": ("TAT001", "tat2026"), "c3": ("ZHN001", "zhn2026"), "c4": ("EMP001", "emp2026"), "c5": ("EST001", "est2026"), "c6": ("PGL001", "pgl2026")}
    for comp in companies:
        if "dashboard_code" not in comp:
            fallback = code_map.get(comp["id"], (f"CMP{comp['id'].upper()}", f"pass{comp['id']}"))
            comp["dashboard_code"] = fallback[0]
            comp["dashboard_password_hash"] = hash_password(fallback[1])
            changed = True
    if changed:
        with open(COMPANIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(companies, f, ensure_ascii=False, indent=4)

def get_staff_from_file():
    with open(STAFF_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_sectors_from_file():
    with open(SECTORS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_companies_from_file():
    with open(COMPANIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

_migrate_company_credentials()

# Removed duplicate routes

@app.get("/api/companies")
async def get_companies():
    return get_companies_from_file()

@app.post("/api/companies")
async def update_companies(request: Request, admin: dict = Depends(get_current_admin)):
    data = await request.json()
    with open(COMPANIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return {"status": "success"}

# Global settings endpoints removed. Settings are now tied to companies.

@app.post("/api/company/settings")
async def update_company_settings(request: Request, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    data = await request.json()
    companies = get_companies_from_file()
    for c in companies:
        if c["id"] == admin["company_id"]:
            c["brand_color"] = data.get("brand_color", c.get("brand_color"))
            c["logo_url"] = data.get("logo_url", c.get("logo_url"))
            
            # Init settings block if not present
            if "settings" not in c:
                c["settings"] = DEFAULT_SETTINGS.copy()
            
            # Update working hours and settings
            s_data = data.get("settings", {})
            for k in ["startTime", "endTime", "intervalMinutes", "closedDays", "breakStartTime", "breakEndTime", "hasBreak"]:
                if k in s_data:
                    c["settings"][k] = s_data[k]
                    
            break
    
    with open(COMPANIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(companies, f, ensure_ascii=False, indent=4)
        
    log_action(db, admin, "BRANDING_UPDATE", "Kurumsal kimlik (renk/logo) güncellendi.")
    return {"status": "success"}

@app.get("/api/sectors")
async def get_sectors():
    return get_sectors_from_file()

@app.post("/api/sectors")
async def update_sectors(request: Request, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    data = await request.json()
    with open(SECTORS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    log_action(db, admin, "SECTORS_UPDATE", "Hizmet kataloğu senkronize edildi.")
    return {"status": "success"}

@app.get("/api/staff")
async def get_staff():
    return get_staff_from_file()

@app.post("/api/staff")
async def update_staff(request: Request, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    data = await request.json()
    with open(STAFF_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    log_action(db, admin, "STAFF_UPDATE", f"Personel listesi güncellendi. Toplam: {len(data)}")
    return {"status": "success"}

@app.get("/api/my-appointments")
async def my_appointments(phone: str, db: Session = Depends(get_db)):
    import re
    clean_phone = re.sub(r'\D', '', phone)
    
    companies = get_companies_from_file()
    sectors = get_sectors_from_file()
    
    # Tüm randevuları çekip python'da filtrelemek SQLite için en kolayıdır
    all_appointments = db.query(Appointment).order_by(Appointment.created_at.desc()).all()
    appointments = []
    for a in all_appointments:
        if a.user_email and re.sub(r'\D', '', a.user_email) == clean_phone:
            appointments.append(a)

    res = []
    print(f"[DEBUG] Fetching appointments for {clean_phone}. Total in DB: {len(all_appointments)}")
    for app in appointments:
        comp_id = str(app.company_id).strip() if app.company_id else ""
        comp = next((c for c in companies if str(c["id"]).strip() == comp_id), None)
        sect = next((s for s in sectors if comp and str(s["id"]).strip() == str(comp["sector_id"]).strip()), None)
        
        print(f"[DEBUG] App ID: {app.id}, Comp ID in DB: '{app.company_id}', Found Comp: {comp['name'] if comp else 'None'}, Found Sect: {sect['name'] if sect else 'None'}")
        
        res.append({
            "id": app.external_id,
            "db_id": app.id,
            "cancel_token": app.cancel_token,
            "service_name": app.service_name,
            "company_name": comp["name"] if comp else "Bilinmeyen Şirket",
            "sector_name": sect["name"] if sect else "Şube", 
            "staff_name": app.staff_name or "Belirtilmedi",
            "date": app.appointment_date,
            "time": app.appointment_time,
            "amount": app.amount,
            "status": app.status,
            "created_at": app.created_at.isoformat() if app.created_at else None,
            "theme_accent": sect["theme"]["accent"] if sect and "theme" in sect else "#8B5CF6"
        })
    return res

@app.get("/api/admin/analytics")
async def get_analytics(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    company_id = admin.get("company_id")
    
    # 1. Daily Revenue (Last 7 Days)
    today = datetime.utcnow().date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    revenue_trend = []
    
    for day in days:
        day_str = day.isoformat()
        total = db.query(func.sum(Appointment.amount)).filter(
            Appointment.company_id == company_id,
            Appointment.appointment_date == day_str,
            Appointment.status != AppointmentStatus.CANCELLED.value
        ).scalar() or 0
        revenue_trend.append({"date": day.strftime("%d %b"), "amount": float(total)})
        
    # 2. Service Popularity
    service_counts = db.query(
        Appointment.service_name, 
        func.count(Appointment.id)
    ).filter(
        Appointment.company_id == company_id
    ).group_by(Appointment.service_name).all()
    
    popularity = [{"name": s[0], "count": s[1]} for s in service_counts]
    
    # 3. Staff Performance
    staff_stats = db.query(
        Appointment.staff_name,
        func.sum(Appointment.amount)
    ).filter(
        Appointment.company_id == company_id,
        Appointment.status != AppointmentStatus.CANCELLED.value
    ).group_by(Appointment.staff_name).all()
    
    performance = [{"name": s[0] or "Atanmamış", "revenue": float(s[1] or 0)} for s in staff_stats]

    return {
        "revenue_trend": revenue_trend,
        "service_popularity": popularity,
        "staff_performance": performance
    }

@app.get("/api/admin/appointments")
async def admin_appointments(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    query = db.query(Appointment).order_by(Appointment.created_at.desc())
    if admin.get("company_id"):
        query = query.filter(Appointment.company_id == admin["company_id"])
    return query.all()

@app.delete("/api/admin/appointments/{app_id}")
async def admin_delete_appt(app_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    appt = db.query(Appointment).filter(Appointment.id == app_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Not found")
    if admin.get("company_id") and appt.company_id != admin["company_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    db.delete(appt)
    db.commit()
    return {"status": "success"}

@app.delete("/api/admin/appointments/clear-all")
async def admin_clear_all_appts(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    query = db.query(Appointment)
    if admin.get("company_id"):
        query = query.filter(Appointment.company_id == admin["company_id"])
    deleted_count = query.delete(synchronize_session=False)
    db.commit()
    return {"status": "success", "count": deleted_count}

@app.post("/api/admin/appointments/{app_id}/cancel")
async def admin_cancel_appt(app_id: int, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    appt = db.query(Appointment).filter(Appointment.id == app_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Not found")
    appt.status = AppointmentStatus.CANCELLED.value
    db.commit()
    return {"status": "success"}

@app.post("/api/admin/appointments/{app_id}/complete")
async def admin_complete_appt(app_id: int, request: Request, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    data = await request.json()
    appt = db.query(Appointment).filter(Appointment.id == app_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Not found")
    
    final_price = data.get("final_price", appt.amount)
    payment_method = data.get("payment_method", "Nakit")
    
    appt.status = AppointmentStatus.COMPLETED.value
    appt.admin_notes = f"{appt.admin_notes or ''} [Ödeme: {final_price} TL - {payment_method}]".strip()
    
    db.commit()
    log_action(db, admin, "APPOINTMENT_COMPLETE", f"Randevu tamamlandı. Tutar: {final_price} TL, Yöntem: {payment_method}")
    return {"status": "success"}

@app.post("/api/admin/appointments/create")
async def admin_create_appt(request: PaymentIntentRequest, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    payment_id = f"manual_{str(uuid.uuid4())[:8]}"
    db_appointment = Appointment(
        external_id=payment_id,
        service_name=request.service_name,
        staff_name=request.staff_name,
        company_id=request.company_id,
        user_name=request.customer_name,
        user_email=request.customer_phone,
        appointment_date=request.appointment_date,
        appointment_time=request.appointment_time,
        amount=request.deposit_amount,
        status=AppointmentStatus.CONFIRMED.value,
        cancel_token=str(uuid.uuid4())
    )
    db.add(db_appointment)
    db.commit()

    # Send SMS Confirmation for Manual Booking
    try:
        from app.services.sms import sms_service
        msg = f"Sayın {db_appointment.user_name}, {db_appointment.appointment_date} {db_appointment.appointment_time} randevunuz manuel olarak oluşturulmuştur."
        import asyncio
        asyncio.create_task(sms_service.send_sms(db_appointment.user_email, msg))
    except Exception as e:
        print(f"Manual SMS Confirmation error: {e}")

    return {"status": "success"}

@app.post("/api/admin/appointments/{app_id}/notes")
async def admin_notes_appt(app_id: int, request: Request, db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    data = await request.json()
    appt = db.query(Appointment).filter(Appointment.id == app_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Not found")
    appt.admin_notes = data.get("note", "")
    db.commit()
    return {"status": "success", "note": appt.admin_notes}

@app.post("/api/reviews")
async def create_review(req: ReviewRequest, db: Session = Depends(get_db)):
    review = Review(appointment_id=req.appointment_id, rating=req.rating, comment=req.comment)
    db.add(review)
    db.commit()
    return {"status": "success"}

@app.get("/api/reviews")
async def get_public_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    out = []
    for r in reviews:
        # Daha esnek bir filtreleme: Yorumu olan her şeyi veya yüksek puanları göster
        if not r.comment and r.rating < 3:
             continue
        appt = db.query(Appointment).filter(Appointment.id == r.appointment_id).first()
        out.append({
            "id": r.id, 
            "rating": r.rating, 
            "comment": r.comment,
            "created_at": r.created_at,
            "user_name": appt.user_name if appt else "Değerli Müşterimiz",
            "service_name": appt.service_name if appt else "Hizmet",
            "company_id": appt.company_id if appt else (appt.external_id.split('_')[1] if appt and appt.external_id.startswith('manual_') else None)
        })
    return out

@app.get("/api/admin/reviews")
async def admin_reviews(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    out = []
    for r in reviews:
        appt = db.query(Appointment).filter(Appointment.id == r.appointment_id).first()
        if admin.get("company_id") and appt and appt.company_id != admin["company_id"]:
            continue
        out.append({
            "id": r.id, 
            "rating": r.rating, 
            "comment": r.comment,
            "created_at": r.created_at,
            "user_name": appt.user_name if appt else "Bilinmeyen Başvuru"
        })
    return out

@app.get("/api/admin/audit-logs")
async def admin_audit_logs(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    query = db.query(AuditLog).order_by(AuditLog.created_at.desc())
    if admin.get("company_id"):
        query = query.filter(AuditLog.company_id == admin["company_id"])
    return query.limit(100).all()

@app.get("/api/admin/analytics")
async def admin_analytics(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    query = db.query(Appointment)
    if admin.get("company_id"):
        query = query.filter(Appointment.company_id == admin["company_id"])
    all_apps = query.all()
    total_rev = sum(a.amount for a in all_apps if a.status == AppointmentStatus.CONFIRMED.value)
    pending = sum(1 for a in all_apps if a.status == AppointmentStatus.PENDING.value)
    cancelled = sum(1 for a in all_apps if a.status == AppointmentStatus.CANCELLED.value)
    confirmed = sum(1 for a in all_apps if a.status == AppointmentStatus.CONFIRMED.value)
    return {
        "revenue": total_rev,
        "total": len(all_apps),
        "pending": pending,
        "cancelled": cancelled,
        "confirmed": confirmed
    }

@app.get("/api/admin/analytics/charts")
async def admin_analytics_charts(db: Session = Depends(get_db), admin: dict = Depends(get_current_admin)):
    """
    Returns chart data:
    - daily_revenue: last 14 days of revenue (date, amount, count)
    - service_popularity: service name -> count mapping
    - hourly_heatmap: hour -> appointment count
    """
    query = db.query(Appointment)
    if admin.get("company_id"):
        query = query.filter(Appointment.company_id == admin["company_id"])
    all_apps = query.all()
    
    # 1. Daily Revenue Trend (last 14 days)
    today = datetime.utcnow().date()
    daily_data = {}
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        daily_data[d.isoformat()] = {"revenue": 0, "count": 0}
    
    for a in all_apps:
        if a.status != AppointmentStatus.CONFIRMED.value:
            continue
        date_str = str(a.appointment_date).split("T")[0] if a.appointment_date else None
        if date_str and date_str in daily_data:
            daily_data[date_str]["revenue"] += a.amount or 0
            daily_data[date_str]["count"] += 1
    
    daily_revenue = [{"date": k, "revenue": v["revenue"], "count": v["count"]} for k, v in daily_data.items()]
    
    # 2. Service Popularity
    service_counts = {}
    for a in all_apps:
        name = a.service_name or "Bilinmeyen"
        service_counts[name] = service_counts.get(name, 0) + 1
    
    service_popularity = [{"name": k, "count": v} for k, v in sorted(service_counts.items(), key=lambda x: -x[1])[:8]]
    
    # 3. Hourly Heatmap
    hourly = {}
    for a in all_apps:
        if a.appointment_time:
            hour = a.appointment_time.split(":")[0]
            hourly[hour] = hourly.get(hour, 0) + 1
    
    hourly_heatmap = [{"hour": k, "count": v} for k, v in sorted(hourly.items())]
    
    # 4. Company Revenue Breakdown
    company_rev = {}
    for a in all_apps:
        if a.status == AppointmentStatus.CONFIRMED.value:
            cid = a.company_id or "Bilinmeyen"
            company_rev[cid] = company_rev.get(cid, 0) + (a.amount or 0)
    
    company_breakdown = [{"company_id": k, "revenue": v} for k, v in sorted(company_rev.items(), key=lambda x: -x[1])]
    
    return {
        "daily_revenue": daily_revenue,
        "service_popularity": service_popularity,
        "hourly_heatmap": hourly_heatmap,
        "company_breakdown": company_breakdown
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
