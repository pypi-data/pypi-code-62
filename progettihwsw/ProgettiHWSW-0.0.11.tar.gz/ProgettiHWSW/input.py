# Copyright (c) 2020 Arda Seremet <ardaseremet@outlook.com>

from ProgettiHWSW.api import API
from ProgettiHWSW.const import STATUS_XML_PATH
from lxml import etree

class Input:
	"""Class that represents an input object."""

	def __init__(self, api: API, input_number: int, is_old: bool):
		"""Initialize Input class."""
		self.input_number = input_number
		self.api = api
		self.state = None
		self.is_old = is_old

	@property
	def id(self) -> int:
		"""Return the input number."""
		return self.input_number

	@property
	def is_on(self) -> bool:
		"""Return if the input is on."""
		return self.state

	def update(self):
		"""Update the input status."""
		request = self.api.request("get", STATUS_XML_PATH)
		if request == False:
			return None
		
		root = etree.XML(request.text)
		number = self.input_number - 1 if self.is_old else self.input_number
		self.state = True if root.xpath(f"//btn{number}")[0].text == "up" else False