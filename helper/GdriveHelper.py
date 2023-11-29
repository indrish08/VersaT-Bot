import os
import gdown

class GdriveHelper:
    def download(message):
        url = message.command[1]
        msg = message.reply('Downloading...', True)
        file_name = gdown.download(url, quiet=True, resume=True, fuzzy=True)
        if file_name:
            if os.path.exists(f'./downloads/{file_name}'):
                os.remove(f'./downloads/{file_name}')
            os.rename(file_name, f'./downloads/{file_name}')
            return f'downloads/{file_name}'
            # msg.edit_text(f"Downloaded successfully to: \n`downloads\{file_name}`")
        else:
            return 'Downloaded Failed!'
            # msg.edit_text("Downloaded Failed!")