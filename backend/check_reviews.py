from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.appointment import Review, Appointment

engine = create_engine("sqlite:///backend/dita_appointments.db")
Session = sessionmaker(bind=engine)
db = Session()

reviews = db.query(Review).all()
print(f"Total reviews: {len(reviews)}")
for r in reviews:
    appt = db.query(Appointment).filter(Appointment.id == r.appointment_id).first()
    print(f"ID: {r.id}, Rating: {r.rating}, Comment: {r.comment}, Company: {appt.company_id if appt else 'N/A'}")
