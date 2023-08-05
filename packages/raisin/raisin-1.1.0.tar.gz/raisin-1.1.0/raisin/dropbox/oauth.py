atiente
						with Printer("is it the same compresslevel", signature=self.signature):#regarder si il faut comprimer plus le resultat
							if res["compresslevel"] > requette[0][0]:						#si il faut plus compresser le resultat	
								p.show("no")												#on enleve le faux espoir de l'utilisateu
								res_bis = res.copy()										#on fait une copie du traivail
								res_bis["compresslevel"] = 0								#afin de pouvoir changer le taux de compression sans qu'il n'y ai trop d'impactes
								res_bis = self.update_res(res_bis)							#on recupere les valeurs actuelles
								self.del_res(res["res_hash"])								#affin de pouvoir les supprimer de la base sans encombres
								res_bis["compresslevel"] = res["compresslevel"]				#on revient au taux de compression requiere
								return self.update_res(res_bis)								#enregistrement de ce nouveau resultati avec le bon taux de compression
							else:															#dans le cas ou le taux reel de compression est egal ou meilleur a celui requiere
								p.show("yes")												#on rejouit l'utilisateur
								if not "res" in res:										#si le resultat doit etre deserialise
									res["res"] = requette[0][1]								#on va deja voir si il est stocke dans la base ou pas
									if res["res"] != b"":									#si le resultat est dans la base
										res["res"] = deserialize(res["res"], signature=self.signature)#on le deserialise localement
									else:													#si il est dans un fichier sur le disque
										with open(os.path.join(raisin.rep, "res_"+res["res_hash"]+".rais"), "rb") as f:#ouverture du resultat
											res["res"] = deserialize(f, signature=self.signature)#on deserialise le gros resultat
								return res													#on sort de cette fonction
					else:																	#si elle n'est pas dans la base
						p.show("no")														#on indique qu'il faut l'enregistrer
						path_file = os.path.join(raisin.rep, "res_"+res["res_hash"]+".rais")#ca, c'est le chemin qui mene au bon fichier
						if "res" in res:													#si le resultat est sous forme objet
							pack_gener = serialize(res["res"], compresslevel=res["compresslevel"], generator=True, signature=self.signature)#serialisation du resultat
						else:																#dans le cas ou il est deja serialise
							pack_gener = self.generateur(res["res_data"])					#c'est que les donnees sont sous une autre forme
						with open(path_file, "wb") as f:									#on va enregistrer le resultat
							for pack in pack_gener:											#en faisant gaffe de ne pas faire cracher le pc
								f.write(pack)												#on rempli alors le fichier petit a petit
						if os.path.getsize(path_file) < 1024*1024:							#si le fichier n'est pas tres gros
							with open(path_file, "rb") as f:								#il va directement etre stocke dans la base de donnees
								res_data = f.read()											#il est donc important de lire le fichier
							os.remove(path_file)											#pour pouvoir faire du menage
						else:																#si le fichier est gros
							res_data = b""													#on ne le stock pas dans la base mais a cote
						with Lock("bdd", signature=self.signature):							#depot d'un verrou sur la base de donne
							curseur = self.bdd.cursor()										#creation d'un pointeur vers la base
							curseur.execute("""INSERT INTO res
								(res_hash, compresslevel, res_data)
									VALUES (?,?,?)""",(res["res_hash"], res["compresslevel"], res_data))#ajout de ligne
							self.bdd.commit()
						return res															#on retourne le resultat
			else:																			#si l'identifiant n'est pas connu
				if "res" in res:
					res["res_hash"] = self.get_hash(res["res"])								#recuperation du hash du resultat
				else:
					res["res"] = deserialize(res["res_data"], signature=self.signature)
				return self.update_res(res)													#avec cet element, on peu passer a la suite

	class server_lock:
		"""
		est un objet verrou sur les differents serveurs
		"""
		def __init__(self, server, timeout=60, signature=None):
			self.server = server
			self.timeout = timeout
			self.signature = signature
			if self.signature == None:
				signature = self.server.signature

		def acquire(self):
			"""
			attend que l'acces soit libre
			"""
			def free_acces(identifiant, validity_time):
				"""
				retourne True si l'acces et libre
				retourne False si il faut encore attendre
				"""
				try:
					ver = self.server.load("lock", signature=self.signature)
					ver = deserialize(ver, signature=self.signature)
					if ver["id"] == identifiant:
						return True
					if time.time() > ver["expiration_date"]:
						self.server.remove("lock", signature=self.signature)
						return False
				except:
					verrou = {"expiration_date":time.time()+validity_time, "id":identifiant}
					verrou = serialize(verrou, compresslevel=0, signature=self.signature, generator=False)
					try:
						self.server.send(verrou, "lock", signature=self.signature)
					except:
						pass
					return False

			with Printer("wait acces...", signature=self.signature):
				self.verrou_identifiant = 1000*int(time.time())
				while not(free_acces(self.verrou_identifiant, self.timeout)):#tant que le verrou n'est pas depose
					pass											#on reste a l'ecoute
				return None

		def release(self):
			"""
			rend l'acces disponible sur le serveur en question
			"""
			try:
				with Printer("unlock...", signature=self.signature):
					ver = self.server.load("lock", signature=self.signature)
					if ver != None:
						ver = deserialize(ver, signature=self.signature)
						if ver["id"] == self.verrou_identifiant:
							self.server.remove("lock", signature=self.signature)
			except:
				pass
			return None

		def is_free(self):
			"""
			retourne True si il n'y a pas de verrou
			"""
			try:
				ver = self.server.load("lock", signature=self.signature)
				ver = deserialize(ver, signature=self.signature)
				if ver["id"] == identifiant:
					return True
				if time.time() > ver["expiration_date"]:
					self.server.remove("lock", signature=self.signature)
					return False
			except:
				return True

		def __enter__(self):
			self.acquire()
			return None

		def __exit__(self, *args):
			self.release()
			return None

