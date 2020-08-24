"""
Библиотека для сервиса
https://vkmix.com/settings/api
"""

import requests, urllib.parse, json


class VkMixException(Exception):
	"""[summary]

	Args:
		Exception ([type]): [description]
	"""
	pass


class VkMixApiError(VkMixException):
	"""[summary]

	Args:
		VkMixException ([type]): [description]
	"""
	pass


class VkMix:
	"""API для ботов API VKMix
Мы предоставляем открытый для всех разработчиков доступ к созданию заданий в нашей системе.

Взаимодействие с API
Всем методам необходимо передавать токен авторизации параметром api_token}.
Успешный результат в виде
{response: результат работы метода}
Ошибки:
{error: тип ошибки}
Список доступных методов"""

	s = requests.session()
	ua = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
	s.headers = {"User-Agent": ua, "X-Requested-With": "XMLHttpRequest"}
	api_token = ""
	url = "https://vkmix.com/api/2/"

	def __init__(self, api_token):
		"Авторизация"
		self.api_token = api_token

	def _request(self, uri, method="get", data={}, headers={}, **kw):
		method = method.lower()
		if method not in ["get", "post"]:
			raise ValueError("method GET or POST")

		kw.update({"api_token": self.api_token})
		data.update(kw)

		if method == "get":
			hndlr = self.s.get
			uri = uri + "?" + urllib.parse.urlencode(data)
			data = {}

		if method == "post":
			hndlr = self.s.post

		try:
			resp = hndlr(
				self.url + uri, data=data, headers=headers, allow_redirects=False
			).content.decode("utf8")
		except:
			raise

		if resp == "":
			raise VkMixApiError("empty response")

		try:
			j = json.loads(resp)
		except json.JSONDecodeError:
			raise VkMixApiError("not json" + resp)

		if "error" in j and not "response" in j:
			raise VkMixApiError(j["error"])

		return j["response"]

	def getServices(self):
		"""getServices

Получение списка сервисов
Результат
Метод возвращает список сервисов для создания заданий"""
		
		return self._request("getServices")
	
	def createTask(self, **kw):
		"""Добавление нового задания

Параметры
network
Социальная сеть задания. Укажите одно из значений:
vk - ВКонтакте
instagram - Инстаграм
youtube - Ютуб
telegram - Телеграм
ok - Одноклассники
twitter - Твиттер

section
Тип задания. Для каждой социальной сети доступны свои типы:
vk: likes, reposts, comments, friends, groups, polls
instagram: likes, subscribers, comments, comments_likes
youtube: likes, friends, dislikes, comments
twitter: retweets, followers, favorites
ok: likes, friends, groups
telegram: subscribers
Для Instagram дополнительно доступны: likes_q4, subscribers_q4, likes_q5, subscribers_q5, likes_q7, subscribers_q7. 

link
Ссылка на объект задания.

count
Количество необходимых выполнений.

amount
Вознаграждение пользователю за выполнение задания.

comments (опц. для section = comments)
Массив вариантов комментариев
	# todo: массив comments может передаваться не корректно

poll (опц. для section = polls)
Номер варианта за который необходимо проголосовать

hourly_limit
Лимит выполнений в час

Результат
Метод возвращает ID созданного задания."""

		return self._request("createTask", method="post", data=kw)

	def getTasks(self, ids="", count=100, offset=0):
		"""Получение списка заданий

Параметры
ids
Id заданий. Если не передан - вернёт все задания

count
Количество заданий, которые необходимо вернуть. Не более 100

offset
Смещение необходимое для выборки определенного подмножества

Результат
Метод возвращает список заданий."""

		return self._request("getTasks", ids=ids, count=count, offset=offset)

	def getBalance(self):
		"""Получение текущего баланса аккаунта

Результат
Метод возвращает баланс аккаунта."""

		return self._request("getBalance")
