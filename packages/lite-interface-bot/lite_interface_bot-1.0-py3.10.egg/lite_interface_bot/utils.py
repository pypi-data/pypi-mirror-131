from aiogram import types

class Keyboards():
	"""
	Все, що пов'язане з кнопками
	"""
	@staticmethod
	def inline_init(*args):
		"""
		Генератор кнопок
		
		Створюємо кнопки лаконічно і просто.
		Щоб отримати заповнений заповнений об'єкт InlineKeyboardMarkup потрібно тільки передати параменти для кнопок.
		
		В args отримуємо кнопки рядка.
		В кожному списку дані однієї кнопки: список з назви кнопки і рядка callback_data
		Приклад:
		Keyboards.inline_init([['Button1', 'btn1'], ['Button2', 'btn2']])
		
		:param args: Список кнопок
		"""
		keyboard = types.InlineKeyboardMarkup()
		for row in args:
			_row = []
			for rowrow in row:
				_row.append(types.InlineKeyboardButton(
						rowrow[0],
						callback_data=rowrow[1],
					))
			if len(_row) > 1:
				keyboard.row(*_row)
			else:
				keyboard.add(_row[0])
		return keyboard
