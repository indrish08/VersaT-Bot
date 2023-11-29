import os
import urllib.parse
import urllib.request

class DirectLinkDL:
    def download(message, msg):
        file_name = os.path.basename(message.command[1])
        os.system(f'wget -q "{message.command[1]}" -P ./downloads')
        return f'downloads/{file_name}'
        # data = urllib.parse.urlparse(message.command[1])
        # # print(data)
        # urllib.request.urlretrieve(message.command[1], filename=f'downloads/{os.path.basename(data.path)}')