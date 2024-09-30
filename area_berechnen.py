import requests
import json
import csv
import urllib3
import pandas as pd
import geopandas as gpd
import pycountry
from tqdm import tqdm
import math
import osmnx as ox

from osmnx._errors import InsufficientResponseError


def lat_lng_to_quadkey(lat, lng, zoom):
    # Berechne die Kachelkoordinaten
    lat_rad = math.radians(lat)

    # Berechnung der Kachelkoordinaten (x, y)
    n = 2.0 ** zoom
    x = (lng + 180.0) / 360.0 * n
    y = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n

    # Umwandlung in Ganzzahlen
    x, y = int(x), int(y)

    # Generiere den Quadkey
    quadkey = ""
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (x & mask) != 0:
            digit += 1
        if (y & mask) != 0:
            digit += 2
        quadkey += str(digit)

    return quadkey


OUTPUT = []


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


urllib3.disable_warnings()
url = 'https://www.eurorepar.de/werkstatten-anforderung-von-terminen.html#listing-garages'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}
stopp = False
valid_countries = {'IT', 'DE', 'NL', 'FR', 'AT', 'BE', 'ES', 'UK', 'PL', 'PT'}
my_liste = []
k = 1
# with open("C:\\Users\\emv.WOLK\\Python\\worldcitiesAll.csv", encoding='utf-8') as csvdatei:
with open("/home/kirill/Desktop/Projects/Python-Scraping/Excel_CSV_help/worldcitiesAll.csv",
          encoding='utf-8') as csvdatei:
    csv_reader_object = csv.reader(csvdatei, delimiter=';')
    l = 0
    for row_csv in csv_reader_object:
        if stopp:
            break
        # if (l > 0) and row_csv[5].find('AT') > -1:
        if 0 < l < 35:
            if row_csv[5] in valid_countries:
                url = 'https://dl-emea.dxtservice.com/dl/api/search?latitude=' + row_csv[2] + '&longitude=' + row_csv[
                    3] + '&searchRadius=500&includeStores=COUNTRY&pageIndex=0&pageSize=100&minDealers=10&maxDealers=20000&storeTags=[BCS]'
                print('url: ' + url)
                r = requests.get(url, headers=headers, verify=False)
                if r.status_code == 200:
                    print('json erreicht')
                    try:
                        json_response = json.loads(r.text)
                        print('result: ' + str(json_response['data']['results']))
                        for i in range(0, int(json_response['data']['results'] / 100) + 1):
                            if stopp:
                                break
                            print('i:' + str(i))
                            page_url = 'https://dl-emea.dxtservice.com/dl/api/search?latitude=' + row_csv[
                                2] + '&longitude=' + row_csv[
                                           3] + '&searchRadius=500&includeStores=COUNTRY&pageIndex=' + str(
                                i) + '&pageSize=100&minDealers=10&maxDealers=20000&storeTags=[BCS]'
                            print('page_url: ' + page_url)
                            r_page = requests.get(page_url, headers=headers, verify=False)
                            if r_page.status_code == 200:
                                plz = fax = email = web = source = contact = name = contact_name = country = firstname = lastname = position = phone = address = street = city = lat = lng = services = contracts = garage_id = ''
                                print('json page erreicht')
                                json_page = json.loads(r_page.text)
                                for y in json_page['data']['items']:
                                    if len(my_liste) >= 100:
                                        stopp = True
                                    if stopp:
                                        break
                                    garage_id = y['storeId']
                                    name = y['displayName'].replace(',', '.')
                                    try:
                                        web = y['address']['webAddress']
                                    except:
                                        web = ''
                                    try:
                                        phone = y['address']['officePhoneNumber']
                                    except:
                                        phone = ''
                                    if y['address']['mobilePhoneNumber']:
                                        if phone:
                                            phone = phone + '|' + y['address']['mobilePhoneNumber']
                                        else:
                                            phone = y['address']['mobilePhoneNumber']
                                    try:
                                        fax = y['address']['faxNumber'].replace(' ', '').replace('(', '').replace(')',
                                                                                                                  '').replace(
                                            '-', '')
                                    except:
                                        fax = ''
                                    try:
                                        email = y['address']['email']
                                    except:
                                        email = ''
                                    try:
                                        street = y['address']['addressLine1'].replace(',', '.').replace("'",
                                                                                                        "`") + ' ' + \
                                                 y['address']['addressLine2']
                                    except:
                                        street = y['address']['addressLine1'].replace(',', '.').replace("'", "`")
                                    try:
                                        city = y['address']['city'].replace(',', '.').replace(';', ' ')
                                    except:
                                        city = ''
                                    try:
                                        plz = y['address']['zipcode']
                                    except:
                                        plz = ''
                                    try:
                                        lat = y['geoCoordinates']['latitude']
                                    except:
                                        lat = ''
                                    try:
                                        lng = y['geoCoordinates']['longitude']
                                    except:
                                        lng = ''

                                    country = y['address']['country'].strip()
                                    if country == 'IT' or country == 'Italy':
                                        iso2 = 'IT'
                                        contract = '1566'
                                        source = 'https://www.boschcarservice.com/it/it'
                                    elif country == 'DE' or country == 'Germany':
                                        iso2 = 'DE'
                                        contract = ' 1570'
                                        source = 'https://www.boschcarservice.com/de/de'
                                    elif country == 'NL' or country == 'Netherlands':
                                        iso2 = 'NL'
                                        contract = '1565'
                                        source = 'https://www.boschcarservice.nl'
                                    elif country == 'FR' or country == 'France':
                                        iso2 = 'FR'
                                        contract = '1554'
                                        source = 'https://www.boschcarservice.fr/'
                                    elif country == 'AT' or country == 'Austria':
                                        iso2 = 'AT'
                                        contract = '331'
                                        source = 'https://www.bosch-service.at'
                                    elif country == 'BE' or country == 'Belgium':
                                        iso2 = 'BE'
                                        contract = '1100'
                                        source = 'https://www.boschcarservice.be'
                                    elif country == 'ES' or country == 'Spain':
                                        iso2 = 'ES'
                                        contract = '1558'
                                        source = 'https://www.boschcarservice.es'
                                    elif country == 'UK' or country == 'United Kingdom':
                                        iso2 = 'UK'
                                        contract = '1555'
                                        source = 'https://www.bosch.co.uk'
                                    elif country == 'PL' or country == 'Poland':
                                        iso2 = 'PL'
                                        contract = '1362'
                                        source = 'www.boschcarservice.com/pl'
                                    elif country == 'PT' or country == 'Portugal':
                                        iso2 = 'PT'
                                        contract = '1563'
                                        source = 'www.boschcarservice.com/pt'
                                    else:
                                        iso2 = country
                                        contract = 'ungewußt'
                                    check = checkduplicate(OUTPUT, name, street, plz, city)
                                    if check and iso2 in valid_countries:
                                        print(f'garage {k}')
                                        # print('search by: ', row_csv[0])
                                        # print('name: ' + str(name))
                                        # print('street: ' + street)
                                        # print('city: ' + city)
                                        # print('plz: : ' + plz)
                                        # print('country: ', country)
                                        # print('services: ' + str(services))
                                        # print('web: ', web)
                                        # print('phone: ' + str(phone))
                                        # print('fax: ', fax)
                                        # print('email: ' + str(email))
                                        # print('latitude: ' + str(lat))
                                        # print('longitude: ' + str(lng))
                                        print('------------------------------------------------')
                                        k += 1
                                        my_liste.append([{
                                            'street': street,
                                            'city': city,
                                            'postal_code': plz,
                                            'latitude': lat,
                                            'longitude': lng,
                                        }, {
                                            'abc': 'ID',
                                            'country': iso2,
                                            'target_groups': 'independent car service',
                                            'contracts': contract,
                                            'name': name,
                                            'phone': phone,
                                            'fax': fax,
                                            'web': web,
                                            'email': email,
                                            'services': services,
                                            'garage_id': garage_id,
                                            'contact_title': '',
                                            'contact_first_name': firstname,
                                            'contact_last_name': lastname,
                                            'contact_position': '',
                                            'contact_email': '',
                                            'source': source
                                        }])

                                        # with open('Bosch.csv', 'a', newline='', encoding="utf-8") as csvfile:
                                        #     csv_writer = csv.writer(csvfile)
                                        #     csv_writer.writerow(
                                        #         [name, street, city, plz, contract, country, iso2, phone, fax, web, email, services,
                                        #          lat, lng, garage_id])
                    except:
                        print('no bosch service exist')
        l += 1

