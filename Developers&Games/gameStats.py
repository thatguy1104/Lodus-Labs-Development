import requests
import json
from bs4 import BeautifulSoup
import lxml

url = 'https://www.androidrank.org/api/application/com.whatsapp?key=9GmLbwMLMgxz3BeAo3Two0NzeuRVN8Jin6EPcerWVfesQH4BhLuLeUSlETXfrnMd'
response = requests.get(url)
print(response)