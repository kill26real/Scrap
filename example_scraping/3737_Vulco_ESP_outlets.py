import csv
import requests
import datetime, time
import urllib3
import re
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import pandas as pd
import os
from test_input import send_data_csv, send_data_raw
from lxml import etree

OUTPUT = []

def initlize_values():
    id = ''
    name = ''
    lat = ''
    lng = ''
    plz = ''
    city_address = ''
    email = ''
    phone = ''
    street = ''
    link = ''
    services = ''
    fax = ''
    return id, name, lat, lng, plz, city_address, email, phone, street, link, services, fax


def get_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        if response.status_code == 404:
            return '404'
        else:
            print("Failed to retrieve the web page")
            return 'error'

# with open('3737_Vulco_raw_werkstattdb.csv', 'w', newline='', encoding="utf-8") as csvfile:
#    csv_writer = csv.writer(csvfile)
#    csv_writer.writerow(
#        ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone',
#         'fax', 'web', 'email', 'services', 'latitude', 'longitude', 'garage_id', 'source'])


urllib3.disable_warnings()
st = datetime.datetime.fromtimestamp(time.time()).strftime('%m.%d.%Y')
response = get_url('https://www.vulco.es/buscador-de-talleres/')
soup = BeautifulSoup(response, "html.parser")

garage_classes = {'col-12', 'col-md-6', 'col-lg-4', 'mb-4'}
def has_all_classes(tag):
    return tag.has_attr('class') and garage_classes.issubset(tag['class'])
garages = soup.find_all(has_all_classes)

print('len', len(garages))

i = 0
for garage in garages:
    i += 1
    print(f'Number {i} of {len(garages)}')
    id, name, lat, lng, plz, city_address, email, phone, street, link, services, fax = initlize_values()

    link = 'https://www.vulco.es' + garage.find_all('a', class_='text-decoration-none')[0].get('href')
    print('main link', link)
    response2 = get_url(f'{link}')
    soup2 = BeautifulSoup(response2, "html.parser")

    weg = soup2.find('h1').find('span', class_='small').text
    name = soup2.find('h1').text.replace(weg, '')
    # print('name', name)

    contact_classes = {'col-lg-6', 'mb-lg-0', 'mb-4'}
    def has_all_classes(tag):
        return tag.has_attr('class') and contact_classes.issubset(tag['class'])
    contact = soup2.find_all(has_all_classes)[0]

    address = [re.sub(r'\s+', ' ', x).strip() for x in contact.find('p').text.splitlines()]
    if len(address) < 4:
        pattern2 = r'\d{5} [a-zA-ZäöüÄÖÜßáéíóúñÁÉÍÓÚÑ]+(?:\s+[a-zA-ZäöüÄÖÜßáéíóúñÁÉÍÓÚÑ]+)*'
        match = re.search(pattern2, address[-2])
        plz = str(match.group()[:5])
        city = match.group()[6:]
        street = address[-2].replace(match.group(), '')
    else:
        street = address[-3]
        plz = str(address[-2][:5])
        city = address[-2][6:]
    # print('street', street)
    # print('plz', plz)
    # print('city', city)

    contact2 = contact.find_all('li')
    phone = str(contact2[0].text).strip()
    if contact.find('i', class_='fa-print'):
        fax = str(contact2[1].text).strip().replace('.', '')
    if contact.find('i', class_='fa-mobile'):
        phone += f' | {str(contact2[1].text).strip()}'
    # print('phone', phone)
    # print('fax', fax)

    service_row = soup2.find_all('div', class_='col-12')
    for row in service_row:
        services_in_row = row.find_all('div', class_='card service border-top-0 border-bottom-0')
        for service in services_in_row:
            services = services + GoogleTranslator(source='auto', target='en').translate(service.find('img', class_='service-icon').get('alt')) + ' | '
    services = services[:-1]

    latlng = soup2.find_all('script', type='text/javascript')[2].text
    pattern = r'\s*parseFloat\("(-?\d+\.\d+)"\),\s*\s*parseFloat\("(-?\d+\.\d+)"\)'
    matches = re.search(pattern, latlng)
    if matches:
        lat = matches.group(1)
        lng = matches.group(2)
    #     print("Latitude:", lat)
    #     print("Longitude:", lng)
    # else:
    #     print('no latlng')
    #
    # print('services', services)
    print('-------------------------------------------------------------------------------------------')

    OUTPUT.append({
        'abc': 'abc',
        'country': 'ES',
        'target_groups': 'Tyre Service',
        'contracts': 'Vulco',
        'name': name,
        'street': street,
        'city': city,
        'postal_code': plz,
        'phone': phone,
        'fax': fax,
        'web': link,
        'email': email,
        'services': services,
        'latitude': lat,
        'longitude': lng,
        'garage_id': '',
        'source': 'https://www.vulco.es/'
    })

send_data_raw(OUTPUT)

#     with open('3737_Vulco_raw_werkstattdb.csv', 'a', newline='', encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(
#             ['abc', 'ES', 'Tyre Service', 'Vulco', name, street, city, plz, phone, fax, link, email, services, lat,
#              lng, '', 'https://www.vulco.es/'])
#
#
# df = pd.read_csv('3737_Vulco_raw_werkstattdb.csv', sep=",", skipinitialspace=True,  dtype={'postal_code': 'string'})
#
# df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")
# df['postal_code'] = df['postal_code'].astype(pd.StringDtype())
# df['phone'] = df['phone'].astype(pd.StringDtype())
# df['fax'] = df['fax'].astype('string')
#
# df['phone'] = df['phone'].str.replace(" ", "")
# df['fax'] = df['fax'].str.replace(" ", "")
#
# df.loc[28, 'city'] = "L'Hospitalet de Llobregat"
# df.loc[28, 'street'] = df.loc[28, 'street'].replace(" 'Hospitalet de Llobregat", '')
#
# df.to_csv(f'3737_Vulco_werkstattdb.csv', index=False)
#
# new_datei = '3737_Vulco_werkstattdb.csv'
# alt_datei = '3737_Vulco_raw_werkstattdb.csv'
#
# if os.path.exists(alt_datei) and os.path.exists(new_datei):
#     os.remove(alt_datei)

# send_data_csv(new_datei)
