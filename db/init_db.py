import sqlite3
from fake_data import fake_persons

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute('''INSERT INTO JUROR (first_name, last_name, birth_date, phone)
    VALUES ("David", "Cohen", "2000-03-21", "7325466520")''')
cur.execute('''INSERT INTO JUROR (first_name, last_name, birth_date, phone)
    VALUES ("Yash", "Patel", "2000-01-01", "9735192324")''')
cur.execute('''INSERT INTO JUROR (first_name, last_name, birth_date, phone)
    VALUES ("Cassandra", "Sehic", "2000-07-31", "7322442946")''')
cur.execute('''INSERT INTO JUROR (first_name, last_name, birth_date, phone)
    VALUES ("Kush", "Patel", "2000-01-01", "2185136493")''')

for juror in fake_persons(1000):
    cur.execute('INSERT INTO JUROR (first_name, last_name, birth_date, phone, ssn) VALUES (?, ?, ?, ?, ?)',
        (juror['first_name'], juror['last_name'], juror['birth_date'], juror['phone'], juror['ssn'])
    )

connection.commit()
connection.close()