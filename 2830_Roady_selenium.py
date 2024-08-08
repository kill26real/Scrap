import csv
import requests
from bs4 import BeautifulSoup
import json
import datetime, time
import urllib3
import datetime, time
import urllib3
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, ElementNotInteractableException, ElementNotVisibleException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)
url = 'https://www.roady.fr/'
driver.maximize_window()
driver.get(url)

# with open('2830_Roady_werkstattdb.csv', 'w', newline='', encoding="utf-8") as csvfile:
#    csv_writer = csv.writer(csvfile)
#    csv_writer.writerow(
#        ['abc', 'country', 'target_groups', 'contracts', 'name', 'street', 'city', 'postal_code', 'phone',
#         'fax', 'web', 'email', 'services', 'latitude', 'longitude', 'garage_id', 'sources'])


def get_info(web):
    mail = ""
    street = ""
    plz = ""
    city = ""
    name = ''
    service = ''
    lat = ''
    lng = ''

    time.sleep(1)

    address = driver.find_element(By.XPATH, '//*[@id="content-column"]/div/div[1]/div/div[3]/div[2]/div/div[1]/address').text.splitlines()
    name = address[0]
    street = address[-3]
    plz = address[-2][:5]
    city = address[-2][6:]
    print('name', name)
    print(street)
    print(plz)
    print(city)

    phone_info = driver.find_element(By.CLASS_NAME, 'store-phone.hidden-md.hidden-sm.hidden-xs').text.split('.')
    phone = ''.join(phone_info)
    print('phone', phone)

    services = driver.find_elements(By.CLASS_NAME, 'service')
    for serv in services:
        service += serv.text + ' | '
    service = service[:-2]
    print('services', service)


    # map = driver.find_element(By.XPATH, '//*[@id="content-column"]/div/div[1]/div/div[3]/div[1]/div[2]/div[1]/a')
    # href = map.get_attribute('href')
    # print('map link', href)
    # pattern = re.compile(r'@(.*?),(.*?)/')
    # match = pattern.search(href)
    # if match:
    #     lat = match.group(1)
    #     lng = match.group(2)
    #     print(f"Latitude: {lat}, Longitude: {lng}")
    # else:
    #     print("Keine Koordinaten in der URL gefunden.")


    with open('2830_Roady_werkstattdb.csv', 'a', newline='', encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ['abc', 'FR', 'IAM Autocenter', 'Roady', name, street, city, plz, phone, '', web, '', service, lat,
             lng, '', 'https://www.roady.fr/'])
    print('-------------------------------------------------------------------------')



def cookies():
    try:
        accept_cookies_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="didomi-notice-agree-button"]'))
        )
        accept_cookies_button.click()
        print("Cookies akzeptiert")
    except Exception as e:
        print(f"Fehler beim Akzeptieren der Cookies")



def find_objects(place):
    try:
        dropdown = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/nav/div[4]/div[1]/div[2]/div/div/button')
        dropdown.click()
    except (ElementClickInterceptedException, NoSuchElementException):
        try:
            dropdown = driver.find_element(By.CLASS_NAME, 'navbar-link.dropdown-toggle.headerDropdown-toggle')
            dropdown.click()
        except:
            pass

    time.sleep(2)

    try:
        dropdown2 = driver.find_element(By.XPATH, '//*[@id="header"]/div[1]/div/nav/div[4]/div[1]/div[2]/div/div/div/button')
        dropdown2.click()
    except (NoSuchElementException, ElementNotInteractableException):
        try:
            dropdown2 = driver.find_element(By.CLASS_NAME, 'headerDropdown-link.headerShortStore-link.btn.btn-link.btn-quaternary')
            dropdown2.click()
        except:
            pass
    time.sleep(2)

    try:
        suche = driver.find_element(By.XPATH, '//*[@id="999_autocomplete"]')
    except NoSuchElementException:
        try:
            suche = driver.find_element(By.CLASS_NAME, 'form-control.searchForm-input.pac-target-input')
        except NoSuchElementException:
            suche = driver.find_element(By.ID, '999_autocomplete')

    time.sleep(2)
    suche.send_keys(f"{place}")
    time.sleep(1)
    suche.send_keys(Keys.ARROW_DOWN)
    suche.send_keys(Keys.ENTER)
    time.sleep(1)

    try:
        killometer = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div/div/ul/li[2]/span[6]')
        killometer.click()
        time.sleep(1)
    except NoSuchElementException:
        pass


places = ('Marmande', 'Cholet', 'Reims', 'Grenoble')

for place in places:
    cookies()
    find_objects(place)
    elements = driver.find_elements(By.CLASS_NAME, 'storelocatorSearch__store')
    print('Len', len(elements))

    for i in range(len(elements)):
        print(f'{i} of {len(elements)} :', place)
        xpath = f'/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div[{i+1}]/div[3]/a'
        time.sleep(2)
        try:
            all_info = driver.find_element(By.XPATH, xpath)
        except (NoSuchElementException, ):
            try:
                info = driver.find_elements(By.TAG_NAME, 'a')
                for inf in info:
                    all_info = inf.find_element(By.CLASS_NAME, 'btn.btn-sm.btn-transparent')
            except:
                all_info = driver.find_element(By.CSS_SELECTOR,
                                            'body > div.modal.modal-sticky.modal-hidden-stack.modal-stack-idx-1.fade.in > '
                                            'div > div > div:nth-child(2) > div:nth-child(2) > div > div > div > div:nth-child(1) > '
                                            'div > div > div:nth-child(1) > div.storelocatorSearch__store-buttons > a')

        link = all_info.get_attribute('href')
        all_info.click()
        get_info(link)
        driver.back()
        find_objects(place)
















