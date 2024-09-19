import requests
import json
import csv
import re
import datetime, time
from bs4 import BeautifulSoup
import urllib3
import pymssql
import googlemaps
#from cae_import import *

gmaps = googlemaps.Client(key='AIzaSyBvWoZE8T4mAhXfiVBufDL9BNI2r8XJPUI')
urllib3.disable_warnings()
st = datetime.datetime.fromtimestamp(time.time()).strftime('%m.%d.%Y')

def titleize(text):
    not_these = ['ABS','AH','AHG','AHS','AC','GmbH','KG','AR','CCA','DHT','CCH','OHG','SHG','AMB','ASM','ASW','AMB']
    return ' '.join(word
               if word in not_these
               else word.title()
               for word in text.split(' '))


with open('2830_Roady_FR_outlets_werkstattdb.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['abc','country','target_groups','contracts','name', 'street', 'city' ,'postal_code', 'phone','fax', 'web','email', 'services', 'latitude', 'longitude','garage_id','source_id'])

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'content-type':'application/json',
    'origin':'https://www.roady.fr',
    'referer':'https://www.roady.fr/',
    'x-http-method-override':'GET'
}
url="https://www.roady.fr/ajax.V1.php/fr_FR/Rbs/Storelocator/Store/"
print('url: ' + url)


data = {"websiteId":100217,"sectionId":100217,"pageId":100608,"data":{"currentStoreId":"null","distanceUnit":"kilometers","distance":"500kilometers","coordinates":{"latitude":row_csv[2],"longitude":row_csv[3]},"commercialSign":0},"dataSets":"coordinates,address,card,allow","URLFormats":"canonical,contextual","visualFormats":"original,listItem","pagination":"0,50","referer":"https://www.roady.fr/"}
pageCountry = requests.post(url=url,headers=headers, data = json.dumps(data))
#pageCountry = scraper.get(url)
print('status: ' + str(pageCountry.status_code))
if pageCountry.status_code == 200:
    outlets = json.loads(pageCountry.text)
    print('count outlets: ' + str(len(outlets['items'])))
    i=0
    for x in outlets['items']:
        plz=fax =name = email =web =contact=contact_name=country=preselect=hq=siret=firstname=lastName=position=phone=address=street=city=lat=lng=hq=services=contacts_email=garage_id=''
        garage_id = x['common']['id']
        name = x['address']['fields']['name']
        print('name: ' + str(name))
        street = x['address']['fields']['street']
        print('street: ' + str(street))
        plz = x['address']['fields']['zipCode']
        print('plz: ' + str(plz))
        city = x['card']['phoneData']['country']
        print('city: ' + str(city))
        phone = x['card']['phone']
        email = x['card']['email']
        print('phone: ' + str(phone))
        lat = x['coordinates']['latitude']
        lng = x['coordinates']['longitude']
        print('lat: ' + str(lat))
        print('lng: ' + str(lng))
        web = x['common']['URL']['canonical']
        print('web: ' + str(web))
        servT = x['allow'].keys()
        for eachK in servT:
            if x['allow'][eachK]:
                    services = services + eachK + '|'
        services = services[:-1]
        print('services: ' + str(services))

print ('data saved succesfully in this file')
print ('1003_outlets.csv')