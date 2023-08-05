#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#----------raisin: travail en grappe!----------


#pour agir en tant que client pour aider la comunautee:
#
#code simple:
#
#	import raisin
#	raisin.Server()
#
#code plus precis:
#	import raisin
#	c = raisin.Server(image="dropbox",
#		code="iLBBfZeySgAAAAAAAAAADuDdmpArERX2s_UwuulUAOMNDLjDh6MzzL9NVDUp3P7x",
#		cpu=50, dt=10, display=True)													#pourcentage maximum de cpu admisible pour faire une requette
#pour le cpu, on peut utiliser un dictionaire pour faire un taux de cpu variable
#ex cpu={"12h":50,"13h15":80}	met le cpu a 50% entre 12h et 13h15 et a 80% le reste du temps



#pour se faire aider des autres:
#
#def fonction(x,y):
#	return x**2+y**2
#
#code simple:
#	import raisin
#	if __name__ == '__main__':									#important pour pouvoir utiliser les perfs de la machine
#		print(raisin.Session().Process(f, 3, 0).get(wait=True))	#affiche 9
#
#code plus pousse:
#
#	import raisin
#	if __name__ == '__main__':									#permet d'eviter des boucles infinies
#		sess = raisin.Session(image="dropbox", code="iLBBfZeySgAAAAAAAAAADuDdmpArERX2s_UwuulUAOMNDLjDh6MzzL9NVDUp3P7x", display=True)
#		res1 = sess.Process(fonction, 4, 3)
#		res2 = sess.Process(fonction, 5, 7)
#		while 1:
#			time.sleep(60)										#on fait une pause d'une minute a chaque fois
#			print(res1.get_all(), res2.get_all())				#on verifie si il y a un resultat et on recupere par la meme occasion toutes les informations complementaires
#ou bien avec la methode 'map':
#
#	import raisin
#	if __name__ == '__main__':
#		sess = raisin.Session(image="dropbox", code="iLBBfZeySgAAAAAAAAAADuDdmpArERX2s_UwuulUAOMNDLjDh6MzzL9NVDUp3P7x", display=True)
#		res = sess.map(fonction, range(5), [1,2,4,6,3])
#		while 1:
#			time.sleep(60)
#			print(res.get(wait=False))							#affiche [1,5,None,45,None]


#pour ajouter un autre type de serveur:
#	creer un nouvel objet qui a pour argument 'father'
#	Le nom de l'objet commence par une MAJUSCULE et continue avec des minuscules
#	il a pour methode:
#		connect(code): retourne 0 si la connection au serveur a fonctionnee
#		send(obj, name): poste l'objet 'obj' sous le nom 'name', retourne 0 en cas de reussite
#		load(name): retourne l'objet de nom 'name' ou retourne None en cas d'echec
#		remove(name): supprime le fichier de nom 'name', retourne 0 en cas de reussite
#		ls(): retourne la liste de tous les dossiers presents dans le serveur, retourne [] en cas de probleme
#	ajouter l'appel de ce nouvel objet:
#		dans Connecter(), dans la methode serveur_request(), ajouter:
#		if image == 'nom tout en minuscule du nouveau serveur':
#			return Nouvel_objet(self.father)

__version__ = "1.1.0"
__all__ = ["Session", "Server", "Upgrade", "Install"]
__author__ = "Robin RICHARD <serveurpython.oz@gmail.com>"

import datetime
import raisin.dropbox as dropbox
import inspect
import multiprocessing
import os
import pickle
import shutil
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import urllib

#liens vers les differents types de serveurs

class Dropbox(object):
	"""
	lien vers dropbox
	pour la creation d'une api, executer les lignes de comandes suivantes:
		cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf -
		~/.dropbox-dist/dropboxd
	"""
	def __init__(self, father):
		self.father = father													#objet qui appel celui-ci il a au moin pour methode show() et sign()

	def connect(self, access_token):
		"""
		tente d'etablire une connection avec le serveur
		tous va se passer a la racine: '/'
		"""
		self.father.show("connection to dropbox...")
		if 1:
			self.dbx = dropbox.Dropbox(access_token)
			self.dbx.users_get_current_account()								#releve les informations du compte pour etre certain que la connection est bonne
			self.father.sign(True)
			return 0
		else:
			self.father.sign(False)
			return 1

	def send(self, object, name):
		"""
		serialise l'objet 'object' et le met dans '/name'
		'name' est donc le nom du fichier dans drop box
		retourne 0 en cas de reussite et 1 en cas d'erreur
		"""
		self.father.show("sending python object...")
		try:
			self.dbx.files_upload(pickle.dumps(object, protocol=2), os.path.join("/",name))
			self.father.sign(True)
			return 0
		except:
			self.father.sign(False)
			return 1

	def load(self, name):
		"""
		deserialise l'objet '/name'
		'name' est donc le nom du fichier sur dropbox
		retourne l'objet en cas de reussite
		retourne None en cas d'erreur
		"""
		self.father.show("loading "+name+"...")
		try:
			obj = pickle.loads(self.dbx.files_download(os.path.join("/",name))[1].content)
			self.father.sign(True)
			return obj
		except:
			self.father.sign(False)
			return None

	def remove(self, name):
		"""
		supprime le fichier '/name'
		'name' est donc le nom du fichier dans dropbox
		"""
		self.father.show("deleted "+name+"...")
		try:
			self.dbx.files_delete(os.path.join("/", name))
			self.father.sign(True)
			return 0
		except:
			self.father.sign(False)
			return 1

	def ls(self):
		"""
		retourne la liste de tous les dossier present sur dropbox
		quelqu'en soit leur nature
		"""
		try:
			return [e.name for e in self.dbx.files_list_folder("").entries]
		except:
			return []

class Local(object):
	"""
	lien avec un disque dur phisique
	"""
	def __init__(self, father):
		self.father = father													#objet qui appel celui-ci il a au moin pour methode show() et sign()

	def connect(self, emplacement):
		"""
		etablie un connection vers l'emplacement passe en parametre
		'emplacement' pointe vers un dossier accessible par les autres
		"""
		self.father.show("connection to "+emplacement+"...")
		if os.path.exists(emplacement):
			self.emplacement = emplacement
			self.father.sign(True)
			return 0
		self.father.sign(False)
		return 1

	def send(self, object, name):
		"""
		serialise l'objet 'object' et le met dans 'self.emplacement/name'
		'name' est donc le nom du fichier
		retourne 0 en cas de reussite et 1 en cas d'erreur
		"""
		self.father.show("sending python object...")
		try:
			with open(os.path.join(self.emplacement, name), "wb") as f:
				f.write(pickle.dumps(object, protocol=2))
			self.father.sign(True)
			return 0
		except:
			self.father.sign(False)
			return 1

	def load(self, name):
		"""
		deserialise l'objet 'self.emplacement/name'
		'name' est donc le nom de l'objet
		retourne dans la meusure du possible, l'objet deserialise
		retourne None en cas d'echec
		"""
		self.father.show("loading "+name+"...")
		try:
			with open(os.path.join(self.emplacement, name), "rb") as f:
				obj = pickle.loads(f.read())
			self.father.sign(True)
			return obj
		except:
			self.father.sign(False)
			return None

	def remove(self, name):
		"""
		supprime le fichier de nom 'name'
		retourne 0 en cas de reussite et 1 en cas d'erreur
		"""
		self.father.show("deleted "+name+"...")
		try:
			os.remove(os.path.join(self.emplacement, name))
			self.father.sign(True)
			return 0
		except:
			self.father.sign(False)
			return 1

	def ls(self):
		"""
		retourne la liste de tous les fichiers, de tous types
		"""
		try:
			return os.listdir(self.emplacement)
		except:
			return []

