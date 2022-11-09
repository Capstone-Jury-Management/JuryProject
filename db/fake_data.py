import random
from faker import Faker
from collections import OrderedDict

def fake_participants(n=10):
    nj_counties = ['Atlantic', 'Bergen', 'Burlington', 'Camden', 'Cape May', 'Cumberland',
        'Essex', 'Gloucester', 'Hudson', 'Hunterdon', 'Mercer', 'Middlesex',
        'Monmouth', 'Morris', 'Ocean', 'Passaic', 'Salem', 'Somerset',
        'Sussex', 'Union', 'Warren']
    fake_participants = []
    fake = Faker()
    for _ in range(n):
        fake_participant = OrderedDict()
        fake_participant['summons_date'] = fake.date_between(start_date='-3y', end_date='today')
        fake_participant['last_name'] = fake.last_name()
        fake_participant['first_name'] = fake.first_name()
        fake_participant['address'] = fake.street_address()
        fake_participant['city'] = fake.city()
        fake_participant['state'] = 'NJ'
        fake_participant['zip'] = fake.postcode_in_state('NJ')
        fake_participant['county'] = random.choice(nj_counties)
        fake_participant['dob'] = fake.date_between(start_date='-90y', end_date='-21y')
        fake_participant['ssn'] = fake.ssn().replace('-',"")
        fake_participant['mvc_id'] = fake.ean(length=13)
        fake_participants.append(fake_participant)
    return fake_participants
