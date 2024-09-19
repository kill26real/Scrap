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

urllib3.disable_warnings()
st = datetime.datetime.fromtimestamp(time.time()).strftime('%m.%d.%Y')

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'content-type':'application/json',
    'origin':'https://www.auto.leclerc',
    'referer':'https://www.auto.leclerc/',
    'x-http-method-override':'GET'
}
url="https://api.woosmap.com/stores/?key=woos-f21489c3-7cd5-3cef-986f-1680ac792ea9"
print('url: ' + url)

data = {
    "key": 'woos-f21489c3-7cd5-3cef-986f-1680ac792ea9',
}

data2 = {
    "key": 'woos-f21489c3-7cd5-3cef-986f-1680ac792ea9',
    'page': 2
}
i = 0
def get_info(url, headers, data):
    response = requests.get(url=url,headers=headers, data = json.dumps(data))
    print('status: ' + str(response.status_code))
    outlets = json.loads(response.text)
    for outlet in outlets['features']:
        global i
        i += 1
        print('nummer ', i)
        info = outlet['properties']

        name = info['name']
        store_id = info['store_id']
        print('name', name)
        print('store_id', store_id)

        contact = info['contact']
        email = contact['email']
        phone = contact['phone']
        web = 'https://www.auto.leclerc/centre-auto/' + contact['website'].split('/')[-1]
        print('email', email)
        print('phone', phone)
        print('web', web)

        address = info['address']
        street = address['lines'][0] + address['lines'][1]
        city = address['city']
        zipcode = address['zipcode']
        print('street', street)
        print('city', city)
        print('zipcode', zipcode)

        user_properties = info['user_properties']
        lat = user_properties['lat']
        lng = user_properties['lng']
        print('lat', lat)
        print('lng', lng)

        print('--------------------------------------------------------------')
get_info(url, headers, data)
get_info(url, headers, data2)

