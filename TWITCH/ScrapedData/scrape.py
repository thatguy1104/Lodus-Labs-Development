import requests
import json
from bs4 import BeautifulSoup
import lxml

def writeToJSON(file_data):
    with open('data.json', 'a') as outfile:
        json.dump(file_data, outfile)

def getOnePage(link_):
    response = requests.get(link_)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='ranked-item')
    data = {}

    for i in items:
        position = i.find('div', class_='ri-position hidden-xxs').text
        image = i.find('div', class_='ri-image')
        img = image.find('img')['src'].split(' ')[0]
        hours_watched = i.find('div', class_='ri-value').text.replace('\n', '')
        names = i.find('div', class_='ri-name').text.replace('\n', '')
        change = i.find('div', class_='ri-change hidden-xs').text.replace('\n', '').split('c')[0]
        share = i.find('div', class_='ri-share hidden-xs').text.replace('\n', '').split(' ')[0]

        data[names] = []
        data[names].append({
            'Rank'          : position,
            'Name'          : names,
            'HoursWatched'  : hours_watched,
            'PercentChange' : change,
            'PercentShare'  : share,
            'ImageLink'     : img
        })

    writeToJSON(data)

def all_pages():
    pages_count = 485
    with open('data.json', 'w') as outfile:
        json.dump('', outfile)

    for i in range(pages_count + 1):
        print("Loading {0} / {1}".format(i, pages_count))
        link = 'https://twitchtracker.com/games/time-watched?page=' + str(i)
        getOnePage(link)

all_pages()
