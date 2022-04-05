from attr import attr
import requests
from bs4 import BeautifulSoup as BS

# headers = {
#     'Access-Control-Allow-Origin': '*',
#     'Access-Control-Allow-Methods': 'GET',
#     'Access-Control-Allow-Headers': 'Content-Type',
#     'Access-Control-Max-Age': '3600',
#     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
#     }

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
req = requests.get(url)
soup = BS(req.content, 'html.parser')
lister = soup.findAll('div', attrs={'class':'lister'})
movies = []
for item in lister:
    movies.append(item.table.tbody.tr)
for item in movies:
    print(item)