with open('Bosch_area_osmnx.csv', 'w', newline='', encoding="utf-8") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        ['street', 'city', 'postal_code', 'country', 'latitude', 'longitude', 'area nähste', 'Anzahl der Eckpunkten',
         'area liste', 'area min', 'area median', 'suche form', 'web'])


def get_epsg_code(latitude, longitude):
    # Bestimme die UTM-Zone
    utm_zone = int((longitude + 180) / 6) + 1

    # Bestimme, ob es Nord- oder Südhalbkugel ist
    if latitude >= 0:
        epsg_code = f"326{utm_zone:02d}"  # Nördliche Hemisphäre
    else:
        epsg_code = f"327{utm_zone:02d}"  # Südliche Hemisphäre

    return epsg_code


def area_berechen(building, lat, lng):
    area_liste = []

    epsg_code = int(get_epsg_code(lat, lng))

    for ind in range(len(building)):
        building_polygon = building.iloc[ind].geometry
        gdf2 = gpd.GeoDataFrame([1], geometry=[building_polygon], crs="EPSG:4326")
        gdf_utm = gdf2.to_crs(epsg=epsg_code)  # 32633 - mitteleuropa
        area = round(gdf_utm['geometry'].area[0], 2)
        area_liste.append(area)
    return area_liste


