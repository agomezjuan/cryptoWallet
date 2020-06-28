# -*- coding: utf-8 -*-

import os
from os import path
from datetime import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import string
import random
import json


# Consulta coinmarketcap
def coinmarket_api():
	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

	parameters = {
		'symbol': ['BTC', 'ETH', 'XRP']
	}
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': 'ec69bd6c-2009-4908-9640-4ba3747d28eb',
	}

	session = Session()
	session.headers.update(headers)

	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
		return data
	except (ConnectionError, Timeout, TooManyRedirects) as e:
		print(e)


# Funcion crear nueva cuenta
def account_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


# Actualizar cuenta de origen
def update_registry_sender(code, coin, amount, receiver):
	# Si la cuenta existe se actualiza la nueva transaccion
	if path.isfile('accounts/' + code + '.json'):

		# Lectura del historial de transacciones
		with open('accounts/' + code + '.json', 'r') as f:
			data = json.load(f)

		# Nueva transaccion para actualizar
		timestamp = datetime.now().ctime()
		data['transactions'].append({
			'timestamp': timestamp,
			'origin': code,
			'coin': coin,
			'amount': amount * (-1),
			'receiver': receiver
		})

		# Los datos se guardan en el archivo
		with open('accounts/' + code + '.json', 'w') as f:
			json.dump(data, f, indent=4)
			print("\nSe han transferido " + str(amount) + " " + coin + " a la cuenta " + receiver + ".")
	else:
		# Si el archivo no existe se preparan los datos para la primera transaccion
		data = {}
		timestamp = datetime.now().ctime()
		data['transactions'].append({
			'timestamp': timestamp,
			'origin': code,
			'coin': coin,
			'amount': amount * (-1),
			'receiver': receiver
		})
		# Se crea la cuenta con la primera transaccion
		with open('accounts/' + code + '.json', 'w') as f:
			json.dump(data, f, indent=4)


# Actualizar cuenta destinataria
def update_registry_receiver(code, coin, amount, receiver):
	# Si la cuenta existe se actualiza la nueva transaccion
	if path.isfile('accounts/' + receiver + '.json'):

		# Lectura del historial de transacciones
		with open('accounts/' + receiver + '.json', 'r') as f:
			data = json.load(f)

		# Nueva transaccion para actualizar
		timestamp = datetime.now().ctime()
		data['transactions'].append({
			'timestamp': timestamp,
			'origin': code,
			'coin': coin,
			'amount': amount,
			'receiver': receiver
		})

		# Los datos se guardan en el archivo
		with open('accounts/' + receiver + '.json', 'w') as f:
			json.dump(data, f, indent=4)
			print("Se recibieron correctamente " + str(amount) + " " + coin + " en la cuenta " + receiver + ".\n")
	else:
		# Si el archivo no existe se preparan los datos para la primera transaccion
		data = {}
		timestamp = datetime.now().ctime()
		data['transactions'].append({
			'timestamp': timestamp,
			'origin': code,
			'coin': coin,
			'amount': amount,
			'receiver': receiver
		})
		# Se crea la cuenta con la primera transaccion
		with open('accounts/' + receiver + '.json', 'w') as f:
			json.dump(data, f, indent=4)


