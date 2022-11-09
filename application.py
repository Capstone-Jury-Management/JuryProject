from flask import Flask, request, render_template, url_for, abort
import requests
from db.access import search_jurors, get_juror
from db.init_db import init_db

application = Flask(__name__)

init_db()

# backend routes

#application.add_url_rule('/search', view_func=backend.search, methods=['POST'])
@application.route('/search', methods=['POST'])
def search():
    last_name = request.form.get('last_name')
    first_name = request.form.get('first_name')
    dob = request.form.get('dob')
    ssn = request.form.get('ssn')
    mvc_id = request.form.get('mvc_id')
    jurors = search_jurors(last_name=last_name, first_name=first_name, dob=dob, ssn=ssn, mvc_id=mvc_id)
    return jurors

#application.add_url_rule('/juror/<id>', view_func=backend.juror, methods=['GET'])
@application.route('/juror/<id>', methods=['GET'])
def juror(id):
    juror = get_juror(id)
    if not juror:
        abort(404)
    return juror

# frontend routes

# application.add_url_rule('/', view_func=frontend.search_form, methods=['GET'])
@application.route('/', methods=['GET'])
def search_form():
    return render_template('search_form.html')

# application.add_url_rule('/search_results', view_func=frontend.search_results, methods=['POST'])
@application.route('/search_results', methods=['POST'])
def search_results():
    response = requests.post(request.host_url + url_for('search'), data=request.form)
    jurors = response.json()
    key_map = {
        'participant_id': 'ID',
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'dob': 'Date of Birth',
        'ssn': 'SSN',
        'mvc_id': "DMV Number"
    }
    return render_template('entities.html', title='Search Results', entities=jurors, key_map=key_map)

# application.add_url_rule('/juror_details/<id>', view_func=frontend.juror_details, methods=['GET'])
@application.route('/juror_details/<id>', methods=['GET'])
def juror_details(id):
    response = requests.get(request.host_url + url_for('juror', id=id))
    if response.status_code == 404:
        error = {
            'error_message': 'Juror with id ' + id + ' not found.'
        }
        return render_template('entity.html', title='Juror Details', entity=error, key_map=None)
    else:
        juror = response.json()
        key_map = {
            'participant_id': 'ID',
            'summons_date': 'Summons Date',
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'address': 'Street Address',
            'city': 'City',
            'state': "State",
            'zip': 'ZIP',
            'county': 'County',
            'dob': 'Date of Birth',
            'ssn': 'SSN',
            'mvc_id': "DMV Number"
    }
        return render_template('entity.html', title='Juror Details', entity=juror, key_map=key_map)

if __name__ == "__main__":
    application.debug = True
    application.run()