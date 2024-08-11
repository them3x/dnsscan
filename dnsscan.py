import dnsclass
import dnsmenu
import sys, os


help = f"""MANUAL DNSSCAN
-----
+ Brute force subdominio e verificação CNAME
python3 {sys.argv[0]} [dominio] [wordlist]

+ Menu interativo
python3 {sys.argv[0]} menu
-----
"""

inicio = dnsmenu.Menu
inicio(False)

if len(sys.argv) == 1:
	print(help)
	exit(0)

if sys.argv[1] == "menu":
	inicio.menu()

else:
	try:
		dominio = sys.argv[1]
		wordlist = sys.argv[2]

		if os.path.isfile(wordlist) == False:
			print(f"Wordlist {wordlist} não foi encontrada!")
			exit(0)

	except IndexError:
		print("É precisso definir uma wordlist")
		exit(0)


	print("+----------------")
	print(f"| DOMINIO:  {dominio}\n| WORDLIST: ", end="")
	print(wordlist.split("/")[-1] if "/" in wordlist else wordlist)
	print("+----------------")

	inicio(dominio)
	dns = dnsclass.Dnsscan

	dns.whois(dominio)
	dns.subdomainBF(dominio, wordlist)
	dns.cnameckeck(dominio, wordlist)

	inicio.menu()
