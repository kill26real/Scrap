import csv
import datetime, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementNotVisibleException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from deep_translator import GoogleTranslator
import pandas as pd
import os
from test_input import send_data_csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
url = 'https://www.wurth.fi/'
driver.maximize_window()
driver.get(url)

with open('2780_Wurth_raw_werkstattdb.csv', 'w', newline='', encoding="utf-8") as csvfile:
   csv_writer = csv.writer(csvfile)
   csv_writer.writerow(
       ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone',
        'fax', 'web', 'email', 'services', 'latitude', 'longitude', 'garage_id', 'sources'])

try:
    accept_cookies_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'button-optin.btn.btn-block.btn-info')))
    accept_cookies_button.click()
    print("Cookies akzeptiert")
except Exception as e:
    print(f"Fehler beim Akzeptieren der Cookies")

time.sleep(1)

aktive = driver.find_element(By.XPATH, '//*[@id="megaDropdown"]/div/div[1]/ul/li[4]/a')
aktive.click()

time.sleep(2)

main = driver.find_element(By.XPATH, '//*[@id="map_canvas"]/div/div[3]/div[1]/div[2]/div/div[3]')
garages = main.find_elements("tag name", "div")

print('Len', len(garages))
for i in range(1, len(garages) + 1):
    print(f'{i} of {len(garages)}')
    time.sleep(3)

    garage = driver.find_element(By.XPATH, f'//*[@id="map_canvas"]/div/div[3]/div[1]/div[2]/div/div[3]/div[{i}]')
    driver.execute_script("arguments[0].click();", garage)

    addresse = driver.find_element(By.XPATH, '//*[@id="layout2col_content"]/div[4]/div/div[1]/p[1]').text.splitlines()
    print('address', addresse)

    email = str(addresse[-1]).lower()
    phone = addresse[-2]
    plz = str(addresse[-4][:5])
    city = addresse[-4][6:]
    street = addresse[-5]
    name = addresse[-6]

    print('name', name)
    print('street', street)
    print('plz', plz)
    print('city', city)
    print('phone', phone)
    print('email', email)

    service = ''
    try:
        suche = driver.find_element(By.XPATH, '//*[@id="layout2col_content"]/div[4]/div/div[3]/ul')
        services = suche.find_elements(By.TAG_NAME, 'li')
        for serv in services:
            service = service + GoogleTranslator(source='auto', target='en').translate(serv.text) + ' | '
        service = service[:-3]
    except NoSuchElementException:
        pass
    print('services :', service)

    link = driver.find_element(By.XPATH, '//*[@id="layout2col_content"]/div[4]/div/div[1]/p[2]/a').get_attribute('href')
    print('link', link)
    driver.back()
    print('--------------------------------------------')

    with open('2780_Wurth_raw_werkstattdb.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['abc', 'ESP', 'Direct Marketer', 'Würth', name, street, city, plz, phone, '', link, email, service, '',
             '', '', 'https://www.wurth.fi/'])

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

