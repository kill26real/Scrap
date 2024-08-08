import csv
import requests
import datetime, time
import urllib3
import re
from bs4 import BeautifulSoup
from lxml import etree
from deep_translator import GoogleTranslator


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
    return id,name,lat,lng,plz,city_address,email,phone,street,link


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

with open('3790_CaryGroup_werkstattdb.csv', 'w', newline='', encoding="utf-8") as csvfile:
   csv_writer = csv.writer(csvfile)
   csv_writer.writerow(
       ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone',
        'fax', 'web', 'email', 'services', 'latitude', 'longitude', 'garage_id', 'sources'])


urllib3.disable_warnings()
st = datetime.datetime.fromtimestamp(time.time()).strftime('%m.%d.%Y')


def fill_csv(csv_name, id_company, country, outlets_type, name, street, city, plz, preselect, phone, fax, web, email,
             contact_title, contact_first_name, contact_last_name \
             , contact_position, contact_email, source, lat, lng, hq, garage_id, services):

    if email:
        email = email.lower()

    source = source.replace("'", "")
    contract = re.sub(r"^[0-9_]+", "", csv_name)

    with open('3790_' + csv_name + '_werkstattdb.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['abc', country, outlets_type, contract, name, street, city, plz, phone, fax, web, email, services, lat,
             lng, garage_id, source])






response = get_url('https://rydsbilglas.se/hitta-verkstad/?_gl=1*1khcc7r*_up*MQ..*_ga*Nzc1ODYzNjc5LjE3MjI4NDUzNjg.*_ga_4PQQZ2LC5H*MTcyMjg0NTM2Ni4xLjEuMTcyMjg0NTM3MS4wLjAuMA.', None)


soup = BeautifulSoup(response, "html.parser")

garages = soup.find_all('div', class_='marker')
# print('GARAGE', garages[0])

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

    link = 'https://rydsbilglas.se/' + garage_dienst.find('a').get('href')
    email = dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[1]/a')[0].text
    phone = dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[1]/text()')[0].strip().replace('.', '-')
    street = dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[2]')[0].text
    addresse = str(dom.xpath('//*[@id="hitta-verkstad-desktop"]/div[4]/p[2]/text()[2]')[0]).replace(' ', '')

    plz = addresse[0:5]
    city_address = addresse[5:]


    fill_csv('CaryGroup', '3790', 'SE', 'IAM Garage marketing system', name, street, city_address, plz, '', phone,
             '', link, email, '', '', '', '', '', 'https://rydsbilglas.se/', lat, lng, '', '', services)