# Funcion Recibir dinero
def receive(code):
	code = code
	coin = input("Indique la moneda a recibir: ").upper()
	i = 2

	# Ciclo verifica si la criptomoneda seleccionada se encuentra en la billetera.
	# En caso de que no, el programa termina al tercer intento incorrecto
	while not coin == "BTC" and not coin == "ETH" and not coin == "XRP":
		print ("Su billetera solo almacena las criptomonedas BTC, ETH y XRP.\n")
		coin = input("Indique la moneda a recibir: ").upper()
		i = i - 1
		if i == 0:
			print ("Has superado el límite de intentos. Hasta pronto!\n")
			exit()

	k = 3
	while True:
		try:
			# Si ma moneda es correcta se pide la cantidad a recibir
			amount = float(input("Indique la cantidad de " + coin + " a recibir: "))
			break
		except ValueError:
			clear()
			print("Debe indicar un valor numérico positivo.")
			k = k - 1
			if k == 0:
				clear()
				print ("Has superado el límite de intentos. Hasta pronto!\n")
				exit()

	# Confirmacion de la cantidad a recibir en la moneda seleccionada
	print ("\nUsted recibirá " + str(amount) + " " + coin + " en su cuenta.")

	confirm = input("¿Desea continuar? (si/no) ")
	if confirm == "si" or confirm == "":

		# Si la cuenta existe se actualiza la nueva transaccion
		if path.isfile('accounts/' + code + '.json'):

			# Lectura del historial de transacciones
			with open('accounts/' + code + '.json', 'r') as f:
				data = json.load(f)

			# Nueva transaccion para actualizar
			timestamp = datetime.now().ctime()
			data['transactions'][coin].append({
				'timestamp': timestamp,
				'origin': "Deposit",
				'amount': amount
			})

			# Los datos se guardan en el archivo
			with open('accounts/' + code + '.json', 'w') as f:
				json.dump(data, f, indent=4)
				print("\nSe han depositado " + str(amount) + " " + coin + " en la cuenta " + code + ".")
		else:
			# Si el archivo no existe se preparan los datos para la primera transaccion
			data = {}
			timestamp = datetime.now().ctime()
			data['transactions'].append({
				'timestamp': timestamp,
				'origin': "Deposit",
				'coin': coin,
				'amount': amount
			})
			# Se crea la cuenta con la primera transaccion
			with open('accounts/' + code + '.json', 'w') as f:
				json.dump(data, f, indent=4)

	elif confirm == "no":
		success_end(code)


# Funcion transferir dinero
def transfer(code):
	code = code
	coin = input("Indique la moneda a transferir: ").upper()
	i = 2

	# Ciclo verifica si la criptomoneda seleccionada se encuentra en la billetera.
	# En caso de que no, el programa termina al tercer intento incorrecto
	while not coin == "BTC" and not coin == "ETH" and not coin == "XRP":
		print ("Su billetera solo almacena las criptomonedas BTC, ETH y XRP.\n")
		coin = input("Indique la moneda a transferir: ").upper()
		i = i - 1
		if i == 0:
			print ("Has superado el límite de intentos. Hasta pronto!\n")
			exit()

	# Si ma moneda es correcta se pide la cantidad a recibir
	amount = float(input("Indique la cantidad de " + coin + " que va a transferir: "))

	j = 3
	while True:
		# Cuenta de destino
		receiver = input("Indique el código de cuenta de destino: ").upper()

		if path.exists('accounts/' + receiver + '.json'):
			# Confirmacion de la cantidad a recibir en la moneda seleccionada
			print ("\nUsted transferirá " + str(amount) + " " + coin + " a la cuenta " + receiver + ".")
			confirm = input("¿Desea continuar? (si/no) ")

			if confirm == "si" or confirm == "":
				update_registry_sender(code, coin, amount, receiver)
				update_registry_receiver(code, coin, amount, receiver)
				success_end(code)
				break
			elif confirm == "no":
				success_end(code)
		else:
			msg = "Este código de cuenta no existe. Por favor verifique e intente nuevamente."
			invalid_input(j, msg)


# Funcion consultar saldo
def balance_coin(code):
	code = code
	coin = input("Indique la moneda a consultar saldo: ").upper()
	i = 2

	# Ciclo verifica si la criptomoneda seleccionada se encuentra en la billetera.
	# En caso de que no, el programa termina al tercer intento incorrecto
	while not coin == "BTC" and not coin == "ETH" and not coin == "XRP":
		print ("Su billetera solo almacena las criptomonedas BTC, ETH y XRP.\n")
		coin = input("Indique la moneda a transferir: ").upper()
		i = i - 1
		if i == 0:
			print ("Has superado el límite de intentos. Hasta pronto!\n")
			exit()

	# Si la cuenta existe se actualiza la nueva transaccion
	if path.isfile('accounts/' + code + '.json'):
		# Lectura del historial de transacciones
		with open('accounts/' + code + '.json', 'r') as f:
			data = json.load(f)

		values = data['transactions'][coin]['amount'].values()
		print(values)


