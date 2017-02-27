from urllib.request import urlretrieve
from os import mkdir
from os.path import abspath, isdir
from shutil import rmtree
from random import randint

from argparse import ArgumentParser
from pybooru import Danbooru
from pytg import Telegram
from pytg.sender import Sender

parser = ArgumentParser(description='Sends imageboard photos to Telegram users', prog='sender')
parser.add_argument('tags', type=str, help='A tag or a collection of tags seperated by ` `')
parser.add_argument('-t', '--tg', type=str, default='', help='The path to the Telegram binary.')
parser.add_argument('-p', '--pub', type=str, default='', help='The path to the Telegram server public key file.')
parser.add_argument('-u', '--user', type=str, default='', help='The user to send the photos to (replace ` ` with `_`).')
parser.add_argument('-a', '--amount', type=int, default=0, help='The amount of photos to send (default is 10).')
parser.add_argument('-n', '--number', type=int, default=0, help='The page number to send images from (default is 1st page)')
args = parser.parse_args()
telegram_path = args.tg if args.tg != '' else input('Enter the path to your telegram-cli installation (installation instructions: https://github.com/vysheng/tg#installation): ')
pubkey_file_path = args.pub if args.pub != '' else input('Enter the path to the Telegram server public key file (for example, https://github.com/vysheng/tg/tg-server.pub): ')
tg = Telegram(telegram=telegram_path, pubkey_file=pubkey_file_path)
#sender = Sender(host="localhost", port=4458)
sender = tg.sender
contacts = sender.contacts_list()
contactFound = False
while not contactFound:
    recipient = args.user if args.user != '' else input('Enter the recepients username (replace ` ` with `_`): ')
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
tags = args.tags if args.tags != '' else input('Enter a tag or a collection of tags seperated by ` `: ')
limit = args.amount if args.amount != 0 else input('Enter the amount of photos to send (default is 10): ')
page = args.number if args.number != 0 else input('Enter the page number to send images from (default is 1st page): ')
#posts = client.post_list(limit=2, page=randint(1, 50), tags=tags)
posts = client.post_list(limit=limit, page=page, tags=tags)
print('Found {0} photos'.format(len(posts)))
if isdir('tmp'): 
    rmtree('tmp')
mkdir('tmp')
for post in posts:
    if not 'file_url' in post:
        break 
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
