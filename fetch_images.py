import os
import requests

from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse, urlsplit

def check_for_redirect(response):
    if response.history:
        raise HTTPError('Старинца не найдена')


def download_image(url: str, token='', folder='images/', prefix=''):
    params = {}
    if token:
        params = {
            'api_key': token
        }
    response = requests.get(url, params=params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urlparse(url).path.split('/')[-1]
    os.makedirs(os.path.join(folder), exist_ok=True)
    image_filepath = os.path.join(folder, f'{prefix}{filename}')
    with open(image_filepath, 'wb') as file:
        file.write(response.content)
    return image_filepath


if __name__ == '__main__':
    pass
