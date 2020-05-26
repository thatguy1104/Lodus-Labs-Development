from bs4 import BeautifulSoup
import requests
import lxml
import json


class GameStats():
    def __init__(self):
        self.link = 'https://steamcharts.com/top/p.'
        