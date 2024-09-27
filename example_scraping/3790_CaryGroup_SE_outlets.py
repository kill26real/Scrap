import csv
import requests
import datetime, time
import urllib3
import re
from bs4 import BeautifulSoup
from lxml import etree
from deep_translator import GoogleTranslator
from test_input import send_data_csv, send_data_raw
import pandas as pd
import os
# from cae_import import *


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
    return id, name, lat, lng, plz, city_address, email, phone, street, link


def get_url(url, data):
    if data is None:
        response = requests.get(url)
    else:
        response = requests.get(url, data)
        # Check if the request was successful
    if response.status_code == 200:
        html_content = response.text
        return html_content
    else:
        if response.status_code == 404:
            return '404'
        else:
            print("Failed to retrieve the web page")
            return 'error'

# with open('3790_CaryGroup_SE_outlets.csv', 'w', newline='', encoding="utf-8") as csvfile:
#    csv_writer = csv.writer(csvfile)
#    csv_writer.writerow(
#        ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone', 'fax', 'web',
#         'email', 'services', 'latitude', 'longitude', 'garage_id', 'source'])

urllib3.disable_warnings()
st = datetime.datetime.fromtimestamp(time.time()).strftime('%m.%d.%Y')

response = get_url('https://rydsbilglas.se/hitta-verkstad/?_gl=1*1khcc7r*_up*MQ..*_ga*Nzc1ODYzNjc5LjE3MjI4NDUzNjg.*_ga_4PQQZ2LC5H*MTcyMjg0NTM2Ni4xLjEuMTcyMjg0NTM3MS4wLjAuMA.', None)
soup = BeautifulSoup(response, "html.parser")
garages = soup.find_all('div', class_='marker')
for garage in garages:
    id, name, lat, lng, plz, city_address, email, phone, street, link = initlize_values()

    dom = etree.HTML(str(garage))
    name = dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[1]/h2')[0].text

    img_url = garage.find('img').get('src')
    regex = r"center=(?P<lat>-?\d+\.\d+),(?P<lng>-?\d+\.\d+)"
    match = re.search(regex, img_url)
    if match:
        lat = match.group("lat")
        lng = match.group("lng")

    garage_dienst = garage.find('div', class_="verkstad-tjanster verkstad-kolumn verkstad-kolumn-2")
    services_elements = garage_dienst.find('p')
    text_content = services_elements.get_text(separator=' ') if services_elements else ''
    dienst_all = re.findall(r'\b\w+\b', text_content)

    services_list = [GoogleTranslator(source='auto', target='en').translate(elem) for elem in dienst_all]
    services = ''
    for serv in services_list[:-1]:
        services += serv + ' | '
    services += services_list[-1]

    web = 'https://rydsbilglas.se/' + garage_dienst.find('a').get('href')
    email = dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[1]/a')[0].text
    phone = dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[1]/text()')[0].strip().replace('.', '')
    street = dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[2]')[0].text
    addresse = str(dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[2]/text()[2]')[0]).replace(' ', '')

    plz = str(addresse[0:5])
    city = addresse[5:]
    fax = ''
    firstname = ''
    lastName = ''
    garage_id = ''

    OUTPUT.append({
        'abc': 'abc',
        'country': 'SE',
        'target_groups': 'IAM Garage marketing system',
        'contracts': 'Cary Group',
        'name': name,
        'street': street,
        'city': city,
        'postal_code': plz,
        'phone': phone,
        'fax': '',
        'web': web,
        'email': email,
        'services': services,
        'latitude': lat,
        'longitude': lng,
        'garage_id': garage_id,
        'source': 'https://rydsbilglas.se/'
    })

send_data_raw(OUTPUT)


    # success = fill_csv('3790_CaryGroup_SE_outlets', '3790', 'SE', 'IAM Garage marketing system', name, street, city, plz, '', phone,
    #                    fax, web, email, '', firstname, lastName \
    #                    , '', '', 'https://rydsbilglas.se/', lat, lng, '0', garage_id, services, 'IAM Garage marketing system',
    #                    'CaryGroup')


# df = pd.read_csv('3790_CaryGroup_raw_werkstattdb.csv', sep=",", skipinitialspace=True,  dtype={'postal_code': 'string'})
#
# df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")
# df['postal_code'] = df['postal_code'].astype(pd.StringDtype())
# df['phone'] = df['phone'].astype(pd.StringDtype())
# df['fax'] = df['fax'].astype('string')
#
# df['phone'] = df['phone'].str.replace(" ", "")
# df['fax'] = df['fax'].str.replace(" ", "")
#
# df.to_csv(f'3790_CaryGroup_werkstattdb.csv', index=False)
#
# new_datei = '3790_CaryGroup_werkstattdb.csv'
# alt_datei = '3790_CaryGroup_raw_werkstattdb.csv'
#
# if os.path.exists(alt_datei) and os.path.exists(new_datei):
#     os.remove(alt_datei)
#
# send_data_csv(new_datei)
