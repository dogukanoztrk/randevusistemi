from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.appointment import Review, Appointment, AppointmentStatus
from datetime import datetime

engine = create_engine("sqlite:///backend/dita_appointments.db")
Session = sessionmaker(bind=engine)
db = Session()

# Create dummy appointments to link reviews to
dummy_data = [
    {"user": "Ahmet Y.", "company": "c1", "service": "Mini Dövme", "rating": 5, "comment": "Harika bir deneyimdi, Kaan Bey çok profesyonel."},
    {"user": "Mehmet K.", "company": "c1", "service": "Orta Boy", "rating": 4, "comment": "İşçilik çok temiz, tavsiye ederim."},
    {"user": "Ayşe S.", "company": "c3", "service": "Bireysel Terapi", "rating": 5, "comment": "Melis Hanım ile görüşmek bana çok iyi geldi."},
    {"user": "Fatma G.", "company": "c5", "service": "Cilt Bakımı", "rating": 5, "comment": "Estetik merkezinden çok memnun kaldım, cildim parlıyor!"},
    {"user": "Buse T.", "company": "c6", "service": "Lazer Epilasyon", "rating": 4, "comment": "Temiz ve güler yüzlü bir şube."},
]

for item in dummy_data:
    appt = Appointment(
        external_id=f"seed_{item['company']}_{datetime.now().timestamp()}",
        service_name=item['service'],
        user_name=item['user'],
        user_email="seed@test.com",
        company_id=item['company'],
        status=AppointmentStatus.CONFIRMED.value,
        amount=100
    )
    db.add(appt)
    db.commit()
    db.refresh(appt)
    
    review = Review(
        appointment_id=appt.id,
        rating=item['rating'],
        comment=item['comment']
    )
    db.add(review)
    db.commit()

print("Database seeded with 5 reviews across different companies.")
