import os
import gdown

def download(url):
    if url.startswith('https://drive.google.com/file/'):
        download_file(url)
    else:
        download_folder(url)

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
    file_names = gdown.download_folder('https://drive.google.com/drive/folders/1jVUyvqV_wjRhbYSLeLGfP-NH6n6at81i?usp=sharing')
    return file_names