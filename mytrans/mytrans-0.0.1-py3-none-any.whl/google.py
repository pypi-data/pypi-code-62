from urllib.parse import urlencode
import requests
import re
import os
import pickle
import time

PICKLE_PATH = __file__[:__file__.rfind('\\') + 1]
PICKLE_FILE = PICKLE_PATH + 'tk.file'

TKK = ['', 0]

__all__ = ['trans']

BASE_URL = 'https://translate.google.cn/translate_a/single?'

HEADERS = {
    'referer': 'https://translate.google.cn/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

PARAMS = {
    'client': 'webapp',
    'sl': 'auto',
    'tl': 'zh-CN',
    'hl': 'zh-CN',
    'otf': 1,
    'ssel': 5,
    'tsel': 5,
    'xid': 45662847,
    'kc': 4,
    'tk': 0,
    'q': ''
}

DT = '&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t'


def trans(words, source_lang='auto', target_lang='zh-CN'):
    if words:
        PARAMS['q'] = words
        PARAMS['sl'] = source_lang
        PARAMS['tl'] = target_lang
        PARAMS['tk'] = _tk(words)
        ps = urlencode(PARAMS) + DT
        try:
            response = requests.get(BASE_URL + ps, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print('The link has expired!')
        except requests.ConnectionError:
            print('The link has expired or timed out!')
    return ''


############
#  js decode
############
def _get_tkk():
    if os.path.exists(PICKLE_FILE):
        global TKK
        with open(PICKLE_FILE, 'rb') as f:
            TKK = pickle.load(f)
            if TKK[0] != '' and int(time.time() - TKK[1]) < 3600:
                return TKK[0]

    try:
        res = requests.get('https://translate.google.cn/', timeout=10)
        if res.status_code == 200:
            temp = re.search("tkk:'(.*?)'", res.text)
            TKK[0] = temp[1]
            TKK[1] = time.time()

            with open(PICKLE_FILE, 'wb') as f:
                pickle.dump(TKK, f)
            return TKK[0]
    except requests.ConnectionError:
        print('The link has expired or timed out!')
    return ''


def _yu(a, b):
    for c in range(0, len(b) - 2, 3):
        d = b[c + 2]
        d = ord(d[0]) - 87 if 'a' <= d else int(d)
        d = a >> d if '+' == b[c + 1] else a << d
        a = a + d & 4294967295 if '+' == b[c] else a ^ d
    return a


def _tk(a):
    tkk = _get_tkk()
    d = tkk.split('.')
    b = int(d[0])

    e = []
    f = g = 0

    while g < len(a):
        h = ord(a[g])
        if 128 > h:
            e.append(h)
        else:
            if 2048 > h:
                e[f] = h >> 6 | 192
                f += 1
            else:
                if 55296 == (h & 64512) and g + 1 < len(a) and 56320 == (
                        ord(a[g + 1]) & 64512):
                    g += 1
                    h = 65536 + ((h & 1023) << 10) + (ord(a[g + 1]) & 1023)
                    e.append(h >> 18 | 240)
                    e.append(h >> 12 & 63 | 128)
                else:
                    e.append(h >> 12 | 224)
                    e.append(h >> 6 & 63 | 128)
            e.append(h & 63 | 128)
        g += 1

    a = b
    for f in range(0, len(e)):
        a += e[f]
        a = _yu(a, '+-a^+6')
    a = _yu(a, '+-3^+b+-f')
    a ^= int(d[1]) | 0

    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a = int(a % 1E6)
    return '{}.{}'.format(a, a^b)