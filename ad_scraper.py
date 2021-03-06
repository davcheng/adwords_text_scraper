from bs4 import BeautifulSoup
import requests
import sqlite3
import re
from urllib.request import urlopen
import urllib

# array of objects
item_list = ["phone", "smartphone"]

# create db to store
# conn = sqlite3.connect('ads.db')
# c = conn.cursor()
# c.execute('DROP TABLE IF EXISTS ads;')
# c.execute('CREATE TABLE ads ( id integer primary key autoincrement, item text not null, ad_text text);')

# main ad scraper
def get_ads_for_item(item):

    # get google ads
    google_ad_scrape(item)
    # bing_ad_scrape(item)


def google_ad_scrape(item):
    google_address = "http://www.google.com/search?q={0}&num=100&hl=en&start=0".format(item)

    # spoofing agent
    request = urllib.request.Request(google_address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page, 'html.parser')

    # get headline text
    for node in soup.findAll(attrs={'class': re.compile(r".*\bads-creative\b.*")}):
        # headline
        print(node.text)
        write_to_output_file(node.text)
        # subtext
        print(node.findNext('div').contents[0])
        write_to_output_file(node.findNext('div').contents[0])


def bing_ad_scrape(item):
    bing_address = "https://www.bing.com/search?q={0}".format(item)

    # spoofing agent
    request = urllib.request.Request(bing_address, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page, 'html.parser')

    # get body text
    for node in soup.findAll(attrs={'class': re.compile(r".*\bb_secondaryText\b.*")}):
        # print(node.findPrevious('p').contents[0])
        # write_to_output_file(node.findPrevious('p').contents[0])
        for text_line in node.contents:
            print(text_line)
            write_to_output_file(text_line)


def write_to_output_file(write_content):
    with open("Output.txt", "a") as output_file:
        output_file.write(write_content)
        output_file.write("\n")


if __name__ == '__main__':
    for item in item_list:
        get_ads_for_item(item)
