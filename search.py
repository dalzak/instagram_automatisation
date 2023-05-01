from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import re
from time import sleep
import csv 
import requests
from urllib.request import urlopen
import urllib.error
import os
import random

class search:

    def __init__(self, platform, topic, video_type, csvfolder, number_of_vids_per_day, mp4_folder, number_of_scrolls):

        self.platform = platform
        self.topic = topic
        self.csvfolder = csvfolder
        self.video_type = video_type
        self.number_of_vids_per_day = number_of_vids_per_day
        self.mp4_folder = mp4_folder
        self.number_of_scrolls = number_of_scrolls


    def links(self):

        driver = webdriver.Chrome(executable_path="/path/to/chromedriver")     

        print('goes to website...')
        
        driver.get(f"https://www.tiktok.com/search/video?lang=en&q={self.topic}%20{self.video_type}")
        
        sleep(30)

        print('scrolls down...')

        for i in range(0, self.number_of_scrolls):
            driver.find_element("xpath", '//*[@id="main-content-search_video"]/div[2]/div[2]/button').click()
            print("xxxx")
            sleep(5)

        print('scrapes the href...')
        soup = BeautifulSoup(driver.page_source, "html.parser")
        scrapped_video_links = soup.find_all('div', {'class': 'tiktok-yz6ijl-DivWrapper e1cg0wnj1'})

        
        print('writes all links to folder...')

        with open(f"{self.csvfolder}.csv", 'a') as file:

            writer = csv.DictWriter(file, fieldnames=["URL"])
            
            for links in scrapped_video_links:  
                writer.writerow({"URL": links.a['href']})

        return 

        

    def download(self):
        
        with open(f"{self.csvfolder}.csv") as file:
            reader  = csv.DictReader(file, fieldnames=["URL"])
            url_list = [rows['URL'] for rows in reader]
        
        print("readin urls...")
        
        random_post_index = random.randint(0, len(url_list))

        headers = {
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'HX-Target': 'target',
            'HX-Current-URL': 'https://ssstik.io/en',
            'sec-ch-ua-mobile': '?1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://ssstik.io/en',
            'HX-Trigger': '_gcaptcha_pt',
            'HX-Request': 'true',
            'sec-ch-ua-platform': '"Android"',
        }

        params = {
            'url': 'dl',
        }

        data = {
            'id': url_list[random_post_index],
            'locale': 'en',
            'tt': 'VEtzd3Q_',
        }



        max_retries = 3
        retry_delay = 5

        for i in range(max_retries):
            try:
                
                print(f"sending request, on try number: {i}")

                response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
                download_soup = BeautifulSoup(response.text, 'html.parser')

                print("success!")

                sleep(2)

                break

            except requests.exceptions.RequestException as e:

                print(f"Error: {e}")
                sleep(retry_delay)


        for i in range(max_retries):
            try:
                

                sleep(2)

                print("url_opening...")

                download_link = urlopen(download_soup.a["href"])

                print("urlopen!")

                break

            except urllib.error.HTTPError as e:

                print(f"Error: {e}")
                sleep(retry_delay)

        

        matches = re.search(r"^.*com/(.*)/video.*$", str(url_list[random_post_index])).groups(1)

        with open(f"downloaded_videos/{matches}.mp4", 'wb') as output:    
            while True:
                data = download_link.read(4096)
                if not data:
                    break
                output.write(data)
        output.close()

        print("video downloaded")

        print(url_list[random_post_index])

        url_list.remove(url_list[random_post_index])

        with open(f"{self.csvfolder}", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['URL'])
            writer.writerows([[url] for url in url_list])
        file.close()

        return f"{matches}.mp4"
    
