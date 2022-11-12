from flask import Flask
from flask import abort
from flask import request

import mysql.connector
import requests


app = Flask(__name__)


def main():
    requests.packages.urllib3.disable_warnings()  # Disable SSL warnings.
    app.run(debug=True, host='0.0.0.0')

    
@app.route('/api/search', methods=['POST'])
def search():
    """
    Form a JSON response with a list of jury participants that match given
    search parameters.
    """

    # Set default response.
    response = {'success': 0}

    # Abort on a bad request.
    if ('first_name' not in request.form
            and 'last_name' not in request.form
            and 'dob' not in request.form
            and 'ssn' not in request.form
            and 'mvc_id' not in request.form):
        abort(400, 'Bad Request. Check data parameters.')

    # Define search parameters and build dynamic SQL query.
    query = ('SELECT participant_id, first_name, middle_name, last_name,\n'
             '   dob, ssn\n'
             'FROM PARTICIPANTS\n'
             'WHERE')

    search = dict()
    if ('first_name' in request.form):
        search['first_name'] = request.form['first_name']
    if ('last_name' in request.form):
        search['last_name'] = request.form['last_name']
    if ('dob' in request.form):
        search['dob'] = tokenize(request.form['dob'])
    if ('ssn' in request.form):
        search['ssn'] = tokenize(request.form['ssn'])
    if ('mvc_id' in request.form):
        search['mvc_id'] = tokenize(request.form['mvc_id'])

    for i, condition in enumerate(search.keys()):
        if (i > 0):
            query += ' AND'
        query += ' ' + condition + ' = %s'

    # Query the database and process the results.
    try:
        url = 'jury-test-database-1.cuy4fcuqkw4f.us-east-1.rds.amazonaws.com'
        cnx = mysql.connector.connect(host=url,
                                      user='admin',
                                      password='NJCourts',
                                      database='JURY-TEST-DATABASE-1')
        cursor = cnx.cursor()
        cursor.execute(query, tuple(search.values()))

        # Build JSON response.
        participants = list()
        for ptr in cursor:
            row = dict()
            row['participant_id'] = ptr[0]
            row['first_name'] = ptr[1]
            row['middle_name'] = ptr[2]
            row['last_name'] = ptr[3]
            row['dob'] = detokenize(ptr[4])
            row['ssn'] = '***-**-' + detokenize(ptr[5])[-4:]
            participants.append(row)
        response['participants'] = participants

        cursor.close()
        cnx.close()

    except Exception as e:
        abort(500, 'Internal Server Error. ' + str(e))

    return response


@app.route('/api/participant', methods=['POST'])
def participant():
    """
    Form a JSON response with details for the jury participant associated with
    the given participant_id.
    """

    # Set default response.
    response = {'success': 0}

    # Abort on bad request.
    if 'participant_id' not in request.form:
        abort(400, 'Bad Request. Check data parameters.')

    try:
        url = 'jury-test-database-1.cuy4fcuqkw4f.us-east-1.rds.amazonaws.com'
        cnx = mysql.connector.connect(host=url,
                                      user='admin',
                                      password='NJCourts',
                                      database='JURY-TEST-DATABASE-1')

        query = 'SELECT * FROM PARTICIPANTS WHERE participant_id = %s'
        cursor = cnx.cursor(buffered=True)
        cursor.execute(query, tuple(request.form['participant_id']))

        if (cursor.rowcount == 0):
            return response

        row = cursor.fetchone()
        key = cursor.column_names
        for i in range(len(row)):
            if key[i] == 'dob' or key[i] == 'ssn' or key[i] == 'mvc_id':
                response[key[i]] = detokenize(row[i])
            else:
                response[key[i]] = row[i]

        cursor.close()
        cnx.close()

    except Exception as e:
        abort(500, 'Internal Server Error. ' + str(e))

    response['success'] = 1

    return response


@app.errorhandler(400)
def bad_request(error):
    """Handle a bad request error with a JSON response."""
    
    return {
        'success': 0,
        'code': error.code,
        'message': error.description
    }


@app.errorhandler(500)
def internal_server_error(error):
    """Handle an internal server error with a JSON response."""

    return {
        'success:': 0,
        'code': error.code,
        'message': error.description
    }


def tokenize(data):
    """Return tokenized data using the IBM Guardium API."""

    url = 'https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/tokenize'
    data = {'data': data, 'tokengroup': 'NJITGrp', 'tokentemplate': 'NJITTmpl'}
    
    response = requests.post(url, json=data, verify=False).json()
    return response['token']


def detokenize(token):
    """Return detokenized data using the IBM Guardium API."""

    url = 'https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/detokenize'
    data = {'token': token, 'tokengroup': 'NJITGrp', 
            'tokentemplate': 'NJITTmpl'}
    
    response = requests.post(url, json=data, verify=False).json()
    return response['data']


if __name__ == '__main__':
    main()
