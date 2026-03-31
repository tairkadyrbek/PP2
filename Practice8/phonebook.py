import psycopg2
from config import load_config

def get_conn():
    return psycopg2.connect(**load_config())

# Create table
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        phone    VARCHAR(20) UNIQUE NOT NULL 
    );
    """
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            
    print("Table ready.")

# 1. Search by pattern
def search_contacts():
    pattern = input("Enter search pattern (name or phone): ").strip()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
            rows = cur.fetchall()
            
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

# 2. Insert / Update
def upsert_contact():
    username = input("Username: ").strip()
    phone = input("Phone: ").strip()
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s)", (username, phone))

    print("Done!")

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

# 4. Paginated view
def view_paginated():
    limit  = int(input("Contacts per page(limit): ").strip())
    offset = int(input("Skip (offset): ").strip())
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
            rows = cur.fetchall()
            
    for row in rows:
        print(row)


# 5. Delete contact
def delete_contact():
    print("1 - Username, 2 - Phone")
    choice = input("Choice: ").strip()
    
    if choice == '1':
        value  = input("Username: ").strip()
        p_type = 'username'
    elif choice == '2':
        value  = input("Phone: ").strip()
        p_type = 'phone'
    else:
        print("Invalid choice.")
        return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s, %s)", (value, p_type))

    print("Contact deleted!")

# ── MAIN MENU
def main():
    create_table()
    while True:
        print("PHONEBOOK")
        print("\n1 - Search contacts (by pattern)")
        print("2 - Add / Update a contact")
        print("3 - Add many")
        print("4 - View contacts (with pagination)")
        print("5 - Delete a contact")
        print("0 - Exit")
        print("================================")
        
        choice = input("Choose an option: ").strip()

        if choice == '1': search_contacts()
        elif choice == '2': upsert_contact()
        elif choice == '3': insert_many()
        elif choice == '4': view_paginated()
        elif choice == '5': delete_contact()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option")

if __name__ == '__main__':
    main()