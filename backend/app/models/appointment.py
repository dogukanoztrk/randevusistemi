from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean
from sqlalchemy.orm import declarative_base

import enum
import hashlib
from datetime import datetime

Base = declarative_base()

def hash_password(password: str) -> str:
    return hashlib.sha256(f"dita_salt_2026_{password}".encode('utf-8')).hexdigest()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AppointmentStatus(enum.Enum):
    PENDING = "Beklemede"
    CONFIRMED = "Kesinleşti"
    CANCELLED = "İptal Edildi"
    FAILED = "Ödeme Başarısız"
    COMPLETED = "Tamamlandı"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True)   # Payment session UUID
    payment_id = Column(String, nullable=True)              # Iyzico/Shopier payment ID for refund
    cancel_token = Column(String, unique=True, nullable=True, index=True)  # Secure cancellation token
    service_name = Column(String, nullable=True)
    staff_name = Column(String, nullable=True)
    company_id = Column(String, nullable=True)
    user_name = Column(String)
    user_email = Column(String)
    admin_notes = Column(String, nullable=True)
    appointment_date = Column(String)
    appointment_time = Column(String)
    amount = Column(Float)
    status = Column(String, default=AppointmentStatus.PENDING.value)
    reminded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, index=True)
    admin_name = Column(String)
    action = Column(String) # e.g. "STAFF_UPDATE", "PRICE_CHANGE"
    detail = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer)
    rating = Column(Integer)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
