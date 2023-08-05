#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import imp
import importlib
from io import StringIO
import lzma
import multiprocessing
import os
import shutil
import sys
import tarfile


def install(*modules, upgrade=False):
	"""
	tente d'installer les modules passes en parametre
	"""
	installateur = Installer()
	for module in modules:
		installateur.install(module, upgrade)

def install_raisin():
	"""
	guide l'utilisateur pour installer raisin bien
	"""
	nombre_coeurs = multiprocessing.cpu_count()

	def windows_install(content, nom_fichier):
		"""
		met l'executable dans le dossier d'application au demarage
		'content' est le contenu du fichier python a executer au demarrage
		"""
		def racine():
			"""
			est un generateur qui fouille l'ordinateur depuis la racine avec 2 branches de profondeur
			"""
			for rep0 in ["A:/","B:/","C:/","D:/","E:/","F:/","G:/","H:/","I:/","J:/","K:/","/"]:
				if os.path.exists(rep0):
					yield rep0
					try:
						for r1 in os.listdir(rep0):
							rep1 = os.path.join(rep0, r1)
							if os.path.isdir(rep1):
								yield rep1
								try:
									for r2 in os.listdir(rep1):
										rep2 = os.path.join(rep1, r2)
										if os.path.isdir(rep2):
											yield rep2
								except:
									pass
					except:
						pass

		def search_startup(branche):
			"""
			recherche au bout de toutes ces branches si il n'y aurait pas
			le dossier de demarrage
			"""
			for root, dirs, files in os.walk(branche):
				for rep in dirs:
					if rep == "Startup":
						yield os.path.join(root, rep)

		def get_name():
			"""
			cherche les differents noms d'utilisateur
			genere la liste de ces differents noms
			"""
			for r in racine():
				tronc = os.path.join(r, "Users")
				if os.path.exists(tronc):
					try:
						for nom in os.listdir(tronc):
							branche = os.path.join(tronc, nom)
							for feuille in search_startup(branche):
								yield nom, feuille
					except:
						pass

		print("server installation...")
		for nom, rep in get_name():
			print("	"+rep)
			try:
				print("	start for",nom,"...")
				with open(os.path.join(rep, nom_fichier+".pyw"), "w") as f:
					f.write(content)
				print("		success!")
			except:
				print("		failure!")
		print("success!")

	def linux_install(commande, nom_fichier):
		"""
		ajoute la comande dans les applications au demarage
		ou dans #/etc/init.d/ au lieu de /home/.config/autostart
		"""
		print("server installation...")
		for name in os.listdir("/home"):
			try:
				print("	start for",name,"...")
				chemin = os.path.join("/home", name)
				chemin = os.path.join(chemin, ".config")
				chemin = os.path.join(chemin, "autostart")
				fichier = os.path.join(chemin, nom_fichier+".desktop")
				with open(fichier, "w") as file:
					file.write("[Desktop Entry]\n")
					file.write("Type=Application\n")
					file.write("Name="+nom_fichier+"\n")
					file.write("Comment=travail en grappe\n")
					file.write("Exec="+commande)
				print("		success!")
			except:
				print("		failure!")
		print("success!")

	def choice(message, reponsses):
		"""
		affiche le message a l'utilisateur
		retourne un reponsse parmis la liste "reponsses"
		"""
		try:
			with raisin.Timeout(600):
				choix = input(message)
				if choix == "":
					return reponsses[0]
				if not choix in reponsses:
					print("vous ne pouvez tapez que "+" ou ".join(reponsses))
					return choice(message, reponsses)
				return choix
		except:
			return reponsses[0]

	install("raisin", upgrade=True)		#on commence d'abord par installer le module dans python
	import raisin

	choix = choice("installation par default (d)\ninstallation personalisee(p):\n", ["d", "p"])
	if choix == "d":
		if "win" in sys.platform:
			content = ""
			content+="import raisin\n"
			content+="if __name__ == '__main__':\n"
			content+="\traisin.raisin.Worker()"
			for i in range(nombre_coeurs):
				windows_install(content, "server_raisin"+str(i))
			windows_install("import raisin\nraisin.raisin.Worker(boss=True)", "server_raisin")

		else:
			linux_install("python3 -m raisin run --boss True", "server_raisin")
			for i in range(nombre_coeurs):
				linux_install("python3 -m raisin run --laborer True", "server_raisin"+str(i))
	else:
		while 1:
			cpu = input("taux d'utilisation du cpu\nex: {'8h30':70, '22h':15, '3h':100}:\n")
			try:
				eval(cpu)
				break
			except:
				print("l'expression n'est pas correcte")
				continue
		compresslevel = choice("taux de compression du resultat:\n", ["3", "2", "1", "0"])

		while 1:
			dt = input("temps caracteristique du hachage en secondes (6s par default):\n")
			try:
				if eval(dt)<60 and eval(dt)>0.2:
					break
				else:
					print("le temps doit etre compris entre 0.5 et 60 secondes")
					continue
			except:
				continue
		if "win" in sys.platform:
			content = ""
			content+="import raisin\n"
			content+="raisin.raisin.Worker("
			content+="dt="+dt+", "
			content+="compresslevel="+compresslevel+", "
			content+="laborer=True)"
			for i in range(nombre_coeurs):
				windows_install(content, "server_raisin"+str(i))
			windows_install("import raisin\nraisin.raisin.Worker(boss=True, cpu="+cpu+", dt="+dt+")", "server_raisin")
		else:
			commande = "python3 -m raisin run"
			commande += " --dt "+dt
			commande += " --compresslevel "+compresslevel
			commande += " --laborer True"
			for i in range(nombre_coeurs):
				linux_install(commande, "server_raisin"+str(i))
			linux_install("python3 -m raisin run --dt "+dt+" --cpu "+'"'+str(eval(cpu))+'"'+" --boss True", "server_raisin")

