from email import header
import requests
import os
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse, urlsplit

from dotenv import load_dotenv
load_dotenv()

def check_for_redirect(response):
    if response.history:
        raise HTTPError('Старинца не найдена')


def get_file_extension_from_url(url: str) -> str:
    extension = os.path.splitext(url)[-1]
    return extension.split('.')[-1]


def download_image(url: str, folder='images/'):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urlparse(url).path.split('/')[-1]
    os.makedirs(os.path.join(folder), exist_ok=True)
    image_filename = os.path.join(folder, f'nasa_{filename}')
    with open(image_filename, 'wb') as file:
        file.write(response.content)
    return image_filename


def download_image_with_token(url: str, token, folder='images/'):
    params = {
        'api_key': token
    }
    response = requests.get(url, params=params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urlparse(url).path.split('/')[-1]
    os.makedirs(os.path.join(folder), exist_ok=True)
    image_filename = os.path.join(folder, f'nasa_{filename}')
    with open(image_filename, 'wb') as file:
        file.write(response.content)
    return image_filename


def fetch_spacex_last_launch(url: str) -> list:
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    return response.json()['links']['flickr']['original']


def fetch_nasa_day_pictures(start_date: str, end_date: str):
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': os.environ.get('NASA_TOKEN')
    }
    response = requests.get(nasa_url, params=params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    return [x['url'] for x in response.json()]


def get_nasa_earth_pictures_names(date):
    nasa_url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
    params = {
        'api_key': os.environ.get('NASA_TOKEN')
    }
    response = requests.get(nasa_url, params=params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    return [x['image'] for x in response.json()]


def fetch_nasa_earth_pictures(date):
    pictures_names = get_nasa_earth_pictures_names(date)
    year, month, day = date.split('-')
    pictures_urls = []
    for picture_name in pictures_names:
        picture_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{picture_name}.png'
        pictures_urls.append(picture_url)
    return pictures_urls


def main():
#    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
#    urls = fetch_spacex_last_launch('https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a')
#    urls = fetch_nasa_day_pictures('2022-09-01', '2022-09-21')
    urls = fetch_nasa_earth_pictures('2019-05-30')
    for url in urls:
#        print(get_file_extension_from_url(url))
        download_image_with_token(url, os.environ.get('NASA_TOKEN'))
#        download_image(url)


if __name__ == '__main__':
    main()
