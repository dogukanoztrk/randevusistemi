# DiTA - Premium Appointment Booking System

DiTA is a standalone, luxury-themed appointment booking application built with Vue 3 and FastAPI.

## Project Structure

- `/src`: Vue 3 Frontend (Vite, Pinia, Tailwind CSS)
- `/backend`: FastAPI Backend (SQLAlchemy, SQLite, Pydantic)

## Getting Started

### Frontend
1. Navigate to the root directory.
2. Install dependencies: `npm install`
3. Run development server: `npm run dev`
4. Access at: `http://localhost:5173/randevu`

### Backend
1. Navigate to `/backend`.
2. Create a virtual environment: `python -m venv venv`
3. Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Run API server: `python -m app.main`
6. API Documentation: `http://localhost:8000/docs`

## Customization
- **Theme**: Modify `tailwind.config.js` and `src/style.css` for aesthetic changes.
- **Appointments**: Logic is managed in `src/stores/appointment.ts` and `backend/app/main.py`.

---
*DiTA Executive Luxury Design System v3.2*
