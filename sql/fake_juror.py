from lib2to3.pgen2 import token
from faker import Faker
from collections import OrderedDict
import requests
import json
import numpy as np 
import pymysql

db = pymysql.connect(host='jury-test-database-1.cuy4fcuqkw4f.us-east-1.rds.amazonaws.com', 
                    user= "admin", 
                    password="NJCourts",
                    database = 'JURY-TEST-DATABASE-1')
cursor = db.cursor()

def tokenize (data):
    url = "https://dpqa.aocnp.njcourts.gov:2155/vts/rest/v2.0/tokenize"
    body = {
        "data" : data , 
        "tokengroup": "NJITGrp",
        "tokentemplate" : "NJITTmpl"
        }
    x = requests.post(url, json = body, verify=False)
    token = json.loads(x.text)
    return (token["token"])


def fake_persons(n=10):
    fake_persons = []
    fake = Faker()
    for _ in range(n):
        fake_person = OrderedDict()
        name = fake.name()
        fake_person['participant_id']= fake.ean(length=8)
        fake_person['summons_date']= fake.date()
        fake_person['last_name'] = name.split()[1]
        fake_person['first_name'] = name.split()[0]
        fake_person["gender"] = np.random.choice(["M", "F"], p=[0.5, 0.5])
        fake_person["address"] = fake.street_address()
        fake_person["city"] = fake.city()
        fake_person["state"] = 'NJ'
        fake_person["zipcode"] = fake.postcode()
        fake_person["county"] = "Essex"
        fake_person['phone'] = fake.msisdn()[3:]

        # need to be encrypted 
        fake_person['birth_date'] = tokenize(fake.date())
        fake_person['ssn'] = tokenize(fake.ssn().replace('-',""))
        fake_person["license"] = tokenize(fake.ean(length=13))

        fake_persons.append(fake_person)

    return fake_persons

for juror in fake_persons(99):
    print (juror)
    cursor.execute ('INSERT INTO PARTICIPANTS ( summons_date, first_name, last_name, gender, address, city, state, zip, county, mobile_phone, dob, ssn, mvc_id)'
    + "VALUES ( %s, %s, %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s)",
        ([juror["summons_date"]], [juror['first_name']], 
        [juror['last_name']],[juror['gender']] ,[juror['address']] ,[juror['city']] ,
        [juror['state']] ,[juror['zipcode']],[juror['county']] ,[juror['phone']], 
        [juror['birth_date']], [juror['ssn']], [juror['license']])
    )
db.commit()
db.close()
print(fake_persons(n=1))