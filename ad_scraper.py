from bs4 import BeautifulSoup
import requests
import sqlite3
import re
from urllib.request import urlopen
import urllib

# array of objects
item_list = ["phone", "smartphone"]

# create db to store
conn = sqlite3.connect('ads.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS ads;')
c.execute('CREATE TABLE ads ( id integer primary key autoincrement, item text not null, ad_text text);')

# main ad scraper
def get_ads_for_item(item):

    # get google ads
    google_ad_scrape(item)
    bing_ad_scrape(item)


def google_ad_scrape(item):
    google_address = "http://www.google.com/search?q={0}&num=100&hl=en&start=0".format(item)

    # spoofing agent
    request = urllib.request.Request(google_address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page, 'html.parser')

    # get headline text
    for node in soup.findAll(attrs={'class': re.compile(r".*\bads-creative\b.*")}):
        print(node.text)


def bing_ad_scrape(item):
    bing_address = "https://www.bing.com/search?q={0}".format(item)

    # spoofing agent
    request = urllib.request.Request(bing_address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page, 'html.parser')

    # get body text
    for node in soup.findAll(attrs={'class': re.compile(r".*\bb_secondaryText\b.*")}):
        print(node.text)


if __name__ == '__main__':
    for item in item_list:
        get_ads_for_item(item)
