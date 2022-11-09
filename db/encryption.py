import requests

def tokenize(data):
    """Return tokenized data using the IBM Guardium API."""

    url = 'https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/tokenize'
    data = {'data': data, 'tokengroup': 'NJITGrp', 'tokentemplate': 'NJITTmpl'}
    
    response = requests.post(url, json=data, verify=False).json()
    return response['token']

def detokenize(token):
    """Return detokenized data using the IBM Guardium API."""

    url = 'https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/detokenize'
    data = {'token': token, 'tokengroup': 'NJITGrp', 'tokentemplate': 'NJITTmpl'}
    
    response = requests.post(url, json=data, verify=False).json()
    return response['data']