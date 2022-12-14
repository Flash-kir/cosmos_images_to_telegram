import requests
import argparse

from fetch_images import download_image, check_for_redirect

def fetch_spacex_launch_pictures(launch_id: str) -> list:
    url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    return response.json()['links']['flickr']['original']


def parse_args():
    parser = argparse.ArgumentParser(description="загрузит фото от SpaceX по указанному ID запуска")
    parser.add_argument('-l', '--launch_id', default='latest', help='ID запуска')
    parser.add_argument('-f', '--folder', default='images/spasex/', help='папка для изображений')
    return parser.parse_args()


def fetch_images(launch_id, folder):
    urls = fetch_spacex_launch_pictures(launch_id)
    for url in urls:
        download_image(url, folder=folder, prefix='spasex_')


def main():
    args = parse_args()
    fetch_images(args.launch_id, args.folder)


if __name__ == '__main__':
    main()
