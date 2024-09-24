import requests
import json
url = "https://www.autofit.com/api/search/universal_workshops"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://www.autofit.com',
    'Referer': 'https://www.autofit.com/werkstattsuche',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}
payload = {
    "layouts": ["auto_fit"],
    "city": None,
    "open": None,
    "selectedServices": [],
    "limit": 3,
    "offset": 0
}
response = requests.post(url, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    data = response.json()
    garages = data['data']['workshops']
    print('gefundene garages: ', len(garages))
    print("Erhaltene Daten:")
    print(json.dumps(data, indent=4))


# opts = webdriver.ChromeOptions()
# options = Options()
# options.add_argument("--disable-web-security")
# options.add_argument("--webdriver-logfile=webdrive.log")
# options.add_argument("--disable-popup-blocking")
# options.add_argument("--disable-notifications")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# s = Service('C:\\Users\\emv\\chromedriver.exe')
# driver = webdriver.Chrome(service=s, options=options)


def checkduplicate(output, name, street, plz, city):
    if len(output) == 0:
        return True
    for entry in output:
        if (entry['name'] == name and
            entry['street'] == street and
            entry['postal_code'] == plz and
            entry['city'] == city):
            return False
    return True

# check = checkduplicate(OUTPUT, name, street, plz, city)
# if check and iso2 in valid_countries:
#     print(f'garage {k}')
#     print('search by: ', row_csv[0])
#     print('name: ' + str(name))
#     print('street: ' + street)
#     print('city: ' + city)
#     print('plz: : ' + plz)
#     print('country: ', country)
#     print('services: ' + str(services))
#     print('web: ', web)
#     print('phone: ' + str(phone))
#     print('fax: ', fax)
#     print('email: ' + str(email))
#     print('latitude: ' + str(lat))
#     print('longitude: ' + str(lng))
#     print('------------------------------------------------')
#     k += 1
#     with open('Bosch.csv', 'a', newline='', encoding="utf-8") as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(
#             [name, street, city, plz, contract, country, iso2, phone, fax, web, email, services,
#              lat, lng, garage_id])
#     OUTPUT.append({
#         'abc': 'ID',
#         'country': iso2,
#         'target_groups': 'independent car service',
#         'contracts': contract,
#         'name': name,
#         'street': street,
#         'city': city,
#         'postal_code': plz,
#         'phone': phone,
#         'fax': fax,
#         'web': web,
#         'email': email,
#         'services': services,
#         'latitude': lat,
#         'longitude': lng,
#         'garage_id': garage_id,
#         'contact_title': '',
#         'contact_first_name': firstname,
#         'contact_last_name': lastname,
#         'contact_position': '',
#         'contact_email': '',
#         'source': source
#     })
# send_data_raw(OUTPUT, 'Bosch')


regex = r'https:\\/\\/www.blacktire.pt\\/blog\\/oficina\\/[a-zA-Z\-]+'

# if bool(re.search(r'[a-zA-Z]', text)):
#     plz = ''
