from flask import Flask, request, render_template, url_for
import requests
from db.access import search_jurors, get_juror

app = Flask(__name__)


# backend routes

# app.add_url_rule('/search', view_func=backend.search, methods=['POST'])
@app.route('/search', methods=['POST'])
def search():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birth_date = request.form.get('date_of_birth')
    ssn = request.form.get('ssn')
    phone = request.form.get('phone')
    jurors = search_jurors(first_name=first_name, last_name=last_name, birth_date=birth_date, ssn=ssn, phone=phone)
    return jurors

#app.add_url_rule('/juror/<id>', view_func=backend.juror, methods=['GET'])
@app.route('/juror/<id>', methods=['GET'])
def juror(id):
    return get_juror(id)

# frontend routes

#app.add_url_rule('/', view_func=frontend.search_form, methods=['GET'])
@app.route('/', methods=['GET'])
def search_form():
    return render_template('search_form.html')

#app.add_url_rule('/search_results', view_func=frontend.search_results, methods=['POST'])
@app.route('/search_results', methods=['Post'])
def search_results():
    response = requests.post(request.host_url + url_for('search'), data=request.form)
    jurors = response.json()
    key_map = {
        'juror_id': 'ID',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'birth_date': 'Date of Birth',
        'phone': 'Phone',
        'ssn': 'Social Security Number'
    }
    return render_template('entities.html', title='Search Results', entities=jurors, key_map=key_map)

#app.add_url_rule('/juror_details/<id>', view_func=frontend.juror_details, methods=['GET'])
@app.route('/juror_details/<id>', methods=['GET'])
def juror_details(id):
    response = requests.get(request.host_url + url_for('juror', id=id))
    juror = response.json()
    key_map = {
        'juror_id': 'ID',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'birth_date': 'Date of Birth',
        'phone': 'Phone',
        'ssn': 'Social Security Number'
    }
    return render_template('entity.html', title='Juror Details', entity=juror, key_map=key_map)