class Lock:
	"""
	est un verrou global
	"""
	def __init__(self, id="default", timeout=60, priority=0, signature=None, display=True, local=False):
		"""
		'id' (STR) => est l'identifiant de ce verrou, c'est ce qui permet de le rendre independant des autres
		'timeout' (INT, FLOAT) => temps de validite du verrou en s
		'priority' (INT) => l'utilisateur n est prioritaire devant [n-1, n-2, ..., 2, 1, 0] avec n < 1000
		'signature' (obj) => permet si voulu, d'informer l'utilisateur du processus appelant
		'display' (BOOL) => True pour afficher et False pour ne pas appeller afficher
		'local' (BOOL) => True: depose le verrou dans un repertoir accessible par ce programme seulement False: verrou vu par tous
 		"""
		self.id = id																		#identifiant de ce verrou
		self.timeout = timeout																#temps de validitee du verrou pose
		self.priority = priority															#est un entier, plus il est elever, plus la prioritee est haute
		self.signature = signature															#permet d'afficher le message au bon endroit
		self.display = display																#True si il faut afficher le message
		self.local = local																	#est True si ce verrou est seulement actif sur ce programe
		self.code = str(uuid.uuid4())														#identifiant unique propre a ce verrou
		if self.local:																		#si le verrou est local, propre a ce processus
			self.path_file = os.path.join(raisin.temprep, "lock_"+self.id+".txt")			#le chemin qui mene jusqu'au verrou
		else:																				#si seul tout le monde doit pouvoir y avoir acces
			self.path_file = os.path.join(raisin.rep, "lock_"+self.id+".txt")				#chemin bien visible par tous

	def acquire(self):
		"""
		depose le verrou et retourne une fois qu'il est depose
		"""
		while os.path.exists(self.path_file):												#tant que le fichier existe
			try:																			#on va essayer de lire ce qu'il y a dedand
				with open(self.path_file, "r") as f:										#tentative d'ouverture
					lock_priority, lock_code, lock_timeout = f.read().split(";")			#et de lecture du fichier
					lock_priority, lock_code, lock_timeout = int(lock_priority), lock_code, float(lock_timeout)#convertion dans les bon types
				if (lock_code == self.code) and (lock_priority == 999):						#si on en est plainement maitre
					return None																#on se sauve vite de la
				elif (lock_code == self.code) and (lock_priority != 999):					#si personne ne semble se manifester
					with open(self.path_file, "w") as f:									#on va tenter de s'en emparer vraiment
						f.write("999;"+self.code+";"+str(time.time()+self.timeout))			#en y metant nos empreintes
				elif (lock_code != self.code) and (self.priority > lock_priority):			#si un autre processus depose timidement son verrou mais que l'on est plus fort que lui
					with open(self.path_file, "w") as f:									#on va alors a notre tour tenter de le prendre timidement
						f.write(str(self.priority)+";"+self.code+";"+str(time.time()+self.timeout))#en y inscrivant notre volontee
					if self.priority != 999:
						time.sleep(0.02)													#on est poli, on laisse la priorite au plus fort
				elif time.time() > lock_timeout:											#si le verrou est trop vieu pour avoir encore de la valeur
					os.remove(self.path_file)												#on tente alors de le degomer
				else:																		#dans le cas ou l'on est dans aucune des ces situation, c'est qu'il faut attendre
					time.sleep(0.01)														#on fait alors une petite pause qui soulage le resources
			except:
				time.sleep(0.3)

		try:																				#si il n'y a pas de fichiers
			with open(self.path_file, "w") as f:											#c'est alors possible de prendre la main
				f.write(str(self.priority)+";"+self.code+";"+str(time.time()+self.timeout))	#on essai donc de le faire
			if self.priority != 999:
				time.sleep(0.02)															#on laisse le tamps au processus plus fort de se retourner
			return self.acquire()															#on repart donc en haut
		except:																				#si il y a eu une erreur quelqonque
			return self.acquire()															#on retent notre chance une deuxieme fois

	def release(self):
		"""
		tente de liberer l'acces
		"""
		try:																				#on essai de supprimer le fichier
			os.remove(self.path_file)
		except:
			pass
		return None

	def is_lock(self):
		"""
		retourne False si l'acces est libre
		"""
		if not os.path.exists(self.path_file):												#dans le cas ou il n'y a pas de fichier
			return False																	#c'est que l'acces est libre
		try:																				#dans le cas ou il y a un fichier
			with open(self.path_file, "r") as f:											#on va tenter de le lire
				lock_priority, lock_code, lock_timeout = f.read().split(";")				#et de lecture du fichier
				lock_priority, lock_code, lock_timeout = int(lock_priority), lock_code, float(lock_timeout)#convertion dans les bon types
			if time.time() > lock_timeout:													#si le verrou date de gerusalem
				return False																#alor on considere que l'acces est libre
			return True																		#dans le cas contraire, la voix n'est pas libre
		except:																				#si ca capote
			return True 																	#en cas d'erreur aussi, la voix n'est pas disponible

	def is_free(self):
		"""
		reourne True si l'acces est libre
		"""
		return not(self.is_lock())

	def __enter__(self):
		if self.display:
			with Printer("wait "+str(self.id)+" freedom...", signature=self.signature):		#attente de la cess libre
				self.acquire()
		else:
			self.acquire()

	def __exit__(self, *args):
		if self.display:
			with Printer("release "+self.id+"...", signature=self.signature):				#rendre a nouveau l'acces libre
				self.release()
		else:
			self.release()

