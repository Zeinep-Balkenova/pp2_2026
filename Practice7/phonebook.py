import psycopg2
import csv
from connect import get_connection

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

# --- ИМПОРТ ИЗ CSV ---
def import_from_csv(filename):
    with open(filename, mode='r') as f:
        reader = csv.reader(f)
        next(reader)  # Пропуск заголовка
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany("INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING", list(reader))
                conn.commit()

# --- ДОБАВЛЕНИЕ ---
def add_contact(name, phone):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
            conn.commit()

# --- ПОИСК (ФИЛЬТРЫ) ---
def query_contacts(filter_type, value):
    query = ""
    if filter_type == "name":
        query = "SELECT * FROM contacts WHERE name ILIKE %s"
        value = f"%{value}%"
    elif filter_type == "prefix":
        query = "SELECT * FROM contacts WHERE phone LIKE %s"
        value = f"{value}%"
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (value,))
            return cur.fetchall()

# --- УДАЛЕНИЕ ---
def delete_contact(identifier):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Удаляем либо по имени, либо по номеру
            cur.execute("DELETE FROM contacts WHERE name = %s OR phone = %s", (identifier, identifier))
            conn.commit()

