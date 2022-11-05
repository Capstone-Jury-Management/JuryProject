from flask import Flask
from flask import abort
from flask import request

import mysql.connector
import requests


app = Flask(__name__)


def main():
    requests.packages.urllib3.disable_warnings()  # Disable SSL warnings.


@app.route('/search', methods=['POST'])
def search():
    """
    Form a JSON response with a list of jury participants that match the data 
    parameters in the POST request.
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
        if (i != 0):
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


@app.route('/participant', methods=['POST'])
def participant():
    """
    Form a JSON response with the details for the jury participant that matches
    the id given in the POST request.
    """

    # Set default response.
    response = {'success': 0}
    
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
    """Return an encrypted string using the IBM Guardium API."""

    url = 'https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/tokenize'
    data = {'data': data, 'tokengroup': 'NJITGrp', 'tokentemplate': 'NJITTmpl'}
    
    response = requests.post(url, json=data, verify=False).json()
    return response['token']


def detokenize(token):
    """Return a decrypted token using the IBM Guardium API."""

    url = 'https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/detokenize'
    data = {'token': token, 'tokengroup': 'NJITGrp', 
            'tokentemplate': 'NJITTmpl'}
    
    response = requests.post(url, json=data, verify=False).json()
    return response['data']


if __name__ == '__main__':
    main()
    app.run(debug=True, host='0.0.0.0')
