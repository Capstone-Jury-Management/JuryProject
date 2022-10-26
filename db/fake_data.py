from faker import Faker
from collections import OrderedDict

def fake_persons(n=10):
    fake_persons = []
    fake = Faker()
    for _ in range(n):
        fake_person = OrderedDict()
        name = fake.name()
        fake_person['first_name'] = name.split()[0]
        fake_person['last_name'] = name.split()[1]
        fake_person['birth_date'] = fake.date_between(start_date='-90y', end_date='-21y')
        fake_person['phone'] = fake.msisdn()[3:]
        fake_person['ssn'] = fake.ssn()
        fake_persons.append(fake_person)
    return fake_persons
