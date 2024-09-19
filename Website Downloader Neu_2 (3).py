import os
import csv
import math
from datetime import datetime, timedelta
from urllib.parse import urlparse
from scrapy import Spider, Request
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.http import TextResponse
from urllib.parse import urljoin
import urllib.parse
from multiprocessing import Process,Manager
from scrapy.settings import Settings
from scrapy import signals
import subprocess
import logging
from scrapy.utils.log import configure_logging
import string
import time


logging.getLogger('scrapy').setLevel(logging.ERROR)

def read_websites():
    with open('websites.csv', 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        websites = list(reader)
        return websites
    
def load_csv(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            reader = csv.DictReader(f, delimiter=';')
            return list(reader)
    else:
        return []

class DefaultEncodingMiddleware:
    def process_response(self, request, response, spider):
        if isinstance(response, TextResponse):
            response._cached_ubody = None
            response._encoding = 'utf-8'
        return response

def sanitize_filename(filename):
    invalid_chars = '/\0\\?$"\'$&;|:*<>'
    valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and periods
    filename = filename.strip('. ')
    
    # Remove multiple underscores and replace with a single one
    filename = '_'.join(filter(None, filename.split('_')))
    
    # Remove any invalid characters again
    filename = ''.join(c for c in filename if c in valid_chars)
    
    return filename


class MySpider(Spider):
    name = 'myspider'
    max_count = 1
    #pid = self.instance
    
    def __init__(self, websites,instance):
        self.websites = websites
        self.instance = instance
        self.checked_urls_ = {}

    def start_requests(self):
        depth_limit = self.settings.get('DEPTH_LIMIT')
        pid = self.instance
        for website in self.websites:
            url = website['URL']
            if not url.startswith('http'):
                url = 'https://' + url
            if self.settings.get('KEEP_RUNNING') == True:
                yield Request(url, callback=self.parse_one, meta={'id': website['ID'], 'company': website['Company Name'], 'url': url,'depth_limit':depth_limit, 'depth': 0,})
            else:
                with open('restart_debugging.txt','a',encoding='utf-8') as a:
                    a.write(f'restarted at {datetime.now()}\n')
                break

    def parse_one(self, response):
            pid = self.instance
            soup = BeautifulSoup(response.body, 'html.parser')
            self.checked_urls_[response.meta['id']] = []
            for script in soup(['script', 'style']):
                script.extract()

            for tag in soup:
                if tag.string:
                    tag.string = " " + tag.string
            
            depth_limit = response.meta.get('depth_limit', 1)
            if depth_limit > 1:
                if response.status in [400,404,404,503]:
                    with open('non_working_ids_depth_1.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(response.meta['id'])
                        pass
                elif response.status >= 500:
                    with open('non_working_ids_depth_1.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(response.meta['id'])
                        pass
                elif response.status == 0:
                    with open('non_working_ids_depth_1.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(response.meta['id'])
                        pass
            else:
                if response.status in [400,404,404,503]:
                    with open('non_working_ids_deep.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(response.meta['id'])
                        pass
                elif response.status >= 500:
                    with open('non_working_ids_deep.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(response.meta['id'])
                        pass
                elif response.status == 0:
                    with open('non_working_ids_deep_1.csv', 'a', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(response.meta['id'])
                        pass
            ## check for \n
            text = soup.get_text(separator=' ')
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # Extract internal links
            links = [urljoin(response.url, link.get('href')) for link in soup.find_all('a', href=True)]
            links = [link for link in links if link.startswith('http')]
            text += "\n\nLinks:\n" + '\n'.join(links)

            # Extract image names and alt attributes
            images = [(img.get('src'), img.get('alt')) for img in soup.find_all('img', src=True)]
            text += "\n\nImage names and ALT attributes:\n" + '\n'.join([f'{src} - ALT: {alt}' for src, alt in images])

            # Create folder path
            if depth_limit > 1:
                folder_path = os.path.join(f"{datetime.now().year}-{datetime.now().month:02}_deep", response.meta['id'])
                try:
                    os.makedirs(folder_path, exist_ok=True)
                except Exception as e:
                    print(f"Process ID: {pid}, Company: {response.meta['id']} - Error creating folder: {e}")
            else:
                folder_path = os.path.join(f"{datetime.now().year}-{datetime.now().month:02}", response.meta['id'])
                try:
                    os.makedirs(folder_path, exist_ok=True)
                except Exception as e:
                    print(f"Process ID: {pid}, Company: {response.meta['id']} - Error creating folder: {e}")

            # Write the original text to a file
            original_filename = f"{response.meta['id']}-{response.meta['company']}.txt"
            original_filename = sanitize_filename(original_filename)
            with open(os.path.join(folder_path, original_filename), 'w', encoding='utf-8') as f:
                f.write(f'WOLK LINK FOR SCRAPING:\n{response.url}\n\n')
                f.write(text)
                f.write('\n\n\nPAGE END!\n\n\n')
            if depth_limit > 1:
                depth = 1
                self.checked_urls_[response.meta['id']] = [response.meta.get('url')]
                links_to_parse = [
                    urljoin(response.url, urllib.parse.quote(link.get('href'), safe=':/#?'))  # Encode the link URL
                    for link in soup.find_all('a', href=True)
                    if urlparse(link.get('href')).netloc == urlparse(response.url).netloc
                ]
                links_to_parse = [
                    link for link in links_to_parse 
                    if link.startswith('http') and not link.endswith('.pdf')
                ]
                for link in links_to_parse:
                  yield Request(link, callback=self.parse_more, meta={'id': response.meta['id'], 'company': response.meta['company'], 'url': link, 'depth': depth})


              
    def parse_more(self, response):
        pid = self.instance
        depth_limit = response.meta.get('depth_limit', 1)
        depth = response.meta.get('depth', 1)
        checked_urls = self.checked_urls_[response.meta['id']]
        if depth <= depth_limit:
            current_url = response.url

            if current_url not in checked_urls:
                print(f"Process ID: {pid}, Company: {response.meta['id']} - Processing: {response.url}")

                soup = BeautifulSoup(response.body, 'html.parser')
                for script in soup(['script', 'style']):
                    script.extract()

                for tag in soup:
                    if tag.string:
                        tag.string = " " + tag.string

                # check for \n
                text = soup.get_text(separator=' ')
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

                # Extract internal links
                links = [urljoin(response.url, link.get('href')) for link in soup.find_all('a', href=True)]
                links = [link for link in links if link.startswith('http')]
                text += "\n\nLinks:\n" + '\n'.join(links)

                # Extract image names and alt attributes
                images = [(img.get('src'), img.get('alt')) for img in soup.find_all('img', src=True)]
                text += "\n\nImage names and ALT attributes:\n" + '\n'.join([f'{src} - ALT: {alt}' for src, alt in images])

                # Create folder path
                folder_path = os.path.join(f"{datetime.now().year}-{datetime.now().month:02}_deep", response.meta['id'])
                os.makedirs(folder_path, exist_ok=True)

                sanatized_url = sanitize_filename(response.meta.get('url'))

                # Write the original text to a file
                original_filename = f"{response.meta['id']}-{response.meta['company']}_{sanatized_url}.txt"
                original_filename = sanitize_filename(original_filename)
                with open(os.path.join(folder_path, original_filename), 'w', encoding='utf-8') as f:
                    f.write(f'WOLK LINK FOR SCRAPING:\n{current_url}\n\n')
                    f.write(text)
                    f.write('\n\n\nPAGE END!\n\n\n')

                # Update checked_urls and create a copy for the next request
                self.checked_urls_[response.meta['id']].append(current_url)

                links_to_follow = [
                    urljoin(current_url, urllib.parse.quote(link.get('href'), safe=':/#?'))  # Encode the link URL
                    for link in soup.find_all('a', href=True)
                    if urlparse(link.get('href')).netloc == urlparse(current_url).netloc
                ]
                links_to_follow = [
                    link for link in links_to_follow 
                    if link.startswith('http') and not link.endswith('.pdf')
                ]

                for link in links_to_follow:
                    yield Request(link, callback=self.parse_more, meta={'id': response.meta['id'], 'company': response.meta['company'], 'url': link, 'depth': depth})
                    response.meta['depth'] = depth + 1
                else:
                    # print(f"Process ID: {pid}, Company: {response.meta['id']} - Already processed {response.url}")
                    pass
                f.close()


def run_spider(websites,settings,instance_number):
    settings['LOG_LEVEL'] = 'ERROR'  # Set log level to ERROR
    settings['LOG_ENABLED'] = False  # Disable logging
    process = CrawlerProcess(settings)
    process.crawl(MySpider, websites=websites,instance=instance_number)
    process.start()


if __name__ == "__main__":
    there_are_more_websites = True
    while there_are_more_websites:
        configure_logging({'LOG_LEVEL': 'ERROR'})
        websites = read_websites()
        new_websites = []
        custom_settings = {
        'DEPTH_LIMIT': 3,
        'DOWNLOAD_DELAY': 0.5,
        'DOWNLOAD_FAIL_ON_DATALOSS': False,
        'CONCURRENT_REQUESTS': 20,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 20,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'KEEP_RUNNING':True,
        'AUTOTHROTTLE_ENABLED':True 
        }   
        if custom_settings['DEPTH_LIMIT'] == 1:
            date_folder = f"{datetime.now().year}-{datetime.now().month:02}"
            for website in websites:
                    non_working_ids = load_csv('non_working_ids_depth_1.csv')
                    id_folder = website['ID']
                    full_folder_path = os.path.join(date_folder, id_folder)
                    if os.path.isdir(full_folder_path):
                        print(f"ID {website['ID']} has already been processed this month. Skipping.")
                        continue
                    elif website['ID'] in non_working_ids:
                        print(f"ID {website['ID']} has already been processed this month. Skipping.")
                        continue
                    else:
                        new_websites.append(website)
        else:
            date_folder = f"{datetime.now().year}-{datetime.now().month:02}_deep"
            for website in websites:
                    non_working_ids = load_csv('non_working_ids_deep.csv')
                    id_folder = website['ID']
                    full_folder_path = os.path.join(date_folder, id_folder)
                    if os.path.isdir(full_folder_path):
                        print(f"ID {website['ID']} has already been processed this month. Skipping.")
                        continue
                    elif website['ID'] in non_working_ids:
                        print(f"ID {website['ID']} has already been processed this month. Skipping.")
                        continue
                    else:
                        new_websites.append(website)
        if len(new_websites) > 0:
            websites = new_websites
        else:
            there_are_more_websites = False
            break

        settings = Settings()
        settings.setdict(custom_settings)

        start_time = datetime.now()
        two_hours_later = start_time + timedelta(hours=2)

        n = 15  # number of spider processes
        chunk_size = math.ceil(len(websites) / n)

        processes = []
        for i in range(n):
            chunk = websites[i * chunk_size: (i + 1) * chunk_size]
            p = Process(target=run_spider, args=(chunk,custom_settings,i+1))
            p.start()
            processes.append(p)

        while datetime.now() < two_hours_later:
            continue
        
        # Update the keep_running flag to False in the Spider class
        for process in processes:
            custom_settings['KEEP_RUNNING'] = False

        # Wait for ongoing processes to finish before restarting
        for process in processes:
            process.join()
        
        break

