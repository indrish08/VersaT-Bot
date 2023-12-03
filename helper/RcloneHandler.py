import os

import urllib.parse

def download(message):
    path = message.command[1]
    if message.command[1].startswith('https://alchemist.cyou/'):
        path = get_path_from_alc(message.command[1])
    loc_path = download_from_path(path)
    return loc_path

def download_from_path(path):
    dest = os.path.join(os.getcwd(), "downloads", os.path.basename(path))
    os.system(f'rclone copy "{path}" "{dest}"')
    return dest
    
def get_path_from_alc(url):
    path = url[69:].replace('/', ':', 1)
    path = urllib.parse.unquote(urllib.parse.unquote(path).replace('•','-'))
    return path

def copy(message):
    path = message.command[1]
    if message.command[1].startswith('https://alchemist.cyou/'):
        path = get_path_from_alc(message.command[1])
    msg = message.reply('Transfer Started...')
    os.system(f'rclone copy "{path}" "bot:{os.path.basename(path)}" -P')
    msg.delete()
    message.reply('Transfer Completed...')