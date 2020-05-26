from bs4 import BeautifulSoup
import requests
import lxml

class steamConcurrent():
    def __init__(self):
        self.link = 'https://store.steampowered.com/stats/'
        self.response = requests.get(self.link)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def getConcurrent(self):
        all_current = self.soup.find_all('span', class_='statsTopHi')
        current = all_current[0].text.replace(',', '')
        peak_today = all_current[1].text.replace(',', '')
        print("Concurrent Steam Users:	")
        print("Current:", int(current))
        print("Peak:", int(peak_today))

    # def getTopGamesByPlayerCount(self):

