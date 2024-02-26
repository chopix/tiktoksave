from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
import time
import os

api_id = 21102006
api_hash = 'b1bd8f4b57de3ba7a0a04d1c93a84a00'

app = Client(name='vidbot', api_id=api_id, api_hash=api_hash)
bot_chat_id = 7161096362


@app.on_message(filters=filters.chat(bot_chat_id))
async def hello(client: Client, message: Message):
    caption = message.text.split(' ')[-1]
    url = message.text.split(' ')[0]
    name = ''.join(str(time.time()).split('.'))
    file = 0

    try:
        if YouTube(url).length < 3600:
            file = requests.get(YouTube(url=url).streams.get_highest_resolution().url).content
            print('got file')
        else:
            await app.send_message(f'{bot_chat_id}', f'FILESIZE {caption}')
    except AgeRestrictedError:
        await app.send_message(f'{bot_chat_id}', f'ERROR {caption}')

    if file:
        with open(fr'vid/{name}.mp4', 'wb') as f:
            f.write(file)
            print('write')

        a = open(fr'vid/{name}.mp4', 'rb')
        print('open')
        await app.send_video(f'{bot_chat_id}', a, caption=caption, width=464, height=261)
        print('sended')
        a.close()

        os.remove(fr'vid/{name}.mp4')

app.run()