#exploitation de ces liens

class Connecter(object):
	"""
	etablie les connections avec les serveurs
	gere le fichier 'image_code.pk'
	"""
	def __init__(self, father, image=None, code=None):
		self.start = False														#reste False tant qu'il n'y a pas eu d'interaction avec 'image_code.pk'
		self.rang = 0															#position actuelle dans la liste 'image_code'
		self.image_code = []													#recence tous les potentiel serveurs [(derniere activite, image, code) , ...]
		self.father = father													#objet qui cree cet objet, doit posseder les methodes show() et sign()
		self.image = image														#image du serveur (nom du serveur en minuscule)
		self.code = code														#code qui permet de se connecter au serveur 'image' (facultatif)
		self.server = None														#objet serveur au quel on se connecte
		self.file = "image_code.pk"												#emplacement du fichier 'image_code.pk'

	def server_request(self, image):
		"""
		c'est ici que la modification doit etre faite pour ajouter un serveur
		retourne le serveur correspondant a image
		retourne None si image ne correspond a rien de connu
		"""
		if image == "dropbox":
			return Dropbox(self.father)
		if image == "local":
			return Local(self.father)

		return None

	def search_server(self):
		"""
		retroune la liste des serveurs potentiel
		la liste est triee par pertinance
		cre la variable self.image_code
		se sert du fichier 'image_code.pk'
		le fichier est un liste qui contient les tuples suivants: (date_derniere_activitee, image, code)
		"""
		self.father.show("looking for valid server...")

		#verification du fichier 'image_code.pk'
		if not(os.path.exists(self.file)):
			with open(self.file, "wb") as f:
				pickle.dump([], f, protocol=2)

		#extraction des donnees
		try:
			with open(self.file, "rb") as f:									#on ouvre le fichier 'image_code.pk'
				image_code = (pickle.load(f))									#on en profite pour supprimer les doublons
			image_code = sorted(image_code, key=lambda x: x[0], reverse=True)	#tri selon la date d'acces, du plus recent au plus encien
		except:
			os.remove(self.file)												#si le fichier est casse, on abrege ces souffrances
			self.father.sign(False)
			return self.search_server()											#on repart a neuf

		#tri en pertinance selon les parametres
		if self.image == None:
			im = "dropbox"
		else:
			im = self.image
		image_code = [i for i in image_code if i[1] == im]+[i for i in image_code if i[1] != im]#on met en priorite les serveurs le plus proches de la demande

		#restitution du travail
		if (self.code == None):
			self.image_code = [c for c in image_code]
		else:
			self.image_code = [(0, self.image, self.code)]+image_code.copy()
		self.father.sign(True)
		return self.image_code

	def connect(self, first=False, all_server=True):
		"""
		retourne l'objet un serveur connecte
		c'est a dire ou l'appelle de la methode 'connect' a retourne un resultat favorable
		si on est deja connecte, on se deconnecte et on continue de
		parcourir la liste pour se connecter a autre chose
		'first' est True si l'on shouaite seulement se connecter au premier de la liste
		'all' est True si on autorise tous les types de serveurs
			est donc False si onne tente de se connecter qu'au serveur definit dans __init__()
			'first' est prioritaire sur 'all'
		"""
		if self.start == False:													#si c'est la premiere fois que l'on appele cette methode
			self.image_code = self.search_server()								#on preleve les donnees
			self.start = True													#on fait en sorte que cela ne se produise qu'une seule fois

		#test preliminaire
		if self.image_code == []:												#si l'on ne connait absolument aucun serveur
			return None															#on ne tente pas le diable

		#parametrage de la connection
		if first == True:														#si l'on doit seulement tester le premier de la liste
			self.rang = -1														#on se place au dernier element
			facteur = 0															#affin que celui d'apres soit le premier
			somme = 1															#on ne fait qu'un tour de boucle
		else:																	#si on doit tout parcourir
			facteur = 1															#on fait autant d'iterations que d'elements dans la liste
			somme = 0															#on comence par le suivant

		#connection
		for j in range(facteur*len(self.image_code)+somme):						#on fait au plus un tour de liste
			i = (j+self.rang+1)%len(self.image_code)							#on se place au bon endroit de la liste
			date, image, code = self.image_code[i]								#recuperation des informations pour pouvoir se connecter
			if (image == self.image) or all_server:								#si l'on ne doit pas chercher sur ce serveur, on passe au suivant
				server = self.server_request(image)								#on va faire appelle au bon serveur
				if server != None:												#si un serveur a bien ete appele
					if server.connect(code) == 0:								#on tente de s'y connecter
						self.server = server									#on enregistre ce serveur
						return self.server										#au quel cas, on s'arrete la!
		self.server = None														#sin on a rien trouve, on se souvient du fait que rein ne fonctionne
		return None																#on reste sur ce pc

	def clean(self):
		"""
		permet de faire du menage dans le serveur
		supprime les vieux fichiers
		et met a jour 'code_image.pk'
		a appeler apres s'etre conneter a un serveur
		ne retourne rien
		"""
		self.father.show("clean the server...")

		#test preliminaires
		if self.server == None:
			self.father.sign(False)
			return None

		#suppresion des fichiers de gerusalem
		for file in self.server.ls():											#on regarde chaque fichier
			if (file[0]=="w" and file[1:].isdigit()) or (file.isdigit()):		#si il s'agit d'un travail ou d'un resultat
				try:															#on tente de le regarder plus en profondeur
					if time.time() > self.server.load(file)["sending_date"]+(3600*24*7):#si il a ete poste il y a plus d'une semaine
						self.server.remove(file)								#le fichier est supprime
				except:															#si le serveur merdoit
					pass														#ce n'est pas bien grave, on passe a la suite

		#recuperation des differents serveurs
		try:																	#on va tenter d'ouvrir le fichier qui contient les infos sur les differents serveurs
			nouveau_image_code = self.server.load("info")						#extration des nouveau codes et serveurs
			if nouveau_image_code == None:										#seulement dans le cas ou cela fonctionne
				nouveau_image_code = []
			self.image_code = self.update_image_code(nouveau_image_code)		#ajout a cela de nos informations
		except:
			pass

		self.father.sign(True)
		return None

	def update_image_code(self, new):
		"""
		ajoute au fichiers 'image_code.pk'
		les nouvelle informations presentes dans 'new'
		poste le fichier mis a jour dans le serveur actuel
		retourne la liste de touts les images et les codes
		triee par pertinance
		'new' est donc une liste de tuple a 3 elements
		"""
		self.father.show("update the dataset of servers...")

		try:
			dico = {}															#dictionaire dans lequel on va peu a peu ajouter les serveurs
			for date, image, code in (new+self.image_code):						#on parcours toutes les donnees que l'on a
				dico[(image, code)] = max(dico.get((image, code), date), date)	#on evite les doublons et on garde la plus recente visite
			self.image_code = [(dico[(image, code)], image, code) for image, code in dico.keys()]#on met tout a plat dans une liste
			self.server.remove("info")											#on remplace l'encien fichier present sur le serveur
			self.server.send(self.image_code, "info")							#par le nouveau
			with open(self.file, "wb") as f:									#de meme
				pickle.dump(self.image_code, f, protocol=2)						#on enregistre localement ces nouvelle infos pour le prochain demarage
			self.image_code = self.search_server()								#on les telecharges et on les tri par odre de pertinance
			self.father.sign(True)
		except:
			self.father.sign(False)
		return self.image_code

	def update_date(self):
		"""
		met a jour la date de dernier acces au serveur actuellement connecter
		"""
		self.image_code[self.rang] = (time.time(), self.image_code[self.rang][1], self.image_code[self.rang][2])#juste une mise a jour de la date
		return None

