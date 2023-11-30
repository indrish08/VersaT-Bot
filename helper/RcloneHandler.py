import rclone as rc
import os

import urllib.parse

def download(message):
    path = message.command[1]
    if message.command[1].startswith('https://alchemist.cyou/'):
        path = get_path_from_alc(message.command[1])
    download_from_path(path)
    return os.path.join('downloads', os.path.basename(path))

def download_from_path(path):
    os.system(f'rclone copy "{path}" "{os.path.join(os.getcwd(), "downloads", os.path.basename(path))}"')
    
def get_path_from_alc(url):
    path = url[69:].replace('/', ':', 1)
    path = urllib.parse.unquote(urllib.parse.unquote(path).replace('•','-'))
    return path