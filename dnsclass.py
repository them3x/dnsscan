import socket
import json
import dns.resolver
import time

class Dnsscan:
	def whois(dominio):
		def openSocket(d, data):
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((d, 43))
			s.send(data.encode())
			return s

		d = dominio + "\r\n"

		s = openSocket("whois.iana.org", d)
		whois1 = s.recv(1024).decode().split("refer:        ")[1].split("\n")[0]
		s.close()

		s = openSocket(whois1, d)
		whois2 = s.recv(1024).decode().split("Registrar WHOIS Server: ")[1].split("\r")[0]
		s.close()

		s = openSocket(whois2, d)

		resposta = ""
		while True:
			data = s.recv(8024)
			if data:
				resposta += data.decode()
			else:
				break


		with open(f"scans/{dominio}/{dominio}.whois", "w") as f:
			f.write(resposta)

		print("+-----------------------------------------------------")
		print("| WHOIS salvo em scan/{dominio}/{dominio}.whois")
		print("+-----------------------------------------------------")

	def cnameckeck(dominio, wlist):
		cname_dict = {}

		print("+-----------------------------------------------------\n|   subdominio          |          registro CNAME\n+-----------------------------------------------------")
		with open(wlist) as f:
			for i in f.readlines():
				try:
					i = i.replace("\n", "")
					subdominio = f"{i}.{dominio}"

					while True:
						try:
							resposta = dns.resolver.resolve(subdominio, "CNAME")
							cname = resposta[0].target
							cname_dict[subdominio] = str(cname)

							print (f"| {subdominio:<30} {cname}")
							break

						except dns.resolver.NoAnswer:
							break
						except dns.resolver.NXDOMAIN:
							break
						except dns.resolver.LifetimeTimeout:
							print ("CAIU NO TIMEOUT CNAME")
							time.sleep(2)
				except KeyboardInterrupt:
					print("\nAVISO: Se parar a execução o registro JSON não sera criado")
					s = input("Deseja parar o scan ? [N/s]").lower()
					if s == "s":
						exit(0)

		cname_json = json.dumps(cname_dict)
		with open(f"scans/{dominio}/{dominio}-cname.json", "w") as f:
			f.write(cname_json)

		print("+-----------------------------------------------------")
		print(f"| Scan salvo em scan/{dominio}/{dominio}-cname.json")
		print("+-----------------------------------------------------")

	def subdomainBF(dominio, wlist):

		def DNSipv6(dominio_montado):
			try:
				dados = socket.getaddrinfo(dominio_montado, None, socket.AF_INET6)
				addr = dados[2][4][0]
				print(f"| {dominio_montado:<30} {addr}")

				return addr

			except socket.gaierror:
				return 0

		def DNSipv4(dominio_montado):
			try:
				dados = socket.getaddrinfo(dominio_montado, None, socket.AF_INET)
				addr = dados[2][4][0]
				print(f"| {dominio_montado:<30} {addr}")

				return addr
			except socket.gaierror:
				return 0

		consultado = []
		dominios6 = {}
		dominios4 = {}
		dominios = {}

		print("+-----------------------------------------------------\n|   subdominio          |          endereço IP\n+-----------------------------------------------------")
		with open(wlist) as wordlist:
			for i in wordlist.readlines():
				try:
					i = i.replace("\n", "")
					dominio_montado = f"{i}.{dominio}"

					if dominio_montado not in consultado:
						addr6 = DNSipv6(dominio_montado)
						addr4 = DNSipv4(dominio_montado)

						if addr6 != 0:
							dominios6[dominio_montado] = addr6

						if addr4 != 0:
							dominios4[dominio_montado] = addr4

						consultado.append(dominio_montado)
				except KeyboardInterrupt:
					print("\nAVISO: Se parar a execução o registro JSON não sera criado")
					s = input("Deseja parar o scan ? [N/s]").lower()
					if s == "s":
						exit(0)

		print("+-----------------------------------------------------")
		dominios["ipv4"] = dominios4
		dominios["ipv6"] = dominios6

		dominios_json = json.dumps(dominios)

		with open(f"scans/{dominio}/{dominio}-subdomains.json", "w") as f:
			f.write(dominios_json)

		print (f"| Scan salvo em scan/{dominio}/{dominio}-subdomains.json")
		print("+-----------------------------------------------------")

