from attr import attr
import requests
from bs4 import BeautifulSoup as BS

class ParseRequests(object):
    def parse_url(self, url):
        header = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Accept-Language': 'en-US,en;q=0.5'
            }

        parsed_list = []
        req = requests.get(url, headers=header)
        soup = BS(req.content, 'html.parser')
        titles = soup.findAll('td', attrs={'class':'titleColumn'})
        for item in titles:
            parsed_list.append('https://www.imdb.com'+item.a.get('href'))
        return parsed_list
shows_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

movies = ParseRequests().parse_url(movies_url)
shows = ParseRequests().parse_url(shows_url)

print(len(movies), len(shows))

for item in movies:
    print(item)
