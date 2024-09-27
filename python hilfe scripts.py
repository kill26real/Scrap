import re
import csv


# SELENIUM OPTIONS
# opts = webdriver.ChromeOptions()
# options = Options()
# options.add_argument("--disable-web-security")
# options.add_argument("--webdriver-logfile=webdrive.log")
# options.add_argument("--disable-popup-blocking")
# options.add_argument("--disable-notifications")
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# s = Service('C:\\Users\\emv\\chromedriver.exe')
# driver = webdriver.Chrome(service=s, options=options)



# REGEX FÜR WEBSEITEN
regex = r'https:\\/\\/www.blacktire.pt\\/blog\\/oficina\\/[a-zA-Z\-]+'


# ÜBERPRUFEN, OB STRING TEXT BUCHSTABEN HAT
# if bool(re.search(r'[a-zA-Z]', text)):
#     plz = ''
