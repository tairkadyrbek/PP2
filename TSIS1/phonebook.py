import psycopg2
import json
import csv
from config import load_config

def get_conn():
    return psycopg2.connect(**load_config())

# Create tables
def create_tables():
    print("Please run schema.sql first to create tables.")
    print("Example: psql -U your_user -d your_db -f schema.sql")


# 1. Search by pattern
def search_contacts():
    pattern = input("Enter search pattern (name/phone/email): ").strip()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            rows = cur.fetchall()
            
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

# 2. Insert / Update contact
def upsert_contact():
    username = input("Username: ").strip()
    email = input("Email (optional): ").strip() or None
    birthday = input("Birthday (YYYY-MM-DD, optional): ").strip() or None
    group_name = input("Group (Family/Work/Friend/Other): ").strip() or 'Other'
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s, %s, %s)", 
                       (username, email, birthday, group_name))
    
    # Add phones
    print("\nAdd phone numbers (press Enter with empty number to finish)")
    while True:
        phone = input("Phone number: ").strip()
        if not phone:
            break
        phone_type = input("Type (home/work/mobile): ").strip() or 'mobile'
        
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL add_phone(%s, %s, %s)", (username, phone, phone_type))
    
    print("Contact saved!")

# 3. Insert many contacts
def insert_many():
    usernames = []
    phones = []
    
    while True:
        username = input("Username (empty to stop): ").strip()
        if not username:
            break
        phone = input("Phone: ").strip()
        
        usernames.append(username)
        phones.append(phone)
        
    if usernames:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL insert_many_contacts(%s, %s)", (usernames, phones))
        print("Done.")

# 4. Paginated view with navigation
def view_paginated():
    limit  = int(input("Contacts per page(limit): ").strip())
    offset = int(input("Skip (offset): ").strip())
    
    while True:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_page(%s, %s)", (limit, offset))
                rows = cur.fetchall()
        
        if not rows:
            print("No more contacts.")
            break
            
        print(f"\n--- Page {offset//limit + 1} ---")
        for row in rows:
            print(row)
        
        print("\nOptions: [n]ext, [p]rev, [q]uit")
        choice = input("Choice: ").strip().lower()
        
        if choice == 'n':
            offset += limit
        elif choice == 'p':
            offset = max(0, offset - limit)
        elif choice == 'q':
            break

# 5. Delete contact
def delete_contact():
    print("1 - Username, 2 - Phone")
    choice = input("Choice: ").strip()
    
    if choice == '1':
        value = input("Username: ").strip()
        if not value:
            print("Username cannot be empty!")
            return
        p_type = 'username'
    elif choice == '2':
        value = input("Phone: ").strip()
        if not value:
            print("Phone cannot be empty!")
            return
        p_type = 'phone'
    else:
        print("Invalid choice.")
        return
    
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s, %s)", (value, p_type))
        if p_type == 'username':
            print("Contact deleted!")
        else:
            print("Phone number deleted!")
    except Exception as e:
        print(f"Error: {e}")


# 6. Filter by group
def filter_by_group():
    print("\nAvailable groups: Family, Work, Friend, Other")
    group_name = input("Enter group name: ").strip()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name as group_name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                WHERE g.name = %s
            """, (group_name,))
            rows = cur.fetchall()
    
    if rows:
        for row in rows:
            print(row)
    else:
        print(f"No contacts in group '{group_name}'")

# 7. Search by email
def search_by_email():
    email_pattern = input("Enter email pattern: ").strip()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name as group_name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                WHERE c.email ILIKE %s
            """, (f"%{email_pattern}%",))
            rows = cur.fetchall()
    
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