class Printer:
	"""
	gere l'affichage des different apelle de raisin
	"""
	def __init__(self, *message, signature=None, display=None):
		"""
		'display' est soit un booleen, soit un entier, qui permet de gerer l'affichage
		'signature' peu etre n'importe quoi mais evec une particularitee:
			signature = {"rep":"C://...", "signature":"element..."} => le repertoir de travail est impose
		"""
		self.rep = raisin.temprep
		if type(signature) == dict:
			self.rep = signature.get("rep", raisin.temprep)
		self.message = self.concatenate(*message)								#on raboute tout les messages pour en faire un seul
		self.signature = signature
		if type(signature) == dict:
			self.signature = signature.get("signature", signature)				#permet de savoir dans quelle colone on affiche le message
		self.main_default = 6													#c'est le nombre d'indentation par defaut dans la colonne principale
		self.second_default = self.main_default//2								#c'est le nombre d'indentation par defaut dans les autres colones
		self.display = self.get_display(display)								#recuperation du nombre d'indentations que l'on affiche	
		self.largueur = 80														#c'est le nombre de caracteres affichables en une ligne de console (158 sur linux)
		self.espaces = "    "													#marquer des indentions

	def get_size(self, default):
		"""
		retourne la taille de la console
		"""
		try:																	#on tente un autre truc
			return shutil.get_terminal_size((80, 20)).columns					#avec un modul python cette fois ci
		except:																	#si vraiment rien ne marche
			return default

	def concatenate(self, *message):
		"""
		retourne une seule chaine de caractere a la maniere de 'print'
		"""
		chaine = ""																#initialisation de la chaine de caractere
		for obj in message:														#pour chaque objets passe en parametre
			chaine += obj.__str__()												#il est converti en str
			chaine += " "														#on rajoute un espace pour faire comme 'print()'
		return chaine[:-1]														#afin d'etre totalement retourne comme une chaine de caractere

	def get_display(self, display):
		"""
		retourne un entier representant le nombre d'indentaions maximum
		que l'on peut afficher dans ce programme pour la signature 'self.signature'
		"""
		if os.path.exists(os.path.join(self.rep, "printerNone")) and (display == None):#on va cherher la valeur par defaut
			with open(os.path.join(self.rep, "printerNone"), "r") as f:	#pour cela on regarde ce qu'il se passe pour le programme principal
				principal = int(f.read())										#c'est a dir de quel alinea est-ce qu'il a le droit
		else:																	#si c'est la premiere fois que cette fonction est appelee
			with open(os.path.join(self.rep, "printerNone"), "w") as f:	#il faut bien creer le fichier
				if (self.signature == None) and (type(display) == int):			#si on a un ordre
					f.write(str(max(0, display)))								#on met ce qui est demande
				elif (self.signature == None) and (display == True):			#si l'ordre est de tout afficher
					f.write("255")												#on prevoit une grosse marge
				elif (self.signature == None) and (display == False):			#si on a l'ordre de ne rien afficher
					f.write("0")												#on autorise 0 indentations
				else:															#si on fait comme on veut
					f.write(str(self.main_default))								#on y met la valeur par defaut
			return self.get_display(None)										#une fois le fichier cree, on peu recomencer les choses serieuses
		if principal != 0:														#si un quelqonque affichage est permis
			if self.signature == None:											#si le programe appelant est le programme par defaut
				return principal												#la valeur a deja ete exctractee
			if os.path.exists(os.path.join(self.rep, "printer"+str(self.signature))) and (display == None):#si on a des infos
				with open(os.path.join(self.rep, "printer"+str(self.signature)), "r") as f:#on va aller les chercher
					return int(f.read())										#et le retourner de suite
			else:																#si un changement nous est impose
				with open(os.path.join(self.rep, "printer"+str(self.signature)), "w") as f:#il faut bien creer le fichier
					if (self.signature == None) and (type(display == int)):		#si on a un ordre
						f.write(str(max(0, self.display)))						#on met ce qui est demande
					elif (self.signature == None) and (display == True):		#si l'ordre est de tout afficher
						f.write("255")											#on prevoit une grosse marge
					elif (self.signature == None) and (display == False):		#si on a l'ordre de ne rien afficher
						f.write("0")											#on autorise 0 indentations
					else:														#si on fait comme on veut
						f.write(str(self.second_default))						#on y met la valeur par defaut
				return self.get_display(None)									#on retourne cette nouvelle valeur
		else:																	#si il n'y a pas le droit a l'affichage
			return 0															#on retourne 0

	def get_infos(self, indentation):
		"""
		enregistre le nouveaux parametres pour la suite
		retourne differentes informations
		- le nombre de colones
		- le numero de la colonne a afficher INT (de 0 a n)
		- les indentations a metre
		"""
		#lecture
		path = os.path.join(self.rep, "printer_infos.pk")						#chemin d'acces aux informations
		if os.path.exists(path):												#si des infos existes
			try:																#on prend des precautions car le fichier peut etre vide
				with open(path, "rb") as f:										#on va aller voir ce qu'elle disent
					dico = pickle.load(f)										#on lit donc ce qui y est inscrit
			except:																#si le fichier est vide
				dico = {None:{"numero":0, "alinea":0}}							#on pose une valeur par defaut
		else:																	#dans le cas ou le fichier n'existe pas encore
			dico = {None:{"numero":0, "alinea":0}}								#on initialise l'affichage
		#traitement
		dico[self.signature] = dico.get(self.signature, {"numero":len(dico), "alinea":0})#on recupere ou bien l'on initialise l'affichage propre a cet affichage
		nombre = len(dico)														#on recupere les informations
		numero = dico[self.signature]["numero"]									#le numero de la colone
		alinea = dico[self.signature]["alinea"]									#le indention a imediatment afficher
		dico[self.signature]["alinea"] = max(0, dico[self.signature]["alinea"]+indentation)#on se pre