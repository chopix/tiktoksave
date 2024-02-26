import re
import requests


def get_tiktok_video_id(url):
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)


def tiktok(url):
    response = requests.get(url)

    video_id = get_tiktok_video_id(response.url)

    response = requests.get(f'https://tikcdn.io/ssstik/{video_id}')
    print(response)

    if response.status_code == 200:
        return response.content
    else:
        return


def tt(url):
    response = requests.get(url)

    video_id = get_tiktok_video_id(response.url)

    data = {
        'url': fr'https://vt.tiktok.com/{video_id}'
    }

    response = requests.post('https://ssstiktokio.com/wp-json/aio-dl/video-data/', data=data)

    if response.status_code == 200:
        return requests.get(response.json()['medias'][0]['url']).content
    else:
        return

