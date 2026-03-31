import psycopg2
from config import load_config

def get_conn():
    return psycopg2.connect(**load_config())

# 1. Create table
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
    
# 2. Insert from console
def insert_from_csv(filepath='contacts.csv'):
    import csv
    with get_conn() as conn:
        with conn.cursor() as cur, open(filepath, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    """ INSERT INTO phonebook (username, phone)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING""",
                    (row['username'], row['phone'])
                )
        conn.commit()
    print("CSV imported.")
    
# 3. Insert from console
def insert_from_console():
    username = input("Username: ").strip()
    phone = input("Phone: ").strip()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """ INSERT INTO phonebook (username, phone)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING""",
                (username, phone)
            )
        conn.commit()
    print("Contact added.")

# 4. Update
def update_contact():
    username = input("Enter username of contact to update: ").strip()
    print("What to update? 1) Username  2) Phone")
    choice = input("Choice: ").strip()
    
    if choice == '1':
        new_val = input("New username: ").strip()
        update_query = "UPDATE phonebook SET username = %s WHERE username = %s"
    elif choice == '2':
        new_val = input("New phone: ").strip()
        update_query = "UPDATE phonebook SET phone = %s WHERE username = %s"
    else:
        print("Invalid choice")
        return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(update_query, (new_val, username))
            
    print("Updated.")
    
# 5 Query / Search
def query_contacts():
    print("Search by:   1) Username   2) Phone prefix   3) All")
    
    choice = input("Choice: ").strip()
    if choice not in {'1', '2', '3'}:
        print("Invalid choice")
        return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            if choice == '1':
                name = input("Username: ").strip()
                cur.execute(
                    "SELECT * FROM phonebook WHERE username ILIKE %s",
                    (f'%{name}%',)
                )
            elif choice == '2':
                prefix = input("Enter phone prefix: ").strip()
                cur.execute(
                    "SELECT * FROM phonebook WHERE phone LIKE %s",
                    (f"{prefix}%",)
                )
            else:
                cur.execute("SELECT * FROM phonebook ORDER BY username")
            rows = cur.fetchall()
    
    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")
    
# 6 Delete
def delete_contact():
    print("Delele by:   1) Username   2) Phone")
    choice = input("Choice: ").strip()
    
    if choice not in {'1', '2'}:
        print("Invalid choice")
        return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            if choice == '1':
                username = input("Username: ").strip()
                cur.execute(
                    "DELETE FROM phonebook WHERE username = %s",
                    (username,)
                )
            else:
                phone = input("Phone: ").strip()
                cur.execute(
                    "DELETE FROM phonebook WHERE phone = %s",
                    (phone,)
                )

            if cur.rowcount == 0:
                print("No contact found.")
            else:
                print("Deleted.")
    
# MENU
def main():
    create_table()
    
    while True:
        print("PHONEBOOK APP")
        print("1 - Import contacts from CSV")
        print("2 - Add a new contact")
        print("3 - Update a contact")
        print("4 - Search contacts")
        print("5 - Delete a contact")
        print("0 - Exit")
        
        choice = input("Choose an option: ").strip()
        
        if choice == '1':
            insert_from_csv()
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option")

if __name__ == '__main__':
    main()