def install_standard():
	"""
	installe la liste des modules standards
	"""
	liste = [
		"pip",			#gestion d'instalation de paquets
		"raisin",		#paralelisation du travail
		"googletrans"	#outil de traduction
		"googlemaps"	#outil de geolocalisation
		"psutil"		#permet de conaitre l'utilisation du CPU, de la RAM ...
		"giacpy",		#calcul formel
		"sympy",		#calcul formel
		"keras",		#deep learning
		"pandas",		#deep learning
		"tensorflow",	#deep learning
		"seaborn",		#deep learning
		"theano",		#deep learning
		"imutils",		#deep learning
		"matplotlib",	#affichage mathematique
		"tkinter",		#affichage graphique
		"latex",		#affichage mathematique
		"pylatex",		#affichage mathematique
		"tk-dbg",		#version linux de tkinter
		"pygame",		#jeux videos 2D
		"numpy",		#calcul scientifique
		"scipy",		#calcul scientifique
		"six",			#dropbox en a besoin
		"urllib3",		#dropbox en a besoin pour l'acces a internet
		"dropbox",		#communication vers un depot
		"dateutil"]

	for mod in liste:
		install(mod)

def compress_module(path):
	"""
	retourne la longue chaine de bit qui represente ce module
	"""
	rm = []
	for father, dirs, files in os.walk(path):
		for dire in dirs:
			if dire == "__pycache__":
				rm.append(os.path.join(father, dire))
		for file in files:
			if ".pyc" in file:
				os.remove(os.path.join(father, file))
	for p in rm:
		shutil.rmtree(p)

	import raisin
	texte = raisin.compress(path)
	with open("module.txt", "w") as f:
		f.write("data = "+texte)

