import telebot
import sqlite3
from tt import tiktok, tt
from inst import get_post, get_reel, get_stories
import requests
from pytube import YouTube


TOKEN = '7161096362:AAFU6w1h5wje-0E15d1snLtPxBUSO8-6sHY'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Здравствуйте! Здесь вы можете скачать любой понравившийся вам пост из Instagram, reels, youtube видео, shorts или tiktok\n'
                                           'Достаточно прислать ссылку этому боту и скачанное видео уже у вас!')


@bot.message_handler(content_types=['text'])
def send_video(message):
    try:
        if 'tiktok' in message.text:
            m = bot.send_message(message.from_user.id, '⬇️ Видео загружается на сервер, подождите немного')
            try:
                bot.send_video(message.from_user.id, tiktok(message.text), timeout=200, caption=f'скачано с @{bot.get_me().username}')
            except:
                bot.send_video(message.from_user.id, tt(message.text), timeout=200, caption=f'скачано с @{bot.get_me().username}')

            bot.delete_message(message.from_user.id, m.message_id)

        elif 'reel' in message.text:
            m = bot.send_message(message.from_user.id, '⬇️ Рилс загружается на сервер, подождите немного')
            bot.send_video(message.from_user.id, get_reel(message.text), timeout=200, caption=f'скачано с @{bot.get_me().username}', width=243, height=432)
            bot.delete_message(message.from_user.id, m.message_id)

        elif 'stories' in message.text:
            m = bot.send_message(message.from_user.id, '⬇️ Сторис загружается на сервер, подождите немного')
            objects = get_stories(message.text)
            l = []
            for i in objects['photo']:
                l.append(telebot.types.InputMediaPhoto(i, caption=f'скачано с @{bot.get_me().username}'))
            for i in objects['video']:
                l.append(telebot.types.InputMediaVideo(i, caption=f'скачано с @{bot.get_me().username}'))

            bot.send_media_group(message.from_user.id, l, timeout=200)
            bot.delete_message(message.from_user.id, m.message_id)

        elif 'instagram' in message.text:
            m = bot.send_message(message.from_user.id, '⬇️ Пост загружается на сервер, подождите немного')
            objects = get_post(message.text)
            l = []
            for i in objects['photo']:
                l.append(telebot.types.InputMediaPhoto(i, caption=f'скачано с @{bot.get_me().username}'))
            for i in objects['video']:
                l.append(telebot.types.InputMediaVideo(i, caption=f'скачано с @{bot.get_me().username}'))

            bot.send_media_group(message.from_user.id, l, timeout=200)
            bot.delete_message(message.from_user.id, m.message_id)

        elif 'ERROR' in message.text:
            connection = sqlite3.connect('my_database.db')
            cursor = connection.cursor()
            l = cursor.execute('SELECT user_id FROM Users WHERE m_id =  ?', (message.text.split(' ')[-1],)).fetchone()

            bot.send_message(l[0], 'Невозможно скачать видео')
            bot.delete_message(l[0], message.text.split(' ')[-1])
            cursor.execute('DELETE FROM Users WHERE m_id = ?', (message.caption.split(' ')[-1],))
            connection.commit()
            connection.close()

        elif 'FILESIZE' in message.text:
            connection = sqlite3.connect('my_database.db')
            cursor = connection.cursor()

            l = cursor.execute('SELECT user_id FROM Users WHERE m_id =  ?', (message.text.split(' ')[-1],)).fetchone()

            bot.send_message(l[0], 'Видео слишком большое')
            bot.delete_message(l[0], message.text.split(' ')[-1])
            cursor.execute('DELETE FROM Users WHERE m_id = ?', (message.caption.split(' ')[-1],))
            connection.commit()
            connection.close()

        elif 'shorts' in message.text:
            m = bot.send_message(message.from_user.id, '⬇️ Видео загружается на сервер, подождите немного')
            bot.send_video(message.from_user.id, requests.get(YouTube(url=message.text).streams.get_highest_resolution().url).content, timeout=200, caption=f'скачано с @{bot.get_me().username}', width=243, height=432)
            bot.delete_message(message.from_user.id, m.message_id)

        elif 'youtu' in message.text:
            m = bot.send_message(message.from_user.id, '⬇️ Видео загружается на сервер, подождите немного')

            connection = sqlite3.connect('my_database.db')
            cursor = connection.cursor()

            cursor.execute('INSERT INTO Users (user_id, m_id) VALUES (?, ?)',
                           (message.from_user.id, m.message_id))

            connection.commit()
            connection.close()

            bot.send_message(7192675375, f'{message.text} {m.message_id}')

        else:
            bot.send_message(message.from_user.id, '⬇️ Введите корректный URL')
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id, 'Возникли неполадки, попробуйте еще раз')


@bot.message_handler(content_types=['video'])
def send_yt(message):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()

    l = cursor.execute('SELECT user_id FROM Users WHERE m_id =  ?', (message.caption.split(' ')[-1],)).fetchone()

    bot.send_video(l[0], message.video.file_id, timeout=200, caption=f'скачано с @{bot.get_me().username}')
    bot.delete_message(l[0], message.caption.split(' ')[-1])

    cursor.execute('DELETE FROM Users WHERE m_id = ?', (message.caption.split(' ')[-1],))

    connection.commit()
    connection.close()


bot.infinity_polling(none_stop=True, interval=0)
