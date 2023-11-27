import os
import urllib.parse
import urllib.request

class DirectLinkDL:
    def download(message):
        msg = message.reply('Downloading...', True)
        os.system(f'wget "{message.command[1]}" -P ./downloads')
        msg.edit_text(f"Downloaded successfully to: \n`'downloads'`")
        # data = urllib.parse.urlparse(message.command[1])
        # # print(data)
        # urllib.request.urlretrieve(message.command[1], filename=f'downloads/{os.path.basename(data.path)}')