import os
import urllib.parse
import urllib.request

class DirectLinkDL:
    def download(message):
        msg = message.reply('Downloading...', True)
        os.system(f'wget "{message.command[1]}" -P ./downloads')
        msg.edit_text(f"Downloaded successfully to: \n`'downloads'`")
        return os.path.basename('https://mirror.jackdrive038.workers.dev/0:/Avengers.Infinity.War.2018.2160p.10bit.HDR.BluRay.8CH.x265.HEVC_PSA.mkv')
        # data = urllib.parse.urlparse(message.command[1])
        # # print(data)
        # urllib.request.urlretrieve(message.command[1], filename=f'downloads/{os.path.basename(data.path)}')