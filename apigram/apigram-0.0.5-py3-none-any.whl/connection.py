import requests
import threading
import json
import six

class session(object):
    def __init__(self, token:str):
        """ Initialize Bot's working. Token you can take via creating bot's page at BotFather: t.me/BotFather """
        self.token = token
        self.lock = threading.Lock()
        self.http = requests.session()
        self.http.headers.update({'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"})
        
        res = self.method()
        
        self.id = res['id']
        self.username = res['username']
        self.name = res['first_name']
        self.update_id = 0
        
        print(f"@{self.username} launched!")

    def method(self, method='getMe', values=None):
        """ Use method with parameters. Manual: https://core.telegram.org/bots/api#available-methods """
        params = values.copy() if values else {}
        
        with self.lock:
            response = self.http.post(
                    f'https://api.telegram.org/bot{self.token}/{method}', params)

        if response.ok:
            response = response.json()
            
            if response['ok']:
                return response['result']
            
            else:
                print('[{error_code}] {description}'.format(response))
                quit()

    def getFile(self, file_id: str):
        with self.lock:
            response = self.http.post(
                    f'https://api.telegram.org/bot{self.token}/getFile', {'file_id': file_id}).json()

            if response['ok']:
                path = response['result']['file_path']
            else:
                print('[{error_code}] {description}'.format(response))
                quit()

        return {
            'file_name': path.rsplit('/', 1)[1],
            'file_content': self.http.get(f'https://api.telegram.org/file/bot{self.token}/{path}', allow_redirects=True).content
        }


    def check(self):
        """ Get updates one time """
        for event in self.method('GetUpdates', {'offset': self.update_id + 1}) or []:
            self.update_id = event['update_id']
            yield event

    def listen(self):
        """ Get updates until broke """
        while True:
            for event in self.check():
                yield event
        
class get_api():
    """ Simplest access to Telegram Bot Api methods. ``api.*method*(kwargs)`` """
    
    __slots__ = ('_bot', '_method')
    def __init__(self, bot, method=None):
        self._bot = bot
        self._method = method

    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        return get_api(self._bot, (self._method + '.' if self._method else '') + method)

    def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        return self._bot.method(self._method, kwargs)