from faker import Faker

import json
import mysql.connector
import os
import string
import random
import requests


def main():
    requests.packages.urllib3.disable_warnings()  # Disable SSL warnings.
    
    try:
        cnx = mysql.connector.connect(host=os.environ['RDS_HOSTNAME'],
                                      user=os.environ['RDS_USERNAME'],
                                      password=os.environ['RDS_PASSWORD'],
                                      database=os.environ['RDS_DB_NAME'])
        cursor = cnx.cursor()

        query = '''
                INSERT INTO PARTICIPANTS(`summons_date`, `undeliverable`,
                    `perm_disq`, `last_name`, `first_name`, `middle_name`,
                    `address`, `city`, `state`, `zip`, `county`, `dob`,
                    `drivers_state`, `ssn`, `race`, `mvc_id`, `gender`,
                    `hispanic`, `home_phone`, `mobile_phone`, `work_phone`,
                    `work_phone_ext`, `email`, `gov_employee`, `opt_in`,
                    `occupation`)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''

        for i in range(1000):
            participant = random_participant()
            cursor.execute(query, tuple(participant.values()))
            print(i, participant, '\n')

        cnx.commit()

        cursor.close()
        cnx.close()
    
    except Exception as e:
        print("ERROR: ", e)


def random_participant():
    fake = Faker()
    participant = {}
    county, city = random_nj_county_city()
    gender = random.choice(('Male', 'Female'))

    participant['summons_date'] = str(fake.date_this_year())
    participant['undeliverable'] = 0
    participant['perm_disq'] = 0
    participant['last_name'] = fake.last_name()
    # suffix
    if (gender == 'Male'):
        participant['first_name'] = fake.first_name_male()
        participant['middle_name'] = fake.first_name_male()
    else:
        participant['first_name'] = fake.first_name_female()
        participant['middle_name'] = fake.first_name_female()
    participant['address'] = fake.street_address()
    participant['city'] = city
    participant['state'] = 'NJ'
    participant['zip'] = fake.postcode()
    participant['county'] = county
    participant['dob'] = tokenize(str(fake.date_of_birth(minimum_age=18, 
                                                         maximum_age=80)))
    participant['drivers_state'] = 'NJ'
    # voters_no
    participant['ssn'] = tokenize(fake.ssn().replace('-', ''))
    participant['race'] = random_race()
    participant['mvc_id'] = tokenize(random_mvc_id())
    participant['gender'] = gender
    if (participant['race'] == 'Hispanic' or participant['race'] == 'Latino'):
        participant['hispanic'] = 1
    else:
        participant['hispanic'] = 0
    participant['home_phone'] = random_phone_number()
    participant['mobile_phone'] = random_phone_number()
    participant['work_phone'] = random_phone_number()
    participant['work_phone_ext'] = random_phone_number_ext()
    participant['email'] = ''.join((participant['first_name'].lower(),
                                    random.choice(('', '.')),
                                    participant['last_name'].lower(),
                                    str(random.randint(1, 99)),
                                    '@', 
                                    random.choice(('gmail.com', 
                                                   'yahoo.com', 
                                                   'hotmail.com',
                                                   'icloud.com',
                                                   'aol.com'))))
    participant['gov_employee'] = random_is_gov_employee()
    # perm_disq_reason  
    participant['opt_in'] = random.randint(0, 1)
    # unique_id
    # employer
    participant['occupation'] = random_occupation()
    # occupation_other

    return participant


def random_nj_county_city():
    county = ''
    city = ''
    with open('counties_cities.json', 'r') as file:
        data = json.load(file)
        county = random.choice(tuple(data.keys()))
        city = random.choice(tuple(data[county]))
    return (county, city)


def random_race():
    return random.choice(('Caucasian', 
                          'African American', 
                          'Asian', 
                          'Hispanic', 
                          'Latino'))


def random_mvc_id():
    mvc_id = ''
    mvc_id += random.choice(string.ascii_uppercase)
    for i in range(14):
        mvc_id += random.choice(string.digits)
    return mvc_id


def random_phone_number():
    phone_number = random.choice(('212', '609', '732', '856', '908', '973'))
    for i in range(7):
        phone_number += random.choice(string.digits)
    return phone_number


def random_phone_number_ext():
    ext = ''
    for i in range(random.randint(0, 4)):
        ext += random.choice(string.digits)
    return ext


def random_is_gov_employee():
    p = random.randint(0, 9)
    if (p == 0):
        return 1
    return 0


def random_occupation():
    occupation = ''
    with open('occupations.json', 'r') as file:
        data = json.load(file)
        occupation = random.choice(tuple(data))
    return occupation


def tokenize(data):
    '''Return tokenized data using the IBM Guardium API.'''

    url = 'https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/tokenize'
    data = {'data': data, 'tokengroup': 'NJITGrp', 'tokentemplate': 'NJITTmpl'}
    
    response = requests.post(url, json=data, verify=False).json()
    return response['token']


if __name__ == '__main__':
    main()
