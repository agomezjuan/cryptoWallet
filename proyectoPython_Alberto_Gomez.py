# -*- coding: utf-8 -*-

import os
from os import path
from datetime import datetime
import string
import random
import json


# Funcion crear nueva cuenta
def account_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


# Funcion Recibir dinero
def receive(user):
	code = user
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

	# Si ma moneda es correcta se pide la cantidad a recibir
	amount = float(input("Indique la cantidad: "))

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
			data['transactions'].append({
				'timestamp': timestamp,
				'coin': coin,
				'amount': amount
			})

			# Los datos se guardan en el archivo
			with open('accounts/' + code + '.json', 'w') as f:
				json.dump(data, f, indent=4)
		else:
			# Si el archivo no existe se preparan los datos para la primera transaccion
			data = {}
			timestamp = datetime.now().ctime()
			data['transactions'].append({
				'timestamp': timestamp,
				'coin': coin,
				'amount': amount
			})
			# Se crea la cuenta con la primera transaccion
			with open('accounts/' + code + '.json', 'w') as f:
				json.dump(data, f, indent=4)

	elif confirm == "no":
		success_end()


# Salir del programa
def exit_program():
	print ("Hasta pronto!\n")
	exit()


# Respuesta de una operacion exitosa
def success_end():
	print ("Gracias por usar su billetera.\n")
	restart = input("¿Desea realizar otra operación? (si/no) ")
	if restart == "si" or restart == "":
		Wallet()
	else:
		print ("Hasta pronto!\n")
		exit()


# Limpiar la pantalla
def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")


def invalid_input(count):
	count = count - 1
	if count == 0:
		print ("Has superado el límite de intentos. Hasta pronto!\n")
		exit()
	else:
		clear()
		print ("Seleccione una opción válida.\n")


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
					self.operations(code)
					break
				else:
					if i == 0:
						print ("Has superado el límite de intentos. Hasta pronto!\n")
						exit()
					else:
						clear()
						print("La cuenta indicada no existe. Si aun no la tiene se recomienda crear una nueva.\n")
						i = i - 1
			elif self.account == '2':
				clear()
				print ("Está a punto de crear una nueva cuenta de criptomonedas BTC, ETH y XRP.")
				confirm = input("¿Desea continuar? (si/no) ")
				if confirm == "si" or confirm == "":
					new_account = account_generator()
					data = {'account': [], 'transactions': []}
					timestamp = datetime.now().ctime()
					data['account'].append({
						'timestamp': timestamp,
						'code': new_account
					})
					# Se crea la cuenta con la primera transaccion
					with open('accounts/' + new_account + '.json', 'w') as f:
						json.dump(data, f, indent=4)

					if path.isfile('accounts/' + new_account + '.json'):
						print("La cuenta " + new_account + "se ha creado correctamente.\n"
							  "Ahora puede realizar transacciones.\n")
						self.operations(new_account)
						break
				else:
					exit_program()
			elif self.account == '3':
				exit_program()
			else:
				invalid_input(i)

	def operations(self, code):
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
				print("Ha escogido Recibir dinero")
				clear()
				receive(code)
				success_end()
				break
			elif option == '2':
				print("Ha escogido Transferir dinero")
			elif option == '3':
				print("Ha escogido Mostrar balance en moneda específica")
			elif option == '4':
				print("Ha escogido Mostrar balance general")
			elif option == '5':
				print("Mostrar histórico de transacciones")
			elif option == '6':
				print ("Hasta pronto!\n")
				exit()
			else:
				invalid_input()


if __name__ == '__main__':
	Wallet()
