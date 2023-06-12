class datatype:
	def __init__(**k):
		self._dict = {**k, **self.__dict__}

	def __getattribute__(self, k):
		return object.__getattribute__(self, "_dict")[k]

	def __setattr__(self, k, v):
		object.__getattribute__(self, "_dict")[k] = v


class VectorDict:
	def __init__(self):
		self._dict = {}

	def __getitem__(self, k):
		if k not in self._dict.keys():
			self._dict[k] = {}
		return self._dict.key()
