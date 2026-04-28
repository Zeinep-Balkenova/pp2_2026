import psycopg2
import json
import csv
from connect import get_connection


def search_all(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    print(f"\nFound {len(rows)} results for '{query}':")
    for row in rows:
        print(f"  ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Birthday: {row[3]} | Group: {row[4]} | Phone: {row[5]} | Type: {row[6]}")


def filter_by_group():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM groups ORDER BY id")
    groups = cur.fetchall()
    cur.close()
    conn.close()

    print("\nAvailable groups:")
    for g in groups:
        print(f"  {g[0]}. {g[1]}")

    choice = input("Enter group number: ")

    group_id = None
    for g in groups:
        if str(g[0]) == choice:
            group_id = g[0]

    if group_id == None:
        print("Group not found")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.contact_id, c.contact_name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        WHERE c.group_id = %s
        ORDER BY c.contact_name
    """, (group_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if len(rows) == 0:
        print("No contacts in this group")
    else:
        for row in rows:
            print(f"  ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Birthday: {row[3]} | Group: {row[4]}")


def list_sorted():
    print("\nSort by:")
    print("  1. Name")
    print("  2. Birthday")
    print("  3. Date added")
    choice = input("Select: ")

    if choice == '1':
        order = 'contact_name'
    elif choice == '2':
        order = 'birthday'
    elif choice == '3':
        order = 'contact_id'
    else:
        print("Wrong choice, sorting by name")
        order = 'contact_name'

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT c.contact_id, c.contact_name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY {order}
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    for row in rows:
        print(f"  ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Birthday: {row[3]} | Group: {row[4]}")


def paginated_browse():
    limit = int(input("How many contacts per page? "))
    page = 1

    while True:
        offset = (page - 1) * limit

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        print(f"\n--- Page {page} ---")
        if len(rows) == 0:
            print("No more contacts")
            break

        for row in rows:
            print(f"  ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

        cmd = input("\nType 'next', 'prev' or 'quit': ")
        if cmd == 'next':
            page = page + 1
        elif cmd == 'prev':
            if page > 1:
                page = page - 1
            else:
                print("Already on first page")
        elif cmd == 'quit':
            break
        else:
            print("Unknown command")


def add_phone():
    name = input("Enter contact name: ")
    phone = input("Enter phone number: ")
    print("Phone type: 1=home  2=work  3=mobile")
    t = input("Select: ")

    if t == '1':
        ptype = 'home'
    elif t == '2':
        ptype = 'work'
    else:
        ptype = 'mobile'

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("Phone added successfully")
    except Exception as e:
        print(f"Error: {e}")
    cur.close()
    conn.close()


def move_to_group():
    name = input("Enter contact name: ")
    group = input("Enter group name: ")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Contact moved successfully")
    except Exception as e:
        print(f"Error: {e}")
    cur.close()
    conn.close()


def export_to_json():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.contact_id, c.contact_name, c.email, c.birthday::text, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.contact_id
    """)
    contacts = cur.fetchall()

    result = []
    for row in contacts:
        cid = row[0]
        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (cid,))
        phones = cur.fetchall()

        phones_list = []
        for p in phones:
            phones_list.append({'phone': p[0], 'type': p[1]})

        contact_dict = {
            'name': row[1],
            'email': row[2],
            'birthday': row[3],
            'group': row[4],
            'phones': phones_list
        }
        result.append(contact_dict)

    cur.close()
    conn.close()

    filename = input("Enter filename (e.g. contacts.json): ")
    if filename == '':
        filename = 'contacts.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(result)} contacts to {filename}")


def import_from_json():
    filename = input("Enter json filename: ")

    try:
        f = open(filename, 'r', encoding='utf-8')
        contacts = json.load(f)
        f.close()
    except:
        print("File not found or invalid")
        return

    conn = get_connection()
    cur = conn.cursor()

    for c in contacts:
        name = c.get('name', '')
        if name == '':
            continue

        cur.execute("SELECT contact_id FROM contacts WHERE contact_name = %s", (name,))
        existing = cur.fetchone()

        if existing != None:
            print(f"\nContact '{name}' already exists")
            action = input("Type 's' to skip or 'o' to overwrite: ")
            if action != 'o':
                print(f"Skipped '{name}'")
                continue
            contact_id = existing[0]
            cur.execute("UPDATE contacts SET email=%s, birthday=%s WHERE contact_id=%s",
                        (c.get('email'), c.get('birthday'), contact_id))
        else:
            group_id = None
            if c.get('group') != None:
                cur.execute("SELECT id FROM groups WHERE name = %s", (c['group'],))
                g = cur.fetchone()
                if g != None:
                    group_id = g[0]

            cur.execute("""
                INSERT INTO contacts(contact_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s) RETURNING contact_id
            """, (name, c.get('email'), c.get('birthday'), group_id))
            contact_id = cur.fetchone()[0]

        for ph in c.get('phones', []):
            cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                        (contact_id, ph.get('phone'), ph.get('type')))

        conn.commit()
        print(f"Imported '{name}'")

    cur.close()
    conn.close()


def import_csv_extended():
    filename = input("Enter csv file path: ")

    conn = get_connection()
    cur = conn.cursor()

    try:
        f = open(filename, 'r', encoding='utf-8')
        reader = csv.DictReader(f)

        for row in reader:
            name = row.get('name', '')
            phone = row.get('phone', '')
            ptype = row.get('type', 'mobile')
            email = row.get('email', '')
            birthday = row.get('birthday', '')
            group = row.get('group', '')

            if name == '':
                continue

            if email == '':
                email = None
            if birthday == '':
                birthday = None

            group_id = None
            if group != '':
                cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
                g = cur.fetchone()
                if g != None:
                    group_id = g[0]

            cur.execute("SELECT contact_id FROM contacts WHERE contact_name = %s", (name,))
            existing = cur.fetchone()

            if existing != None:
                contact_id = existing[0]
            else:
                cur.execute("""
                    INSERT INTO contacts(contact_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s) RETURNING contact_id
                """, (name, email, birthday, group_id))
                contact_id = cur.fetchone()[0]

            if phone != '':
                cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                            (contact_id, phone, ptype))

            conn.commit()
            print(f"Imported '{name}' from csv")

        f.close()
    except Exception as e:
        print(f"Error: {e}")

    cur.close()
    conn.close()


def show_menu():
    print("\n--- PhoneBook App ---")
    print("1. Search contact")
    print("2. Filter by group")
    print("3. Show all contacts (sorted)")
    print("4. Browse contacts page by page")
    print("5. Add phone to contact")
    print("6. Move contact to group")
    print("7. Export to json")
    print("8. Import from json")
    print("9. Import from csv")
    print("0. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose option: ")

        if choice == '1':
            query = input("Enter search term: ")
            search_all(query)
        elif choice == '2':
            filter_by_group()
        elif choice == '3':
            list_sorted()
        elif choice == '4':
            paginated_browse()
        elif choice == '5':
            add_phone()
        elif choice == '6':
            move_to_group()
        elif choice == '7':
            export_to_json()
        elif choice == '8':
            import_from_json()
        elif choice == '9':
            import_csv_extended()
        elif choice == '0':
            print("Bye!")
            break
        else:
            print("Wrong option, try again")


if __name__ == '__main__':
    main()
