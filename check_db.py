import sqlite3
import json

def check_data():
    conn = sqlite3.connect('backend/dita_appointments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT company_id, service_name, staff_name FROM appointments LIMIT 5")
    rows = cursor.fetchall()
    print("Appointments in DB:", rows)
    conn.close()

    with open('backend/dita_companies.json', 'r', encoding='utf-8') as f:
        companies = json.load(f)
        print("Companies in JSON IDs:", [c['id'] for c in companies])

if __name__ == "__main__":
    check_data()
