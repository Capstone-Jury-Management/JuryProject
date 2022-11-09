import os
from .access import get_db_connection
from .fake_data import fake_participants
from .encryption import tokenize

def init_db():
    cnx = get_db_connection()
    cursor = cnx.cursor()

    db_schema_file_path = 'db/schema.sql'
    with open(db_schema_file_path) as f:
        cursor.execute(f.read().split(';')[0].strip())
        cnx.commit()
    with open(db_schema_file_path) as f:
        cursor.execute(f.read().split(';')[1].strip())
        cnx.commit()

    cursor.execute('SELECT * FROM PARTICIPANTS LIMIT 1')
    row = cursor.fetchone()
    if not row:
        keys = ['summons_date', 'undeliverable', 'last_name', 'first_name', 'address', 'city', 'state', 'zip', 'county',
            'dob', 'ssn', 'mvc_id']
        encrypted_keys = ['dob', 'ssn', 'mvc_id']
        query = 'INSERT INTO PARTICIPANTS (' + ', '.join(keys) + ') VALUES (' + \
            ', '.join(['%s' for _ in keys]) + ')'
        for participant in fake_participants(100):
            for key in encrypted_keys:
                participant[key] = tokenize(str(participant[key]))
            cursor.execute(query, [participant[key] for key in keys])
            cnx.commit()

    cursor.close()
    cnx.close()
