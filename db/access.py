import os
import mysql.connector
from collections import OrderedDict
from .encryption import tokenize, detokenize

def get_db_connection():
    cnx = mysql.connector.connect(
        host=os.environ['RDS_HOSTNAME'],
        port=os.environ['RDS_PORT'],
        database=os.environ['RDS_DB_NAME'],
        user=os.environ['RDS_USERNAME'],
        password=os.environ['RDS_PASSWORD'])
    return cnx

def encrypt_if_encrypted(value, key, encrypted_keys):
    return tokenize(str(value)) if key in encrypted_keys else value

def decrypt_if_encrypted(value, key, encrypted_keys):
    return detokenize(value) if key in encrypted_keys else value

def row_to_OrderedDict(row, keys, encrypted_keys):
    r = OrderedDict()
    for i, k in enumerate(keys):
        r[k] = decrypt_if_encrypted(row[i], k, encrypted_keys)
    return r

def result_to_list_of_OrderedDict(result, keys, encrypted_keys):
    return [row_to_OrderedDict(row, keys, encrypted_keys) for row in result]

def search_jurors(**kwargs):
    keys = ['participant_id', 'last_name', 'first_name', 'dob', 'ssn', 'mvc_id']
    encrypted_keys = ['dob', 'ssn', 'mvc_id']
    search_keys = ['last_name', 'first_name', 'dob', 'ssn', 'mvc_id']
    encrypted_search_keys = ['dob', 'ssn', 'mvc_id']
    query = 'SELECT ' + ', '.join(keys) + ' FROM PARTICIPANTS'
    conditions = ' AND '.join([key + ' = "' + \
        encrypt_if_encrypted(kwargs[key], key, encrypted_search_keys) + \
        '"' for key in search_keys if key in kwargs and kwargs[key]])
    if conditions:
        query += ' WHERE ' + conditions
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result_to_list_of_OrderedDict(result, keys, encrypted_keys)

def get_juror(juror_id):
    keys = ['participant_id', 'summons_date', 'undeliverable', 'last_name', 'first_name', 'address', 'city', 'state', 'zip', 'county',
            'dob', 'ssn', 'mvc_id']
    encrypted_keys = ['dob', 'ssn', 'mvc_id']
    query = 'SELECT ' + ', '.join(keys) + ' FROM PARTICIPANTS WHERE participant_id = ' + juror_id
    cnx = get_db_connection()
    cursor = cnx.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    cnx.close()
    return row_to_OrderedDict(row, keys, encrypted_keys) if row else None
