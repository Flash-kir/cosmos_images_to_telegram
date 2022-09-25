import requests
import argparse
import os

from dotenv import load_dotenv

from fetch_images import download_image, check_for_redirect

def fetch_nasa_day_pictures(start_date: str, end_date: str, token):
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': token
    }
    response = requests.get(nasa_url, params=params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    return [picture_context['url'] for picture_context in response.json()]


def parse_args():
    parser = argparse.ArgumentParser(description="загрузит фото от SpaceX по указанному ID запуска")
    parser.add_argument('-s', '--start_date', default='2022-09-01', help='начальная дата')
    parser.add_argument('-e', '--end_date', default='2022-09-02', help='конечная дата')
    return parser.parse_args()


def fetch_images(start_date, end_date, token, folder='images/apod/'):
    urls = fetch_nasa_day_pictures(start_date, end_date, token)
    for url in urls:
        download_image(url, token=token, folder=folder, prefix='nasa_apod_')


def main():
    args = parse_args()
    load_dotenv()
    token = os.environ.get('NASA_TOKEN')
    fetch_images(args.start_date, args.end_date, token)


if __name__ == '__main__':
    main()