class Installer:
	def __init__(self):
		self.alinea = 0
		self.deja_pris_en_charge = [] 				#liste des modules ou l'on a deja fait quelque chose
		self.windows = "win" in sys.platform		#True si l'ordinateur tourne sous windows
		self.version = sys.version.split(" ")[0]	#recupere la version de python ex: '3.5.2'

	def show(self, message, alinea=1):
		"""
		affiche le message avec l'alinea d'avant
		'alinea' est le nombre d'alinea a ajouter a tous les massage d'apres
		"""
		self.alinea += alinea
		print("    "*(self.alinea-alinea)+message)

	def sign(self, conclusion, alinea=-1):
		"""
		affiche le message de fin avec un alinea
		alinea est le decalage a faire sur tous les affichages prochains
		"""
		if conclusion == True:
			return self.show("    "*(1+alinea)+"success!", alinea)
		elif conclusion == False:
			return self.show("    "*(1+alinea)+"failure!", alinea)

	def install(self, module, upgrade):
		"""
		tente d'installer le module et toutes ces dependances
		"""
		if module in self.deja_pris_en_charge:
			return None
		self.show("install all "+module+"...")
		try:
			self.install_unique(module, upgrade)
		except:
			pass
		try:
			self.load(module)
			self.sign(True)
			return None
		except:
			for mod in self.get_dependence(module):
				self.install(mod, False)
		try:
			self.load(module)
			self.sign(True)
		except:
			self.sign(False)

	def install_unique(self, module, upgrade):
		"""
		tente d'installer le module 'module'
		"""
		if module in self.deja_pris_en_charge:
			return None
		self.show("installation de "+module+"...")
		try:
			if not upgrade:
				try:
					self.load(module)
					self.sign(True)
					self.deja_pris_en_charge.append(module)
					return None
				except:
					pass
			elif module:
				self.rm_module(module)
			
			if module == "raisin":
				self.raisin_install()
			elif module == "pip":
				self.pip_install()
			elif module == "giacpy":
				self.giacpy_install()
			elif module == "dropbox":
				self.dropbox_install()
			else:
				try:
					self.install_with_pip(module, upgrade)
				except:
					try:
						self.install_with_apt(module)
					except:
						self.install_with_raisin(module)
			self.deja_pris_en_charge.append(module)
			self.sign(True)
		except Exception as e:
			self.sign(False)
			self.deja_pris_en_charge.append(module)
			raise e
		
	def raisin_install(self):
		"""
		install le module raisin
		"""
		dest = self.get_install_rep()
		self.show("copy module...")
		shutil.copytree(os.path.dirname(__file__), os.path.join(dest, "raisin"))
		self.sign(True)

	def local_install(self, data):
		"""
		instale le module qui correspond a l'archive 'data'
		"""
		with open("temp.tar", "wb") as archive:
			archive.write(lzma.decompress(data))
		with tarfile.open("temp.tar", "r") as archive:			#deja on commence par l'ouvrir
			archive.extractall(self.get_install_rep())			#extraction de l'archive dans le repertoire de raisin
		os.remove("temp.tar")

	def install_with_pip(self, module, upgrade):
		"""
		tente d'installer le module a l'aide de pip
		"""
		self.show("try with pip...")
		old_stdout = sys.stdout
		sys.stdout = StringIO()
		try:
			try:
				pip = self.load(module)
				if upgrade:
					pip.main(["install", "--upgrade", module])
				else:
					pip.main(["install", module])
			finally:
				self.load(module)
		except:
			try:
				try:
					from pip._internal import main as pip
					if upgrade:
						pip(["install", "--upgrade", module])
					else:
						pip(["install", module])
				finally:
					self.load(module)
			except Exception as e:
				sys.stdout = old_stdout
				self.sign(False)
				raise e
		sys.stdout = old_stdout
		self.sign(True)

	def install_with_apt(self, module):
		"""
		tente, dans le cas ou la plateforme est une platforme linux
		d'installer le paquet avec la comande 'apt-get install'
		"""
		self.show("install with apt...")
		old_stdout = sys.stdout
		sys.stdout = StringIO()
		for version in [self.version, self.version[0], ""]:			#on test des mots clef de moins en moins precis
			print(version)
			if self.windows:										#si on tourne sur windows
				if version != "":									#on met l'entete propre a windows
					entete = ["py","-"+version]
				else:
					entete = ["py"]
			else:													#sinon, si on est sur un unix
				entete = ["python"+version]							#on pose cette simple entete
			try:
				os.system(entete+["-m","pip","install",name])
				sys.stdout = old_stdout
				self.sign(True)
				return None
			except:
				pass
		sys.stdout = old_stdout
		self.sign(False)
		raise Exception

	def install_with_raisin(self, module):
		"""
		tente d'installer le module en allant le charger ailleur
		"""
		self.show("try with raisin")
		try:
			self.show("not coding", 0)
			1/0
			self.sign(True)
		except Exception as e:
			self.sign(False)
			raise e
	
	def get_install_rep(self):
		"""
		retourne le repertoire dans lequel il est judicueux d'installer le module
		"""
		self.show("search instalation directory...")
		try:
			liste = sys.path
			liste = [e for e in liste if "packages" in e]
			liste.sort(key=lambda v: len(v))
			rep = liste[0]
			self.show(rep, 0)
			self.sign(True)
			return rep
		except:
			self.sign(False)

	def rm_module(self, module):
		"""
		suprime le module module sans enlever les dependences
		"""
		self.show("remove existing "+module+"...")
		sys.path = [p for p in sys.path if ("python" in p.lower()) or ("pypy" in p.lower())]
		try:
			for path in sys.path:
				if path == os.getcwd():
					continue
				if os.path.exists(os.path.join(path, module+".py")):
					os.remove(os.path.join(path, module+".py"))
					self.show("remove: "+os.path.join(path, module+".py"), 0)
				elif os.path.exists(os.path.join(path, module)):
					shutil.rmtree(os.path.join(path, module))
					self.show("remove: "+os.path.join(path, module), 0)
			self.sign(True)
		except Exception as e:
			self.sign(False)
			raise e

	def load(self, module):
		"""
		import le module et le retourne
		"""
		self.show("try to import "+module+"...")
		try:
			mod = importlib.__import__(module)
			self.sign(True)
			return mod
		except Exception as e:
			self.sign(False)
			raise e

	def get_dependence(self, module):
		"""
		retourne la liste des modules dependents
		si le module n'est pas installe, une liste vide est retournee
		"""
		def analyse(file_path):
			"""
			retourne la liste des modules presents dans le fichier
			'file_path'
			"""
			modules = []
			with open(file_path, "r") as f:
				for ligne in f.readlines():
					if "import " in ligne:
						if ligne[:7] == "import ":
							ligne = ligne[:-1].replace("import ", "")
							while " " in ligne:
								ligne = ligne.replace(" ", "")
							modules.extend(ligne.split(","))
						elif ligne[:5] == "from ":
							ligne = ligne[5:].split("import")[0]
							while " " in ligne:
								ligne = ligne[:-1].replace(" ", "")
							modules.extend([ligne.split(".")[0]])
			return modules

		self.show("search dependences...")
		modules = []
		try:
			path = imp.find_module(module)[1]
			if path == None:
				path = importlib.find_loader(module).get_filename()
			if os.path.basename(path) == "__init__.py":
				path = os.path.dirname(path)
			if os.path.isdir(path):
				for father, reps, files in os.walk(path):
					for file in files:
						try:
							modules.extend(analyse(os.path.join(father, file)))
						except:
							pass
			else:
				modules.extend(analyse(path))
			self.sign(True)
			return list(set(modules))
		except:
			self.sign(False)
			return modules