#mise en place de tout l'environement necessaire

class Session(object):
	"""
	donne du travail aux autres
	et se charge de recuperer les resultats
	"""
	def __init__(self, image=None, code=None, display=True, alinea=0):
		self.display = display													#permet d'afficher ou non, les operations en cours
		self.alinea = alinea													#c'est le nombre d'alinea a faire en affichant le message
		self.image = image														#None: sur la machine / local: sur un disque / dropbox: sur dropbox
		self.code = code														#code pour acceder au serveur
		self.show("session starting...")
		self.permis = self.get_permis()											#on recherche un repertoire ou l'on a les droits d'ecriture et on l'ajoute au sys.path
		os.chdir(self.permis)													#on en fait le repertoire courant
		self.connecter_base()													#on se connecte a la base de donnee qui contient les resultats elle a pour nom 'raisin_resultats.db'
		self.connecter = Connecter(self, self.image, self.code)					#creation d'un lien vers un serveur
		self.server = self.connecter.connect((image!=None and code!=None), (image==None))#connection a un serveur de methodes send(), load() et remove()
		self.id = self.get_id()													#on recupere l'adresse de ce pc
		if not "win" in sys.platform:
			self.pool = multiprocessing.Pool()
		else:
			self.pool = None
		self.sign(True)

	def show(self, message="", alinea=1, s=0):
		"""
		affiche le message avec l'alinea d'avant
		'alinea' est le nombre d'alinea a ajouter a tous les massage d'apres
		"""
		if self.display is True:												#si l'utilisateur donne une consigne generale
			self.display = 5													#on fixe le parametre par defaut
		elif self.display == False:												#si il ne faut rien afficher
			self.display = 0													#on traduit la demande en langage mathematique
		if type(self.display) != int:											#petites verification sur le typage
			raise TypeError("'display' must be an integer")						#de la variable 'self.display' pour eviter les mauvaises surprises
		if type(alinea) != int:													#verification des erreurs
			raise TypeError("'alinea' must be an integer")						#on retourne le message d'erreur
		self.alinea += alinea													#memorisation de l'alinea pour la suite du programme
		if self.display >= self.alinea+s:										#si il y a quelque chose a afficher
			print("    "*(self.alinea-alinea)+message)							#affichage du message
			return True															#comme d'abitude, on retourne True quand cela se passe bien
		return False															#et False quand il y a un quoique

	def sign(self, conclusion, alinea=-1):
		"""
		affiche le message de fin avec un alinea
		alinea est le decalage a faire sur tous les affichages prochains
		"""
		if conclusion == True:
			return self.show("    "*(1+alinea)+"success!", alinea, 1)
		elif conclusion == False:
			return self.show("    "*(1+alinea)+"failure!", alinea, 1)
		elif type(conclusion) == str:
			return self.show("    "*(1+alinea)+conclusion, alinea, 1)
		raise TypeError("'conclusion must be a boolean or a string")

	def get_permis(self):
		"""
		farfouille dans l'ordinateur jusqu'a trouver un endroit
		ou l'on a les droits d'ecriture
		"""
		def test(rep):
			"""
			retourne True si le repertoire est accessible
			retourne False dans le cas contraire
			"""
			try:
				with open(os.path.join(rep,"temp.txt"),"w") as f:
					f.write("test d'acces en ecriture")
				os.remove(os.path.join(rep,"temp.txt"))
				return True
			except:
				return False

		self.show("searching writing directory...")
		montage = [os.path.dirname(__file__),os.getcwd(),"/home","/mnt","H:/","G:/","F:/","E:/","D:/","C:/","B:/","A:/"]
		while 1:
			for rep in montage:
				if os.path.exists(rep):
					try:
						for father, reps, file in os.walk(rep):
							if test(father):
								sys.path.append(father)
								self.show(father,0)
								self.sign(True)
								return father
					except:
						pass

	def connecter_base(self):
		"""
		cree ou verifie l'existance d'une base de donnee
		cette base de donnee contient dans la table 'table_resultats', les colones suivantes:
		-id, INT:				numero de la ligne
		-sending_date, INT:		date de creation de cette ligne
		-state, STR:			'wait', 'process', 'finish'
		-script, STR:			code a executer
		-last_support, INT:		date de la derniere tentative d'execution
		-result_id, STR:		identifiant du resultat a l'exterieur
		-timeout, INT:			temps d'execution maximum
		-res, BLOB:				resultat serialise avec pickle
		"""
		self.show("connection to dataset...")
		base = sqlite3.connect("raisin_resultats.db")							#on se connecte a la base de donnees
		curseur = base.cursor()													#afin de pouvoir faire une requette
		curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")	#on recupere le nom des tables qui compose cette base
		liste = curseur.fetchall()												#on execute la commande, c'est a dire qu'on lance la recherche
		base.close()															#la base peut etre fermee, il n'y en a plus besoin pour le moment
		if liste == [("table_resultats",)]:										#si il s'agit de la bonne base de donnee
			self.sign(True)
			return None															#on s'arrete la
		self.show("creation of dataset...")
		os.remove("raisin_resultats.db")										#on supprime la mauvaise base de donnees
		base = sqlite3.connect("raisin_resultats.db")							#affin d'en creer une vierge
		table_resultats = base.execute("""CREATE TABLE table_resultats
			(id INTEGER PRIMARY KEY,
			sending_date INT,
			state STR,
			script STR,
			last_support INT,
			result_id STR,
			timeout INT,
			res BLOB)""")
		base.close()															#on cre une table vide
		self.sign(True)
		self.sign(True)

	def get_target(self, target, args):
		"""
		fait une copie de la definition qui est appellee, ie: va lire ce que pointe le pointeur 'target'
		met en forme la definition et stocke le resultat dans la variable 'result'
		le resultat est recuperable via la methode 'get_resultat()'
		'target' est un pointeur vers une fonction
		'args' est un tuple qui correspond aux parametres de la fonction 'target'
		retourne la definition en str
		"""
		lignes = [l.replace("  ","\t") for l in [l.replace("   ","\t") for l in [l.replace("    ","\t") for l in inspect.getsourcelines(target)[0]]]]#on recupere toutes les lignes sous forme de chaine de caractere
		while lignes[0][0] == "\t":												#si toute la fonction est indentee
			lignes = [l[1:] for l in lignes]									#on lui retire les tabulations qu'elle a en trop
		entete = [l for l in lignes[0].replace(" ","\t").split("\t") if l!=""][1].split("(")[0]#recuperation du nom de la fonction
		lignes.append("def get_resultat():\n")									#ainsi, on donne un nom commun a toutes le fonctions
		for nom, val in zip(lignes[0].split("(")[1].split(")")[0].split(","),args):#on va faire en sorte que chaque
			while " " in nom:
				nom = nom.replace(" ","")
			lignes.append("\t"+nom+"=pickle.loads("+str(val)+")\n")				#parametres ne puisses pas etre interpretes de travers
		lignes.append("\treturn "+lignes[0].split("def ")[1].split(":")[0])		#ajout de la ligne d'appelle de la definition sans les :
		lignes = ["import pickle\n"]+lignes										#biensur, si on utilise un module, il faut l'importer
		variable = "".join(lignes)												#on reuni toutes le lignes de code dans une seule chaine de caractere
		return variable

	def get_args(self, args, serialise=False):
		"""
		met en forme le parametre d'entree pour qu'il soit sous la forme d'un tuple
		retourne ce tuple
		serialise chaqun des parametre si cela est specifie
		"""
		if serialise:
			return [pickle.dumps(arg, protocol=2) for arg in self.get_args(args)]
		argument = ()
		if type(args) == str:
			return (args,)
		if type(args) == dict:
			return (args,)
		try:
			for i in args:
				argument+=(i,)
		except:
			argument = (args,)
		return argument

	def Process(self, *args):
		"""
		retourne un objet qui a pour methode get() et get_all()
		pour recuperer le resultat
		args[0] est le pointeur de la definition a executer
		args[1:] est la liste des arguments que prend en parametre cette definition
		"""
		target = args[0]														#on recupere la cible
		args = args[1:]															#il s'agit des parametres variables a donner a la definition
		try:																	#si la cible est dans un programe ou un module, que ce n'est pas une fonction toute faite de python
			return self.Pooler_loin(target, self.get_args(args, serialise=True), self)#on tente dans un premier temps de l'envoyer au loin
		except:																	#si il y a un problème de reseau ou bien que le pointeur est trop inaxessible
			if self.pool != None:												#on execute le programme localement sur cet ordinateur
				return self.Pooler_cpu(target, self.get_args(args, serialise=False), self.pool, self)#on reparti la charge sur les differents coeurs si il est raisonable de le faire
			else:																#sinon on se contente de simuler un 'faux paralellisme'
				return self.Pooler_thread(target, self.get_args(args, serialise=False), self)#afin de rendre rapidement la main

	def map(self, *args):
		"""
		execute le travail plein de fois avec des arguments presents dans 'iter'
		retourne un objet de liste
		"""
		target = args[0]
		iterable = args[1:]

		class Mapper(object):
			"""
			contient les 2 methodes get et get_all
			"""
			def __init__(self, liste_res):
				self.liste_res = liste_res

			def get_all(self, wait=False):
				return [res.get_all(wait) for res in self.liste_res]

			def get(self, wait=False):
				return [res.get(wait) for res in self.liste_res]

			def len(self):
				"""
				retourne le nombre d'element de la liste
				"""
				return len(self.liste_res)

		return Mapper([self.Process(target, *args) for args in zip(*iterable)])

	def get_id(self):
		"""
		retourne l'identifiant propre a cette ordinateur
		en cas d'erreur, retourne un identifiant quelconque dependant du temps
		"""
		self.show("ip request...")

		identifiant = {}
		identifiant["hostname"] = socket.gethostname()
		identifiant["executable"] = sys.executable
		identifiant["country"] = None
		identifiant["city"] = None
		identifiant["longitude"] = None
		identifiant["latitude"] = None
		identifiant["ip"] = None

		try:
			try:
				1/0
				dic = eval(urllib.request.urlopen("http://freegeoip.net/json").read().decode())
			except:
				1/0
				dic = eval(urllib.urlopen("http://freegeoip.net/json").read().decode())
			identifiant["country"] = dic["country_code"]
			identifiant["city"] = dic["city"]
			identifiant["longitude"] = dic["longitude"]
			identifiant["latitude"] = dic["latitude"]
			identifiant["ip"] = dic["ip"]
		except:
			try:
				try:
					dic = eval(urllib.request.urlopen("http://ipinfo.io/json").read().decode())
				except:
					dic = eval(urllib.urlopen("http://ipinfo.io/json").read().decode())
				identifiant["country"] = dic["country"]
				identifiant["city"] = dic["city"]
				latitude, longitude = dic["loc"].split(",")
				identifiant["longitude"] = float(longitude)
				identifiant["latitude"] = float(latitude)
				identifiant["ip"] = dic["ip"]
			except:
				self.sign(False)
				return identifiant

		self.sign(True)
		return identifiant

	class Pooler_loin(object):
		"""
		donne le travail loin (pas aux coeurs de cette machine)
		"""
		def __init__(self, target, args, father, timeout=3600):
			self.father = father												#pour avoir acces a tous l'environement
			self.target = target												#fonction a executer
			self.args = args													#parametres a passer dans la fonction
			self.time = 0														#temps d'execution du calcul
			self.id = father.id													#identifiant de l'ordi qui a fait le travail
			self.sending_date = time.time()										#date d'envoi du courrier
			self.blacklisted = []												#c'est l'identifiant de toutes les machine qui ont echouees sur ce travail
			self.state = "wait"													#cela permet de savoir si un ouvrier s'acharne dessus ou si il n'est pas pris en charge
			self.script = self.father.get_target(self.target, self.args)		#recuperation du code source en str
			self.last_support = time.time()-timeout								#date de la derniere tentative d'execution (celle-la est factisse!)
			self.result_id = str(int(1000*time.time()))							#c'est l'identifiant du colis hors de cette machine
			self.timeout = timeout												#temps maximum accepte avant de considerer que le travail a echoue
			self.res = None														#ensemble de tous ce qui constitu le resultat au global
			self.resultat = None												#n'est plus None quand le resultat a ete recupere
			self.is_send = self.check_dataset()									#est True si le travail est parti au loin
			self.start()

		def check_dataset(self):
			"""
			interroge la base de donnee pour savoir si cela est vraimant nesesaire d'envoyer le travail
			au loin, ou si cette operation est deja faite
			return False si il faut l'envoyer
			return True si tout est deja dans la base de donnees
			"""
			self.father.show("tcheking the dataset of results...")
			base = sqlite3.connect("raisin_resultats.db")						#on se connecte a la base de donnees qui contient les resultats
			curseur = base.cursor()												#creation d'un pointeur vers cette base
			ligne = curseur.execute("SELECT res, result_id FROM table_resultats WHERE script = ?",(self.script,))#on selectionne, si elle existe la ligne du script qui est en cours d'execution
			for couple in ligne:												#on lance la requette
				self.res = pickle.loads(couple[0])								#on recupere le resultat (qui est peut etre un None)
				if self.res != None:											#si le resultat est deja la
					try:
						self.id = self.res["id"]								#on recupere l'id de la machine qui a fait le travail
					except:
						self.id = self.res["worker"]
					self.time = self.res["time"]								#le temps d'execution que la machine a mis
					self.resultat = self.res["result"]							#bien sur, on recupere le resultat de calcul
				self.result_id = str(couple[1])									#l'adresse du boulot peut-etre utile
				base.close()													#on ferme la base de donnee pour liberer l'acces
				self.father.sign(True)
				return True														#inutile de continuer la requette plus loin
			base.close()														#on ferme la base de donnee pour liberer l'acces
			self.father.sign(False)
			return False

		def save_work(self):
			"""
			enregistre dans la base de donnee le travail a faire
			ajoute donc une ligne a cette derniere
			"""
			self.father.show("save informations about this work...")
			base = sqlite3.connect("raisin_resultats.db")						#on se connecte a la base de donnees qui contient les resultats
			curseur = base.cursor()												#creation d'un pointeur vers cette base
			curseur = curseur.execute("""INSERT INTO table_resultats
				(sending_date, state, script, last_support, result_id, timeout, res)
			VALUES (?,?,?,?,?,?,?)""",(self.sending_date, self.state, self.script, self.last_support, self.result_id, self.timeout, pickle.dumps(self.res)))
			base.commit()														#on actualise ces changements
			base.close()														#liberation de l'acces
			self.father.sign(True)

		def save_result(self, res):
			"""
			enregistre dans la base de donnee le resultat de ce travail a la bonne ligne
			retourne True si l'enregistrement s'est correctement effectuer
			retourne False dans le cas contraire
			"""
			self.father.show("save the result...")
			if 1:
				base = sqlite3.connect("raisin_resultats.db")					#on se connecte a la base de donnees qui ne contient pas encore le resultat
				curseur = base.cursor()											#creation d'un pointeur vers cette base
				curseur = curseur.execute("""UPDATE table_resultats SET res = ? WHERE result_id = ?""",(pickle.dumps(res, protocol=2), self.result_id))
				base.commit()													#on actualise ces changements
				base.close()													#liberation de l'acces
				self.father.sign(True)
				return True
			else:
				self.father.sign(False)
				return False

		def start(self):
			"""
			poste la demande de travail
			ne retourne rien
			le job est constitue de la facon suivante:
				{
				"sending_date":date d'envoi du boulot
				"blacklisted":[liste des ordis ayant echouer a l'execution du script]
				"state": 'wait', 'process' 	si le programme est entrain d'etre executer sur une machine ou si il attend son tour
				"script": code a executer
				"last_support":date de la derniere tentative d'execution
				"result_id": identifiant du resultat
				"timeout": temps d'execution maximum
				}
			'timeout' est le temps maximum que le sript peut metre a s'executer
			se retourne sois meme afin que l'on puisse faire .get()
			"""
			self.job = {"sending_date": self.sending_date, "blacklisted": self.blacklisted, "state": self.state, "script": self.script, "last_support": self.last_support, "result_id": self.result_id, "timeout": self.timeout}
			if not self.is_send:												#si le travail n'est pas partit
				self.father.show("sending work to do...")						#annonce de son depart iminant
				try:															#on tente de le metre a la poste
					envoi = self.father.server.send(self.job, "w"+self.job["result_id"])#mais le bureau peut etre ferme
				except:															#en effet, self.father.server
					envoi = 1													#peut valoir 'None'
				if envoi == 0:													#si l'envoi a reussi
					self.father.sign(True)
					self.save_work()											#enregistrement de l'action qui vient de se derouler
					self.is_send = True 										#on materialise le fait que le colis est parti
					return self
				else:
					self.father.sign(False)
					raise Exception("fail to send far")
			return self															#si l'offre n'est pas toute fraiche, on sote cette etape

		def get(self, wait=False):
			"""
			attend pas le resultat, sauf si wait=True
			"""
			if self.resultat != None:											#si on a deja recuperer le resultat
				return self.resultat											#on ne va pas chercher plus loin, on le retourne a nouveau
			self.father.show("get result...")
			while 1:															#on met une boucle infini affin de pouvoir recommencer l'opperation
				try:
					res = self.father.server.load(self.job["result_id"])		#on tente de recuperer le resultat
				except:
					res = None
				if res != None:													#si cela a fonctionne
					self.father.sign(True)										#on l'indique a l'utilisateur
					try:
						self.id = res["id"]										#on recupere l'id de la machine qui a fait le travail
					except:
						self.id = res["worker"]
					self.time = res["time"]										#le temps d'execution que la machine a mis
					self.resultat = res["result"]								#bien sur, on recupere le resultat de calcul
					self.father.show("save the result in dataset...")
					if self.save_result(res):									#on enregistre le resultat pour les prochaines fois
						self.father.sign(True)
						self.father.server.remove(self.job["result_id"])		#on tente de supprimer le resultat du server
					else:
						self.father.sign(False)
					break

				else:															#si le resultat n'est toujours pas la
					if wait:													#et que l'on a l'ordre d'attendre
						continue												#on attend que le resultat arrive
					self.father.sign(False)										#on montre notre mecontentement
					break
			return self.resultat												#on retourne enfin le resultat

		def get_all(self, wait=False):
			"""
			retourne l'ensemble du resultat avec les informations supplementaires
			"""
			if self.resultat == None:										#si le resultat n'est pas encore recupere
				self.get(wait)												#on tente de le recuperer
				if self.resultat == None:									#si cela a echoue
					return None												#on ne si acharne pas plus
			return {"result":self.resultat,"time":self.time,"id":self.id}	#on retourne le resultat final

	class Pooler_cpu(object):
		"""
		execution des calculs sur un coeur de cette machine
		"""
		def __init__(self, target, args, pool, father):
			self.target = target											#fonction a executer
			self.args = args												#parametres a passer dans la fonction
			self.pool = pool												#c'est la liste d'attente vers les differents CPU
			self.time = 0													#temps d'execution du calcul
			self.father = father											#pour pouvoir dialoguer avec l'utilisateur
			self.id = self.father.id										#id de cette machine
			self.resultat = None											#ne vaut plus None une fois le calcul termine
			self.start()

		def start(self, timeout=None):
			"""
			timeout est seulement la pour une question d'homogeneite avec Pooler_loin
			"""
			self.father.show("give work to the CPU...")
			self.ti = time.time()
			self.res = self.pool.apply_async(self.target, self.args)
			self.father.sign(True)
			return self

		def get(self, wait=False):
			"""
			retourne imediatement un resultat sauf si wait=True
			on lance le calcul localement
			"""
			if self.resultat != None:
				return self.resultat
			while not self.res.ready():										#si le resultat n'est pas trouve
				if not wait:
					return None												#on retourne rien
			self.resultat = self.res.get()									#si le calcul est fini, on le retourne
			self.time = time.time()-self.ti									#on donne un temps approximatif de calcul

			return self.resultat

		def get_all(self, wait=False):
			"""
			retourne l'ensemble du resultat avec les informations supplementaires
			"""
			if self.resultat == None:										#si le resultat n'est pas encore recupere
				self.get(wait)												#on tente de le recuperer
				if self.resultat == None:									#si cela a echoue
					return None												#on ne s'y acharne pas plus
			return {"result":self.resultat,"time":self.time,"id":self.id}	#on retourne le resultat final

	class Pooler_thread(object):
		"""
		execution des calculs en local et en fragmente sur cette machine
		"""
		def __init__(self, target, args, father):
			self.father = father											#pour avoir acces a tous l'environement
			self.target = target											#fonction a executer
			self.args = args												#parametres a passer dans la fonction
			self.time = 0													#temps d'execution du calcul
			self.id = self.father.id										#identifiant de l'ordi qui a fait le travail
			self.resultat = None											#n'est plus None quand le resultat a ete recupere
			self.start()

		def start(self, timeout=None):
			self.father.show("creation of thread...")
			self.res = self.Thread(self.target, self.args)
			self.res.start()
			self.father.sign(True)

		class Thread(threading.Thread):
			"""
			c'est ici  que le faux calcul en parallele est execute
			"""
			def __init__(self, target, args):
				threading.Thread.__init__(self)
				self.target = target
				self.args = args
				self.result = None
				self.time = time.time()

			def run(self):
			 	self.result = self.target(*self.args)
			 	self.time = time.time()-self.time
			 	return None

		def get(self, wait=False):
			"""
			retourne imediatement un resultat sauf si wait=True
			on lance le calcul localement
			"""
			if self.resultat != None:
				return self.resultat
			while self.res.is_alive():										#si le resultat n'est pas trouve
				if not wait:
					return None												#on retourne rien
			self.resultat = self.res.result									#si le calcul est fini, on le retourne
			self.time = self.res.time										#on recupere le temps d'execution

			return self.resultat

		def get_all(self, wait=False):
			"""
			retourne l'ensemble du resultat avec les informations supplementaires
			"""
			if self.resultat == None:										#si le resultat n'est pas encore recupere
				self.get(wait)												#on tente de le recuperer
				if self.resultat == None:									#si cela a echoue
					return None												#on ne si acharne pas plus
			return {"result":self.resultat,"time":self.time,"id":self.id}	#on retourne le resultat final

