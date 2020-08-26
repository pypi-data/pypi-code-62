import requests
import threading
import json
import six

class session(object):
    def __init__(self, token = None):
        """
        Инициализация бота.
        """
        self.token = token

        self.lock = threading.Lock()
        self.http = requests.session()
        self.http.headers.update({
                        'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
                        })
        
        self.update_id = 0
        res = self.method()
        self.id = res['id']
        self.username = res['username']
        print(f"@{self.username} launched!")

    def method(self, method='getMe', values=None):
        """
        Вызываем метод, см. https://core.telegram.org/bots/api#available-methods
        """
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

    def check(self):
        response = self.method('GetUpdates', {'offset': self.update_id + 1})

        for event in response or []:
            self.update_id = event['update_id']
            yield event

    def listen(self):
        while True:
            for event in self.check():
                yield event
        
class get_api():
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