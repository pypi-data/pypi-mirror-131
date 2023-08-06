import os
from pathlib import Path
from configparser import ConfigParser

class files():
    def __init__(self):
        self.home = os.path.expanduser('~')
        self.botconfig = os.path.join(self.home, 'botterino-config')
        self.configfile = os.path.join(self.botconfig, 'config.ini')
        self.roundsdir = os.path.join(self.botconfig, 'rounds')
        self.rounds = os.path.join(self.roundsdir, 'rounds.yaml')
        self.archive = os.path.join(self.roundsdir, 'archive.yaml')
        self.prawconfig = os.path.join(self.botconfig, 'praw.ini')

botfiles = files()
dirs = [botfiles.botconfig, botfiles.roundsdir]
files = [botfiles.rounds, botfiles.archive, botfiles.prawconfig]
for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)
for f in files:
    with open(f, 'a+'):
        pass

if not os.path.exists(botfiles.configfile):
    parser = ConfigParser()
    parser.add_section('config')
    parser.set('config', 'correct_message', '+correct')
    parser.set('config', 'incorrect_message', '❌')
    with open(botfiles.configfile, 'w', encoding='utf-8') as f:
        parser.write(f)

parser = ConfigParser()
parser.read(botfiles.configfile, encoding='utf-8')
correctMessage, incorrectMessage = parser['config']['correct_message'], parser[
    'config']['incorrect_message']
