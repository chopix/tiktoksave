import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json


def get_post(url):
    link = 'https://instagrab.app/ru/instagram-video-downloader/?'
    user = UserAgent()

    headers = {
        'user-agent': user.random
    }

    data = {
        'page': url,
    }

    r = requests.post(link, data=data, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    res = {
        'video': [],
        'photo': []
    }

    card = soup.find_all('div', class_='card-body')
    for i in card:
        l = i.find_all('a', class_='btn btn-primary btn-dl')
        if len(l) == 3:
            res['photo'].append(requests.get(l[0]['href'], headers=headers).content)
        else:
            res['video'].append(requests.get(l[0]['href'], headers=headers).content)

    return res


def get_reel(url):

    link = 'https://instagram-downloader-main.vercel.app/api/download'
    user = UserAgent().random

    headers = {
        'user-agent': user
    }
    data = {
        "url": url
    }

    r = requests.post(link, data=json.dumps(data), headers=headers)
    response = requests.get(r.text[33:-4])

    if response.status_code == 200:
        return response.content
    else:
        return None


def get_stories(url):

     link = 'https://instagrab.app/ru/instagram-story-downloader/?'
     user = UserAgent()

     headers = {
         'user-agent': user.random
     }

     data = {
         'page': url,
     }

     r = requests.post(link, data=data, headers=headers)
     soup = BeautifulSoup(r.text, 'lxml')

     res = {
         'video': [],
         'photo': []
     }

     card = soup.find_all('div', class_='card-body')
     for i in card:
         l = i.find_all('a', class_='btn btn-primary btn-dl')
         if len(l) == 4:
             res['photo'].append(requests.get(l[0]['href'], headers=headers).content)
         else:
             res['video'].append(requests.get(l[0]['href'], headers=headers).content)

     return res
