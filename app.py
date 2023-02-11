# def get_int():
# 	value = input('Введите число: ')
# 	try:
# 		int_value = int(value)
# 	except ValueError:
# 		print('Указанное число преобразовать в int невозможно')
# 		return

# 	if int_value >= 0:
# 		print('Мы получили число', int_value)
# 	else:
# 		print('Число оказалось отрицательным')

# get_int()

# def handler():
# 	try:
# 		value_1 = input('Введите число: ')
# 		value_2 = input('Введите число: ')
# 		result = int(value_1) / int(value_2)
# 		return result
# 	except ValueError as e:
# 		print('Вы ввели не число')
# 		print(e)
# 	except ZeroDivisionError:
# 		print('На ноль делить нельзя')
# 	except KeyboardInterrupt:
# 		print('Программа прервана')

# handler()

# import this

# обработчик исключений
def get_int():
	value = input('Введите число: ')
	try:
		int_value = int(value)
	except ValueError:
		print('указанное число преобразовать в int невозможно')
		return

	if int_value >= 0:
		print('мы получили число', int_value)
	else:
		print('число оказалось отрицательным')
# get_int()

def handler ():
	try:
		value_1 = input('Введите число: ')
		value_2 = input('Введите число: ')
		result = int(value_1) / int(value_2)
		return result
	except ValueError as e:
		print('вы ввели не число') 
		print(e)
	except ZeroDivisionError:
		print('делить на 0 нельзя')
	except KeyboardInterrupt:
		print('программа прервана')
handler ()