def median(liste):
    liste.sort()
    n = len(liste)
    mitte = n // 2
    if n % 2 != 0:
        return liste[mitte]
    else:
        return liste[mitte - 1]


def get_geometry(building, lat, lng):
    epsg_code = int(get_epsg_code(lat, lng))
    building_polygon = building.iloc[0].geometry
    gdf2 = gpd.GeoDataFrame([1], geometry=[building_polygon], crs="EPSG:4326")
    gdf_utm = gdf2.to_crs(epsg=epsg_code)  # 32633 - mitteleuropa
    area = round(gdf_utm['geometry'].area[0], 2)

    num_vertices = len(building_polygon.exterior.coords) - 1

    area_liste = area_berechen(building, lat, lng)
    # area = area_liste[0]
    area_min = min(area_liste)
    area_median = median(area_liste)

    return area_liste, area, area_min, area_median, num_vertices


pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

print('length liste', len(my_liste))
for garage in tqdm(my_liste, desc='my_liste'):
    lat = garage[0]['latitude']
    lng = garage[0]['longitude']
    plz = garage[0]['postal_code']
    street = garage[0]['street']
    city = garage[0]['city']
    web = garage[1]['web']
    iso2 = garage[1]['country']
    country = pycountry.countries.get(alpha_2=iso2).name
    print('\niso2: ', iso2)
    print('country: ', country)
    print('latitude: ' + str(lat))
    print('longitude: ' + str(lng))
    print('street: ' + street)
    print('city: ' + city)
    print('plz: : ' + plz)

    place_name = street.strip() + ', ' + city + ', ' + country

    print('place name: ', place_name)
    place = ''

    try:
        building = ox.geometries_from_place(place_name, tags={'building': True})
        area_liste, area, area_min, area_median, num_vertices = get_geometry(building, lat, lng)

    except (TypeError, InsufficientResponseError):
        try:
            building = ox.features_from_point((lat, lng), tags={'building': True}, dist=10)
            area_liste, area, area_min, area_median, num_vertices = get_geometry(building, lat, lng)

        except InsufficientResponseError:
            area_liste = area_min = area_median = area = num_vertices = 'no data'

    # print(building.head())
    print('gesuchte Form: ', place)
    print('area liste: ', area_liste)
    print('area min: ', area_min)
    print('area median: ', area_median)
    print('--------------------------------------')

    with open('Bosch_area_osmnx.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            [street, city, plz, country, lat, lng, area, num_vertices, area_liste, area_min, area_median, place, web])


# def get_geometry(building, lat, lng):
#     epsg_code = int(get_epsg_code(lat, lng))
#
#     building_polygon = building.iloc[0].geometry
#     gdf2 = gpd.GeoDataFrame([1], geometry=[building_polygon], crs="EPSG:4326")
#     gdf_utm = gdf2.to_crs(epsg=epsg_code)  # 32633 - mitteleuropa
#
#     area_punkt = round(gdf_utm['geometry'].area[0], 2)
#
#     try:
#         area = f"{area_punkt:.2f}".replace('.', ',')
#         num_eckpunkten = str(len(building_polygon.exterior.coords) - 1)
#     except AttributeError:
#         area, num_eckpunkten = None
#
#     return area, num_eckpunkten



# def get_area(garage):
#     lat = garage['latitude']
#     lng = garage['longitude']
#     plz = garage['postal_code']
#     street = garage['street']
#     city = garage['city']
#     iso2 = garage['country']
#     country = pycountry.countries.get(alpha_2=iso2).name
#     place_name = street.strip() + ', ' + city
#
#     # print('\niso2: ', iso2)
#     # print('country: ', country)
#     # print('latitude: ' + str(lat))
#     # print('longitude: ' + str(lng))
#     # print('street: ' + street)
#     # print('city: ' + city)
#     # print('plz: : ' + plz)
#     # print('place name: ', place_name)
#     try:
#         building = ox.features_from_place(place_name, tags={'building': True})
#         area, num_eckpunkten = get_geometry(building, lat, lng)
#         umkreis = '0'
#     except (TypeError, InsufficientResponseError):
#         try:
#             building = ox.features_from_point((lat, lng), tags={'building': True}, dist=10)
#             area, num_eckpunkten = get_geometry(building, lat, lng)
#             umkreis = '10'
#         except InsufficientResponseError:
#             try:
#                 building = ox.features_from_point((lat, lng), tags={'building': True}, dist=20)
#                 area, num_eckpunkten = get_geometry(building, lat, lng)
#                 umkreis = '20'
#             except InsufficientResponseError:
#                 try:
#                     building = ox.features_from_point((lat, lng), tags={'building': True}, dist=30)
#                     area, num_eckpunkten = get_geometry(building, lat, lng)
#                     umkreis = '30'
#                 except InsufficientResponseError:
#                     try:
#                         building = ox.features_from_point((lat, lng), tags={'building': True}, dist=40)
#                         area, num_eckpunkten = get_geometry(building, lat, lng)
#                         umkreis = '40'
#                     except InsufficientResponseError:
#                         try:
#                             building = ox.features_from_point((lat, lng), tags={'building': True}, dist=50)
#                             area, num_eckpunkten = get_geometry(building, lat, lng)
#                             umkreis = '50'
#                         except InsufficientResponseError:
#                             try:
#                                 building = ox.features_from_point((lat, lng), tags={'building': True}, dist=100)
#                                 area, num_eckpunkten = get_geometry(building, lat, lng)
#                                 umkreis = '100'
#                             except InsufficientResponseError:
#                                 area = num_eckpunkten = umkreis = None
#     if not area:
#         umkreis = None
#
#     return area, umkreis, num_eckpunkten