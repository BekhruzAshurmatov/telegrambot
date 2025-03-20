import psycopg2

def connection():
    conn = psycopg2.connect(host="localhost",
                            dbname="postgres",
                            user="postgres",
                            password="iamcharlie21",
                            port="5432")
    cursor = conn.cursor()
    return cursor, conn

def create_table():
    cursor,conn = connection()
    cursor.execute('''CREATE TABLE IF NOT EXISTS zayavki_tg (
                   id SERIAL PRIMARY KEY,
                   tg_id BIGINT UNIQUE,
                   name VARCHAR,
                   phone VARCHAR,
                   age VARCHAR)''')
    conn.commit()
    return cursor, conn

def check_user_exists(tg_id):
    cursor, conn = connection()
    cursor.execute('''SELECT * FROM zayavki_tg WHERE tg_id = %s''', (tg_id,))
    user = cursor.fetchall()
    conn.commit()
    return user


def save_data(tg_id, name, phone, age):
    cursor, conn = create_table()
    cursor.execute('''INSERT INTO zayavki_tg (tg_id, name, phone, age)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (tg_id)
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        phone = EXCLUDED.phone,
                        age = EXCLUDED.age''',
                   (tg_id, name, phone, age))
    conn.commit()