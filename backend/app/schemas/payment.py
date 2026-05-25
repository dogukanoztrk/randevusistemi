from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class AppointmentInfo(BaseModel):
    date: str
    time: str
    user_name: str
    user_email: str
    user_phone: Optional[str] = None

class CreatePaymentIntentRequest(BaseModel):
    appointment_info: AppointmentInfo
    deposit_amount: float = Field(..., gt=0)
    currency: str = "TRY"

class CreatePaymentIntentResponse(BaseModel):
    payment_id: str
    payment_url: str  # URL to redirect the user to Iyzico/Shopier
    token: Optional[str] = None
    status: str

class IyzicoCallback(BaseModel):
    status: str  # 'success' or 'failure'
    paymentId: str
    conversationId: Optional[str] = None
    mdStatus: Optional[int] = None
    # Add other Iyzico specific fields as needed
    raw_result: Optional[Dict[str, Any]] = None

class PaymentCallbackResponse(BaseModel):
    status: str
    message: str
