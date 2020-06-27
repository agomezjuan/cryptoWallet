# -*- coding: utf-8 -*-
from datetime import datetime
import json


def receive():
	coin = input("Indique la moneda a recibir: ").upper()
	i = 3
	while not coin == "BTC" and not coin == "ETH" and not coin == "XRP":
		print ("Su billetera solo almacena las criptomonedas BTC, ETH y XRP.\n")
		coin = input("Indique la moneda a recibir: ").upper()
		i = i - 1
		if i == 0:
			print ("Has superado el límite de intentos. Hasta pronto!\n")
			exit()

	amount = float(input("Indique la cantidad: "))
	print ("Usted recibirá " + str(amount) + " " + coin + " en su cuenta.")

	confirm = input("¿Desea continuar? (si/no) ")
	if confirm == "si" or confirm == "":
		with open(coin+'.json', 'r') as file:
			data = json.load(file)

		timestamp = datetime.now().ctime()
		data['transactions'].append({
			'timestamp': timestamp,
			'coin': coin,
			'amount': amount
		})

		with open(coin+'.json', 'w') as file:
			json.dump(data, file, indent=4)

	elif confirm == "no":
		success_end()


def success_end():
	print ("Gracias por usar su billetera.\n")
	restart = input("¿Desea realizar otra operación? (si/no) ")
	if restart == "si" or restart == "":
		Wallet()
	else:
		print ("Hasta pronto!\n")
		exit()


class Wallet:
	def __init__(self):

		i = 3
		while True:
			if i == 3:
				print ("Bienvenido a su billetera de criptomonedas.\n")

			print ("Por favor indique la operación que desea realizar:\n"
				   "1. Recibir dinero\n"
				   "2. Transferir dinero\n"
				   "3. Mostrar balance en moneda específica\n"
				   "4. Mostrar balance general\n"
				   "5. Mostrar histórico de transacciones\n"
				   "6. Salir del programa\n")

			self.option = input("")

			if self.option == '1':
				print("Ha escogido Recibir dinero")
				receive()
				success_end()
				break
			elif self.option == '2':
				print("Ha escogido Transferir dinero")
			elif self.option == '3':
				print("Ha escogido Mostrar balance en moneda específica")
			elif self.option == '4':
				print("Ha escogido Mostrar balance general")
			elif self.option == '5':
				print("Mostrar histórico de transacciones")
			elif self.option == '6':
				exit()
			else:
				print ("Seleccione una opción válida.\n")
				i = i - 1
				if i == 0:
					print ("Has superado el límite de intentos. Hasta pronto!\n")
					exit()


if __name__ == '__main__':
	Wallet()