# Salir del programa
def exit_program():
	print ("Hasta pronto!\n")
	exit()


# Respuesta de una operacion exitosa
def success_end(code):
	code = code
	print ("\nGracias por usar su billetera.\n")
	restart = input("¿Desea realizar otra operación? (si/no) ")
	if restart == "si" or restart == "":
		clear()
		operations(code)
	else:
		exit_program()


# Limpiar la pantalla
def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")


# Entradas incorrectas
def invalid_input(count, msg=""):
	count = count - 1
	if count == 0:
		print ("Has superado el límite de intentos. Hasta pronto!\n")
		exit()
	else:
		clear()
		print (msg)


# Operaciones de billetera
def operations(code):
	code = code
	i = 3
	# Ciclo de bienvenida: Se debe indicar una de las 6 opciones validas
	# En caso contrario el programa se cierra al tercer intento erroneo
	while True:
		if i == 3:
			print ("Bienvenido a su billetera de criptomonedas.")

		print ("Por favor indique la operación que desea realizar:\n"
			   "1. Recibir dinero\n"
			   "2. Transferir dinero\n"
			   "3. Mostrar balance en moneda específica\n"
			   "4. Mostrar balance general\n"
			   "5. Mostrar histórico de transacciones\n"
			   "6. Salir del programa\n")

		option = input("")

		if option == '1':
			clear()
			print("Ha escogido Recibir dinero")
			receive(code)
			success_end(code)
			break
		elif option == '2':
			clear()
			print("Ha escogido Transferir dinero")
			transfer(code)
			success_end(code)
			break
		elif option == '3':
			clear()
			print("Ha escogido Mostrar balance en moneda específica")
			balance_coin(code)
			break
		elif option == '4':
			print("Ha escogido Mostrar balance general")
		elif option == '5':
			print("Mostrar histórico de transacciones")
		elif option == '6':
			clear()
			print ("Hasta pronto!\n")
			exit()
		else:
			msg = "Seleccione una opción válida.\n"
			invalid_input(i, msg)


# Clase principal billetera
class Wallet:
	def __init__(self):
		clear()
		i = 3
		while True:
			if i == 3:
				print ("Bienvenido a su billetera de criptomonedas.\n")
			self.account = input("1. Iniciar sesión con una cuenta existente.\n"
								 "2. Crear nueva cuenta.\n"
								 "3. Salir del programa.\n")

			if self.account == '1':
				code = input("\nIndique su código de cuenta: ").upper()
				if path.exists('accounts/' + code + '.json'):
					clear()
					print ("Inicio exitoso.\n"
						   "Su código de cuenta es: " + code + "\n")
					operations(code)
					break
				else:
					msg = "La cuenta indicada no existe. Si aun no la tiene se recomienda crear una nueva.\n"
					invalid_input(i, msg)

			elif self.account == '2':
				clear()
				print ("Está a punto de crear una nueva cuenta de criptomonedas BTC, ETH y XRP.")
				confirm = input("¿Desea continuar? (si/no) ")
				if confirm == "si" or confirm == "":
					new_account = account_generator()
					data = {'account': [], 'transactions': {'BTC': [], 'ETH': [], 'XRP': []}}
					timestamp = datetime.now().ctime()
					data['account'].append({
						'timestamp': timestamp,
						'code': new_account
					})
					# Se crea la cuenta con la primera transaccion
					with open('accounts/' + new_account + '.json', 'w') as f:
						json.dump(data, f, indent=4)

					if path.isfile('accounts/' + new_account + '.json'):
						print("La cuenta " + new_account + " se ha creado correctamente.\n"
							  "Ahora puede realizar transacciones.\n")
						operations(new_account)
						break
				else:
					exit_program()
			elif self.account == '3':
				exit_program()
			else:
				msg = "Seleccione una opción válida.\n"
				invalid_input(i, msg)


if __name__ == '__main__':
	Wallet()
