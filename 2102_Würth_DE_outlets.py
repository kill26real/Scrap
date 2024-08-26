import requests
import json
import datetime, time
import urllib3
from deep_translator import GoogleTranslator
from tqdm import tqdm
# from cae_import import *

urllib3.disable_warnings()
st = datetime.datetime.fromtimestamp(time.time()).strftime('%m.%d.%Y')

url="https://www.wuerth.de/web/de/awkg/niederlassungen/branches_json_v2.json"


i = 0
response = requests.get(url=url)
print('status: ' + str(response.status_code))
outlets = json.loads(response.text)
lenght = len(outlets)
for outlet in tqdm(outlets, desc="Lade Daten", ncols=80):
    i += 1
    print(f'nummer {i} of {lenght}')
    name = 'Würth ' + outlet['branch']
    garage_id = outlet['branchnumber']
    print('name', name)
    print('store_id', garage_id)

    service = ''
    services = [GoogleTranslator(source='auto', target='en').translate(serv['label']) + ' | ' for serv in outlet['equipments']]
    for s in services:
        service += s
    service = service[:-3]
    print('')
    print('services', service)

    email = outlet['email']
    phone = outlet['phone'].replace(' ', '')
    fax = outlet['fax'].replace(' ', '')
    web = outlet['nlDetailUrl']
    print('email', email)
    print('phone', phone)
    print('web', web)
    print('fax', fax)
    firstname = ''
    lastName = ''

    street = outlet['address']
    city = outlet['location']
    plz = outlet['zip']
    print('street', street)
    print('city', city)
    print('zipcode', plz)

    lat = outlet['latitude']
    lng = outlet['longitude']
    print('lat', lat)
    print('lng', lng)
    print('--------------------------------------------------------------')

    success = fill_csv('2102_WÜRTH_DE_outlets', '2102', 'DE', 'Direct marketer', name, street, city, plz, '', phone,
                       fax, web, email, '', firstname, lastName, '', '', 'https://www.wuerth.de/', lat, lng, '0',
                       garage_id, services, 'IAM Autocenter', 'E.LECLERC')

