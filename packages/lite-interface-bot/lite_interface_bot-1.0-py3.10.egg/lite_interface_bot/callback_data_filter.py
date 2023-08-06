from aiogram import types
from aiogram.dispatcher.filters import Filter

class CallbackDataFilter(Filter):
	"""
	Фільтр для власної реалізації CallbackData
	"""
	def __init__(self, method, handler):
		"""
		Ініціалізуємо фільтр
		
		:param method: Обробник(клас)
		:param handler: Користувацька функія(метод) 
		"""
		self.method = method
		self.handler = handler
	
	async def check(self, query: types.CallbackQuery):
		"""
		Чекер для aiogram
		
		:param query: CallbackQuery
		"""
		try:
			data = query.data
		except ValueError:
			return False
		prefix, *parts = data.split(':')
		method, handler = prefix.split('|', 2)
		if method != self.method.__name__:
			return False

		if len(handler) < 1:
			handler = None
		if self.handler is not None and self.handler.__name__ != handler:
			return False
		if handler is not None and self.handler is None:
			return False
		
		values = {}
		for part in parts:
			key, value = part.split('=', 2)
			if value == 'None':
				value = None
			elif value == 'True':
				value = True
			elif value == 'False':
				value = False
			values[key] = value
		values['handler'] = handler
		if len(values) > 0:
			return values
		else:
			return True