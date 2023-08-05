#!/usr/bin/env python3
# -*- coding: utf-8 -

"""
C'est ici que ce trouve l'ensemble de tous les serveurs
Chaque objet contient differentes methodes:
	__init__(self, name, key, id):
		#'name' est l'identifiant humainement comprehenssible de ce serveur (STR)
		#'key' est le code d'acces au serveur, peut etre un objet en tout genre celon le besoins
		#'id' est un (INT), l'objet doit contenir self.id
		#signature = None pour un afichage dans les bonnes colones
	send(self, data, name, signature=None):
		#depose sur le serveur l'objet avec le nom 'name' (STR)
		#'data' est de type (BYTES)
	load(self, name, signature=None):
		#retourne la sequence de (BYTES) correspondant au fichier de nom 'name' (STR)
	remove(self, name, signature=None):
		#supprime du serveur le fichier associe au nom 'name' (STR)
	ls(self, signature=None):
		#retourne la liste de tous les noms de tous les fichiers (LIST)
	is_free(self, signature=None):
		#retourne True si le serveur n'est pas en pleine activitee

les erreurs ne doivent pas etre gerees ici: les blocs Try, Except sont deja inclus dans l'objet appelant
'signature' est n'importe quel objet qui permet d'identifier ce serveur pour qu'il soit unique, du point de vu de l'affichage
"""

import dropbox
import os
import raisin
import time

class Dropbox:
	"""
	lien vers dropbox
	"""
	def __init__(self, name, key, id):
		self.name = name
		self.access_token = key
		self.linked = False			#est True quand le serveur est bien connecte
		self.last_connection = 0	#date de la derniere tentative reussi de conection au serveur
		self.signature = None
		self.id = id
		self.free = True			#est True quand c'est libre

	def connect(self, signature=None):
		"""
		tente d'etablire une connection avec le serveur
		tout va se passer a la racine: '/'
		"""
		if self.linked and (self.last_connection+600 > time.time()):
			return
		with raisin.raisin.Signature(self, signature):
			try:
				with raisin.raisin.Printer("connection to "+self.name+"...", signature=self.signature):
					self.dbx = dropbox.Dropbox(self.access_token)				#on se lie theoriquement
					self.dbx.users_get_current_account()						#releve les informations du compte pour etre certain que la connection est bonne
					self.linked = True
					self.last_connection = time.time()
			except Exception as e:
				self.linked = False
				time.sleep(60)													#si la conection a echouee, on retentera plus tard
				raise e

	def send(self, data, name, signature=None):
		with raisin.raisin.Signature(self, signature):
			with raisin.Lock(self.name, timeout=600, signature=self.signature):
				self.connect()
				with raisin.raisin.Printer("sending to "+self.name+"...", signature=self.signature) as p:
					chunk_size = 1024*1024										#taille maximum de chaque petits paquets
					taille = len(data)											#c'est la taille totale du fichier
					if taille <= chunk_size:									#si on ne nous demande pas d'envoyer un trop gros objet
						self.dbx.files_upload(data, os.path.join("/", name))	#on l'envoi directement
					else:														#dans le cas ou il est un peu concequant
						upload_session_start_result = self.dbx.files_upload_session_start(b"")#on en ouvre un fichier vide
						cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id, offset=0)#que l'on va remplir petit a petit
						commit = dropbox.files.CommitInfo(os.path.join("/", name))#ce fichier est mis a la base
						for index in range(0, taille-chunk_size, chunk_size):	#pour chaque petit sous paquet
							cursor.offset = index								#on continue le fichier au bon endroit
							self.dbx.files_upload_session_append(data[index:index+chunk_size], cursor.session_id, cursor.offset)#on envoi le petit paquet
							p.show(str(round(100*index/taille, 1))+"%")
						cursor.offset = index+chunk_size
						self.dbx.files_upload_session_finish(data[cursor.offset:], cursor, commit)#on fait apparaitre le fichier dans dropbox

	def load(self, name, signature=None):
		"""
		deserialise l'objet '/name'
		'name' est donc le nom du fichier sur dropbox
		retourne l'objet en cas de reussite
		retourne None en cas d'erreur
		"""
		with raisin.raisin.Signature(self, signature):
			self.connect()
			with raisin.raisin.Printer("loading "+name+" from "+self.name+"...", signature=self.signature):
				data = self.dbx.files_download(os.path.join("/", name))[1].content
				return data

	def remove(self, name, signature=None):
		"""
		supprime le fichier '/name'
		'name' est donc le nom du fichier dans dropbox
		"""
		with raisin.raisin.Signature(self, signature):
			with raisin.Lock(self.name, timeout=60, signature=self.signature):
				self.connect()
				with raisin.raisin.Printer("deleted "+name+" from "+self.name+"...", signature=self.signature):
					self.dbx.files_delete(os.path.join("/", name))

	def ls(self, signature=None):
		"""
		retourne la liste de tous les dossier present sur dropbox
		quelqu'en soit leur nature
		"""
		with raisin.raisin.Signature(self, signature):
			self.connect()
			with raisin.raisin.Printer("get all name from "+self.name+"...", signature=self.signature):
				return [e.name for e in self.dbx.files_list_folder("").entries]

	def is_free(self, signature=None):
		with raisin.raisin.Signature(self, signature):
			return raisin.Lock(self.name, signature=self.signature).is_free()

servers = [
Dropbox("dropbox robin", "iLBBfZeySgAAAAAAAAAADuDdmpArERX2s_UwuulUAOMNDLjDh6MzzL9NVDUp3P7x", 1),
Dropbox("dropbox sylvain", "I5SSyJu4YeIAAAAAAAAVNwvsyPf7NRROs4BvKY6GcqWhYfnRPnBXNEpKFkYGszBH", 2),
Dropbox("dropbox louis", "ZJ9ccoM5wlAAAAAAAAAALfsexhJlBhuidc_t5_IIY5kFGikSars-KNnL9FTg85XP", 3),
Dropbox("dropbox winona", "n9a3sVc71GAAAAAAAAAAEuhu2Zjm-l0vFkde4lZ0x5QFI3c-Chiso-yz2f8PMwjp", 4)
]

