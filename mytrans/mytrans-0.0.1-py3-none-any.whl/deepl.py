import requests
import time
import random

__all__ = ['trans']

BASE_URL = 'https://www2.deepl.com/jsonrpc'

HEADERS = {
    'Content-Type':'application/json',
    'referer':
    'https://www.deepl.com/zh/translator',
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}

PAYLOAD = '{{"jsonrpc":"2.0","method": "LMT_handle_jobs","params":{{"jobs":[{{"kind":"default","raw_en_sentence":"{}","raw_en_context_before":[],"raw_en_context_after":[],"preferred_num_beams":4,"quality":"fast"}}],"lang":{{"user_preferred_langs":["DE","ZH","EN"],"source_lang_user_selected":"{}","target_lang":"{}"}},"priority":-1,"commonJobParams":{{"formality":null}},"timestamp":{}}},"id":{}}}'


def trans(words, source_lang='auto', target_lang='ZH') -> str:
    timestamp = int(time.time() * 1000)
    id_ = int(1e4 * int(random.random() * 1e4))
    if words:
        pl = PAYLOAD.format(words, source_lang, target_lang, timestamp,
                            id_).encode('utf-8')
        try:
            response = requests.post(BASE_URL, headers=HEADERS, data=pl, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print('The link has expired!')
        except requests.ConnectionError:
            print('The link has expired or timed out!')
    return ''