
import psycopg2

conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


# 1. Добавление / обновление
def upsert(name, phone):
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()


# 2. Поиск
def search(pattern):
    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    return cur.fetchall()


# 3. Пагинация
def get_page(limit, offset):
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    return cur.fetchall()


# 4. Удаление
def delete(value):
    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()


# 5. Массовая вставка
def insert_many(names, phones):
    cur.execute(
        "CALL insert_many_contacts(%s, %s, NULL)",
        (names, phones)
    )
    conn.commit()


cur.close()
conn.close()
