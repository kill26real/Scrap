import csv
import requests
import datetime, time
import urllib3
import re
from bs4 import BeautifulSoup
import pandas as pd
import os
from cae_import import *

raw_datei_name = '2780_Wurth_raw_werkstattdb.csv'
datei_name = '2780_Wurth_werkstattdb.csv'


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

with open('2780_Würth_FI_outlets_werkstattdb.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['abc','country','target_groups','contracts','name', 'street', 'city' ,'postal_code', 'phone','fax', 'web','email', 'services', 'latitude', 'longitude','garage_id','source_id'])


urllib3.disable_warnings()
response = get_url('https://www.wurth.fi/fi/wurth_fi/center/wuerth_centerit/branch_finder.php')
soup = BeautifulSoup(response, "html.parser")
all_info = soup.find_all('script', type='text/javascript')[24].string

pattern = re.search(r"locations\s*=\s*(\[\s*\[.*?\]\s*\]);", all_info, re.DOTALL)
locations_str = pattern.group(1).replace("null", "None")
locations = eval(locations_str)

for loc in locations:
    plz=fax =name =garage_id= email =web =contact=contracts=target_groups=contact_name=outlets_type=preselect=hq=siret=firstname=lastName=\
            position=phone=address=street=city=hq=services=contact=tg=phone_temp=lat=lng=tg=contract=''
    garage_id = str(loc[0])
    name = loc[1]
    street = loc[2]
    plz = str(loc[3])
    city = loc[4]
    phone = str(loc[5]).replace(' ', '')
    email = loc[7]
    lat = loc[8]
    lng = loc[9]

    success = fill_csv('2780_Würth_FI_outlets','2780','FI','direct marketer',name, street, city ,plz,'',phone,fax, web,email,'',firstname,lastName\
                ,'','','https://www.wurth.fi/',lat,lng,'0',garage_id, services, 'direct marketer', 'Würth')


# df = pd.read_csv(raw_datei_name, sep=",", skipinitialspace=True,  dtype={'postal_code': 'string'})

# df['postal_code'] = df['postal_code'].apply(lambda x: f"{x:05}")
# df['postal_code'] = df['postal_code'].astype(pd.StringDtype())

# df['phone'] = df['phone'].astype(pd.StringDtype())
# df['phone'] = df['phone'].str.replace(" ", "")


# df.to_csv(datei_name, index=False)


# if os.path.exists(raw_datei_name) and os.path.exists(datei_name):
#     os.remove(raw_datei_name)

# send_data_csv(new_datei)