"""

| Библиотека для сервиса
| https://vkmix.com/settings/api

"""

import json
import urllib.parse

import requests


class VkMixException(Exception):
	"Base Exception"
	pass


class VkMixApiError(VkMixException):
	"Api Exception"
	pass


class VkMix():
	"""API для ботов API VKMix

| Мы предоставляем открытый для всех разработчиков доступ к созданию заданий в
| нашей системе.

| Взаимодействие с API
| Всем методам необходимо передавать токен авторизации параметром `api_token`.

Авторизация

:param api_token: Ваш ключ API
:type api_token: str

:raises VkMixApiError: Тип ошибки
"""

	s: any = requests.session()
	ua: str = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"
	s.headers: dict = {"User-Agent": ua, "X-Requested-With": "XMLHttpRequest"}
	api_token: str = ""
	url: str = "https://vkmix.com/api/2/"

	def __init__(self, api_token: str) -> None:
		self.api_token = api_token

	def _request(self, uri: str, method: str = "get", data: dict = {}, headers: dict = {}, **kw) -> dict:
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

		resp = hndlr(
			self.url + uri, data=data, headers=headers, allow_redirects=False
		).content.decode("utf8")

		if resp == "":
			raise VkMixApiError("empty response")

		try:
			j = json.loads(resp)
		except json.JSONDecodeError:
			raise VkMixApiError("not json" + resp)

		if "error" in j and "response" not in j:
			raise VkMixApiError(j["error"])

		return j["response"]

	def getServices(self) -> list:
		"""Получение списка сервисов

.. seealso:: :func:`VkMix.createTask`

:return: Метод возвращает список сервисов для создания заданий
:rtype: list
"""

		return self._request("getServices")

	def createTask(self, **kw) -> dict:
		"""Добавление нового задания

:param network: Социальная сеть задания. Укажите одно из значений: \

* vk - ВКонтакте
* instagram - Инстаграм
* youtube - Ютуб
* telegram - Телеграм
* ok - Одноклассники
* twitter - Твиттер

:type network: str

:param section: Тип задания. Для каждой социальной сети доступны свои типы: \

* vk: likes, reposts, comments, friends, groups, polls
* instagram: likes, subscribers, comments, comments_likes
* youtube: likes, friends, dislikes, comments
* twitter: retweets, followers, favorites
* ok: likes, friends, groups
* telegram: subscribers
* Для Instagram дополнительно доступны: likes_q4, subscribers_q4, likes_q5, subscribers_q5, likes_q7, subscribers_q7.

:type section: str

:param link: Ссылка на объект задания.
:type link: str

:param count: Количество необходимых выполнений.
:type count: int

:param amount: Вознаграждение пользователю за выполнение задания.
:type amount: int

:param comments: для ``section = comments`` \
Массив вариантов комментариев
:type comments: list, optional

:param poll: для ``section = polls`` \
Номер варианта за который необходимо проголосовать
:type poll: int, optional

:param hourly_limit: Лимит выполнений в час
:type hourly_limit: int

:return: Метод возвращает ID созданного задания.
:rtype: dict
"""

		return self._request("createTask", method="post", data=kw)

	def getTasks(self, ids: list = [], count: int = 100, offset: int = 0) -> list:
		"""Получение списка заданий

		:param ids: Id заданий. Если не передан - вернёт все задания, defaults to []
		:type ids: list, optional

		:param count: Количество заданий, которые необходимо вернуть. Не более 100, defaults to 100
		:type count: int, optional

		:param offset: Смещение необходимое для выборки определенного подмножества, defaults to 0
		:type offset: int, optional

		:return: Метод возвращает список заданий
		:rtype: list
		"""

		return self._request("getTasks",
			ids=",".join(list(map(str, ids))),
			count=count, offset=offset)

	def getBalance(self) -> float:
		"""Получение текущего баланса аккаунта

:return: Метод возвращает баланс аккаунта
:rtype: float
"""

		return self._request("getBalance")
