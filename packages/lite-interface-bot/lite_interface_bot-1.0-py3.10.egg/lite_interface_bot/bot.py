from aiogram import Bot as AIBot, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .callback_data_filter import CallbackDataFilter
from .basic_handler import BasicHandler
STORAGE = MemoryStorage()

class Bot():
	"""
	Налаштування над aiogram, для швидшої, та лаконічнішої розробки ботів
	"""
	_dispatcher = None
	
	def __init__(self, *args, **kwargs):
		"""
		Ініціалізуємо базовий клас
		
		:param args: Тут думаю все зрозуміло. Всі параметри передаємо в орігінальний aiogram
		:param kwargs: Тут думаю все зрозуміло. Всі параметри передаємо в орігінальний aiogram
		"""
		self.bot = AIBot(*args, **kwargs)
	
	def dispatcher(self):
		"""
		Локальний кеш для диспетчера.
		Dispatcher створється автоматично, немає потреби викликати метод самостійно
		
		:return: Диспетчер aiogram dispatcher
		"""
		if self._dispatcher is None:
			self._dispatcher = Dispatcher(self.bot, storage=STORAGE)
		return self._dispatcher
	
	def message_handler(self, cls:BasicHandler, *custom_filters, step=None, any_state=False, use_command_handler=False, **kwargs):
		"""
		Обробник для реєстрації повідомлень
		Потрібно для реалізації таких функцій як: step(кроки), commands(в класі обробника)
		
		:param cls: Клас обробник
		:param custom_filters: Передається без зміни у register_message_handler
		:param step: Метод, який буде обробляти крок. Важливо! Метод має буде у класі cls
		:param any_state: Викликати з будь-яким станом
		:param use_command_handler: локальний аргумент, при ==True аргумент commands буде визначатися з класу обробника
		"""
		_object = cls(self)
		_args = []
		_kwargs = kwargs
		if step is None:
			_args.append(_object.handler)
			if any_state:
				_kwargs['state'] = '*'
		else:
			_args.append(getattr(_object, step.__name__))
			_kwargs['state'] = step.__qualname__
		
		if use_command_handler:
			if isinstance(_object.commands(), str):
				commands = {_object.commands()}
			else:
				commands = {*_object.commands()}
			kwargs['commands'] = commands
		
		if len(custom_filters) > 0:
			_args.append(*custom_filters)
		
		dispatcher = self.dispatcher()
		dispatcher.register_message_handler(*_args, **_kwargs)
			
	def callback_handler(self, cls:BasicHandler, *custom_filters, handler=None, step=None, any_state=False, **kwargs):
		"""
		Обробник для реєстрації зворотних викликів
		Потрібно для реалізації таких функцій як: step(кроки), handler(виклик користувацького методу з callback_query)
		
		:param cls: Клас обробник
		:param custom_filters: Передається без зміни у register_message_handler
		:param handler: Користувацький метод, для виклику з callback_query. Важливо! Метод має буде у класі cls
		:param step: Крок на якому буде оброблятися виклик. Списком можна передавати кілька
		:param any_state: Викликати з будь-яким станом
		"""
		_object = cls(self)
		filter = CallbackDataFilter(_object, handler)
		_args = [_object._callback_handler, filter]
		_kwargs = kwargs
		if step is None:
			if any_state:
				_kwargs['state'] = '*'
		else:
			if isinstance(step, list):
				_kwargs['state'] = [s.__qualname__ for s in step]
			else:
				_kwargs['state'] = step.__qualname__
			
		if len(custom_filters) > 0:
			_args.append(*custom_filters)
		
		dispatcher = self.dispatcher()
		dispatcher.register_callback_query_handler(*_args, **_kwargs)
	
	def command_handler(self, *args, **kwargs):
		"""
		Обробник для реєстрації команд
		Майже не потрібна штука, але хай буде.
		Надбудова над message_handler, яка робить код лаконічніше
		"""
		return self.message_handler(*args, use_command_handler=True, **kwargs)

	def photo_handler(self, *args, **kwargs):
		"""
		Обробник для реєстрації фото
		Майже не потрібна штука, але хай буде.
		Надбудова над message_handler, яка робить код лаконічніше
		"""
		return self.message_handler(*args, content_types=['photo'], **kwargs)