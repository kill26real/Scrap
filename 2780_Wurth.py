import csv
import requests
import datetime, time
import urllib3
import re
from bs4 import BeautifulSoup
import pandas as pd
import os
from test_input import send_data_csv


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

with open('2780_Wurth_raw_werkstattdb.csv', 'w', newline='', encoding="utf-8") as csvfile:
   csv_writer = csv.writer(csvfile)
   csv_writer.writerow(
       ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone',
        'fax', 'web', 'email', 'services', 'latitude', 'longitude', 'garage_id', 'sources'])


urllib3.disable_warnings()
response = get_url('https://www.wurth.fi/fi/wurth_fi/center/wuerth_centerit/branch_finder.php')
soup = BeautifulSoup(response, "html.parser")
all_info = soup.find_all('script', type='text/javascript')[24].string

pattern = re.search(r"locations\s*=\s*(\[\s*\[.*?\]\s*\]);", all_info, re.DOTALL)
locations_str = pattern.group(1).replace("null", "None")
locations = eval(locations_str)

for loc in locations:
    garage_id = str(loc[0])
    name = loc[1]
    street = loc[2]
    plz = str(loc[3])
    city = loc[4]
    phone = str(loc[5]).replace(' ', '')
    email = loc[7]
    lat = loc[8]
    lng = loc[9]

    with open('2780_Wurth_raw_werkstattdb.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['abc', 'ESP', 'Direct Marketer', 'Würth', name, street, city, plz, phone, '', '', email, '', lat,
             lng, garage_id, 'https://www.wurth.fi/'])


df = pd.read_csv('2780_Wurth_raw_werkstattdb.csv', sep=",", skipinitialspace=True,  dtype={'postal_code': 'string'})

df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")
df['postal_code'] = df['postal_code'].astype(pd.StringDtype())

df['phone'] = df['phone'].astype(pd.StringDtype())
df['phone'] = df['phone'].str.replace(" ", "")


df.to_csv(f'2780_Wurth_werkstattdb.csv', index=False)

new_datei = '2780_Wurth_werkstattdb.csv'
alt_datei = '2780_Wurth_raw_werkstattdb.csv'

if os.path.exists(alt_datei) and os.path.exists(new_datei):
    os.remove(alt_datei)

# send_data_csv(new_datei)