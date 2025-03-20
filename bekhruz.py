# import sqlite3
#
# conn = sqlite3.connect('quiz_bot.db')
# cursor = conn.cursor()
#
# cursor.execute('''PRAGMA foreign_keys = on''')
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS quiz (
#                id INTEGER PRIMARY KEY,
#                name VARCHAR)''')
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS question (
#                id INTEGER PRIMARY KEY,
#                question VARCHAR,
#                answer VARCHAR,
#                wrong1 VARCHAR,
#                wrong2 VARCHAR,
#                wrong3 VARCHAR)''')
#
# cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_content (
#                id INTEGER PRIMARY KEY,
#                quiz_id INTEGER,
#                question_id INTEGER,
#                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
#                FOREIGN KEY (question_id) REFERENCES question (id))''')
#
#
# questions = [
#     ('Bir kunda necha soat bor?', '24', '12', '9', '20'),
#     ('Bir soatda necha minut bor?', '60', '48', '100', '45'),
#     ('Bir minutda necha sekund bor?', '60', '20', '45', '100')
# ]
# cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)''', questions)
#
# quizes = [
#     ('Millioner',),
#     ('Zakovat',),
#     ('Vunderkind',)
# ]
# cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
#
# answer = input("Birlashtirasizmi? (yes/no): ")
# while answer != 'no':
#     quiz_id = int(input("id viktorina: "))
#     question_id = int(input("id savol: "))
#     cursor.execute('''INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)''', [quiz_id, question_id])
#     conn.commit()
#     answer = input("Birlashtirasizmi? (yes/no): ")
#
# conn.commit()

import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="iamcharlie21", port="5432")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS quiz (
               id SERIAL PRIMARY KEY,
               name VARCHAR)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS question (
               id SERIAL PRIMARY KEY,
               question VARCHAR, 
               answer VARCHAR, 
               wrong1 VARCHAR, 
               wrong2 VARCHAR, 
               wrong3 VARCHAR)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_content (
               id SERIAL PRIMARY KEY, 
               quiz_id INTEGER, 
               question_id INTEGER,
               FOREIGN KEY (quiz_id) REFERENCES quiz (id),
               FOREIGN KEY (question_id) REFERENCES question (id))''')


questions = [
    ('Bir kunda necha soat bor?', '24', '12', '9', '20'),
    ('Bir soatda necha minut bor?', '60', '48', '100', '45'),
    ('Bir minutda necha sekund bor?', '60', '20', '45', '100')
]
cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (%s, %s, %s, %s, %s)''', questions)

quizes = [
    ('Millioner',),
    ('Zakovat',),
    ('Vunderkind',)
]
cursor.executemany('''INSERT INTO quiz (name) VALUES (%s)''', quizes)

answer = input("Birlashtirasizmi? (yes/no): ")
while answer != 'no':
    quiz_id = int(input("id viktorina: "))
    question_id = int(input("id savol: "))
    cursor.execute('''INSERT INTO quiz_content (quiz_id, question_id) VALUES (%s, %s)''', [quiz_id, question_id])
    conn.commit()
    answer = input("Birlashtirasizmi? (yes/no): ")

conn.commit()






