# 8. Sort and view contacts
def view_sorted():
    print("\nSort by:")
    print("1 - Name")
    print("2 - Birthday")
    print("3 - Date added")
    choice = input("Choice: ").strip()
    
    sort_map = {
        '1': 'c.username',
        '2': 'c.birthday',
        '3': 'c.created_at'
    }
    
    sort_field = sort_map.get(choice, 'c.username')
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT c.id, c.username, c.email, c.birthday, g.name as group_name, c.created_at
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                ORDER BY {sort_field}
            """)
            rows = cur.fetchall()
    
    for row in rows:
        print(row)

# 9. Export to JSON
def export_to_json():
    filename = input("Enter filename (e.g., contacts.json): ").strip()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Get all contacts
            cur.execute("""
                SELECT c.id, c.username, c.email, c.birthday, g.name as group_name
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
            """)
            contacts_rows = cur.fetchall()
            
            contacts = []
            for row in contacts_rows:
                contact_id, username, email, birthday, group_name = row
                
                # Get phones for this contact
                cur.execute("""
                    SELECT phone, type FROM phones WHERE contact_id = %s
                """, (contact_id,))
                phones_rows = cur.fetchall()
                
                contact_data = {
                    'username': username,
                    'email': email,
                    'birthday': str(birthday) if birthday else None,
                    'group': group_name,
                    'phones': [{'phone': p[0], 'type': p[1]} for p in phones_rows]
                }
                contacts.append(contact_data)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(contacts)} contacts to {filename}")

# 10. Import from JSON
def import_from_json():
    filename = input("Enter filename (e.g., contacts.json): ").strip()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return
    
    for contact in contacts:
        username = contact['username']
        email = contact.get('email')
        birthday = contact.get('birthday')
        group_name = contact.get('group', 'Other')
        phones = contact.get('phones', [])
        
        # Check if contact exists
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
                existing = cur.fetchone()
        
        if existing:
            action = input(f"Contact '{username}' exists. [s]kip or [o]verwrite? ").strip().lower()
            if action != 'o':
                continue
        
        # Upsert contact
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s, %s, %s)", 
                           (username, email, birthday, group_name))
        
        # Add phones
        for phone_data in phones:
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("CALL add_phone(%s, %s, %s)", 
                               (username, phone_data['phone'], phone_data['type']))
    
    print(f"Import complete!")

# 11. Import from CSV
def import_from_csv():
    filename = input("Enter CSV filename: ").strip()
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                username = row.get('username', '').strip()
                email = row.get('email', '').strip() or None
                birthday = row.get('birthday', '').strip() or None
                group_name = row.get('group', 'Other').strip()
                phone = row.get('phone', '').strip()
                phone_type = row.get('phone_type', 'mobile').strip()
                
                if not username:
                    continue
                
                with get_conn() as conn:
                    with conn.cursor() as cur:
                        cur.execute("CALL upsert_contact(%s, %s, %s, %s)", 
                                   (username, email, birthday, group_name))
                        
                        if phone:
                            cur.execute("CALL add_phone(%s, %s, %s)", 
                                       (username, phone, phone_type))
        
        print("CSV import complete!")
    except FileNotFoundError:
        print(f"File {filename} not found.")

# 12. Add phone to existing contact
def add_phone_to_contact():
    username = input("Contact username: ").strip()
    phone = input("Phone number: ").strip()
    phone_type = input("Type (home/work/mobile): ").strip() or 'mobile'
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s)", (username, phone, phone_type))
    
    print("Phone added!")

# 13. Move contact to group
def move_contact_to_group():
    username = input("Contact username: ").strip()
    group_name = input("New group (Family/Work/Friend/Other): ").strip()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s)", (username, group_name))
    
    print(f"Moved '{username}' to group '{group_name}'")


# MAIN MENU

def main():
    print("PhoneBook - TSIS1 Extended Contact Management")
    print("Run schema.sql first if tables don't exist.\n")
    
    while True:
        print("\n" + "="*50)
        print("PHONEBOOK MENU")
        print("="*50)
        print("\n--- SEARCH & VIEW ---")
        print("1  - Search contacts (name/phone/email)")
        print("2  - Filter by group")
        print("3  - Search by email")
        print("4  - View sorted (name/birthday/date)")
        print("5  - View paginated (with navigation)")
        
        print("\n--- ADD & UPDATE ---")
        print("6  - Add/Update contact")
        print("7  - Add phone to contact")
        print("8  - Move contact to group")
        print("9  - Add many contacts")
        
        print("\n--- IMPORT/EXPORT ---")
        print("10 - Export to JSON")
        print("11 - Import from JSON")
        print("12 - Import from CSV")
        
        print("\n--- DELETE ---")
        print("13 - Delete contact / phone number")
        
        print("\n0  - Exit")
        print("="*50)
        
        choice = input("\nChoose an option: ").strip()

        if choice == '1': search_contacts()
        elif choice == '2': filter_by_group()
        elif choice == '3': search_by_email()
        elif choice == '4': view_sorted()
        elif choice == '5': view_paginated()
        elif choice == '6': upsert_contact()
        elif choice == '7': add_phone_to_contact()
        elif choice == '8': move_contact_to_group()
        elif choice == '9': insert_many()
        elif choice == '10': export_to_json()
        elif choice == '11': import_from_json()
        elif choice == '12': import_from_csv()
        elif choice == '13': delete_contact()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option")

if __name__ == '__main__':
    main()