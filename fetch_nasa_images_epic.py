import requests
import argparse
import os

from dotenv import load_dotenv
load_dotenv()

from fetch_images import download_image, check_for_redirect

def get_nasa_earth_pictures_names(date):
    nasa_url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}'
    params = {
        'api_key': os.environ.get('NASA_TOKEN')
    }
    response = requests.get(nasa_url, params=params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    return [x['image'] for x in response.json()]


def fetch_nasa_earth_pictures(date, pictures_names):
    year, month, day = date.split('-')
    pictures_urls = []
    for picture_name in pictures_names:
        picture_url = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{picture_name}.png'
        pictures_urls.append(picture_url)
    return pictures_urls


def parse_args():
    parser = argparse.ArgumentParser(description="загрузит фото от SpaceX по указанному ID запуска")
    parser.add_argument('-d', '--date', default='2022-09-01', help='дата')
    return parser.parse_args()


def fetch_images(date, folder='images/epic/'):
    pictures_names = get_nasa_earth_pictures_names(date)
    urls = fetch_nasa_earth_pictures(date, pictures_names)
    for url in urls:
        download_image(url, token=os.environ.get('NASA_TOKEN'), folder=folder, prefix='nasa_')


def main():
    args = parse_args()
    fetch_images(args.date)


if __name__ == '__main__':
    main()
