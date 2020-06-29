# -*- coding: utf-8 -*-

import json
import os
import random
import string
from datetime import datetime
from os import path

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


# Consulta coinmarketcap
def coinmarket_api():
	# Llamado a la API de coinmarketcap
	url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

	parameters = {
		'symbol': 'BTC,ETH,XRP'
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
		data['transactions'][coin].append({
			'timestamp': timestamp,
			'origin': code,
			'amount': amount * (-1),
			'receiver': receiver
		})

		# Los datos se guardan en el archivo
		with open('accounts/' + code + '.json', 'w') as f:
			json.dump(data, f, indent=4)
			print("\nSe han transferido " + str(amount) + " " + coin + " a la cuenta " + receiver + ".")


# Actualizar cuenta destinataria
def update_registry_receiver(code, coin, amount, receiver):
	# Si la cuenta existe se actualiza la nueva transaccion
	if path.isfile('accounts/' + receiver + '.json'):
		# Lectura del historial de transacciones
		with open('accounts/' + receiver + '.json', 'r') as f:
			data = json.load(f)

		# Nueva transaccion para actualizar
		timestamp = datetime.now().ctime()
		data['transactions'][coin].append({
			'timestamp': timestamp,
			'origin': code,
			'amount': amount,
			'receiver': receiver
		})

		# Los datos se guardan en el archivo
		with open('accounts/' + receiver + '.json', 'w') as f:
			json.dump(data, f, indent=4)
			print("Se recibieron correctamente " + str(amount) + " " + coin + " en la cuenta " + receiver + ".\n")


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
		if path.exists('accounts/' + code + '.json'):

			# Lectura del historial de transacciones
			with open('accounts/' + code + '.json', 'r') as f:
				data = json.load(f)

			# Nueva transaccion para actualizar
			timestamp = datetime.now().ctime()
			data['transactions'][coin].append({
				'timestamp': timestamp,
				'origin': "Deposit",
				'amount': amount,
				'receiver': code
			})

			# Los datos se guardan en el archivo
			with open('accounts/' + code + '.json', 'w') as f:
				json.dump(data, f, indent=4)
				print("\nSe han depositado " + str(amount) + " " + coin + " en la cuenta " + code + ".")

			# Lectura del historial de transacciones
			with open('accounts/' + code + '.json', 'r') as f:
				data = json.load(f)

				# Consulta las transacciones y suma el total de los registros
				transactions = data['transactions'][coin]

				balance = 0
				for value in transactions:
					balance = balance + value['amount']

				print("El nuevo saldo de " + coin + " en la cuenta es: " + str(balance) + " " + coin + ".\n")

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
		coin = input("Indique la moneda a consultar saldo: ").upper()
		i = i - 1
		if i == 0:
			print ("Has superado el límite de intentos. Hasta pronto!\n")
			exit()

	# Si la cuenta existe se actualiza la nueva transaccion
	if path.exists('accounts/' + code + '.json'):
		# Lectura del historial de transacciones
		with open('accounts/' + code + '.json', 'r') as f:
			data = json.load(f)

	#
	transactions = data['transactions'][coin]

	balance = 0
	for value in transactions:
		balance = balance + value['amount']

	binance_response = coinmarket_api()
	coin_global_balance = balance * binance_response['data'][coin]['quote']['USD']['price']

	print("\nEl saldo total de " + coin + " en la cuenta es: " + str(round(balance, 5)) + " " + coin + ".\n"
																									   "El saldo equivalente en USD es: $" + str(
		round(coin_global_balance, 2)))


# Funcion consultar saldo total
def global_balance(code):
	code = code
	if path.exists('accounts/' + code + '.json'):
		# Lectura del historial de transacciones
		with open('accounts/' + code + '.json', 'r') as f:
			data = json.load(f)

		transactions_btc = data['transactions']['BTC']
		transactions_eth = data['transactions']['ETH']
		transactions_xrp = data['transactions']['XRP']

		def balance(transactions):
			balance = 0
			for value in transactions:
				balance = balance + value['amount']
			return balance

		balance_btc = balance(transactions_btc)
		balance_eth = balance(transactions_eth)
		balance_xrp = balance(transactions_xrp)

		binance_response = coinmarket_api()

		balance_btcusd = balance_btc * binance_response['data']['BTC']['quote']['USD']['price']
		balance_ethusd = balance_eth * binance_response['data']['ETH']['quote']['USD']['price']
		balance_xrpusd = balance_xrp * binance_response['data']['XRP']['quote']['USD']['price']

		wallet_global_balance = balance_btcusd + balance_ethusd + balance_xrpusd

		print ("\nEl balance de Bitcoin es: " + str(balance_btc) + " BTC.")
		print ("El balance de Ethereum es: " + str(balance_eth) + " ETH.")
		print ("El balance de Ripple es: " + str(balance_xrp) + " XRP.\n")

		print ("El saldo total de su billetera en USD es: $" + str(round(wallet_global_balance, 2)))


# Funcion consultar historial
def historical(code):
	code = code
	if path.exists('accounts/' + code + '.json'):
		# Lectura del historial de transacciones
		with open('accounts/' + code + '.json', 'r') as f:
			data = json.load(f)

		transactions_btc = data['transactions']['BTC']
		transactions_eth = data['transactions']['ETH']
		transactions_xrp = data['transactions']['XRP']

		def history(transactions, coin):
			if transactions:
				total = 0
				print ("\nFecha					Origen		Destino		Valor\n"
					   "-------------------------------------------------------------------------------------")
				for value in transactions:
					print(str(value['timestamp']) + "		" +
						  str(value['origin']) + "		" +
						  str(value['receiver']) + "		" +
						  str(round(value['amount'], 5)) + " " + coin)
					total = total + value['amount']

				print("-------------------------------------------------------------------------------------\n"
					  "		T O T A L   D E   T R A N S A C C I O N E S		" +
					  str(round(total, 4)) + " " + coin + "\n")
			else:
				print("\nNo se han realizado transacciones en moneda " + coin + ".")

		history(transactions_btc, "BTC")
		history(transactions_eth, "ETH")
		history(transactions_xrp, "XRP")


# Salir del programa
def exit_program():
	print ("Hasta pronto!\n")
	Wallet()


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
			clear()
			print("Ha escogido Mostrar balance general")
			global_balance(code)
			success_end(code)
			break
		elif option == '5':
			clear()
			print("Ha escogido Mostrar histórico de transacciones")
			historical(code)
			success_end(code)
			break
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
				print ("1. Iniciar sesión con una cuenta existente.\n"
					   "2. Crear nueva cuenta.\n"
					   "3. Salir del programa.\n")

			self.account = input("")
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