class Server(object):
	"""
	cherche du travail a faire
	l'execute et renvoi le resultat
	"""
	def __init__(self,  image=None, code=None, cpu={"8h30":50, "12h":80, "13h":50, "19h30":80, "20h":50, "23h":10, "4h":100}, dt=30, display=True, alinea=0):
		self.display = display												#permet d'afficher ou non, les operations en cours
		self.alinea = alinea												#c'est le nombre d'alinea a faire en affichant le message
		self.image = image													#None: sur la machine / local: sur un disque / dropbox: sur dropbox
		self.code = code													#code pour acceder a drop box ou au disque si il est verrouille
		self.show("client starting...")
		self.permis = self.get_permis()										#on recherche un repertoire ou l'on a les droits d'ecriture et on l'ajoute au sys.path
		os.chdir(self.permis)												#on en fait le repertoire courant
		self.connecter = Connecter(self, self.image, self.code)				#creation d'un lien vers un serveur
		self.server = self.connecter.connect()								#connection a un serveur de methodes send(), load(), remove() et get_work()
		self.connecter.clean()												#des la premiere connection, on se renseigne sur l'activite des differents serveurs
		self.fin = False													#est False tant qu'il ne faut pas mourrir
		self.id = self.get_id()												#on recupere un identifiant propre a cette machine, normalement un dictionaire
		self.cpu = cpu														#c'est le taux maximum acceptable de cpu, peut être un nombre ou un dictionaire ex {20.5:20, '6:50', 12:100} = 20% à partir de 20h30, 50% apres 6h...
		self.dt = dt														#c'est le temps de lecture du cpu en seconde
		self.sign(True)
		self.run()															#demarrage reel du client

	def run(self):
		"""
		c'est ici que l'on cherche le travail
		et qu'on l'execute en toile de fond
		'cpu_max' correspond au pourcentage maximum de cpu admissible pour
		que l'on lance un nouveau calcul
		"""
		sys.path.append(os.getcwd())											#afin de pouvoir executer le scripte que l'on recoit
		while not(self.fin):
			self.show("waiting for server...")
			while self.server == None:											#si l'on n'est connecte a aucun serveur
				time.sleep(60)													#on fait une pause d'une minute
				self.server = self.connecter.connect()							#on tente de se reconnecter

			if self.autorize_cpu() < 100:										#seulement dans le cas ou l'on est pas au taket
				while self.get_cpu() > self.autorize_cpu():						#on attend que le processeur est suffisement de marge
					pass														#si ce n'est pas le cas, on attend
			self.sign(True)														#enfin, on peu y aller

			work = self.get_work()												#on tente de recuperer du taff
			if work == None:													#si il n'y a plus d'offre d'emploi
				self.server = self.connecter.connect()							#on tente une nouvelle connection avec un autre serveur
			else:																#si le travail propose nous convient
				if self.apply(work)	== 0:										#on tente de le faire
					self.connecter.update_date()								#si ca fonctionne, on change la date de derniere activitee de ce serveur

	def show(self, message="", alinea=1):
		"""
		affiche le message avec l'alinea d'avant
		'alinea' est le nombre d'alinea a ajouter a tous les messages d'apres
		"""
		if type(alinea) != int:
			raise TypeError("'alinea' must be an integer")
		self.alinea += alinea													#memoriation de l'alinea pour la suite du programme
		if self.display and message:											#si il y a quelque chose a afficher
			print("    "*(self.alinea-alinea)+message)							#affichage du message
			return True
		return False

	def sign(self, conclusion, alinea=-1):
		"""
		affiche le message de fin avec un alinea
		alinea est le decalage a faire sur tous les prochains affichages
		"""
		if type(alinea) != int:
			raise TypeError("'alinea' must be an integer")
		if conclusion == True:
			return self.show("    "*(1+alinea)+"success!",alinea)
		elif conclusion == False:
			return self.show("    "*(1+alinea)+"failure!",alinea)
		elif type(conclusion) == str:
			return self.show("    "*(1+alinea)+conclusion,alinea)
		raise TypeError("'conclusion must be a boolean or a string")

	def get_cpu(self, display=True):
		"""
		retourne le pourcentage de cpu entre 0 et 100
		le pourcentage retourne est le pourcentage moyen sur une periode de dt secondes
		"""
		if display == True:
			self.show("real cpu reading...")
		try:
			import psutil
			cpu = psutil.cpu_percent(self.dt)
			if display == True:
				self.sign("success! "+str(cpu)+"%")
			return cpu
		except:
			try:
				"""
				extraction du fichier /proc/stat qui contient:
				user: processus en usermode
				nice: processus avec un nice level en usermode
				system: processus en mode kernel
				idle: temps a se tourner les pouces
				iowait: en attente d'entrees/sorties
				irq: servicing interrupts
				softirq: servicing softirqs
				"""
				avant = [int(i) for i in open("/proc/stat","r").read().split("\n")[0].split(" ")[2:]]#temps d'activite depuis le demarage du pc
				time.sleep(self.dt)
				maintenant = [int(i) for i in open("/proc/stat","r").read().split("\n")[0].split(" ")[2:]]#temps d'activite d'avant + celui durant dt
				maintenant = [maintenant[i]-avant[i] for i in range(len(avant))]#recuperation de ce qui c'est passe durant dt
				cpu = 100*(sum(maintenant)-maintenant[3])/sum(maintenant)		#calcul du pourcentage
				if display == True:
					self.sign("success! "+str(cpu)+"%")
				return cpu
			except:
				try:
					i = os.subprocess.Popen("top -d "+str(self.dt).replace(".",",")+" -n 2").read()
					cpu = float(i.split("%Cpu(s):")[-1].split("us,")[0].replace(",",".").replace("  "," ").split(" ")[1])
					if display == True:
						self.sign("success! "+str(cpu)+"%")
					return cpu
				except:
					self.sign(False)
					return 0.0

	def autorize_cpu(self, motif=None):
		"""
		retourne le taux d'utilisation autorise de cpu
		retourne un nombre entre 0 et 100
		"""
		def comprendre(chaine):
			"""
			tente d'interpoler la chaine de caractere pour la transformer en flotant
			ex: 5h15 -> 5.25
			"""
			for car in chaine:
				if not car in "0123456789":
					chaine = chaine.replace(car,",")
			liste = [i for i in chaine.split(",") if i != ""]
			return sum([float(i)/{0:1.0,1:60.0,2:3600.0,3:36000.0}[rang] for rang,i in enumerate(liste)])

		if motif == None:														#si l'on a rien passe en argumment
			motif = self.cpu													#on prend le parametre global

		if type(motif) == int:													#si le taux est donne en entier
			return max(0.0,min(100.0, float(motif)))							#on le renvoi en float
		elif type(motif) == float:												#si il est deja dans le bon format
			return max(0.0,min(100.0, motif))									#on se contente de verifier sa valeur
		elif type(motif) == dict:												#dans le cas ou il faut etre plus precis
			date = datetime.datetime.now()												#on regarde l'heure actuelle
			temps = date.hour+date.minute/60+date.second/3600					#on met cette heure en forme
			correspondant = {}													#on cree un dictionaire qui fait correspondre la date en flotant avec une clef de motif
			for clef in motif.keys():											#pour chaque clef
				if type(clef) == str:											#si l'heure est marque un peu trop humainement
					try:														#on tente de decortiquer ca
						correspondant[comprendre(clef)] = clef					#mais bon,
					except:														#on est jamais trop prudent de se dire qu'il est possible
						pass													#de ne pas comprendre un message humain
				else:															#meme dans le cas ou cela est sense
					try:														#ne pas etre du charabiat
						correspondant[float(clef)] = clef						#il vaut mieux prendre des precautions
					except:														#on ne sait jamais
						pass													#ca se trouve, il ne s'agit meme pas de nombre!
			iden = sorted(correspondant.keys())									#on tri se qu'il nous reste par ordre croissant
			try:
				return self.autorize_cpu(motif[correspondant[([iden[-1]]+[d for d in iden if d <= temps])[-1]]])#on retourne le cpu correspondant a l'heure la plus proche
			except:
				return 100.0
		else:
			return 100.0

	def execute(self, code):
		"""
		execute le code 'code'
		retourne le resultat
		fait en sorte que le cpu ne depasse pas la limite permise,
		si le cpu augmente brusquement, l'execution du code est reportee
		il hache le calcul afin de se reguler
		en cas d'erreur, retourne None, le resultat doit donc etre different de None
		voir prioritée
		"""
		class Executer_vite(object):
			"""
			execute le travail sans faire attantion a l'utilisation du cpu
			c'est plus basique donc plus rapide a l'execution
			"""
			def __init__(self, code, father):
				self.resultat = None											#valeur du resultat, ce que retourne le code
				self.father = father											#pour comuniquer avec le programme principal
				self.code = code												#code a executer
				self.module = self.create_objet()								#on enregistre le module
				self.father.show("*"*20+"EXECUTE"+"*"*20+"\n",0)
				for ligne in self.code.split("\n"):
					self.father.show(ligne,0)

			def run(self):
				"""
				c'est ici que l'on execute le calcul
				"""
				try:
					self.resultat = self.module.get_resultat()					#on fait execute le code
					self.father.show("*"*20+"SUCCESS"+"*"*20+"\n",0)
				except:
					self.father.show("*"*20+"FAILURE"+"*"*20+"\n",0)
				return self.resultat

			def create_objet(self):
				"""
				enregistre le code dans un fichier et l'importe
				ne laisse aucune trace sur le disque dur
				retourne l'objet qui a pour methode self.get_resultat()
				et pour variable interne self.rapport (entre 0 et 1)
				"""
				nom = "".join([chr(int(i)+97) for i in str(int(time.time()))])+".py"#nom du module a importer et a creer
				try:															#on tente de creer phisiquement le module
					with open(os.path.join(self.father.permis,nom), "w", encoding="utf-8") as module:#on cree un fichier en utf-8 pour eviter les erreurs avec les accents
						module.write(self.code)									#une fois ouvert, on le rempli avec le bon contenu
				except:															#en cas d'erreur
					try:
						with open(os.path.join(self.father.permis,nom), "w") as module:#on cree un fichier en utf-8 pour eviter les erreurs avec les accents
							module.write(self.code)
					except:
						self.father.permis = self.father.get_permis()			#on cherche un autre endroit ou creer le fichier
						self.create_objet()										#c'est parti, on retente dans cette configuration

				try:
					module = __import__(nom[:-3])								#on importe le module fraichement cree
				except:
					module = None
				try:															#on tente de faire du menage dans les fichiers crees
					os.remove(os.path.join(self.father.permis,nom))				#mais aussi tout le repertoire cree par la fonction '__import__()'
					shutil.rmtree("__pycache__")								#qui ne servent desormais plus a rien
				except:															#on retire le fichier que l'on vient de faire
					pass														#quelques lignes plus haut
				return module													#on retourne le module

		self.show("execution of script...")										#on travail rapidement
		res = Executer_vite(code, self).run()									#on lance le calcul a fond
		self.sign(res != None)													#on affiche True si tout c'est bien passe
		return res

	def apply(self, work):
		"""
		execute le travail, se charge de la communication avec le serveur
		retourne 0 si il n'y a pas d'erreur
		retourne 1 si on a echouer a executer
		"""
		t_init = time.time()													#afin de chronometrer le temps d'execution
		resultat = self.execute(work["script"])									#execution du script
		t_final = time.time()-t_init											#calcul du temps total passe en execution
		if resultat == None:													#en cas d'echec
			work["state"] = "wait"												#on precise que ce job est desormais libre
			work["last_support"] = time.time()									#on dit a quel moment l'erreur est survenue
			self.server.remove("w"+work["result_id"])							#mise a jour du travail defectueux
			self.server.send(work, "w"+work["result_id"])						#pour l'ajout du travail mis a jour
			return 1
		else:
			lettre = {"id":self.id, "time":t_final, "result":resultat, "sending_date":time.time()}#mise en forme du resultat
			if self.server.send(lettre, work["result_id"]) == 0:				#on envoie le resultat
				self.server.remove("w"+work["result_id"])						#suppresion du travail desormais termine
				return 0
			return 1

	def get_id(self):
		"""
		retourne l'identifiant propre a cette ordinateur
		en cas d'erreur, retourne un identifiant quelconque dependant du temps
		"""
		self.show("ip request...")

		identifiant = {}
		identifiant["hostname"] = socket.gethostname()
		identifiant["executable"] = sys.executable
		identifiant["country"] = None
		identifiant["city"] = None
		identifiant["longitude"] = None
		identifiant["latitude"] = None
		identifiant["ip"] = None

		try:
			try:
				1/0
				dic = eval(urllib.request.urlopen("http://freegeoip.net/json").read().decode())
			except:
				1/0
				dic = eval(urllib.urlopen("http://freegeoip.net/json").read().decode())
			identifiant["country"] = dic["country_code"]
			identifiant["city"] = dic["city"]
			identifiant["longitude"] = dic["longitude"]
			identifiant["latitude"] = dic["latitude"]
			identifiant["ip"] = dic["ip"]
		except:
			try:
				try:
					dic = eval(urllib.request.urlopen("http://ipinfo.io/json").read().decode())
				except:
					dic = eval(urllib.urlopen("http://ipinfo.io/json").read().decode())
				identifiant["country"] = dic["country"]
				identifiant["city"] = dic["city"]
				latitude, longitude = dic["loc"].split(",")
				identifiant["longitude"] = float(longitude)
				identifiant["latitude"] = float(latitude)
				identifiant["ip"] = dic["ip"]
			except:
				self.sign(False)
				return identifiant

		self.sign(True)
		return identifiant

	def get_permis(self):
		"""
		farfouille dans l'ordinateur jusqu'a trouver un endroit
		ou l'on a les droits d'ecriture
		"""
		def test(rep):
			"""
			retourne True si le repertoire est accessible
			retourne False dans le cas contraire
			"""
			try:
				with open(os.path.join(rep,"temp.txt"),"w") as f:
					f.write("test d'acces en ecriture")
				os.remove(os.path.join(rep,"temp.txt"))
				return True
			except:
				return False

		self.show("searching writing directory...")
		montage = [os.path.dirname(__file__),os.getcwd(),"/home","/mnt","H:/","G:/","F:/","E:/","D:/","C:/","B:/","A:/"]
		while 1:
			for rep in montage:
				if os.path.exists(rep):
					try:
						for father, reps, file in os.walk(rep):
							if test(father):
								sys.path.append(father)
								self.show(father,0)
								self.sign(True)
								return father
					except:
						pass

	def get_work(self):
		"""
		cherche si il y a du travail sur le serveur actuel
		si tel est le cas, retourne le travail a faire
		sinon retourne None et ne change pas automatiquement de serveur
		"""
		self.show("searching job...")
		self.lock()																#on commence par deposer un verrou

		for num in range(3):													#on fait plusieurs passes, a chaque fois de - en - conraignantes
			for file in self.server.ls():										#pour chaque fichiers prensents dans la boite dropbox
				if (file[0] == "w") and file[1:].isdigit():						#si il s'agit d'un travail
					job = self.server.load(file)								#on le telecharge pour plus d'informations
					if job != None:												#si le telechargement a completement foire, on passe a la suite
						if not(self.id in job["blacklisted"]):					#on continue seulement si l'on a pas deja echoue dessus
							if (time.time() > job["last_support"]+job["timeout"]) or (num >= 1):#tres vite, on arrete de se preoccuper du moment ou le fichier a ete pris en charge
								if (job["state"] == "wait") or (num >= 2):		#puis on selectionne en priorite les fichier qui ne sont pas deja pris en charge
									job["state"] = "process"					#si on arrive ici, c'est que le poste est pour nous!
									job["last_support"] = time.time()			#on se precipite alors sur l'offre d'emploi
									job["blacklisted"].append(self.id)			#precaution si jamais le script est infini, affin d'eviter de tout blocker trop longtemps
									self.server.remove(file)					#on fait tout pour eliminer la concurrence
									self.server.send(job, file)					#pour cela, on fait comprendre aux autres que c'est nous le patron!
									self.unlock()								#bref, une fois cette demonstration termine
									self.sign(True)								#on laisse un peu de place aux autres
									return job									#et on se met au boulot!
		self.unlock()															#si rien nous plait
		self.sign(False)														#on passe son tour
		return None																#on va voir ailleur

	def lock(self, validity_time=60):
		"""
		pose un verrou, reste bloque tant que le verrou n'est pas depose
		validity_time est le temps ou le verrou rest valide
		un verrou est compose de la facon suivante
		verrou: {"expiration_date": date de non validite du verrou, "id":identifiant}
		"""
		def free_acces(identifiant, validity_time):
			"""
			retourne True si l'acces et libre
			retourne False si il faut encore attendre
			"""
			ver = self.server.load("verrou")
			if ver == None:
				self.server.send({"expiration_date":time.time()+validity_time, "id":identifiant},"verrou")
				return False
			if ver["id"] == identifiant:
				return True
			if time.time() > ver["expiration_date"]:
				self.server.remove("verrou")
				return False

		self.show("wait acces...")
		disp = self.display
		self.display = False

		self.identifiant = 1000*int(time.time())
		while not(free_acces(self.identifiant, validity_time)):					#tant que le verrou n'est pas depose
			pass																#on reste a l'ecoute
		self.display = disp
		self.sign(True)
		return None

	def unlock(self):
		"""
		supprime le verrou depose
		"""
		self.show("unlock...")
		disp = self.display
		self.display = False
		ver = self.server.load("verrou")
		if ver != None:
			if ver["id"] == self.identifiant:
				self.server.remove("verrou")
		self.display = disp
		self.sign(True)
		return None

