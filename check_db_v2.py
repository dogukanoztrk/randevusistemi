import sqlite3
import json

def check_data():
    conn = sqlite3.connect('backend/dita_appointments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, company_id, service_name, staff_name FROM appointments")
    rows = cursor.fetchall()
    
    with open('backend/dita_companies.json', 'r', encoding='utf-8') as f:
        companies = json.load(f)
    
    comp_ids = [c['id'] for c in companies]
    
    print(f"Company IDs in JSON: {comp_ids}")
    for row in rows:
        db_cid = row[1]
        match = db_cid in comp_ids
        print(f"DB Appointment ID {row[0]}: Company ID '{db_cid}' | Match: {match}")
        if not match:
            # Check for similar IDs
            from difflib import get_close_matches
            matches = get_close_matches(db_cid, comp_ids)
            print(f"  Suggested matches for '{db_cid}': {matches}")

    conn.close()

if __name__ == "__main__":
    check_data()
