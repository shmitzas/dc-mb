import time
import requests
from bs4 import BeautifulSoup as BS
from multiprocessing import Process, Pool, freeze_support
import threading

class ParseRequests(object):
    def __init__(self):
        freeze_support()
        shows_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'
        movies_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
        movies = self.parse_url(movies_url)
        shows = self.parse_url

        print(len(movies))

        for item in movies:
            movie_data = self.parse_movie(item)
        print('passed')
    def parse_url(self, url):
        count = 0
        parsed_list = []
        req = requests.get(url)
        soup = BS(req.content, 'html.parser')
        titles = soup.findAll('td', class_ = 'titleColumn')
        for item in titles:
            if count < 50:
                parsed_list.append('https://www.imdb.com'+item.a.get('href'))
                count += 1
        return parsed_list
    counter = 0
    def parse_movie(self, url):
        print(self.counter)
        self.counter += 1
        parsed_dict = {}
        req = requests.get(url)
        soup = BS(req.content, 'html.parser')
        title = soup.findAll(class_ = 'sc-dae4a1bc-0 gwBsXc')
        try: title_split =  title[0].text.split(': ')
        except IndexError:
            title = soup.findAll(class_ = 'sc-b73cd867-0 eKrKux')
            title_split =  title[0].text
        if type(title_split) == str:
            parsed_dict['title'] = title_split
        else:
            parsed_dict['title'] = title_split[1]
        year = soup.findAll(class_ = 'sc-52284603-2 iTRONr')
        parsed_dict['year'] = year[0].text
        rating = soup.findAll(class_ = 'sc-7ab21ed2-1 jGRxWM')
        parsed_dict['rating'] = rating[0].text
        genre  = soup.find_all('a', class_ = 'sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt')
        tmp_genre = []
        for item in genre:
            tmp_genre.append(item.text)
        parsed_dict['genre'] = tmp_genre
        return(parsed_dict)

ParseRequests()

