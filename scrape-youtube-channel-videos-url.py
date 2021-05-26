# https://github.com/banhao/scrape-youtube-channel-videos-url
# scrape-youtube-channel-videos-url.py
#_*_coding: utf-8_*_

import os
import requests
import traceback
import sys, time, datetime
from selenium import webdriver

with open('download.list', 'r') as fp:
    channel_list = map(lambda x: x.split('\t')[0], fp.read().splitlines())
    channel_list = filter(lambda x: not x.startswith('#'), channel_list)
    channel_list = list(channel_list)

for channelid in channel_list:
    # ex. 'https://www.youtube.com/channel/UCcloDgiDqz8twby7zvG-USg/videos'
    url = 'https://www.youtube.com/channel/%s/videos' % channelid
    response = requests.get(url)
    if response.status_code != 200:
        # ex. 'https://www.youtube.com/c/tvchanews/videos'
        url = 'https://www.youtube.com/c/%s/videos' % channelid
        response = requests.get(url)
        if response.status_code != 200:
            # ex. 'https://www.youtube.com/user/hsdjang8/videos'
            url = 'https://www.youtube.com/user/%s/videos' % channelid
            response = requests.get(url)
            if response.status_code != 200:
                print('error: requests get channelid: %s' % channelid)
                continue

    #driver = webdriver.Chrome()
    opt = webdriver.ChromeOptions()
    opt.add_argument('--headless')
    driver = webdriver.Chrome(options=opt)
    driver.get(url)
    time.sleep(5)
    dt = datetime.datetime.now().strftime("%Y%m%d")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    lastheight = 0

    scroll_count = 0
    while True:
        print(height)
        if lastheight == height:
            break
        if scroll_count > 15:
            break
        lastheight = height
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        time.sleep(5)
        height = driver.execute_script("return document.documentElement.scrollHeight")
        scroll_count += 1

    if not os.path.exists('data/%s' % channelid):
        os.makedirs('data/%s' % channelid)

    with open('data/%s/%s.list' % (channelid, dt), 'w') as fout:
        user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')
        for i in user_data:
            try:
                link = i.get_attribute('href')
                print(link, file=fout)
            except:
                traceback.print_exc()
                continue

    driver.close()

