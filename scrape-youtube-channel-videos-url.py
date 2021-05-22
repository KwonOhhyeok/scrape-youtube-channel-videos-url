# https://github.com/banhao/scrape-youtube-channel-videos-url
# scrape-youtube-channel-videos-url.py
#_*_coding: utf-8_*_

import os
import requests
import sys, time, datetime
from selenium import webdriver

channelid = sys.argv[1]

# ex. 'https://www.youtube.com/channel/UCcloDgiDqz8twby7zvG-USg/videos'
url = 'https://www.youtube.com/channel/%s/videos' % channelid
response = requests.get(url)
if response.status_code != 200:
    # ex. 'https://www.youtube.com/c/tvchanews/videos'
    url = 'https://www.youtube.com/c/%s/videos' % channelid
    response = requests.get(url)
    assert response.status_code == 200

#driver = webdriver.Chrome()
opt = webdriver.ChromeOptions()
opt.add_argument('--headless')
driver = webdriver.Chrome(options=opt)
driver.get(url)
time.sleep(5)
dt = datetime.datetime.now().strftime("%Y%m%d")
height = driver.execute_script("return document.documentElement.scrollHeight")
lastheight = 0

while True:
    if lastheight == height:
        break
    lastheight = height
    driver.execute_script("window.scrollTo(0, " + str(height) + ");")
    time.sleep(3)
    height = driver.execute_script("return document.documentElement.scrollHeight")

if not os.path.exists('data/%s' % channelid):
    os.makedirs('data/%s' % channelid)

with open('data/%s/%s.list' % (channelid, dt), 'w') as fout:
    user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
    for i in user_data:
        link = i.get_attribute('href')
        print(link, file=fout)

driver.close()


