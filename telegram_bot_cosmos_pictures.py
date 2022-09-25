import os
import argparse
import time

import telegram
from dotenv import load_dotenv

from fetch_spacex_images import fetch_images as fetch_spacex_images
from fetch_nasa_images_apod import fetch_images as fetch_nasa_apod_images
from fetch_nasa_images_epic import fetch_images as fetch_nasa_epic_images


def fetch_images_for_date(date, token):
    images_folder = os.path.join('./images/', f'{date}/')
    fetch_spacex_images('latest', images_folder)
    fetch_nasa_apod_images(date, date, token, images_folder)
    fetch_nasa_epic_images(date, token, images_folder)
    os.makedirs(os.path.join(images_folder), exist_ok=True)
    day_images = []
    for filename in os.listdir(images_folder):
        day_images.append(os.path.join(images_folder, f'{filename}'))
    return day_images


def parse_args():
    parser = argparse.ArgumentParser(description='bot download and post in telegram chanel pictures from nasa and spacex')
    parser.add_argument('-d', '--date', default='2022-09-01', help='начальная дата')
    parser.add_argument('-t', '--time_sleep', type=int, default='14400', help='пауза между публикациями в секундах')
    parser.add_argument('-p', '--path_infinite', default='', help='путь к файлам для бесконечного цикла публикаций')
    parser.add_argument('-i', '--image_path', default='', help='опубликовать фото по указанному пути')

    return parser.parse_args()


if __name__ == '__main__':
    load_dotenv()
    chat_id = '@Cosmos_pictures'
    telegram_token = os.environ.get('TELEGRAM_TOKEN')
    nasa_token = os.environ.get('NASA_TOKEN')
    bot = telegram.Bot(token=telegram_token)
    args = parse_args()
    infinite_cycle = False
    if os.path.exists(args.path_infinite) & (args.path_infinite != ''):
        infinite_cycle = True
    if os.path.exists(args.image_path) & (args.image_path != ''):
        images_paths = [args.image_path]
    else:
        images_paths = fetch_images_for_date(args.date, nasa_token)
    while True:
        for image_path in images_paths:
            if 'nasa_apod_' in image_path:
                image_from = 'NASA a picture of day'
            elif 'nasa_epic_' in image_path:
                image_from = 'NASA earth picture'
            else:
                image_from = 'SPACEX last launch picture'
            bot.send_message(chat_id=chat_id, text=f'Image from {image_from}')
            with open(image_path, 'rb') as image_file:
                bot.send_document(chat_id=chat_id, document=image_file)
        if not args.path_infinite:
            break
        time.sleep(args.time_sleep)
