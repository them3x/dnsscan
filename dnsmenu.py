import os
import json

class Menu:
	def __init__(self, dominio):
		if os.path.isdir("scans") == False:
			os.mkdir("scans")

		if dominio != False and os.path.isdir(f"scan/{dominio}") == False:
			os.mkdir(f"scans/{dominio}")

	def menu():
		while True:
			scans = os.listdir("scans/")
			if len(scans) < 1:
				print("+-------------------------\n| NENHUM SCAN REALIZADO :(\n+-------------------------")
				exit(0)

			print("+------------------------\n| SELECIONE O ID DO SCAN\n+------------------------")
			id = 0
			for scan in scans:
				print(f"| ({id})\t{scan}")
				id += 1

			print("+------------------------")

			select = input("| > ").lower()
			if select == "exit" or select == "sair":
				exit(0)
			else:
				try:
					select = int(select)
				except ValueError:
					print("| ID INVALIDO")
					continue

			try:
				pasta = scans[select]
			except IndexError:
				print("| ID NÃO ENCONTRADO")
				continue

			try:
				with open(f"scans/{pasta}/{pasta}-cname.json") as f:
					cname = json.loads(f.read())
					lcname = len(cname)
			except FileNotFoundError:
				cname = False
				lcname = "Scan não realizado"

			try:
				with open(f"scans/{pasta}/{pasta}-subdomains.json") as f:
					subdomains = json.loads(f.read())
					subipv4 = subdomains["ipv4"]
					subipv6 = subdomains["ipv6"]
					lipv4 = len(subipv4)
					lipv6 = len(subipv6)

			except FileNotFoundError:
				subdomains = False
				subipv4 = False
				subipv6 = False
				lipv4 = "Scan não realizado"
				lipv6 = "Scan não realizado"
			try:
				with open(f"scans/{pasta}/{pasta}.whois") as f:
					whois = f.read()
			except FileNotFoundError:
				whois = False


			head =f"+-------- | {pasta} | -------------"
			print(head)
			print(f"| Subdominios IPV6: {lipv6}")
			print(f"| Subdominios IPV4: {lipv4}")
			print(f"| Registros CNAME:  {lcname}")
			print("+"+"-"*(len(head) - 1))
			print("| list [ipv4/ipv6/cname/whois]")
			print("+"+"-"*(len(head) - 1))
			while True:
				select = input("| > ")

				if select == "list ipv4":
					if subipv4 == False:
						print("| SCAN NÃO REALIZADO")
					else:
						print("+-----------------------------------------------------\n|   subdominio          |          endereço IP\n+-----------------------------------------------------")
						for ip in subipv4:
							print(f"| {ip:<30} {subipv4[ip]}")
						print("+-----------------------------------------------------")
				elif select == "list ipv6":
					if subipv6 == False:
						print("| SCAN NÃO REALIZADO")
					else:
						print("+-----------------------------------------------------\n|   subdominio          |          endereço IP\n+-----------------------------------------------------")
						for ip in subipv6:
							print(f"| {ip:<30} {subipv6[ip]}")
						print("+-----------------------------------------------------")

				elif select == "list cname":
					if cname == False:
						print("| SCAN NÃO REALIZADO")

					else:
						print("+-----------------------------------------------------\n|   subdominio          |          registro CNAME\n+-----------------------------------------------------")
						for domain in cname:
							print(f"| {domain:<30} {cname[domain]}")
						print("+-----------------------------------------------------")

				elif select == "list whois":
					if whois == False:
						print("| SCAN NÃO REALIZADO")
					else:
						print("+--------------------- | WHOIS | ---------------------")
						print(whois)
						print("+-----------------------------------------------------")
				elif select == "exit":
					break






