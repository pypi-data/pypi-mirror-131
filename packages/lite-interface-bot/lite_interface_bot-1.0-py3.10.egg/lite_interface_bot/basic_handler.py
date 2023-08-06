import inspect
from aiogram import Dispatcher

class BasicHandler():
	"""
	Базовий обробник
	
	Для реалізації користувацького обробника потрібно наслідувати цей клас.
	Далі користувацький клас може бути переданний у message_handler, callback_handler та інші
	
	При ініціалізації обов'язково потрібно створювати асинхронний метод handler,
	який буде обробляти всі аргументи з базових обробників aiogram
	ВАЖЛИВО! Не використовуйте в handler *args та **kwargs, зараз немає можливості їх обробляти (див. callback_data[args_handler])
	"""
	def __init__(self, bot):
		"""
		Ініціалізуємо базовий обробник
		
		:param bot: Наша надбудова Bot(lite_interface_bot.Bot) над aiogram
		"""
		self.ibot = bot
		self.bot = bot.bot
	
	@classmethod
	def callback_data(cls, handler=None, **kwargs):
		"""
		Генератор callback_data строки
		
		Використання CallbackData із пакету aiogram куди краще, ніж реалізації у telebot,
		але мені все ж мені хотілося зручнішої реалізації.
		Тож – це мій варіант callback_data. Можливо не дуже правильна реалізація, та виглядає зручно і лаконічно
		ВАЖЛИВО! методи обов'язково потрібно реєструвати в обробниках
		
		:param handler: Користувацький обробник виклику (Необов'язковий аргумент)
		:param kwargs: Змінні які будуть передані в handler
		"""
		handler_name = handler.__name__ if handler is not None else ''
		if handler is None:
			handler = cls.handler
	
		# В теорії наступні дві перевірки можна видалити, час покаже
		# Перевіряємо, чи всі передані аргументи handler може опрацювати
		args_handler = inspect.getfullargspec(handler).args
		for a in kwargs:
			if a not in args_handler:
				raise ValueError(f"No arg {a} in handler")
		# Аргументи які не передали, робимо None
		for a in args_handler[2:]:
			if a not in kwargs:
				kwargs[a] = None
	
		method_name, *method_args = handler.__qualname__.split('.')
		data = [f"{method_name}|{handler_name}"]
		for a in kwargs:
			value = f'{a}={kwargs[a]}'
			if ':' in value:
				raise ValueError("Symbol : is defined as the separator and can't be used in parts' values")
			data.append(value)
		
	
		callback_data = ':'.join(data)
		if len(callback_data.encode()) > 64:
			raise ValueError('Resulted callback data is too long!')
		
		return callback_data

	async def set_step(self, step):
		"""
		Встановлюємо крок
		
		Просто та лаконічно. Звісно, менш функціонально, ніж базова реалізація у aiogram,
		але як же бляха це зручно. Для простих задач підходить ідеально.
		ВАЖЛИВО! Кроки обов'язково потрібно реєструвати в обробниках
		
		:param step: Метод, який буде обробляти крок
		"""
		_state = Dispatcher.get_current().current_state()
		state_name = step.__qualname__
		await _state.set_state(state_name)
		return True


		
	def commands(self):
		"""
		Назва команди, або кількох команд
		
		Потрібно для використання в Bot.command_handler
		За замовченням назва класу, можна змінювати за будь-яку
		Для зміні потрібно в користувацьому класі перевизначити цей метод
		"""
		return self.__class__.__name__

	async def handler(self):
		"""
		Обробник викликів. В користувацькому класі обов'язкове визначення даного методу
		"""
		raise Exception("Method handler no init")
		
	async def _callback_handler(self, *args, **kwargs):
		"""
		Обробник для callback_handler. ВАЖЛИВО! Не визначайте, та не змінюйте цей метод
		"""
		if 'handler' in kwargs and kwargs['handler'] is not None:
			handler = getattr(self, kwargs['handler'])
		else:
			handler = self.handler
		_kwargs = {}
		args_handler = inspect.getfullargspec(handler).args
		for arg in kwargs:
			if arg in args_handler:
				_kwargs[arg] = kwargs[arg]
		
		return await handler(*args, **_kwargs)

