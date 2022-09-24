import os
import requests

from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse, urlsplit

'''
def get_file_extension_from_url(url: str) -> str:
    extension = os.path.splitext(url)[-1]
    return extension.split('.')[-1]
'''

def check_for_redirect(response):
    if response.history:
        raise HTTPError('Старинца не найдена')


def download_image(url: str, token='', folder='images/', prefix=''):
    params = {}
    if token:
        params = {
            'api_key': os.environ.get('NASA_TOKEN')
        }
    response = requests.get(url, params=params, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    filename = urlparse(url).path.split('/')[-1]
    os.makedirs(os.path.join(folder), exist_ok=True)
    image_filename = os.path.join(folder, f'{prefix}{filename}')
    with open(image_filename, 'wb') as file:
        file.write(response.content)
    return image_filename


if __name__ == '__main__':
    pass