#inplementation du module

class Upgrade(object):
	"""
	met a jour le module
	"""
	def __init__(self, timeout=120):
		with open(__file__,"r") as f:											#on lit le fichier qui est en cours d'execution
			self.contenu = f.read()												#car c'est lui qui est mis a jour
		self.liste_noir = []													#c'est la liste des ordinateurs qui viennent de subir la mise a jour
		self.timeout = timeout													#c'est le temps maximum que l'on s'autorise pandant lequel rien ne se passe
		self.sess = Session(display=False)										#pour pouvoir envoyer le message
		self.run()

	def run(self):
		"""
		lance la mise a jour
		"""
		def installer_contenu(content, liste_noir):
			"""
			installe le nouveau programme
			"""
			import os
			import socket
			import sys

			def find_rep():
				"""
				cherche ou est le module raisin qui est utilise actuellement
				"""
				for rep in sys.path:
					if os.path.isdir(rep):
						if "raisin" in os.listdir(rep):
							r = os.path.join(rep,"raisin")
							if os.path.exists(r):
								return r
				return None

			print("verification si la mise a jour a deja ete faite...")
			identifiant = [socket.gethostname(), sys.executable]
			print("identifiant:",identifiant)
			print("liste_noir:",liste_noir)
			if identifiant in liste_noir:
				print("mise a jour deja faite")
				raise Exception("afin que les autres puissent aussi en profiter")
			print("recherche du fichier a mettre a jour...")
			fichier = os.path.join(find_rep(),"__init__.py")
			print("fichier trouve: ",fichier)
			print("reecriture du fichier...")
			with open(fichier, "w", encoding="utf-8") as f:
				f.write(content)
			print("mise a jour terminee!")
			return identifiant

		temps = time.time()														#on a ainsi un delai temporel
		while time.time()-self.timeout < temps:									#si in est dans les temps
			temps = time.time()													#remise a zero du chronometre
			res = self.sess.Process(installer_contenu, self.contenu, self.liste_noir)#on envoi une mise a jour
			while (res.get() == None) and (time.time()-temps < self.timeout):	#tant que le resultat n'est pas arrive
				pass															#on attend qu'une machine ait fait sa mise a jour
			if res.get() != None:												#si le sablier n'est pas ecoule
				print(res.get())												#on affiche le nom de la personne qui a ete mis a jour
				self.liste_noir.append(res.get())								#on l'ajoute a la liste noir pour pas qu'elle refasse la meme mise a jour

