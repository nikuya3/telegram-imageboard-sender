from urllib.request import urlretrieve
from os import mkdir
from os.path import abspath, isdir
from shutil import rmtree
from random import randint

from pybooru import Danbooru
from pytg import Telegram
from pytg.sender import Sender

telegram_path = input('Enter the path to your telegram-cli installation (installation instructions: https://github.com/vysheng/tg#installation): ')
pubkey_file_path = input('Enter the path to the Telegram server public key file (for example, https://github.com/vysheng/tg/tg-server.pub): ')
tg = Telegram(telegram="telegram-cli", pubkey_file="../tg/tg-server.pub")
#sender = Sender(host="localhost", port=4458)
sender = tg.sender
contacts = sender.contacts_list()
contactFound = False
while not contactFound:
    recipient = input('Enter the recepients username (replace ` ` with `_`): ')
    for contact in contacts:
        if hasattr(contact, 'username'):
            if contact.username == recipient:
                contactFound = True
                break
        else:
            if contact.print_name == recipient:
                contactFound = True
                break
    if not contactFound:
        print('No matching contact found!')
print('Contact found!')
client = Danbooru('danbooru')
tags = input('Enter a tag or a collection of tags seperated by ` `: ')
posts = client.post_list(limit=2, page=randint(1, 50), tags=tags)
print(posts)
if isdir('tmp'):
    rmtree('tmp')
mkdir('tmp')
for post in posts:
    url = 'https://danbooru.donmai.us' + post['file_url']
    path = 'tmp/' + url.split('/')[::-1][0]
    print(url, end='', flush=True)
    urlretrieve(url, path)
    try:
        sender.send_photo(recipient, abspath(path))
        print('\033[92m' + '\t✔' + '\x1b[0m')
    except:
        print('\033[91m' + '\t✗' + '\x1b[0m')
    
rmtree('tmp')
tg.stop_cli()
print('Sucessful')
