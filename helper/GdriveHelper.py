import os
import gdown

def download(url):
    if 'folder' in url:
        return download_folder(url)
    else:
        return download_file(url)

def download_file(url):
    file_name = gdown.download(url, quiet=True, resume=True, fuzzy=True)
    if file_name:
        if os.path.exists(f'./downloads/{file_name}'):
            os.remove(f'./downloads/{file_name}')
        os.rename(file_name, f'./downloads/{file_name}')
        return f'downloads/{file_name}'
    else:
        return None

def download_folder(url):
    file_names = gdown.download_folder(url)
    if file_names:
        return f'downloads/{os.path.dirname(file_names[0])}'
    else:
        return None