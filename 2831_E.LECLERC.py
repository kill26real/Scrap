import csv
import datetime, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
url = 'https://www.auto.leclerc/centre-auto'
driver.maximize_window()
driver.get(url)

with open('2831_E.LECLERC_werkstattdb.csv', 'w', newline='', encoding="utf-8") as csvfile:
   csv_writer = csv.writer(csvfile)
   csv_writer.writerow(
       ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone',
        'fax', 'web', 'email', 'services', 'latitude', 'longitude', 'garage_id', 'sources'])


def get_info(web, garage_id):
    mail = ""
    street = ""
    plz = ""
    city = ""
    name = ''
    service = ''
    lat = ''
    lng = ''

    time.sleep(1)

    name = driver.find_element(By.XPATH, '//*[@id="top_info"]/h1').text

    address = driver.find_element(By.XPATH, '//*[@id="agences"]/div[3]/div[1]').text.splitlines()

    print('address', address)
    print('name', name)

    plz = address[-2][:5]
    city = address[-2][6:]
    phone = address[-1]

    if address[-4] != 'OÙ NOUS TROUVER':
        street = address[-4] + address[-3]
    else:
        street = address[-3]

    print('info', street)
    print(plz)
    print(city)
    print(phone)


    with open('2831_E.LECLERC_werkstattdb.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['abc', 'FR', 'IAM Autocenter', 'E.LECLERC', name, street, city, plz, phone, '', web, '', service, lat,
             lng, garage_id, 'https://www.auto.leclerc/'])
    print('-------------------------------------------------------------------------')

def cookies():
    try:
        accept_cookies_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]'))
        )
        accept_cookies_button.click()
        print("Cookies akzeptiert")
    except Exception as e:
        print(f"Fehler beim Akzeptieren der Cookies")

cookies()

garages = driver.find_elements(By.CLASS_NAME, 'woosmap-tableview-cell')

print('Len', len(garages))
i = 0
for garage in garages:
    i += 1
    print(f'{i} of {len(garages)}')

    all_info = garage.find_element(By.CLASS_NAME, "btn.btn-large.btn-primary.cart-res.blue-w-btn.i_save")
    time.sleep(2)
    garage_id = all_info.get_attribute('onclick')[-14:-1]
    all_info.click()
    time.sleep(1)
    link = driver.current_url
    # garage_id = garage.get_attribute('id')
    print('link', link)
    print('id', garage_id)
    get_info(link, garage_id)
    driver.back()