class Update(object):
	"""
	comme Upgrade()
	"""
	def __init__(self, timeout=120):
		Upgrade(timeout)

class Install(object):
	"""
	permet d'installer le module au bon endroit
	"""
	def __init__(self):
		self.source = self.get_cwdir()
		self.install_raisin()													#installe le module raisin dans le python qui execute cette algo
		if "win" in sys.platform or 1:											#si on est sur windaube
			self.windows_server()												#mise en place du server qui tourne en arriere plan

	def get_cwdir(self):
		"""
		retourne le chemin du dossier "raisin" qui contient le module actuel
		"""
		return os.path.dirname(__file__)

	def install_raisin(self):
		"""
		installe le module raisin au bon endroit
		"""
		print("package installation...")
		reussi = False
		for path in sys.path:
			if (os.path.basename(path) == "dist-packages" or os.path.basename(path) == "site-packages") and not reussi:
				self.destination = os.path.join(path, "raisin")
				if self.source != self.destination:
					print("	copy from:",self.source)
					print("	to:",self.destination)
					try:
						shutil.rmtree(self.destination, ignore_errors=True)
						shutil.copytree(self.source, self.destination)
						print("		success!")
						reussi = True
					except:
						print("		failure!")
		if reussi:
			print("success!")
		else:
			print("failure!")

	def windows_server(self, cpu=None, nom=[]):
		"""
		met l'executable dans le dossier d'application au demarage
		cpu est le taux d'utilisation du cpu
		nom est la liste des noms d'utilisateur a qui il faut appliquer ce cpu
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
				tronc = os.path.join(r,"Users")
				if os.path.exists(tronc):
					try:
						for nom in os.listdir(tronc):
							branche = os.path.join(tronc, nom)
							for feuille in search_startup(branche):
								yield nom, feuille
					except:
						pass

		print("server installation...")
		for nom1, rep in get_name():
			print("	"+rep)
			if (nom1 in nom) or not os.path.exists(os.path.join(rep,"server_raisin1.pyw")):
				try:
					print("	start for",nom1,"...")
					for i in range(1,5):
						with open(os.path.join(rep,"server_raisin"+str(i)+".pyw"), "w") as f:
							f.write("import raisin\n")
							if (nom1 in nom) and (cpu != None):
								f.write("raisin.Server(cpu="+str(cpu)+")")
								continue
							f.write("raisin.Server()")
					print("		success!")
				except:
					print("		failure!")
		print("success!")


def map(*args):
	sess = Session(display=1)
	res = sess.map(*args)
	return res.get(wait=True)
