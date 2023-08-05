import random
import sys
import time
from urllib.parse import urljoin

import requests

address = sys.argv[1].rstrip('/') + '/'

ACTION_URL = urljoin(address, 'action')
STATE_URL = urljoin(address, 'game-state')


def ai():
    if random.random() < 0.75:
        direction = random.choice(['up', 'left', 'right', 'down'])
        print(address, requests.post(ACTION_URL, json={'action': 'move', 'direction': direction}).content)
    else:
        print(address, requests.post(ACTION_URL, json={'action': 'bomb'}).content)
    time.sleep(0.1)
    print('======')


while True:
    try:
        ai()
    except requests.ConnectionError:
        pass
