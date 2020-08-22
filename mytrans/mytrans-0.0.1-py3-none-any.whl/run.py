from . import google, deepl
import json


def mygoogle(words, source_lang='auto', target_lang='zh-CN'):
    text = google.trans(words, source_lang, target_lang)
    return TransResponse('google', text)

def mydeepl(words, source_lang='auto', target_lang='ZH'):
    text = deepl.trans(words, source_lang, target_lang)
    return TransResponse('deepl', text)


class TransResponse():
    def __init__(self, type, text):
        self.type = type
        self.content = text

    @property
    def res(self) -> list:
        if self.type == 'google':
            temp = ''
            try:
                temp = json.loads(self.content)
                if isinstance(temp[0][0][0], str):
                    t = [temp[0][0][0]]
                    t.extend(temp[1][0][1])
                    return t
            except TypeError:
                return [temp[0][0][0]]
            except json.JSONDecodeError:
                print('json parsing failed, please use TransResponse.text.')
            return []
        elif self.type == 'deepl':
            try:
                temp = json.loads(self.content)
                return [
                    t['postprocessed_sentence']
                    for t in temp['result']['translations'][0]['beams']
                ]
            except json.JSONDecodeError:
                print('json parsing failed, please use TransResponse.text.')
        return []

    @property
    def text(self) -> str:
        return self.content

    @property
    def json(self) -> dict:
        try:
            d = json.loads(self.content)
        except json.JSONDecodeError:
            d = {}
            print('json parsing failed, please use TransResponse.text.')
        return d