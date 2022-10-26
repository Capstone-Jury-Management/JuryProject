import sqlite3
from collections import OrderedDict

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def sqlite_row_to_OrderedDict(row):
    r = OrderedDict()
    for k in row.keys():
        r[k] = row[k]
    return r

def sqlite_result_to_list_of_OrderedDict(result):
    return [sqlite_row_to_OrderedDict(row) for row in result]

def search_jurors(**kwargs):
    query = 'SELECT juror_id, first_name, last_name, birth_date, phone, ssn FROM JUROR'
    if 'ssn' in kwargs and kwargs['ssn'] and len(kwargs['ssn']) == 11:
        query += ' WHERE ssn = "' + kwargs['ssn'] + '"'
    else:
        valid_keys = ['first_name', 'last_name', 'birth_date', 'phone']
        conditions = ' AND '.join([k + ' = "' + kwargs[k] + '"' for k in valid_keys if k in kwargs and kwargs[k]])
        if conditions:
            query += ' WHERE ' + conditions
    conn = get_db_connection()
    result = conn.execute(query).fetchall()
    conn.close()
    return sqlite_result_to_list_of_OrderedDict(result)

def get_juror(id):
    query = 'SELECT juror_id, first_name, last_name, birth_date, phone, ssn FROM JUROR WHERE juror_id = ' + id
    conn = get_db_connection()
    row = conn.execute(query).fetchone()
    conn.close()
    return sqlite_row_to_OrderedDict(row)
