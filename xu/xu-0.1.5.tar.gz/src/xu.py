"""Collection of handy random generators."""

__all__ = ["pick", "boolean", "char", "number", "integer", "random", "string"]


class __xu__:
	from random import SystemRandom
	randy = SystemRandom()
	lower = "abcdefghijklmnopqrstuvwxyz"
	upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digit = "0123456789"
	alpha = "".join(a + b for a, b in zip(lower, upper))
	latin = alpha + digit

	class xu:
		"""Random values."""
		def next(self):
			""":return: A random value."""
			pass

		def __pow__(self, size: int or tuple) -> list:
			"""
			:param size: The size of the resulting matrix.

			:return: A matrix of random values.
			"""
			width, height = size if isinstance(size, tuple) else (size, size)
			return self.matrix(width, height)

		def matrix(self, width: int, height=0) -> list:
			"""
			:param width: The width of the resulting matrix.
			:param height: The height of the resulting matrix.

			:return: A matrix of random values.
			"""
			return [self.list(width) for _ in range(height or width)]

		def __mul__(self, size: int) -> list:
			return self.list(size)

		def list(self, size: int) -> list:
			"""
			:param size: The size of the resulting list.

			:return: A list of random values.
			"""
			return [self.next() for _ in range(size)]

		def __str__(self):
			return str(self.next())

	xu.__mul__.__doc__ = xu.list.__doc__

	class bool(xu):
		"""Random booleans."""
		def next(self) -> bool:
			""":return: Either True or False."""
			return bool(integer(1).next())

	class str(xu):
		"""Random strings."""
		def __init__(self, length: int, subset: str = None, *, prefix='', suffix=''):
			self._length = length
			self._subset = subset or __xu__.latin
			self._prefix = prefix
			self._suffix = suffix

		def next(self) -> str:
			""":return: A random string."""
			result = "".join(pick(self._subset, self._length))
			return self._prefix + result + self._suffix

		def using(self, subset: str):
			"""Replace the subset with the provided one."""
			self._subset = subset
			return self

		def extend(self, subset: str):
			"""Extend the subset with the provided one."""
			self._subset += subset
			return self


	class char(str):
		"""Random characters."""
		def __init__(self, subset: str = None):
			""":param subset: The subset of characters to pick from."""
			super().__init__(1, subset)

		def next(self) -> str:
			""":return: A random character."""
			return self._prefix + pick(self._subset) + self._suffix

		def wrap(self, prefix: str, suffix=None):
			"""Use the specified prefix and suffix.
			If the suffix is not provided, then the former remains."""
			self._prefix = prefix
			self._suffix = self._suffix if suffix is None else suffix
			return self

		def suffix(self, suffix: str):
			"""Use the specified suffix."""
			self._suffix = suffix
			return self


def pick(source, quantity=1):
	"""Pick N elements from the source."""
	if hasattr(source, '__getitem__'):
		r = [source[integer(len(source) - 1).next()] for _ in range(quantity)]
		return r[0] if quantity == 1 else r
	return source


class integer(__xu__.xu):
	"""Random integers."""
	def __init__(self, stop: int, start=0, *, step=1):
		self._start = min(stop, start)
		self._stop = max(stop, start) + 1
		self._step = step

	def next(self) -> int:
		""":return: A random integer in the specified range."""
		return __xu__.randy.randrange(self._start, self._stop, self._step)


class number(__xu__.xu):
	"""Random floats."""
	def __init__(self, stop: float, start=0.0):
		self._start = start
		self._stop = stop

	def next(self) -> float:
		""":return: A random float in the specified range."""
		return __xu__.randy.uniform(self._start, self._stop)


class string(__xu__.str):
	"""Random strings."""
	def __init__(self, length: int, subset: str = None, *, prefix='', suffix=''):
		"""
		:param length: The length of the resulting string.
		:param subset: The subset of characters to pick from.
		"""
		super().__init__(length, subset, prefix=prefix, suffix=suffix)
		self.lower = __xu__.str(self._length, __xu__.lower)
		self.upper = __xu__.str(self._length, __xu__.upper)
		self.digit = __xu__.str(self._length, __xu__.digit)
		self.alpha = __xu__.str(self._length, __xu__.alpha)
		self.latin = __xu__.str(self._length, __xu__.latin)


boolean = __xu__.bool()
char = __xu__.char()
random = number(1)
