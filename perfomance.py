import psycopg2
from random import randint, choice
import string
import threading
import time

letters = string.ascii_lowercase + string.ascii_uppercase

def set_db_data(query, data):
    with psycopg2.connect(
            host='localhost',
            port=15432,
            database="postgres",
            user="postgres",
            password="postgres") as conn:

        cur = conn.cursor()

        cur.execute(query, data)
        conn.commit()

def write():
    query = '''INSERT INTO public.books (id, category_id, author, title, year) VALUES (%s,%s,%s,%s,%s)'''
    items = []
    for i in range(10000):
        items.append(
            (
            randint(1, 999999999),
            randint(1, 5),
            ''.join(choice(letters) for i in range(randint(5,20))),
            ''.join(choice(letters) for i in range(randint(5,50))),
            randint(1900, 2022)
            )
        )
    start_time = time.time()
    for i in range(len(items)):
        set_db_data(query=query, data=items[i-1])
    sd = time.time() - start_time
    print(sd)
    #print('Thread duration for 100000 rows: {sd} seconds')


for i in range(5):
    threading.Thread(target=write).start()