#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import base64
import bz2
import copy
try:
	import Crypto.Cipher.AES as AES
	import Crypto.Random
except ImportError:
	logging.warning("'Crypto' failed to import. They are no evailability to cipher and uncrypt datas.")
import datetime
import gzip
import hashlib
import imp
import inspect
import io
import json
import lzma
import math
import multiprocessing
import os
try:
	import cloudpickle as pickle
except:
	logging.warning("'cloudpickle' failed to import. Can generate serialisation problems")
	import pickle
try:
	import psutil
except ImportError:
	logging.warning("'psutil' failed to import. No access to memory and cpu usage informations.")
import raisin
import random
import re
import shutil
import signal
import socket
import sqlite3
import sympy
import sys
import tarfile
import threading
import time
import urllib.request
import uuid

class Garbage_collector:
	"""
	tente de supprimer le fichier temporaire au moment de la mort du programme
	"""
	def __init__(self, path):
		self.path = path		#chemin vers le fichier temporaire

	def __del__(self):
		print("deletion of tempory repository...")
		try:
			shutil.rmtree(self.path)
			print("\tsuccess!")
		except:
			print("\tfailure!")

class Global_var:
	"""
	cree une variable globale partageable entre differents processus
	"""
	def __init__(self, name, local=False, signature=None):
		self.name = name												#nom de la variable, son identifiant
		self.signature = signature
		self.local = local												#True pour un acces par toute cette machine seulement, False pour un acces via internet
		if not self.local:
			self.interim = Interim(self.signature)
			self.name_on_server = "global_var_"+self.interim.get_hash(self.name)
			self.server = self.choice_of_servers()
			
	def choice_of_servers(self):
		"""
		retourne un serveur
		ce serveur est en priorite celui qui contient la variable si elle existe
		sinon, il s'agit d'un serveur disponible
		"""
		for server in raisin.servers.servers:
			if self.name_on_server in server.ls(signature=self.signature):
				return server
		ident = self.interim.get_free_server()
		for server in raisin.servers.servers:
			if server.id == ident:
				return server

	def write(self, obj, signature=None):
		"""
		met dans la variable, l'objet 'obj'
		"""
		with Signature(self, signature):
			with Lock(id=self.name, priority=1, signature=self.signature):
				if self.local:
					with open(os.path.join(raisin.rep, self.name), "wb") as f:
						raisin.dump(obj, f, compresslevel=0)
				else:
					with self.interim.server_lock(self.server, timeout=3600):
						try:											#on va tenter de supprimer le boulot deja existant
							self.server.remove(self.name_on_server, signature=self.signature)#tentative de suppression
						except:
							pass
						self.server.send(serialize(obj, compresslevel=3, signature=self.signature), self.name_on_server, signature=self.signature)

	def read(self, signature=None):
		"""
		retourne la valeur de la variable
		"""
		with Signature(self, signature):
			with Lock(id=self.name, priority=0, signature=self.signature):
				if self.local:
					with open(os.path.join(raisin.rep, self.name), "rb") as f:
						return raisin.load(f)
				else:
					with self.interim.server_lock(self.server, timeout=600):
						return deserialize(self.server.load(self.name_on_server, signature=self.signature), signature=self.signature)

	def add(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.add(*args, **kwargs)
		self.write(var)
		return res

	def append(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.append(*args, **kwargs)
		self.write(var)
		return res
	
	def as_integer_ratio(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.as_integer_ratio(*args, **kwargs)
		self.write(var)
		return res

	def bit_length(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.bit_length(*args, **kwargs)
		self.write(var)
		return res

	def capitalize(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.capitalize(*args, **kwargs)
		self.write(var)
		return res

	def casefold(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.casefold(*args, **kwargs)
		self.write(var)
		return res
		
	def center(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.center(*args, **kwargs)
		self.write(var)
		return res

	def clear(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.clear(*args, **kwargs)
		self.write(var)
		return res

	def conjugate(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.conjugate(*args, **kwargs)
		self.write(var)
		return res

	def copy(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.copy(*args, **kwargs)
		self.write(var)
		return res

	def count(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.count(*args, **kwargs)
		self.write(var)
		return res

	def decode(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.decode(*args, **kwargs)
		self.write(var)
		return res

	def denominator(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.denominator(*args, **kwargs)
		self.write(var)
		return res

	def difference(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.difference(*args, **kwargs)
		self.write(var)
		return res

	def difference_update(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.difference_update(*args, **kwargs)
		self.write(var)
		return res

	def discard(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.discard(*args, **kwargs)
		self.write(var)
		return res

	def encode(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.encode(*args, **kwargs)
		self.write(var)
		return res

	def endswith(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.endswith(*args, **kwargs)
		self.write(var)
		return res	
	
	def expandtabs(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.expandtabs(*args, **kwargs)
		self.write(var)
		return res

	def extend(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.extend(*args, **kwargs)
		self.write(var)
		return res

	def find(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.find(*args, **kwargs)
		self.write(var)
		return res
	
	def format(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.format(*args, **kwargs)
		self.write(var)
		return res

	def format_map(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.format_map(*args, **kwargs)
		self.write(var)
		return res

	def fromhex(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.fromhex(*args, **kwargs)
		self.write(var)
		return res

	def from_bytes(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.from_bytes(*args, **kwargs)
		self.write(var)
		return res	

	def fromkeys(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.fromkeys(*args, **kwargs)
		self.write(var)
		return res

	def get(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.get(*args, **kwargs)
		self.write(var)
		return res

	def hex(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.hex(*args, **kwargs)
		self.write(var)
		return res

	def imag(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.imag(*args, **kwargs)
		self.write(var)
		return res

	def index(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.index(*args, **kwargs)
		self.write(var)
		return res

	def insert(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.insert(*args, **kwargs)
		self.write(var)
		return res

	def intersection(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.intersection(*args, **kwargs)
		self.write(var)
		return res

	def intersection_update(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.intersection_update(*args, **kwargs)
		self.write(var)
		return res

	def isalnum(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isalnum(*args, **kwargs)
		self.write(var)
		return res

	def isalpha(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isalpha(*args, **kwargs)
		self.write(var)
		return res
	
	def isdecimal(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isdecimal(*args, **kwargs)
		self.write(var)
		return res

	def isdigit(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isdigit(*args, **kwargs)
		self.write(var)
		return res

	def isdisjoint(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isdisjoint(*args, **kwargs)
		self.write(var)
		return res

	def isidentifier(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isidentifier(*args, **kwargs)
		self.write(var)
		return res

	def is_integer(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.is_integer(*args, **kwargs)
		self.write(var)
		return res

	def islower(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.islower(*args, **kwargs)
		self.write(var)
		return res

	def isnumeric(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isnumeric(*args, **kwargs)
		self.write(var)
		return res
			
	def isprintable(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isprintable(*args, **kwargs)
		self.write(var)
		return res

	def isspace(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isspace(*args, **kwargs)
		self.write(var)
		return res

	def issubset(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.issubset(*args, **kwargs)
		self.write(var)
		return res
	
	def istitle(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.istitle(*args, **kwargs)
		self.write(var)
		return res
	
	def isupper(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.isupper(*args, **kwargs)
		self.write(var)
		return res
	
	def items(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.items(*args, **kwargs)
		self.write(var)
		return res

	def join(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.join(*args, **kwargs)
		self.write(var)
		return res
	
	def keys(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.keys(*args, **kwargs)
		self.write(var)
		return res

	def ljust(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.ljust(*args, **kwargs)
		self.write(var)
		return res

	def lower(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.lower(*args, **kwargs)
		self.write(var)
		return res

	def lstrip(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.lstrip(*args, **kwargs)
		self.write(var)
		return res

	def maketrans(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.maketrans(*args, **kwargs)
		self.write(var)
		return res

	def numerator(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.numerator(*args, **kwargs)
		self.write(var)
		return res

	def partition(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.partition(*args, **kwargs)
		self.write(var)
		return res		

	def pop(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.pop(*args, **kwargs)
		self.write(var)
		return res

	def popitem(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.popitem(*args, **kwargs)
		self.write(var)
		return res

	def real(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.real(*args, **kwargs)
		self.write(var)
		return res

	def remove(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.remove(*args, **kwargs)
		self.write(var)
		return res

	def replace(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.replace(*args, **kwargs)
		self.write(var)
		return res
	
	def rfind(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.rfind(*args, **kwargs)
		self.write(var)
		return res

	def rindex(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.rindex(*args, **kwargs)
		self.write(var)
		return res
	
	def rjust(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.rjust(*args, **kwargs)
		self.write(var)
		return res

	def rpartition(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.rpartition(*args, **kwargs)
		self.write(var)
		return res

	def rsplit(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.rsplit(*args, **kwargs)
		self.write(var)
		return res

	def rstrip(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.rstrip(*args, **kwargs)
		self.write(var)
		return res

	def setdefault(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.setdefault(*args, **kwargs)
		self.write(var)
		return res

	def sort(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.sort(*args, **kwargs)
		self.write(var)
		return res

	def split(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.split(*args, **kwargs)
		self.write(var)
		return res

	def splitlines(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.splitlines(*args, **kwargs)
		self.write(var)
		return res

	def startswith(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.startswith(*args, **kwargs)
		self.write(var)
		return res

	def strip(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.strip(*args, **kwargs)
		self.write(var)
		return res

	def swapcase(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.swapcase(*args, **kwargs)
		self.write(var)
		return res

	def symmetric_difference(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.symmetric_difference(*args, **kwargs)
		self.write(var)
		return res

	def symmetric_difference_update(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.symmetric_difference_update(*args, **kwargs)
		self.write(var)
		return res

	def title(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.title(*args, **kwargs)
		self.write(var)
		return res

	def to_bytes(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.to_bytes(*args, **kwargs)
		self.write(var)
		return res

	def translate(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.translate(*args, **kwargs)
		self.write(var)
		return res

	def union(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.union(*args, **kwargs)
		self.write(var)
		return res

	def update(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.update(*args, **kwargs)
		self.write(var)
		return res

	def upper(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.upper(*args, **kwargs)
		self.write(var)
		return res

	def values(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.values(*args, **kwargs)
		self.write(var)
		return res

	def zfill(self, *args, **kwargs):
		var = self.read(kwargs.get("signature", self.signature))
		res = var.zfill(*args, **kwargs)
		self.write(var)
		return res

class Interim:
	"""
	gere la base de donnee
	qui recence les offres d'emploi et leurs informations relatives
	"""
	def __init__(self, signature=None):
		"""
		'father' est l'objet qui contient une methode
		'rep' est le repertoire courant
		show() et sign()
		"""
		self.signature = signature										#pour une meilleure gestion de l'affichage
		self.bdd = self.connect()										#on se connecte a la base de donnee
		self.servers = []												#c'est la liste des objets serveur comme Dropbox, Local...
		self.id = raisin.id												#l'identifiant de ce processus
		self.errors = self.get_autorize_errors()						#la liste des erreurs legere, qui n'ont pas lieu sur toutes les machines
		self.servers_list = raisin.servers.servers						#la liste 'melange' des serveurs qui permet une bonne repartition du boulot
		random.shuffle(self.servers_list)								#on melange la liste

	def add_arg(self, arg_hash, arg, compresslevel, signature=None):
		"""
		ajoute une ligne dans la table 'arg'
		en faisant tout de meme quelques verifications
		'arg' est brute, pas de serialisation
		"""
		with Signature(self, signature):
			with Printer("add argument data...", signature=self.signature) as p:#on dit ce que l'on fait
				with Printer("is it existing?...", signature=self.signature):#avant, on fait une verification qui permet d'eviter les doublons
					arg_path = os.path.join(raisin.rep, arg_hash+".rais")	#path du fichier suceptible de comporter les datas de cet argument
					lock = Lock(id="bdd", signature=self.signature)			#creation d'un objet 'verrou'
					lock.acquire()											#pose d'un verrou afin de ne pas creer plus de probleme
					curseur = self.bdd.cursor()								#creation d'un lien vers la base
					curseur.execute("""SELECT compresslevel FROM arg WHERE arg_hash=?""",(arg_hash,))#on prepare la recherche
					requette = curseur.fetchall()							#c'est ici qu'on la lance
					if len(requette) != 0:									#si le resultat est fructueux
						p.show("yes", 0)									#alors l'utilisateur en profite
						with Printer("with same compression?...", signature=self.signature):#il est donc temps de regarder si la compression est la meme
							if compresslevel > requette[0][0]:				#si la compression proposee est meilleur
								p.show("no", 0)								#l'utilisateur est prevenu de l'incident
								with Printer("update argument...", signature=self.signature):#mise a jour de la bonne ligne
									lock.release()							#pour cela, on libere l'acces
									arg_gener = serialize(arg, compresslevel=compresslevel, generator=True, signature=self.signature)
									self.save(self.generateur(arg_gener), arg_path)#le temps d'ecrire le fichier
									lock.acquire()							#bien sur, on le reprend juste apres
									curseur = self.bdd.cursor()				#connection a la base
									curseur.execute("""UPDATE arg SET compresslevel=? WHERE arg_hash=?""",(compresslevel, arg_hash))#preparation de la mise a jour
							else:											#si la compression proposee n'est pas meilleure
								p.show("yes", 0)							#ce n'est pas bien grave
					else:													#si cet emploi n'a aucune chance d'exister
						p.show("no", 0)										#l'ajout d'une nouvelle ligne semble obligatoire
						with Printer("add ligne...", signature=self.signature):#afin de le faire patienter
							lock.release()									#pour cela, on libere l'acces
							if not os.path.exists(arg_path):				#si le fichier n'existe pas
								arg_gener = serialize(arg, compresslevel=compresslevel, generator=True, signature=self.signature)
								self.save(self.generateur(arg_gener), arg_path)#le temps d'ecrire le fichier
							lock.acquire()									#bien sur, on le reprend juste apres
							curseur = self.bdd.cursor()						#creation d'un pointeur vers la base
							curseur.execute("""INSERT INTO arg
								(arg_hash, compresslevel)
							VALUES (?,?)""",(arg_hash, compresslevel))		#ajout de ligne
				self.bdd.commit()											#passage a l'acte des operations
				lock.release()												#liberation du verrou

	def add_interim(self, job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker, signature=None):
		"""
		ajoute une ligne dans la table 'interim'
		ne se pose aucune question et ajoute la ligne
		blacklisted, args_hash et error, reicevers et worker sont des objets python non serialises
		retourne la 'sending_date'
		"""
		with Signature(self, signature):
			with Printer("add interim...", signature=self.signature):			#on dit ce que l'on fait
				blacklisted = serialize(blacklisted, compresslevel=0, signature=self.signature, generator=False)#on serialise 'blacklisted'
				args_hash = serialize(args_hash, compresslevel=0, signature=self.signature, generator=False)#de meme pour 'args_hash'
				error = serialize(error, compresslevel=0, signature=self.signature, generator=False)#de meme pour 'errors'
				receivers = serialize(receivers, compresslevel=0, signature=self.signature, generator=False)#de meme pour 'receivers'
				worker = serialize(worker, compresslevel=0, signature=self.signature, generator=False)
				with Lock(id="bdd", signature=self.signature):					#pose d'un verrou afin de ne pas creer plus de probleme
					if state == "waiting":										#si on depose ce travail pour la premiere fois
						with Printer("is it existing...", signature=self.signature) as p:#verification que ce boulot n'existe pas deja
							curseur = self.bdd.cursor()							#lien vers la base
							req = list(curseur.execute("""SELECT sending_date FROM interim WHERE job_hash=? and args_hash=?""",(job_hash, args_hash)))
							if req == []:										#si ce boulot n'est pas encore sur le marche
								p.show("no", 0)									#on dit qu'il ne l'est pas
								with Printer("create interim job...", signature=self.signature):
									curseur = self.bdd.cursor()					#creation d'un pointeur vers la base
									curseur = curseur.execute("""INSERT INTO interim
										(job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker)
									VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",(job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker))
									self.bdd.commit()							#passage a l'acte
							else:												#s'il existe deja
								p.show("yes", 0)								#on ne fait rien de particulier
								sending_date = req[0][0]						#sauf a se rememorer la bonne ligne
					else:														#a l'inverse, si il s'agit d'un resultat
						with Printer("update interim...", signature=self.signature):
							curseur = self.bdd.cursor()							#connection a la base
							curseur.execute("""UPDATE interim SET job_hash=?, args_hash=?, res_hash=?, state=?, blacklisted=?, timeout=?, last_support=?, error=?, server_id=?, receivers=?, display=?, worker=? WHERE sending_date=?""",(job_hash, args_hash, res_hash, state, blacklisted, timeout, last_support, error, server_id, receivers, display, worker, sending_date))
							self.bdd.commit()									#validation de cette mise a jour
			return sending_date

	def add_job(self, job_hash, target, modules, compresslevel, job_timeout, signature=None):
		"""
		ajoute une ligne dans la table 'job'
		en faisant tout de meme quelques verifications
		'modules' est un dictionaire non serialise
		'target' est le code source non serialise
		"""
		with Signature(self, signature):
			with Printer("add job data...", signature=self.signature) as p:		#on dit ce que l'on fait
				with Printer("is it existing?...", signature=self.signature):	#avant, on fait une verification qui permet d'eviter les doublons
					lock = Lock(id="bdd", signature=self.signature)				#creation d'un objet 'verrou'
					lock.acquire()												#pose d'un verrou afin de ne pas creer plus de probleme
					curseur = self.bdd.cursor()									#creation d'un lien vers la base
					curseur.execute("SELECT compresslevel FROM job WHERE job_hash = ?",(job_hash,))#on prepare la recherche
					requette = curseur.fetchall()								#c'est ici qu'on la lance
					if len(requette) != 0:										#si le resultat est fructueux
						p.show("yes", 0)										#alors l'utilisateur en profite
						with Printer("with same compression?...", signature=self.signature):#il est donc temps de regarder si la compression est la meme
							if compresslevel > requette[0][0]:					#si la compression proposee est meilleur
								p.show("no", 0)									#l'utilisateur est prevenu de l'incident
								with Printer("update job...", signature=self.signature):#mise a jour de la bonne ligne
									lock.release()								#pour cela, on libere l'acces
									target = serialize(target, generator=False, compresslevel=compresslevel, signature=self.signature)
									modules = serialize(modules, generator=False, compresslevel=compresslevel, signature=self.signature)
									lock.acquire()								#bien sur, on le reprend juste apres
									curseur = self.bdd.cursor()					#connection a la base
									curseur.execute("""UPDATE job SET target=?, modules=?, job_timeout=?, compresslevel=? WHERE job_hash = ?""",(target, modules, job_timeout, compresslevel, job_hash))#preparation de la mise a jour
							else:												#si la compression proposee n'est pas meilleur
								p.show("yes",0)									#ce n'est pas bien grave
					else:														#si cette emploi n'a aucune chance d'exister
						p.show("no", 0)											#l'ajout d'une nouvelle ligne semble obligatoire
						with Printer("add ligne...", signature=self.signature):#afin de le faire patienter
							lock.release()										#pour cela, on libere l'acces
							target = serialize(target, generator=False, compresslevel=compresslevel, signature=self.signature)#le temps d'ecrir le fichier
							modules = serialize(modules, generator=False, compresslevel=compresslevel, signature=self.signature)#serialisation du dictionnaire
							lock.acquire()										#bien sur, on le reprend juste apres
							curseur = self.bdd.cursor()							#creation d'un pointeur vers la base
							curseur.execute("""INSERT INTO job
								(job_hash, target, modules, compresslevel, job_timeout)
							VALUES (?,?,?,?,?)""",(job_hash, target, modules, compresslevel, job_timeout))#ajout de ligne
				self.bdd.commit()												#passage a l'acte des operations
				lock.release()													#liberation du verrou

	def add_res(self, res_hash, res, compresslevel, signature=None):
		"""
		ajoute une ligne dans la table 'res'
		en faisant tout de meme quelques verifications
		'res' est de type 'byte' ou bien est un generateur ou un fichier binaire en mode lecture
		ne retourne rien
		"""	
		with Signature(self, signature):
			with Printer("add result data...", signature=self.signature) as p:#on dit ce que l'on fait
				with Printer("is it existing?...", signature=self.signature):#avant, on fait une verification qui permet d'eviter les doublons
					res_path = os.path.join(raisin.rep, res_hash+".rais")	#path du fichier suceptible de comporter les datas de ce resultat
					lock = Lock(id="bdd", signature=self.signature)			#creation d'un objet 'verrou'
					lock.acquire()											#pose d'un verrou afin de ne pas crer plus de probleme
					curseur = self.bdd.cursor()								#creation d'un lien vers la base
					curseur.execute("""SELECT compresslevel FROM res WHERE res_hash=? """,(res_hash,))#on prepare la recherche
					requette = curseur.fetchall()							#c'est ici qu'on la lance
					if len(requette) != 0:									#si le resultat est fructueux
						p.show("yes", 0)									#alors l'utilisateur en profite
						with Printer("with same compression?...", signature=self.signature):#il est donc temps de regarder si la compression est la meme
							if compresslevel > requette[0][0]:				#si la compression proposee est meilleur
								p.show("no", 0)								#l'utilisateur est prevenu de l'incident
								with Printer("update result...", signature=self.signature):#mise a jour de la bonne ligne
									lock.release()							#pour cela, on libere l'acces
									self.save(self.generateur(res_gener), res_path)#le temps d'ecrir le fichier
									lock.acquire()							#bien sur, on le reprend juste apres
									curseur = self.bdd.cursor()				#connection a la base
									curseur.execute("""UPDATE res SET compresslevel=? WHERE res_hash=?""",(compresslevel, res_hash))#preparation de la mise a jour
							else:											#si la compression proposee n'est pas meilleur
								p.show("yes", 0)							#ce n'est pas bien grave
					else:													#si cet emploi n'a aucune chance d'exister
						p.show("no", 0)										#l'ajout d'une nouvelle ligne semble obligatoire
						with Printer("add ligne...", signature=self.signature):#afin de le faire patienter
							lock.release()									#pour cela, on libere l'acces
							if not os.path.exists(res_path):				#si le fichier n'existe pas
								self.save(self.generateur(res), res_path)	#le temps d'ecrir le fichier
							lock.acquire()									#bien sur, on le reprend juste apres
							curseur = self.bdd.cursor()						#creation d'un pointeur vers la base
							curseur.execute("""INSERT INTO res
								(res_hash, compresslevel)
							VALUES (?,?)""",(res_hash, compresslevel))		#ajout de ligne
				self.bdd.commit()											#passage a l'acte des operations
				lock.release()												#liberation du verrou

	def add_server(self, name, key, category, signature=None):
		"""
		ajoute un nouveau server dans la base de donnee
		'key' est de n'import quel type
		"""
		with Signature(self, signature):
			key = serialize(key, compresslevel=0, signature=self.signature, generator=False)#la clef est serialisee de suite
			with Lock(id="bdd", signature=self.signature):					#monopolisation de la base de donnee													#mise en place d'un verrou
				with Printer("add server...", signature=self.signature):	#afin d'ajouter des informations sans probleme
					curseur = self.bdd.cursor()								#creation d'un lien vers la base de donnees
					curseur.execute("""INSERT INTO server
						(name, key, category, state, last_support)
					VALUES (?,?,?,?,?)""",(name, key, category, "waiting", 0))
					self.bdd.commit()										#validation de ce nouveau changement

	def connect(self, signature=None):
		"""
		se connecte a la base de donnee
		TABLE interim:
			id INT PRIMARY KEY			#l'identifiant incremente automatiquement
			job_hash STR				#la somme bit du travail (sans les arguments) (juste le code source)
			args_hash BLOB				#la liste des sommes bit des arguments
			res_hash STR				#identifiant du resultat
			state STR					#{'waiting':"en attente de traitement", 'working':"en cours d'execution", 'fail':"a echoue comme une baleine", 'finish':"est termine"}
			blacklisted BLOB			#liste des identifiants des ordinateurs ayant echoue et le message d'erreur
			timeout INT					#temps total acceptable en secondes depuis l'envoi jusqu'a la reception [intervalle]
			sending_date INT			#date de creation de cet emploi
			last_support INT			#date de la derniere tentative de prise en charge
			error BLOB					#la derniere erreur qui on en fait echouer certains
			server_id INT				#identifiant du serveur dans la table 'server' (0 si non attribue ou local)
			receivers BLOB				#ordinateurs specialement cibles par ce travail
			display STR					#affichage du resultat
			worker BLOB					#ordinateur ayant resolu ce travail
		TABLE job						#la table qui contient les programmes a executer sans les arguments
			id INT PRIMARY KEY			#la premiere ligne, on ne peut pas s'en passer
			job_hash STR				#l'identifiant du resultat non compresse
			target BLOB					#le gros code a executer seralise
			modules BLOB				#les modules dont ce code a besoin pour fonctionner
			compresslevel INT			#taux de compression du travail
			job_timeout INT				#temps d'execution maximum acceptable en seconde
		TABLE res						#la table qui contient les resultats
			id INT PRIMARY KEY			#la premiere ligne, on ne peut pas s'en passer
			res_hash STR				#l'identifiant du resultat non compresse
			compresslevel INT			#taux de compression de la serialisation
			res_data BLOB				#le resultat compresser si il n'est pas tres gros
		TABLE arg						#la table qui contient les parametres
			id INT PRIMARY KEY			#la premiere ligne, on ne peut pas s'en passer
			arg_hash STR				#hash propre a cet argument
			compresslevel INT			#taux de compression
			arg_data BLOB				#contenu de l'argument si il n'est pas trop gros		
		"""
		with Signature(self, signature):
			with Printer("connection to the dataset...", signature=self.signature):#on annonce ce que l'on fait
				self.bdd = sqlite3.connect(os.path.join(raisin.rep, "raisin_dataset.db"))#on se connecte a la base de donnees (ou on la cree)
				with Printer("is it existing?...", signature=self.signature) as p:
					curseur = self.bdd.cursor()									#nous allons verifier qu'il s'agit bien de la bonne base de donnee
					curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")#pour cela, on regarde les tables qu'elle contient
					liste = curseur.fetchall()									#on execute la commande, c'est a dire qu'on lance la recherche
					if liste == [("interim",), ("job",), ("res",), ("arg",)]:#si la base contient les bonnes tables
						p.show("yes", 0)										#on dit que c'est bon
					else:
						p.show("no", 0)
						with Printer("creation of dataset...", signature=self.signature):#nous allons donc creer les bonnes tables
							self.bdd.execute("""CREATE TABLE interim
								(id INTEGER PRIMARY KEY,
								job_hash STR,
								args_hash BLOB,
								res_hash STR,
								state STR,
								blacklisted BLOB,
								timeout INT,
								sending_date INT,
								last_support INT,
								error BLOB,
								server_id INT,
								receivers BLOB,
								display STR,
								worker BLOB)""")
							self.bdd.execute("""CREATE TABLE job
								(id INTEGER PRIMARY KEY,
								job_hash STR,
								target BLOB,
								modules BLOB,
								compresslevel INT,
								job_timeout INT)""")
							self.bdd.execute("""CREATE TABLE res
								(id INTEGER PRIMARY KEY,
								res_hash STR,
								compresslevel INT,
								res_data BLOB)""")
							self.bdd.execute("""CREATE TABLE arg
								(id INTEGER PRIMARY KEY,
								arg_hash STR,
								compresslevel INT,
								arg_data BLOB)""")
							self.bdd.commit()									#enregistrement de ces changements
			return self.bdd

	def del_arg(self, arg_hash, signature=None):
		"""
		supprime la ligne dans la table 'arg'
		ne supprime pas les dependances mais seulement l'argument
		"""
		with Signature(self, signature):
			with Printer("deleting arg...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):				#on pose le verrou
					curseur = self.bdd.cursor()								#connection a la base de donnee
					curseur.execute("DELETE FROM arg WHERE arg_hash=?",(arg_hash,))#supression de la ligne
					self.bdd.commit()										#validation de cette suppression
				try:														#on tente de le supprimer
					os.remove(os.path.join(raisin.rep, "arg_"+arg_hash+".rais"))#mais on prend des precautions
				except:														#dans le cas ou il l'est deja
					pass

	def del_interim(self, sending_date, signature=None):
		"""
		supprime simplement cette ligne dans la table 'interim'
		"""
		with Signature(self, signature):
			with Printer("deleting interim...", signature=self.signature):
				with Lock("bdd", signature=self.signature):					#on pose le verrou
					curseur = self.bdd.cursor()								#connection a la base de donnee
					curseur.execute("DELETE FROM interim WHERE sending_date=?",(sending_date,))#supression de la ligne
					self.bdd.commit()

	def del_job(self, job_hash, signature=None):
		"""
		supprime la ligne dans la table 'job'
		"""
		with Signature(self, signature):
			with Printer("deleting job...", signature=self.signature):
				with Lock("bdd", signature=self.signature):					#on pose le verrou
					curseur = self.bdd.cursor()								#connection a la base de donnee
					curseur.execute("DELETE FROM job WHERE job_hash=?",(job_hash,))#supression de la ligne
					self.bdd.commit()

	def del_res(self, res_hash, signature=None):
		"""
		supprime la ligne dans la table 'job'
		"""
		with Signature(self, signature):
			with Printer("deleting result...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):				#on pose le verrou
					curseur = self.bdd.cursor()								#connection a la base de donnee
					curseur.execute("DELETE FROM res WHERE res_hash=?",(res_hash,))#supression de la ligne
					self.bdd.commit()
				try:
					os.remove(os.path.join(raisin.rep, "res_"+res_hash+".rais"))
				except:
					pass

	def del_server(self, identifiant, signature=None):
		"""
		supprime simplement cette ligne dans la table 'interim'
		"""
		with Signature(self, signature):
			with Printer("deleting server...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):					#on pose le verrou
					curseur = self.bdd.cursor()									#connection a la base de donnee
					curseur.execute("DELETE FROM server WHERE id=?",(identifiant,))#supression de la ligne
					self.bdd.commit()

	def emission(self, server_id, interim, job, args, signature=None):
		"""
		va chercher du travail dans la base de donne pour l'exposer dans le serveur
		'server_id' est l'identifiant du serveur qui va recuperer ce boulot
		'interim, job, args' sont les elements a envoyer
		ne retourne rien et affiche tout dans la colone principale (la courante)
		"""
		def send_employement(interim, job, args):
			"""
			poste cet emploi et retourne la nouvelle liste 'elements'
			'elements' est la liste des nom de tous les fichiers presents sur le serveur
			"""
			elements = server.ls()
			with Printer("send employement...", signature=self.signature) as p:
				for n, arg in enumerate(args):							#on commence par envoyer les arguments pour ne pas creer de conflit
					with Printer("send arg n°"+str(n)+"...", signature=self.signature):
						chunk_size = 1024*1024							#c'est la taille des paquets en octet
						
						arg["chunk_size"] = chunk_size					#cette taille est enregistree dans les parametres
						file = open(os.path.join(raisin.rep, arg["arg_hash"]+".rais"), "rb")#on fait un lien avec le fichier
						size = os.path.getsize(os.path.join(raisin.rep, arg["arg_hash"]+".rais"))#c'est la taille du fichier en octet pour l'affichage du pourcentage
						arg["torrent"] = []								#va contenir le nom de tous les sous-paquets
						data = file.read(chunk_size)					#lecture du fichier (partiellement)
						i = 0											#initialisation du compteur pour le poucentage
						while data != b"":								#tant que le fichier n'est pas entierement lu
							purcent = i*100*chunk_size//size			#le pourcentage d'envoi
							p.show(str(purcent)+"%", 0)					#est afficher pour faire pascienter
							data_hash = self.get_hash(data)				#on recupere la signature pour en faire un nom
							name = "arg_fragment&"+data_hash			#creation du nom a utiliser
							if not name in elements:					#si ce fichier n'existe pas deja
								while server.send(data, name, signature=self.signature):#affin de pouvoir l'envoyer
									server.remove(name, signature=self.signature)#tant que l'envoi ne fonctionne pas, on s'y acharne
								elements.append(name)					#quand l'envoi est termine, on s'en souvient pour eviter les doublons						
							arg["torrent"].append(name)					#on ajoute le nom de ce fichier affin qu'il soit replacer au bon endroit
							data = file.read(chunk_size)				#lecture de la suite du fichier
							i+=1										#incrementation du compteur
						name = "arg&"+arg["arg_hash"]					#voila le nom du fichier qui gere tous les autres
						if not name in elements:						#si ces metadatas ne figurent nule part
							data = serialize(arg, compresslevel=0, signature=self.signature, generator=False)#serialisation de l'argument
							while server.send(data, name, signature=self.signature):#afin de pouvoir l'envoyer
								server.remove(name, signature=self.signature)#tant que l'envoi ne fonctionne pas, on s'y acharne
							elements.append(name)						#quand l'envoi est termine, on s'en souvient pour eviter les doublons

				with Printer("send surce code...", signature=self.signature):
					job_hash = job["job_hash"]							#extraction de l'invariant dans le code a executer
					name = "job&"+str(job_hash)							#c'est le nom qui apparetra dans le serveur
					if not name in elements:							#si il ne se trouve pas deja sur le serveur
						data = serialize(job, compresslevel=0, signature=self.signature, generator=False)#il est necessaire de serialiser le 'job'
						while server.send(data, name, signature=self.signature):#afin de pouvoir le poster
							server.remove(name, signature=self.signature)#on insiste lourdement
						elements.append(name)							#pour que la lettre passe

				with Printer("send interim...", signature=self.signature):
					name = "interim&"+str(interim["sending_date"])		#pour le caracteriser, on le nome par sa date de creation
					if not name in elements:							#si ce travail n'existe pas sur le serveur
						data = serialize(interim, compresslevel=0, signature=self.signature, generator=False)
						while server.send(data, name, signature=self.signature):
							server.remove(name, signature=self.signature)
						elements.append(name)

				return elements

		with Signature(self, signature):
			with Printer("emission...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):				#on pose le verrou
					curseur = self.bdd.cursor()								#nous allons recuperer les informations
					((ident, name, key, category),) = curseur.execute("""SELECT id, name, key, category FROM server WHERE id=?""",(server_id,))#qui permettent de se conecter au serveur
					key = deserialize(key, signature=self.signature)
					if category == "dropbox":								#si il s'agit d'un serveur dropbox
						server = raisin.servers.Dropbox(name, key, ident, signature=self.signature)#on cree un serveur dropbox
					elif category == "local":								#si il s'agit d'une repartition sur un disque local
						server = raisin.servers.Local(name, key, ident, signature=self.signature)#on ajoute ce serveur dans la liste
					else:													#si le serveur demande n'existe pas
						raise Exeption(str(category)+" server is not existing... Only 'dropbox' or 'local'!")#on retourne une erreur
				send_employement(interim, job, args)						#tentative d'envoi du travail
				return None													#rien n'est retourne

	def generateur(self, data, signature=None):
		"""
		genere les donnees par paquets comme elle arrivent
		'data' peut etre un fichier binaire en mode lecture ou une sequence de bytes ou in generateur
		"""
		with Signature(self, signature):
			with Printer("creation of generator...", signature=self.signature):
				if type(data) == io.BufferedReader:								#s'il s'agit d'un pointeur vers un fichier
					while 1:													#on retourne tout petit a petit
						pack = data.read(10**7)									#on lit la suite
						if pack == b"":											#si tout le fichier est lu
							break												#on arrette la
						yield pack												#sinon on retourne le petit bout de fichier que l'on vient de lire
				elif type(data) == bytes:										#si les donnees sont directement en binaire
					yield data													#c'est le plus simple pour nous
				else:															#si il s'agit d'un generateur
					for pack in data:											#on va directement le vider
						yield pack												#petit a petit

	def get_answer(self, sending_date, signature=None, boucle=0):
		"""
		'boucle' et une variable qui permet de limiter la recursivitee
		retourne le resultat si il est arrive
		retourne {} si il n'y a rien
		"""
		with Signature(self, signature):
			with Printer("answer recovery...", signature=self.signature):	#recuperation des resultats
				with Lock(id="bdd", signature=self.signature):				#pose d'un verrou afin de ne pas creer plus de probleme
					curseur = self.bdd.cursor()								#creation d'un pointeur vers la base
					req = list(curseur.execute("""SELECT * FROM interim WHERE sending_date=?""",(sending_date,)))#preparation de la requette
				for ident, job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker in req:			
					if state == "finish":									#si le boulot est arrive et qu'il contient une erreur
						resultat = {}										#initialisation du resultat
						resultat["state"] = "finish"						#on donne des infos sur la reussite ou non
						with open(os.path.join(raisin.rep, res_hash+".rais"), "rb") as f:
							resultat["result"] = deserialize(self.generateur(f, signature=self.signature), signature=self.signature)
						resultat["worker"] = deserialize(worker, signature=self.signature)
						resultat["blacklisted"] = deserialize(blacklisted, signature=self.signature)
						resultat["display"] = display
						return resultat
					elif state == "fail":
						resultat = {}
						resultat["state"] = "fail"
						resultat["worker"] = deserialize(worker, signature=self.signature)
						resultat["error"] = deserialize(error, signature=self.signature)
						resultat["blacklisted"] = deserialize(blacklisted, signature=self.signature)
						resultat["display"] = display
						return resultat
					elif boucle != 0:										#si le resultat n'est pas la alors qu'on vien de tenter de le recuperer
						return {}											#on retourne le None du 'j'ai rien trouve!'
					else:													#si le resultat n'est pas encore arrive
						for server in self.mk_link():						#on va tenter de le prendre directement sur le serveur
							if server.id == server_id:						#on ne regarde que sur le serveur qui nous concerne directement
								self.reception(server, signature=self.signature)#tentative de recuperation du resultat
								return self.get_answer(sending_date, boucle=1)#on regarde si il est arrive
		return {}

	def get_autorize_errors(self):
		"""
		retourne la liste des erreurs autorise par les differents ouvriers
		"""
		liste = [
			KeyboardInterrupt,\
			IOError,\
			OSError,\
			ImportError,\
			MemoryError,\
				]
		return liste

	def get_free_server(self, signature=None):
		"""
		la base de donnee doit etre libre car ne demande pose pas de verrou explicite
		retourne le numero du serveur le moins surbouque
		"""
		with Signature(self, signature):														#pour que tout ce qui s'affine apres s'affiche au bon endroit
			with Printer("choice of best server...", signature=self.signature):					#on va choisir le serveur le plus disponible
				while 1:																		#renvoi de cet identifiant
					for i, server in enumerate(self.servers_list):								#pour chaque serveur
						if not self.is_lock(server, signature=self.signature):					#si il est disponible
							self.servers_list.append(self.servers_list.pop(i))					#pour que l'on n'envoi pas toujours sur le meme serveur
							return server.id													#on retourne son identifiant
						time.sleep(1)															#on ne se precipie pas

	def get_hash(self, objet, signature=None):
		"""
		retourne le hash de l'objet
		"""
		with Signature(self, signature):
			with Printer("hash recovery...", signature=self.signature):		#on dit ce que l'on s'apprete a faire
				if type(objet) == bytes:									#si le fichier est deja de type 'bytes'
					return hashlib.md5(objet).hexdigest()					#il est inutile de le serialiser
				if (len(str(objet)) < 32767):								#on prend des precaution pour windaube
					if os.path.isfile(str(objet)):							#si l'objet est un fichier
						size = os.path.getsize(str(objet))					#on recupere sa dimension
						with open(str(objet), "rb") as file:				#on regarde le debut du fichier
							debut = hashlib.md5(file.read(10**7)).hexdigest()#et on signe ce debut
						return self.get_hash(str(size)+debut)				#on fait un melange des 2
				if os.path.isdir(str(objet)):								#si l'objet est un repertoire
					somme = ""												#nous allons verifier chaque dossier
					for parent, dossiers, fichiers in os.walk(str(objet)):	#on parcours tout l'arbre
						for fichier in fichiers:							#chaque fichier est analise
							somme+=self.get_hash(os.path.join(parent, fichier))#on memorise le contenu de chaque fichier
							somme+=fichier									#et le nom de chaque fichier
					return self.get_hash(somme)								#on fait un gros melange de tout ca
				if type(objet) == str:										#si l'objet est une chaine de caractere
					return self.get_hash(objet.encode("utf-8"))				#on le converti en binaire
				if type(objet) == int:										#si c'est un entier
					return self.get_hash(str(objet))						#il est converti en str	
				else:														#dans le cas, ou il n'est rien de tout cela
					return self.get_hash(serialize(objet, compresslevel=0, signature=self.signature, generator=False))#on le serialise

	def get_work(self, server_id=0, signature=None):
		"""
		'server_id' est l'identifiant du serveur qui fait cette demande
		retourne des elements distincts serialises
		1-interim (dict)
		2-job (dict)
		3-[info_arg (dict)] (list)
		retourne (None, None, None) si il n'y a rien a faire
		"""
		def get_interim(server_id):
			"""
			retourne la bonne ligne de la table 'interim'
			met a jour la table au passage
			si rien n'est pertinent, un 'None' est retourne a la place d'un tuple
			"""
			def check_size(args_hash, curseur):
				"""
				retourne le nombre d'octets que prend la somme des
				arguments
				"""
				somme = 0
				for arg_hash in args_hash:
					req = curseur.execute("SELECT arg FROM arg WHERE arg_hash = ?", (arg_hash,))
					for arg in req:
						try:
							path_file = os.path.join(self.rep, arg[0])
							somme += os.path.getsize(path_file)
						except:
							pass
				return somme

			with Printer("choice of employment...", signature=self.signature) as p:
				with Lock(id="bdd", signature=self.signature):			#on prend la main
					curseur = self.bdd.cursor()							#creation d'un lien vers la base de donnee
					petit_last_support = time.time()					#c'est la date du plus ancien emploi, le plus oublie de tous
					for etat in ["waiting", "working"]:					#la priorite, c'est ceux qui sont tout seul
						for num in range(3):							#on procede par contrainte de plus en plus laxistes
							req = curseur.execute("SELECT * FROM interim WHERE state=?",(etat,))#on prend en priorite ceux qui ne sont pas encore pris en charge
							for ident, job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker in req:
								if num == 0:							#la premiere passe est reservee
									petit_last_support = min(petit_last_support, last_support)#a la recherche du plus ancien boulot
								if ((server_id != server) or (server_id == 0) or (num >= 1)) and (num != 0):#ce serveur ne s'en est jamais servi
									if (last_support <= petit_last_support) or (num >= 2):#et qu'en plus c'est un vieux boulot
										args_hash = deserialize(args_hash, signature=self.signature)#deserialisation de la liste des arguments
										if (check_size(args_hash, curseur) >= 1024*1024*100) and (server_id != server) and (server != 0):#si le fichier est trop gros
											continue					#on ne fait pas de doublons
										if server != 0:					#dans le cas ou il a les yeux plus gros que le ventre
											continue					#on ne fait pas de doublons
										p.show("yes, id="+str(ident), 0)#auquel cas, c'est bon, on avance
										last_support = time.time()		#on met a jour cette date afin d'aider a la bonne repartition du travail
										server = server_id				#on retient la derniere
										curseur.execute("""UPDATE interim SET last_support=?, server=? WHERE id=?""",(last_support, server_id, ident))#mise a jour du travail en question
										self.bdd.commit()				#application de ce changement
										blacklisted = deserialize(blacklisted, signature=self.signature)#deserialisation de la liste des mauvais travailleurs
										error = deserialize(error, signature=self.signature)#de meme pour la liste des erreurs
										receivers = deserialize(receivers, signature=self.signature)#encore pareil pour 'receivers'
										worker = deserialize(worker, signature=self.signature)#de meme pour le travailleur
										interim = {}
										interim["id"] = ident
										interim["job_hash"] = job_hash
										interim["args_hash"] = args_hash
										interim["res_hash"] = res_hash
										interim["state"] = state
										interim["blacklisted"] = blacklisted
										interim["timeout"] = timeout
										interim["sending_date"] = sending_date
										interim["last_support"] = last_support
										interim["error"] = error
										interim["server"] = server
										interim["receivers"] = receivers
										interim["transmitter"] = self.id
										interim["display"] = display
										interim["worker"] = worker
										return interim					#on retourne tout
				p.show("no", 0)											#si tout cela n'a rien donne
				return None

		def get_job(job_hash):
			"""
			retourne dans la meusure du possible un tuple contenant deux choses:
			1-toutes les informations relatives a ce boulot
			2-le boulot lui meme sous forme de io.BufferedReader
			"""
			with Printer("get job...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):			#on prend la main sur la base de donnees
					curseur = self.bdd.cursor()							#mise en place d'un lien
					curseur.execute("SELECT * FROM job WHERE job_hash=?",(job_hash,))#on recupere la ligne
					ident, job_hash, code, modules, compresslevel, timeout, sending_date = curseur.fetchall()[0]#on recupere le resultat
					code = deserialize(code, signature=self.signature)	#on deserialise le code source pour le mettre en str
					modules = deserialize(modules, signature=self.signature)#on deserialise le dictionnaire des modules
					res = {}
					res["id"] = ident
					res["job_hash"] = job_hash
					res["code"] = code
					res["modules"] = modules
					res["compresslevel"] = compresslevel
					res["timeout"] = timeout
					res["sending_date"] = sending_date
					return res											#comme prevu on donne la bonne chose

		def get_arg(arg_hash):
			"""
			retourne dans la mesure du possible un tuple contenant deux choses:
			1-toutes les informations relatives a cet argument
			2-le boulot lui même sous forme de io.BufferedReader
			"""
			with Printer("get arg...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):			#on prend la main sur la base de donnee
					curseur = self.bdd.cursor()							#mise en place d'un lien
					curseur.execute("SELECT * FROM arg WHERE arg_hash=?",(arg_hash,))#on recupere la ligne
					ident, arg_hash, arg, sending_date, compresslevel = curseur.fetchall()[0]#on recupere le resultat
					res = {}
					res["id"] = ident
					res["arg_hash"] = arg_hash
					res["arg"] = arg
					res["sending_date"] = sending_date
					res["compresslevel"] = compresslevel
					return res											#comme prevu on donne la bonne chose

		with Signature(self, signature):
			with Printer("get work...", signature=self.signature):		#nous allons tenter de recuperer du travail et tout son environnement
				interim = get_interim(server_id)						#on recupere le potentiel travail a faire
				if interim == None:										#si l'on a rien trouve
					return None, None, None								#voila la signature de cet effet
				job = get_job(interim["job_hash"])						#on recupere les fichiers en lien avec le code source
				args = list(map(get_arg, interim["args_hash"]))			#et les arguments
				return interim, job, args								#tout est retourne dans un tuple

	def is_lock(self, server, signature=None):
		"""
		retourne True si le serveur est verouille
		retourne False sinon
		"""
		with Signature(self, signature):
			with Printer(server.name+" is it free...", signature=self.signature) as p:#nous allons verifier que le serveur est disponible
				try:
					ver = server.load("lock", signature=self.signature)			#tentative de telechargement
					ver = deserialize(ver, signature=self.signature)			#si un verrou existe
					if time.time() > ver["expiration_date"]:					#mais qu'il n'est plus valide:
						p.show("yes", 0)										#c'est bon, il est tant de laisser la place
						return False											#la reponsse est donc aussi positive
					p.show("no")												#dans le cas ou le verrou est actif
					return True			
				except:
					p.show("yes")
					return False

	def mk_link(self, signature=None):
		"""
		cre des liens avec les differents serveurs
		ne met pas en route les serveurs
		retourne la liste de ces serveurs
		"""
		if self.servers != []:													#si les serveurs sont deja crees
			return self.servers													#on ne perd pas de temps a les reconecter
		with Signature(self, signature):
			with Printer("link to server...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):					#prise en main de la base de donne qui contient l'adresse des differents serveurs
					self.servers = []											#initialisation de la liste
					curseur = self.bdd.cursor()									#lien etroit vers cette base la
					req = curseur.execute("""SELECT id, name, key, category FROM server""")#on selectionne tous les serveurs potentiellement disponibles
					for ident, name, key, category in req:								#pour chaque serveur
						key = deserialize(key, signature=self.signature)
						if category == "dropbox":								#si il s'agit d'un serveur Dropbox
							self.servers.append(raisin.servers.Dropbox(name, key, ident, signature=self.signature))#on ajoute ce serveur dans la liste
						elif category == "local":								#si il s'agit d'une repartition sur un disque local
							self.servers.append(raisin.servers.Local(name, key, ident, signature=self.signature))	#on ajoute ce serveur dans la liste
						else:													#si le serveur demande n'existe pas
							raise Exeption(str(category)+" server is not existing... Only 'dropbox' or 'local'!")#on retourne une erreur
			return self.servers

	def purge_interim(self, identifiant, signature=None):
		"""
		supprime cet offre d'emploi
		et toutes les donnee depandantes
		"""
		with Signature(self, signature):
			with Printer("purge interim...", signature=self.signature):			#suppression de ce travail et de ces depandances
				lock = Lock(id="bdd", signature=self.signature)					#creation d'un verrou
				lock.acquire()													#on depose ce verrou
				curseur = self.bdd.cursor()										#nous allons faire plein de test
				curseur.execute("SELECT job_hash, args_hash, res_hash FROM interim WHERE id=?",(identifiant,))#preparation de la requette
				rep = curseur.fetchall()										#execution de la requete
				if len(rep) == 0:												#si cela n'a rien donne
					lock.release()												#c'est pas bien genant
				else:															#dans le cas ou un resultat est sous-jacent
					job_hash, res_hash, args_hash = rep[0]						#on recupere le resultat
					args_hash = deserialize(args_hash, signature=self.signature)#la partie qui doit etre deserialisee l'est
					liste_arg = []												#liste des arguments a eviter
					with Printer("serching depandencing...", signature=self.signature):#nous allons regarder si les 'hash' sont utiles pour d'autres emplois
						rep = curseur.execute("SELECT job_hash, arg_hash, res_hash FROM interim WHERE id != ?",(identifiant,))
						for job, res, arg in rep:								#pour chacune des autre offre d'emploi
							if job_hash == job:									#si un autre boulot a besoin de la meme structure
								job_hash = False								#elle ne sera pas supprimee
							if res_hash == res:									#de meme pour le resultat
								res_hash = False								#qui sera preserve
							if arg in args_hash:								#pour les arguments
								liste_arg.append(arg)							#si il aparait ailleurs, on ne le suprimera pas
					lock.release()												#on libere l'acces a la base de donnee
					self.del_interim(identifiant)								#supression de l'interim
					if job_hash:												#si il n'est dependant de rien d'autre
						self.del_job(job_hash)									#on supprime le travail qui y est lie
					if res_hash:												#de meme pour le resultat
						self.del_res(res_hash)									#le hash est supprime
					for arg in args_hash:										#enfin, pour chacun des arguments
						if not arg in liste_arg:								#si il n'intervient pas dans d'autre job
							self.del_arg(arg)									#il est a son tour supprime

	def reception(self, server, signature=None):
		"""
		actualise la base de donnee en cherchant des resultats
		ne retourne rien
		ne fait pas le menage dans le serveur
		"""
		def res_generator(server, ress_hash):
			"""
			est un generateur qui renvoi chaque bout de resultat
			"""
			for res_hash in ress_hash:
				data = None
				while data == None:
					try:
						data = server.load("res&"+res_hash, signature=self.signature)
					except:
						data = None
				yield data

		with Signature(self, signature):
			with Printer("looking for jobs that concerns us...", signature=self.signature):
				with Lock("bdd", timeout=10, signature=self.signature):
					curseur = self.bdd.cursor()
					req = curseur.execute("""SELECT * FROM interim WHERE state='working' or state='waiting'""")
			with Printer("chec the server "+server.name+"...", signature=self.signature):	#on affiche toute la suite dans la colone de ce serveur
				with self.server_lock(server, timeout=600, signature=self.signature):		#pose d'un verrou sur le serveur pour evite d'eventuels conflits
					for ident, job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker in req:
						try:
							data = server.load("interim&"+str(sending_date), signature=self.signature)
							interim = deserialize(data, signature=self.signature)
							if interim["state"] == "fail":
								state = "fail"
								error = interim["error"]
							elif interim["state"] == "finish":
								state = "finish"
								error = None
								res_hash = interim["res_hash"]
								res = res_generator(server, interim["ress_hash"])
								compresslevel = interim["compresslevel"]
								self.add_res(res_hash, res, compresslevel, signature=self.signature)
								try:
									server.remove("interim&"+str(sending_date), signature=self.signature)
								except:
									pass
							elif time.time() > sending_date+timeout:
								state = "fail"
								error = TimeoutError("total time over "+str(timeout)+" secondes!")
								try:
									server.remove("interim&"+str(sending_date), signature=self.signature)
								except:
									pass
							else:
								raise Exception
							blacklisted = interim["blacklisted"]
							last_support = interim["last_support"]
							display = interim["display"]
							worker = interim["worker"]
							args_hash = deserialize(args_hash, signature=self.signature)
							receivers = deserialize(receivers, signature=self.signature)	
							self.add_interim(job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker, signature=self.signature)
						except:
							pass

	def run(self, server, signature=None):
		"""
		active le serveur passe en parametre
		"""
		with Signature(self, signature):
			while 1:
				time.sleep(60)

	def save(self, generator, file_path, signature=None):
		"""
		ouvre un fichier suivant 'file_path'
		vide le generateur de bytes dans ce fichier
		ne retourne rien
		"""
		with Signature(self, signature):
			with Printer("file writing...", signature=self.signature):			#prevenance de notre objectif
				with open(file_path, "wb") as file:								#ouverture du fichier
					for pack in generator:										#pour chaque sequence de bytes
						file.write(pack)										#on la met dans le fichier

	def send(self, interim, signature=None):
		"""
		'interim' est le dictionaire posedant au moin les clef suivantes:
			-'sending_date' => identifiant propre a ce boulot
			-'args_hash' => la liste des identifiants de chacun des arguments
			-'job_hash' => l'identifiant propre a ce travail
			-'server_id' => identifiant du serveur (0 si il n'y en a pas)
		ne retourne rien et poste l'objet sur un serveur
		"""
		with Signature(self, signature):
			with Printer("send all interim", interim["sending_date"], signature=self.signature):
				if interim.get("server_id", 0) == 0:									#si l'identifiant n'est pas pertinent
					interim["server_id"] = self.get_free_server()						#on cherche le serveur le plus disponible
				server = [s for s in raisin.servers.servers if s.id == interim["server_id"]][0]#recuperation du bon serveur
				with Printer("send employement...", signature=self.signature) as p:		#affichage de l'operation en cours
					with self.server_lock(server, timeout=3600*24, signature=self.signature):#on depose un verrou pour eviter un tas de conflits
						elements = server.ls(signature=self.signature)					#recuperation de la liste des fichier deja present sur le serveur
						chunk_size = 1024*1024											#c'est la taille des paquets en octet
						
						#arguments
						for n, arg_hash in enumerate(interim["args_hash"]):				#on commence par envoyer les arguments pour ne pas creer de conflit							
							with Printer("send arg n°"+str(n)+"...", signature=self.signature):#on dit quel argument on envoi
								if "arg&"+arg_hash in elements:							#si cet argument est deja sur le serveur
									continue											#on passe au suivant
								arg = {}												#initialisation du dictionaire 'arg'
								arg["arg_hash"] = arg_hash								#on stock le 'arg_hash'
								arg["chunk_size"] = chunk_size							#mais aussi la taille du paquet
								curseur = self.bdd.cursor()								#creation d'un lien vers la base
								curseur.execute("""SELECT arg_data FROM arg WHERE arg_hash=?""",(arg_hash,))#on prepare la recherche
								arg["arg_data"] = curseur.fetchall()[0][0]				#et hop c'est parti, on recupere les donnees
								arg["torrent"] = []										#va contenir le nom de tous les sous-paquets
								if arg["arg_data"] == b"":								#si l'argument est trop gros pour etre stocke ici
									size = os.path.getsize(os.path.join(raisin.rep, "arg_"+arg_hash+".rais"))#la taille du fichier en octet
									with open(os.path.join(raisin.rep, "arg_"+arg_hash+".rais"), "rb") as f:#on va lire le gros fichier
										data = f.read(chunk_size)						#lecture du fichier (partiellement)
										i = 0											#initialisation du compteur pour le pourcentage
										while data != b"":								#tant que le fichier n'est pas entierement lu
											purcent = i*100*chunk_size//size			#le pourcentage d'envoi
											p.show(str(purcent)+"%")					#est afficher pour faire pascienter
											data_hash = self.get_hash(data)				#on recupere la signature pour en faire un nom
											name = "arg_fragment&"+data_hash			#creation du nom a utiliser
											while not name in elements:					#si ce fichier n'existe pas deja
												try:									#mais en prenant 1001 precautions
													server.send(data, name, signature=self.signature)#on tente d'envoyer ce petit paquet
													elements.append(name)				#quand l'envoi est termine, on s'en souvient pour eviter les doublons
													break								#et on sort de la boucle
												except:									#si on a echouer, on va tenter de recomencer
													try:								#car les erreur ne sont pas gerees par le serveur
														server.remove(name, signature=self.signature)#tant que l'envoi ne fonctionne pas, on s'y acharne
													except:								#si on en arrive la
														continue						#c'est qu'il faut recomencer
											arg["torrent"].append(name)					#on ajoute le nom de ce fichier affin qu'il soit replacer au bon endroit
											data = f.read(chunk_size)					#lecture de la suite du fichier
											i+=1										#incrementation du compteur
								name = "arg&"+arg_hash									#voila le nom du fichier qui gere tous les autres
								if not name in elements:								#si ces metadatas ne figurent nule part
									data = serialize(arg, compresslevel=0, generator=False, signature=self.signature)#serialisation de l'argument
									while not name in elements:							#si ce fichier n'existe pas deja
										try:											#mais en prenant 1001 precautions
											server.send(data, name, signature=self.signature)#on tente d'envoyer ce petit paquet
											elements.append(name)						#quand l'envoi est termine, on s'en souvient pour eviter les doublons
											break										#et on sort de la boucle
										except:											#si on a echouer, on va tenter de recomencer
											try:										#car les erreur ne sont pas gerees par le serveur
												server.remove(name, signature=self.signature)#tant que l'envoi ne fonctionne pas, on s'y acharne
											except:										#si on en arrive la
												continue								#c'est qu'il faut recomencer

						#job
						with Printer("send job...", signature=self.signature):			#on peu envoyer le boulot en deuxieme position
							job = {}													#initialisation du boulot
							job["job_hash"]	= interim["job_hash"]						#on y met les infos necessaires
							curseur = self.bdd.cursor()									#mise en lien vers la base de donnee
							curseur.execute("""SELECT target, modules, compresslevel, job_timeout FROM job WHERE job_hash=?""",(job["job_hash"],))#lecture des elements dans la base
							curseur = curseur.fetchall()								#lencement de la requette
							job["target_data"] = curseur[0][0]							#on recupere les champs importants
							job["modules_data"] = curseur[0][1]							#soit, le pointeur vers la definition a executer
							job["compresslevel"] = curseur[0][2]						#les modules nesessaire a l'execution
							job["job_timeout"] = curseur[0][3]							#et le temps maximum acceptable pour executer le boulot
							name = "job&"+job["job_hash"]								#nom qu'aura le boulot sur le serveur
							if not name in elements:									#si le boulot n'est pas sur le serveur
								data = serialize(job, compresslevel=0, generator=False, signature=self.signature)#serialisation du boulot
								if len(data) <= chunk_size:								#si le boulot ne prend pas beaucoup de place
									interim["job_data"] = data							#on va l'associer avec 'interim'
									elements.append(name)								#subterfuge pour sortir du 'if'
								while not name in elements:								#quand que l'envoi ne fonctionne pas
									try:												#mais avec internet, on est jamais sur de rien
										server.send(data, name, signature=self.signature)#tentative d'envoi du boulot
										elements.append(name)							#on le memorise afin de pouvoir sortire de la boucle
										break											#on accelere un peu le mouvement parce ça traine un peu
									except:												#si l'envoi a merdoyer
										try:											#on retente notre chance
											server.remove(name, signature=self.signature)#il faut donc faire de la place pour le prochain
										except:											#si meme la suppression ne fonctione pas
											continue									#on desepere mais cela ne doit pas empecher de perceverer

						#interim
						with Printer("send interim...", signature=self.signature):		#maintenent que toutes les dependances sont sur le serveur
							name = "interim&"+str(interim["sending_date"])+"&waiting"	#pour le caracteriser, on le nome par sa date de creation
							if not name in elements:									#si l'offre d'emploi n'est pas postee
								data = serialize(interim, compresslevel=0, generator=False, signature=self.signature)#serialisation de l'interim
								while not name in elements:								#tant que ce travail ne figure pas sur le marche de l'emploi
									try:												#pour etre certain qu'a la fin c'est ok, on met in try
										server.send(data, name, signature=self.signature)#on tente de poster le code
										elements.append(name)							#on le memorise afin de pouvoir sortire de la boucle
										break											#on accelere un peu le mouvement parce ça traine un peu
									except:												#si l'envoi a merdoyer
										try:											#on retente notre chance
											server.remove(name, signature=self.signature)#il faut donc faire de la place pour le prochain
										except:											#si meme la suppression ne fonctione pas
											continue									#on desepere mais cela ne doit pas empecher de perceverer

	def specific_work(self, sending_date, signature=None):
		"""
		retourne la meme chose que 'get_work' a la difference pres qu'il s'agit d'une recherche tres specifique
		"""
		def get_interim(sending_date):
			"""
			retourne la ligne de la table interim
			"""
			with Printer("serching specific employement...", signature=self.signature) as p:
				with Lock(id="bdd", signature=self.signature):#on prend la main
					curseur = self.bdd.cursor()							#creation d'un lien vers la base de donnee
					req = curseur.execute("SELECT * FROM interim WHERE sending_date=?",(sending_date,))#on tente de recuperer la bonne ligne
					for ident, job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker in req:
						if state == "finish":							#si le resultat est deja la
							break										#on va pas le reenvoyer
						args_hash = deserialize(args_hash, signature=self.signature)#deserialisation des la liste des arguments		
						p.show("yes, id="+str(ident), 0)				#auquel cas, c'est bon, on avance
						last_support = time.time()						#on met a jour cette date afin d'aider a la bonne repartition du travail
						server_id = self.get_free_server()
						curseur.execute("""UPDATE interim SET last_support=?, state=?, server_id=? WHERE id=?""",(last_support, "working", server_id, ident))#mise a jour du travail en question
						self.bdd.commit()								#application de ce changement
						blacklisted = deserialize(blacklisted, signature=self.signature)#deserialisation de la liste des mauvais travailleurs
						error = deserialize(error, signature=self.signature)#de meme pour la liste des erreurs
						receivers = deserialize(receivers, signature=self.signature)#encore pareil pour receivers
						worker = deserialize(worker, signature=self.signature)#de meme pour le travailleur
						interim = {}
						interim["id"] = ident
						interim["job_hash"] = job_hash
						interim["args_hash"] = args_hash
						interim["res_hash"] = res_hash
						interim["state"] = state
						interim["blacklisted"] = blacklisted
						interim["timeout"] = timeout
						interim["sending_date"] = sending_date
						interim["last_support"] = last_support
						interim["error"] = error
						interim["server_id"] = server_id
						interim["receivers"] = receivers
						interim["transmitter"] = self.id
						interim["display"] = display
						interim["worker"] = worker
						return interim									#on retourne tout
				p.show("no", 0)											#si tout cela n'a rien donne
				return None

		def get_job(job_hash):
			"""
			retourne dans la mesure du possible un tuple contenant deux choses:
			1-toutes les informations relatives a ce boulot
			2-le boulot lui meme sous forme de io.BufferedReader
			"""
			with Printer("get job...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):			#on prend la main sur la base de donnee
					curseur = self.bdd.cursor()							#mise en place d'un lien
					curseur.execute("SELECT * FROM job WHERE job_hash=?",(job_hash,))#on recupere la ligne
					ident, job_hash, target, modules, compresslevel, job_timeout = curseur.fetchall()[0]#on recupere le resultat
					modules = deserialize(modules, signature=self.signature)#on deserialise le dictionnaire des modules
					res = {}
					res["id"] = ident
					res["job_hash"] = job_hash
					res["target"] = target
					res["modules"] = modules
					res["compresslevel"] = compresslevel
					res["job_timeout"] = job_timeout
					return res											#comme prevu on donne la bonne chose

		def get_arg(arg_hash):
			"""
			retourne dans la mesure du possible un tuple contenant deux choses:
			1-toutes les informations relatives a cet argument
			2-le boulot lui meme sous forme de io.BufferedReader
			"""
			with Printer("get arg...", signature=self.signature):
				with Lock(id="bdd", signature=self.signature):			#on prend la main sur la base de donnees
					curseur = self.bdd.cursor()							#mise en place d'un lien
					curseur.execute("SELECT * FROM arg WHERE arg_hash=?""",(arg_hash,))#on recupere la ligne
					ident, arg_hash, compresslevel = curseur.fetchall()[0]#on recupere le resultat
					res = {}											#on met les donnees dans un tuple
					res["id"] = ident									#la position dans la base de donnees
					res["arg_hash"] = arg_hash							#ce qui permet de retrouver le gros fichier 
					res["compresslevel"] = compresslevel				#taux de compression de ce fichier
					return res											#comme prevu on donne la bonne chose

		with Signature(self, signature):
			with Printer("get specific work...", signature=self.signature):#nous allons tenter de recuperer du travail et tout son environement
				interim = get_interim(sending_date)							#on recupere le potentiel travail a faire
				if interim == None:											#si l'on a rien trouve
					return None, None, None									#voila la signature de cet effet
				job = get_job(interim["job_hash"])							#on recupere les fichiers en lien avec le code source
				args = list(map(get_arg, interim["args_hash"]))				#et les arguments
				return interim, job, args									#tout est retourne dans un tuple

	def update_arg(self, arg, signature=None):
		"""
		'arg' est un dictionaire qui contient les champs suivants:
			'arg_hash' est le hash de l'argument:
				-None => le arg_hash est automatiquement calcule
				-str => cherche si il y est deja
			'compresslevel' est le taux de compression de l'argument
				-None => valeur par defaut non specifiee
				-int => compresse l'argument avec ce taux la
			'arg' est l'argument brute, non serialise
				-None => valeur par defaut pour une requette
				-object => serialise et enregistre l'argument
		retourne arg complete et tout deserialise
		"""
		with Signature(self, signature):													#on repend la signature pour tous les gosses
			if not "arg_hash" in arg:														#si le hash n'est pas precise
				with Printer("chec argument...", signature=self.signature):					#c'est surement qu'il s'agit d'un enregistrement
					arg["arg_hash"] = self.get_hash(arg["arg"])								#recuperation du hash
					return self.update_arg(arg)												#on recomance avec un hash connu
			with Printer("has it already been saved ?...", signature=self.signature) as p:	#verification de l'existance
				with Lock("bdd", signature=self.signature):									#depos d'un verou car sql le gere mal
					curseur = self.bdd.cursor()												#creation d'un lien vers la base
					curseur.execute("""SELECT compresslevel, arg_data FROM arg WHERE arg_hash=?""",(arg["arg_hash"],))#on prepare la recherche
					requette = curseur.fetchall()											#et hop c'est parti
				if len(requette):															#si la requette est fructueuse
					p.show("yes")															#on on en fait part a l'utilisateur
					if not "compresslevel" in arg:											#si le taux de compression n'est pas definie
						arg["compresslevel"] = requette[0][0]								#on recupere celui de l'objet stoppe
					with Printer("is it the same compresslevel ?...", signature=self.signature):#analyse du taux de compression
						if arg["compresslevel"] > requette[0][0]:							#si il faut plus compresser le resultat
							p.show("no")													#on en averti l'utilisateur
							self.del_arg(arg["arg_hash"])									#on prepare le terrain
							return self.update_arg(arg)										#et on re-enregistre le fichier
						else:																#dans le cas ou le taux de compression requierer et moins bon ou equivalent
							p.show("yes")													#l'utilisateur a le droit de le recuperer
							arg["compresslevel"] = requette[0][0]							#si l'argument est plus compresse, on le fait savoir
							if not "arg" in arg:											#si il faut recuperer l'argument
								arg["arg"] = requette[0][1]									#esperons qu'il soit simplement dans la base de donnee
								if arg["arg"] != b"":										#si il y est bien present
									arg["arg"] = deserialize(arg, signature=self.signature)	#ouf, il est possible de le deserialiser
								else:														#bon, si il faut aller chercher le fichier
									with open(os.path.join(raisin.rep, "arg_"+arg["arg_hash"]+".rais"), "rb") as f:#on l'ouvre
										arg["arg"] = deserialize(f, signature=self.signature)#et on le deserialise aussitot
							return arg														#les valeurs lui sont donc retournees					
				else:																		#si l'argument n'est pas enregistree
					p.show("no")															#on previent l'utilisateur qu'un calcul arrive
					with Printer("save argument...", signature=self.signature):				#et qu'il peu etre long
						if not "compresslevel" in arg:										#si le choix du taux de compression nous est laisse
							arg["compresslevel"] = 1										#on prend 1 car c'est asse rapide
						path_file = os.path.join(raisin.rep, "arg_"+arg["arg_hash"]+".rais")#ca, c'est le chemin qui mene au bon fichier
						pack_gener = serialize(arg["arg"], compresslevel=arg["compresslevel"], generator=True, signature=self.signature)#serialisation de l'argument
						with open(path_file, "wb") as f:									#on va enregistrer l'argument'
							for pack in pack_gener:											#en faisant gaffe de ne pas faire cracher le pc
								f.write(pack)												#on rempli alors le fichier petit a petit
						if os.path.getsize(path_file) < 1024*1024:							#si le fichier n'est pas tres gros
							with open(path_file, "rb") as f:								#il va directement etre stocke dans la base de donnees
								arg_data = f.read()											#il est donc important de lire le fichier
							os.remove(path_file)											#pour pouvoir faire du menage
						else:																#si le fichier est gros
							arg_data = b""													#les donnees ne vont pas etre grosses
						with Lock("bdd", signature=self.signature):							#depot d'un verrou sur la base de donne
							curseur = self.bdd.cursor()										#creation d'un pointeur vers la base
							curseur.execute("""INSERT INTO arg
								(arg_hash, compresslevel, arg_data)
									VALUES (?,?,?)""",(arg["arg_hash"], arg["compresslevel"], arg_data))#ajout de ligne
							self.bdd.commit()
							return arg														#on retourne tous ces arguments

	def update_interim(self, interim, force=False, signature=None):
		"""
		'interim' est un dictionaire qui contient toutes les donnee pour une offre d'emploi (sans aucune serialisation)
		'force' est True si l'on shouaite redonner une chance a cette interim
		retourne 'interim' completee et totalement deserialise
		"""
		def union(l1, l2):
			"""
			fait l'union au sens ensembliste de ces 2 listes
			"""
			for e in l2:
				if not e in l1:
					l1.append(e)
			return l1

		with Signature(self, signature):													#tout ce qui est dans cette methode va etre affiche au bon endroit
			with Printer("chec interim offer...", signature=self.signature) as p:			#avertissemnt de l'opperation en cours
				with Printer("is the 'sending date' known ?...", signature=self.signature):	#on regarde dans un premier temps si cet emploi est identifie
					if "sending_date" in interim:											#si la date d'envoi est connue
						p.show("yes")														#on le precise a l'utilisateur
						with Printer("is interim already been saved ?...", signature=self.signature):#on se demande alors si c'est deja enregistre
							with Lock("bdd", signature=self.signature):						#un petit verrou ne fait pas de mal
								curseur = self.bdd.cursor()									#creation d'un lien vers la base	
								curseur.execute("""SELECT job_hash, args_hash, res_hash, state, blacklisted, timeout, last_support, error, server_id, receivers, display, worker FROM interim WHERE sending_date=?""",(interim["sending_date"],))#on prepare la recherche
								requette = curseur.fetchall()								#lancement de la requette
							if len(requette):												#si cette emploi a deja ete cree
								p.show("yes")												#l'utilisateur est mis au courant
								with Printer("update interim offer...", signature=self.signature):#et c'est bon, on syncronise les 2
									changement = False										#est True si il y a une difference entre la base de donnee et interim
									if requette[0][3] == "finish":							#si le resultat est la
										interim = {"sending_date":interim["sending_date"]}	#on fait en sorte d'etre sur de le recuperer
									if requette[0][3] == "fail":							#si c'est un echec
										error = deserialize(requette[0][7], signature=self.signature)#on regarde a quel point s'en est un
										if (not type(error) in [KeyboardInterrupt, ImportError, MemoryError]):#si c'est un veritable echec
											interim = {"sending_date":interim["sending_date"]}#on evite de faire des mises a jours qui reviennet en ariere
									interim["job_hash"] = requette[0][0]					#ajout ou ecrasement de l'identifiant du job
									if not "args_hash" in interim:							#si le dictionaire est vide de 'args_hash'
										interim["args_hash"] = deserialize(requette[0][1], signature=self.signature)#on lui ajoute pour qu'il ne le soit plus
									interim["res_hash"] = interim.get("res_hash", requette[0][2])#si il n'y est pas, on ajoute l'identifiant du resultat
									if interim["res_hash"] != requette[0][2]:
										changement = True
									interim["state"] = interim.get("state", requette[0][3])	#de meme pour 'state'
									if interim["state"] != requette[0][3]:
										changement = True
									blacklisted_requette = deserialize(requette[0][4], signature=self.signature)	
									interim["blacklisted"] = union(interim.get("blacklisted", []), blacklisted_requette)
									if interim["blacklisted"] != blacklisted_requette:
										changement = True
									interim["timeout"] = interim.get("timeout", requette[0][5])#de meme pour 'timeout'
									if interim["timeout"] != requette[0][5]:
										changement = True
									interim["last_support"] = interim.get("last_support", requette[0][6])#de meme pour 'last support'
									if interim["last_support"] != requette[0][6]:
										changement = True
									if type(interim.get("error", None)) in [KeyboardInterrupt, ImportError, MemoryError, type(None)]:#si il y a deja une erreur
										error = deserialize(requette[0][7], signature=self.signature)#on evite une deserialisation inutile
										if error != None:									#si il n'y a pas vraiment d'erreur
											interim["error"] = error						#on ne l'ajoute pas, sa alourdirait pour irien
											changement = True
									interim["server_id"] = interim.get("server_id", requette[0][8])#de meme pour 'server_id'
									if not "receivers" in interim:							#si on ne sais pas qui doit recevoir l'offre
										receivers = deserialize(requette[0][9], signature=self.signature)#on regarde si il y a des destinataires privilegies
										if receivers != []:									#dans le cas ou il y en a
											interim["receivers"] = receivers				#on les memorises
											changement = True
									interim["display"] = interim.get("display", requette[0][10])#de meme pour 'display'
									if interim["display"] != requette[0][10]:
										changement = True
									if not "worker" in interim:								#si on ne sait pas qui a bosse pour nous
										worker = deserialize(requette[0][11], signature=self.signature)#on regarde si quelqu'un s'est pointe
										if worker != None:									#si une machine s'est arrache pour nous
											interim["worker"] = worker						#on lui fait honneur
											changement = True
									if changement:											#si il y a eu des changements:
										with Lock("interim_bdd", timeout=20, signature=self.signature):#pour eviter des conflit avec l'entenne
											self.del_interim(interim["sending_date"])		#comme tout est stocke, on le supprime de la base
											return self.update_interim(interim)				#et on le reenregistre proprement
									return interim											#si il ne s'est rien passe, on retourne directement
							else:															#si il n'est pas dans la base de donnee
								p.show("no")												#l'utilisateur en est averti
								interim["res_hash"] = interim.get("res_hash", "")			#une chaine vide signifie que le resultat n'est pas arrive
								interim["state"] = interim.get("state", "waiting")			#on l'initialise a "waiting" par defaut
								interim["blacklisted"] = interim.get("blacklisted", [])		#la liste vide sinifie que personne n'a encore echoue sur ce boulot
								interim["timeout"] = interim.get("timeout", 3600*24*31)		#on laisse un mois pour recuperer le resultat
								interim["last_support"] = interim.get("last_support", interim["sending_date"])#au pire, il a ete pris en charche pour la derniere fois lors de sa creation
								interim["error"] = interim.get("error", None)				#le None signifie ici, qu'il n'y a pas d'erreur
								interim["server_id"] = interim.get("server_id", 0)			#0 est le serveur par defaut
								interim["receivers"] = interim.get("receivers", [])			#la liste vide signifie qu'il n'y a pas de destinataire particuliers
								interim["display"] = interim.get("display", "")				#une chaine vide signifi qu'il n'y a rien a afficher
								interim["worker"] = interim.get("worker", None)				#None veut dire qu'encore personne n'a travaille dessu
								job_hash = interim["job_hash"]								#recuperation du "job_hash" pret a l'enregistrement
								args_hash = serialize(interim["args_hash"], compresslevel=0, signature=self.signature)#recuperation des "args_hash" pret a l'enregistrement
								res_hash = interim["res_hash"]								#recuperation du "res_hash" pret a l'enregistrement
								state = interim["state"]									#recuperation du "state" pret a l'enregistrement
								blacklisted = serialize(interim["blacklisted"], compresslevel=0, signature=self.signature)#recuperation des "blacklisted" pret a l'enregistrement
								timeout = interim["timeout"]								#recuperation du "timeout" pret a l'enregistrement
								sending_date = interim["sending_date"]						#recuperation du "sending_date" pret a l'enregistrement
								last_support = interim["last_support"]						#recuperation du "last_support" pret a l'enregistrement
								error = serialize(interim["error"], compresslevel=0, signature=self.signature)#recuperation des "error" pret a l'enregistrement
								server_id = interim["server_id"]							#recuperation du "server_id" pret a l'enregistrement
								receivers = serialize(interim["receivers"], compresslevel=0, signature=self.signature)#recuperation des "receivers" pret a l'enregistrement
								display = interim["display"]								#recuperation du "display" pret a l'enregistrement
								worker = serialize(interim["worker"], compresslevel=0, signature=self.signature)#recuperation des "worker" pret a l'enregistrement
								with Lock("bdd", signature=self.signature):					#depos d'un verrou
									curseur = self.bdd.cursor()								#creation d'un pointeur vers la base
									curseur = curseur.execute("""INSERT INTO interim
										(job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker)
									VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",(job_hash, args_hash, res_hash, state, blacklisted, timeout, sending_date, last_support, error, server_id, receivers, display, worker))
									self.bdd.commit()										#passage a l'acte
								return interim												#on retourne le dictionaire de l'offre d'mploit que la suite du programme attend avec impatience!
					else:																	#si l'on ne connait pas la date d'envoi
						p.show("no")														#il va faloir l'identifier autrement
						args_hash = serialize(interim["args_hash"], compresslevel=0, signature=self.signature)#on recupere donc les args_hash serialises
						job_hash = interim["job_hash"]										#celui-le il n'y a pas besoin de le serialise
						with Lock("bdd", signature=self.signature):							#le verrou est imperatif a chaque requette
							curseur = self.bdd.cursor()										#c'est donc pour cela que l'on va faire une requette
							curseur.execute("""SELECT sending_date FROM interim WHERE args_hash=? AND job_hash=?""",(args_hash, job_hash))#on regarde si cet emploi est donc deja cree
							requette = curseur.fetchall()									#exectution de la requette
						if len(requette):													#si la requette est fructueuse:
							interim["sending_date"] = requette[0][0]						#recuperation de la date d'envoi pour la suite
						else:																#dans le cas ou l'on a rien trouve
							interim["sending_date"] = time.time()							#on considere que l'emploi est envoye maintenant
						return self.update_interim(interim)									#c'est reparti!

	def update_job(self, job, signature=None):
		"""
		'job' est un dictionaire qui peut contenir les clefs suivantes:
			-"job_hash", l'identifiant propre a ce job
			-"target", pointeur vers l'objet a executer, qui prend des parametre
			-"modules", les modules dont ce code a besoin pour fonctionner
			-"job_timeout", temps maximum acceptable d'execution
		retourne le 'job' complete, sans aucune serialisation
		"""
		def get_modules(target, signature):
			"""
			retourne les modules dont la cible a besoin
			la cible peut etre une methode ou une definition
			retourne un dictionaire qui a chaque nom de module,
			associ dans une liste les differentes manieres dont il doit etre importe
			"""
			def is_import(ligne):
				"""
				retourne True si il s'agit bien d'une ligne d'import de modules
				"""
				if re.match(r"import\s\w", ligne) is not None:
					return True
				elif re.match(r"from\s(.)+\simport\s+\w", ligne) is not None:
					return True
				return False

			with Printer("get modules...", signature=signature):
				lignes = []																	#c'est la liste qui comporteras les ligne d'import
				with open(inspect.getsourcefile(target), "r", encoding="utf-8") as file:	#on ouvre le fichier qui contient le code source
					for ligne in file.readlines():											#chaque ligne est lu attentivement
						if is_import(ligne):												#si il s'agit d'une ligne d'import de module
							lignes.append(ligne)											#cette ligne est ajoutee au ligne a analiser plus en profondeur	
				dico = {}																	#c'est le dictionaire qui a chaque module, assosie sa/ces facons d'etre importe
				for ligne in lignes:														#pour chaque lignes qui importe un module
					while ligne[0] in " \t":												#si cette ligne comporte des espaces indesirable
						ligne = ligne[1:]													#on supprime ces espaces
					ligne = ligne.replace("\n", "")											#suppression des retours a la ligne
					module = ligne.split(" ")												#on troncone les commandes d'import en petit bouts
					module = [m for m in module if m != ""]									#on supprimes les espaces en trop
					module = module[1].split(".")[0]										#on selectionne alors la bone partie de la commande
					dico[module] = dico.get(module, [])+[ligne]								#on ajoute donc cette commande
				return dico

		with Signature(self, signature):													#tout ce qui est dans cette methode va etre affiche au bon endroit
			if "job_hash" in job:															#si on sait de quel travail il s'agit
				with Printer("is job already been saved ?...", signature=self.signature) as p:#on regarde si le boulot est deja enregistre dans la base de donnees
					with Lock("bdd", signature=self.signature):								#depos du verrou
						curseur = self.bdd.cursor()											#mise en lien vers la base de donnee
						curseur.execute("""SELECT compresslevel FROM job WHERE job_hash=?""",(job["job_hash"],))
						requette = curseur.fetchall()										#lencement de la requette
					if not "compresslevel" in job:											#si c'est a nous de choisir le taux de compression
						job["compresslevel"] = 1											#on le fixe a 1
					if len(requette):														#si le job est deja enregistre
						p.show("yes")														#il reste plus qu'un derniere etape
						with Printer("is it the same compresslevel", signature=self.signature):#regarder si il faut comprimer plus le boulot
							if job["compresslevel"] > requette[0][0]:						#si il faut plus compresser le resultat
								p.show("no")												#on indique qu'il reste du chemin avant la fin
								job_bis = job.copy()										#on fait une copie du traivail
								job_bis["compresslevel"] = 0								#afin de pouvoir changer le taux de compression sans qu'il n'y ai trop d'impactes
								job_bis = self.update_job(job_bis)							#on recupere les valeurs actuelles
								self.del_job(job["job_hash"])								#affin de pouvoir les supprimer de la base sans encombres
								job_bis["compresslevel"] = job["compresslevel"]				#on revient au taux de compression requiere
								return self.update_job(job_bis)								#enregistrement de ce nouvel emploi avec le bon taux de compression
							else:															#par ailleur, dans le cas ou le taux de compression est bon
								p.show("yes")												#on rejouis l'utilisateur
								with Lock("bdd", signature=self.signature):					#depos du verrou
									curseur.execute("""SELECT target, modules, job_timeout FROM job WHERE job_hash=?""",(job["job_hash"],))
									target, modules, job_timeout = curseur.fetchall()[0]	#recuperation des informations serializes
								if not "target" in job:										#si il faut lui donner le pointeur vers une fonction
									job["target"] = deserialize(target, signature=self.signature)#on la deserialise pour lui presenter joliment
								if not "modules" in job:									#de meme, si il ne sait pas quels modules utiliser
									job["modules"] = deserialize(modules, signature=self.signature)#on lui premache un peu baucoup le travail
								job["job_timeout"] = job_timeout							#pas de craintes d'ecrasement, si il est deja present on l'ecrase avec la meme valeur
								job["compresslevel"] = requette[0][0]						#le vrai taux de compression est retourne
								return job													#on le retourne comme prevu
					else:																	#si le boulot n'est pas enregistre
						p.show("no")														#on le dit a l'utilisateur
						job["job_timeout"] = job.get("job_timeout", 3600*24*7)				#on autorise a ce qu'il monopolise 1 semaine mais pas plus
						job_hash = job["job_hash"]											#extraction des differentes infos affin de les rendre enregistrables
						target = serialize(job["target"], compresslevel=job["compresslevel"], signature=self.signature)#de meme pour la fonction qui est copiee
						if not "modules" in job:											#si les modules ne sont pas definis
							job["modules"] = get_modules(job["target"], self.signature)		#on tente d'aller les lires
						modules = serialize(job["modules"], compresslevel=job["compresslevel"], signature=self.signature)#la liste des modules
						compresslevel = job["compresslevel"]								#voici le taux de compression
						job_timeout = job["job_timeout"]									#et enfin aussi pour le timeout
						with Lock("bdd", signature=self.signature):							#depot d'un verrou
							curseur = self.bdd.cursor()										#creation d'un pointeur vers la base
							curseur.execute("""INSERT INTO job
								(job_hash, target, modules, compresslevel, job_timeout)
							VALUES (?,?,?,?,?)""",(job_hash, target, modules, compresslevel, job_timeout))#ajout de ligne
							self.bdd.commit()												#passage a l'acte des operations
						return job															#on peut donc redonner le job
			else:																			#si le hash est inconu
				job["job_hash"] = self.get_hash(job["target"])								#on le cherche
				return self.update_job(job)													#et on passe a la suite

	def update_res(self, res, signature=None):
		"""
		'res' est un dictionaire qui peut contenir les champs suivants:
			-'res_hash' => identifiant propre a ce resultat
			-'compresslevel' => taux de compression du resultat
			-'res' => l'objet python du resultat en tant que tel
			-'res_data' => l'objet python deja serialise, peut etre un fichier binaire en mode lecture, une sequence de bytes ou un generateur
		retourne le resultat completet et met la base de donnee a jour au passage
		"""
		with Signature(self, signature):
			if "res_hash" in res:															#si l'identifiant est connu
				with Printer("is result already been saved ?...", signature=self.signature) as p:#on regarde si le resultat est deja enregistre dans la base de donnees
					with Lock("bdd", signature=self.signature):								#depos du verrou
						curseur = self.bdd.cursor()											#mise en lien vers la base de donnee
						curseur.execute("""SELECT compresslevel, res_data FROM res WHERE res_hash=?""",(res["res_hash"],))#preparation de la requette
						requette = curseur.fetchall()										#lencement de la requette
					if not "compresslevel" in res:											#si c'est a nous de choisir le taux de compression
						res["compresslevel"] = 2											#on le fixe a 2, de facon a bien le compresser
					if len(requette):														#si il est deja enregistre
						p.show("yes")														#on rend heureux l'utilisateur qui s'impatiente
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
	gere l'affichage des different appels de raisin
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
			return shutil.get_terminal_size((80, 20)).columns					#avec un module python cette fois ci
			#marche aussi avec os.get_terminal_size(fd=STDOUT_FILENO)
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
			with open(os.path.join(self.rep, "printerNone"), "w") as f:			#il faut bien creer le fichier
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
		dico[self.signature]["alinea"] = max(0, dico[self.signature]["alinea"]+indentation)#on se prepare pour la prochaine fois
		
		#supression des colonnes en trop
		if (self.signature != None) and (dico[self.signature]["alinea"] == 0):	#si le programme 'signature' a fini d'afficher
			del dico[self.signature]											#on le supprime
			for signature in dico:												#on va rapprocher toutes les autres colonnes
				if dico[signature]["numero"] > numero:							#si un trou risque d'etre cree
					dico[signature]["numero"] -= 1								#on le bouche tout naturellement

		#enregistrement
		with open(path, "wb") as f:												#il est maintenant temps d'enregistrer ces changements
			pickle.dump(dico, f)												#mais avant ça, il faut le serialiser

		return nombre, numero, alinea

	def show(self, message="", indentation=0, s=1):
		"""
		affiche le message avec l'alinea d'avant
		'indentation' est le nombre d'alinea a ajouter a tous les messages d'apres
		's' vaut 1 si la signature est apellee
		"""
		if self.display == 0:													#si il ne faut rien afficher
			return																#on n'affiche rien, on ne perd pas de temps
		with Lock(id="printer", display=False, local=True, priority=999):		#depose d'un verrou local
			nombre, numero, alinea = self.get_infos(indentation)				#recuperation des informations
		if alinea >= self.display+s:											#si il y a trop d'indentations pour afficher
			return																#on passe directement a la suite

		self.largueur = self.get_size(self.largueur)
		debut = (" "*(self.largueur//nombre-1)+"|")*numero						#partie gauche du message
		if numero+1 < nombre:
			milieu =	(self.espaces*alinea+message+" "*self.largueur)[:(self.largueur//nombre-1)]#la partie centrale avec l'affichage
			fin = ("|"+" "*(self.largueur//nombre-1))*(nombre-numero-2)+"|"
		else:
			milieu = ""
			fin = (self.espaces*alinea+message)[:(self.largueur//nombre-1)]
		
		print(debut+milieu+fin)

	def sign(self, conclusion, alinea=-1):
		"""
		affiche le message de fin avec un alinea
		alinea est le decalage a faire sur tous les affichages prochains
		"""
		if conclusion == True:
			return self.show(self.espaces*(1+alinea)+"success!", alinea, s=1)
		elif conclusion == False:
			return self.show(self.espaces*(1+alinea)+"failure!", alinea, s=1)
		raise TypeError("'conclusion must be a boolean or a string")

	def __enter__(self):
		self.show(self.message, 1, s=0)
		return self

	def __exit__(self, type, value, traceback):
		if (type, value, traceback) == (None, None, None):
			self.sign(True)
		else:
			self.show(str(value))
			self.sign(False)

class Session:
	"""
	poste le travail a faire
	"""
	def __init__(self, signature=None):
		self.signature = signature
		self.pool = self.get_pool()												#permet de paraleliser les opperations si cela est possible
		self.Interim = Interim(signature=self.signature)						#lien vers la base de donnee
		self.id = raisin.id														#l'identifiant de cette machine

	def get_source_file(self, signature=None):
		"""
		retourne le chemin du fichier source, quand c'est possible
		"""
		with Printer("locating the path of the surce file...", signature=self.signature) as p:
			files = [t.filename for t in inspect.stack()]						#recuperations de tous les fichiers potentiel
			files = [f for f in files if os.path.exists(f)]						#on epure pour enlever les fichiers qui n'en sont pas
			files = [f for f in files if f != __file__]							#on enleve un peu des fichiers inutils
			files = [f for f in files if os.path.basename(f) != "__init__.py"]
			p.show(files[0])
		return files[0]


	def get_pool(self, signature=None):
		"""
		retourne False si le mutliprocessing rique de ne pas fonctionner
		retourne True si le paralelisme
		a des chances de bien se passer
		"""
		with Signature(self, signature):
			if not "win" in sys.platform:										#si windows ne peut pas foutre la merde
				return True														#on est tranquille pour la paralelisme
			else:																#bon, si windows est dans les parrages
				with open(self.get_source_file(), "r") as file:					#pour chaque ligne du fichier
					for ligne in file.readlines():								#si l'une d'elle est suceptible d'empecher une erreur
						if ("if" in ligne) and ("__name__" in ligne) and ("==" in ligne) and ("__main__" in ligne):#de paralelisme de donnees
							return True											#si une tele protection existe, on y va
				return False

	def get_job(self, target, signature=None):
		"""
		retourne l'integralite du boulot dans un tuple contenant:
		-le dictionaire des modules
		-le job_hash de ce job
		-la definition ou la methode brute a executer non serialisee
		"""
		with Signature(self, signature):
			with Printer("job recovery...", signature=self.signature):			#nous allons essayer de faire tout cela
				modules = self.get_modules(target)								#recuperation de tous les modules, meme ceux qui ne servent pas
				job_hash = self.Interim.get_hash(target, signature=self.signature)#on en extrait le hash
				return modules, job_hash, target								#on retourne ces differents elements

	def get_modules(self, objet, signature=None):
		"""
		retourne les modules dont l'objet a besoin
		l'objet peut etre une methode ou une definition
		retourne un dictionaire qui a chaque nom de module,
		associ dans une liste les differentes manieres dont il doit etre importe
		"""
		with Signature(self, signature):
			with Printer("get modules...", signature=self.signature):
				lignes = []														#c'est la liste qui comporteras les ligne d'import
				with open(inspect.getsourcefile(objet), "r") as file:			#on ouvre le fichier qui contient le code source
					for ligne in file.readlines():								#chaque ligne est lu attentivement
						if "import " in ligne:									#si il s'agit d'une ligne d'import de module
							lignes.append(ligne)								#cette ligne est ajoutee au ligne a analiser plus en profondeur	
				dico = {}														#c'est le dictionaire qui a chaque module, assosie sa/ces facons d'etre importe
				for ligne in lignes:											#pour chaque lignes qui importe un module
					while ligne[0] in " \t":									#si cette ligne comporte des espaces indesirable
						ligne = ligne[1:]										#on supprime ces espaces
					ligne = ligne.replace("\n", "")								#suppression des retours a la ligne
					module = ligne.split(" ")									#on troncone les commandes d'import en petit bouts
					module = [m for m in module if m != ""]						#on supprimes les espaces en trop
					module = module[1].split(".")[0]							#on selectionne alors la bone partie de la commande
					dico[module] = dico.get(module, [])+[ligne]					#on ajoute donc cette commande
				return dico

	def process(self, target, *args, timeout=3600*24*31, job_timeout=3600*48, args_hash=[], job_hash=None, local=False, force=False):
		"""
		execute le travail de facon differee
		retourne le resultat
		"""
		p = self.process_object(target, *args, timeout=timeout, job_timeout=job_timeout, args_hash=args_hash, job_hash=job_hash, local=local, force=force)
		return p.get()

	def process_object(self, target, *args, timeout=3600*24*31, job_timeout=3600*48, args_hash=[], job_hash=None, local=False, force=False):
		"""
		retourne un objet qui a pour methode get() et get_all() pour recuperer le resultat
		'target' est un pointeur vers une methode ou une fonction
		'timeout' est le temps maximum acceptable en seconde avant avant de retourner une erreur (temps total)
		'job_timeout' est le temps maximum acceptable pour l'execution du job (temps de l'execution seulement sans l'attente)
		'args_hash' est la liste des hash des argument (affin de gagner du temps)
		'job_hash' est le hash du job affin de ne pas tout reoptimiser
		'local' est un booleen qui permet de forcer une execution locale
		"""
		if not local:															#si la cible est dans un programe ou un module, que ce n'est pas une fonction toute faite de python
			return self.Pooler_loin(self, target, args, args_hash, job_hash, timeout, job_timeout, force)#on tente dans un premier temps de l'envoyer au loin, ou dumoin de l'enregistrer
		else:																	#si il y a un probleme de reseau ou bien que le pointeur est trop inaxessible
			if self.pool != False:												#on execute le programme localement sur cet ordinateur
				return self.Pooler_cpu(self, target, args, timeout, job_timeout)#on reparti la charge sur les differents coeurs si il est raisonable de le faire
			else:																#sinon on se contente de simuler un 'faux paralellisme'
				return self.Pooler_thread(self, target, args, timeout, job_timeout)#affin de rendre rapidement la main

	def map(self, target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, in_order=True, signature=None, force=False):
		"""
		execute le boulot pointe par 'target' en lui appliquant differents iterable 'args'
		retourne une liste
		"""
		with Signature(self, signature):
			m = self.map_object(target, *args, timeout=3600*24*31, job_timeout=3600*48, local=local, force=force)
			if in_order:
				for r in m.get():
					yield r
			else:
				with Printer("yield result in the arrival order...", signature=self.signature):
					while len(m.res):
						for i,res in enumerate(m.res):
							if res.ready():
								yield res.get()
								del m.res[i]
								break

	def map_object(self, target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, force=False):
		"""
		execute le boulot pointe par 'target' en lui appliquant differents iterable 'args'
		retourne un Map objet
		"""
		class Local_map:
			def __init__(self, res):
				self.res = res

			def get(self, wait=True):
				"""
				retourne la liste des resultats
				"""
				for r in self.res:
					yield r.get(wait)

			def get_all(self, wait=True):
				"""
				retourne la liste de toutes le informations
				relatives a chaqe resultat
				"""
				for r in self.res:
					yield r.get_all(wait)

			def is_alive(self):
				"""
				retourne True si le processus n'est pas termine
				False si son execution est finie
				"""
				return not(False in [r.is_alive() for r in self.res])

			def ready(self):
				"""
				retiurne la meme chose que 'is_alive()'
				"""
				return not self.is_alive()

		def gener_args(*args):
			"""
			prend une liste rempli d'iterables
			genere des liste qui a chaque etapes, itere d'un increment de plus chaqun des iterables
			yield ((arg1_rang_, arg2_rang_n, ..., argk_rang_n), [hash_arg_1, hash_arg_2, ..., hash_arg_k])
			"""
			def do_iter(iterable):
				"""
				est un generateur infini
				car il fait tourner en boucle l'iterable
				retourne l'iterable et son rang reel (modulo len(iterable)), et son hash
				"""
				def is_iterable(obj):
					"""
					retourne True si l'objet est un iterable
					"""
					try:
						iter(obj)
						return True
					except:
						return False

				producteur = []								#la liste de tous les enciennes iterations
				if is_iterable(iterable):					#dans le cas ou l'objet est un iterable
					iterable = iter(iterable)				#on lui a joute la methode .__next__()
					for i, e in enumerate(iterable):		#pour chaque sous elements
						producteur.append((e, i, self.Interim.get_hash(e)))#on le calcul
						yield producteur[-1]				#et on le retourne
					i = 0									#initialisation du compteur
					while 1:								#on boucle dessus indefiniment
						yield producteur[i]					#on le retourne
						i = (i+1)%len(producteur)			#on passe au rang suivant
				else:										#dans le cas ou il ne l'est pas
					producteur = [(iterable, 0, self.Interim.get_hash(iterable))]#on le calcul qu'un seule fois
					while 1:								#et on le retourne indefiniment
						yield producteur[0]					#rapidement, sans refaire les calculs a chaque boucles

			args = list(map(do_iter, args))					#chaque objet devient un iterable
			maximum = 0										#variable qui va nous permetre de connaitre la fin des boucles
			while 1:										#c'est une boucle presque infinie
				local_max = 0								#le maximum des boucle pour cette etape seulement
				liste_arg = []								#ca va etre le tuple des k arguments au rang n
				liste_hash = []								#la liste des hashe asociee a 'liste_arg'
				for iterable in args:						#pour chaque paquets
					arg, rang, arg_hash = iterable.__next__()#on recupere ces infos
					local_max = max(local_max, rang)		#on recupere le maximum de cette boucle seulement
					liste_arg.append(arg)					#on ajoute l'argument
					liste_hash.append(arg_hash)				#et le hash par la meme occasion
				if local_max < maximum:						#si c'est fini, qu'on saprete a reboucler
					break									#on retourne le StopIterationError
				maximum = local_max							#on se met a jour pour etre ok la boucle d'apres
				yield tuple(liste_arg), liste_hash			#on retourne le truc

		job_hash = None									#pour un gain cherche qu'un seule fois le 'job_hash'
		try:											#on tente de recuperer le job hash
			job_hash = self.Interim.get_hash(target)	#mais on est pas certain de reussir
		except:											#dans le cas ou on n'y arrive pas
			local = True
		res = [self.process_object(target, *args, timeout=timeout, job_timeout=job_timeout, args_hash=args_hash, job_hash=job_hash, local=local, force=force) for args, args_hash in gener_args(*args)]
		return Local_map(res)							#on retourne l'objet qui contient les bons resultat

	def scanner_object(self, target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, force=False):
		"""
		fait un balayage de 'target' par tous les iterables
		"""
		#a faire en mieu
		class Local_Scaner:
			def __init__(self, target, *args, timeout, job_timeout, local, force, i=0):
				self.target = target
				self.args = args
				self.timeout = timeout
				self.job_timeout = job_timeout
				self.local = local
				self.force = force
				self.i = i
				self.res = self.mk_res()

			def mk_res(self):
				"""
				coeur de l'objet, c'est ici qu'un apelle recursif est fait
				"""
				if self.i+1 == len(self.args):
					return [raisin.Process(self.target, *self.args[:-1], e, timeout=self.timeout, job_timeout=self.job_timeout, local=self.local, force=self.force) for e in self.iter_obj(self.args[-1])]
				return [Local_Scaner(self.target, *self.args[:self.i], e, *self.args[self.i+1:], timeout=self.timeout, job_timeout=self.job_timeout, local=self.local, force=self.force, i=self.i+1) for e in self.iter_obj(self.args[self.i])]

			def iter_obj(self, obj):
				"""
				genere l'objet,
				si ce n'est pas un iterable, le genere une seule fois
				si c'est un iterable, le retourne tel quel
				"""
				try:
					for e in iter(obj):
						yield e
				except:
					yield obj

			def get(self, wait=True):
				return [r for r in self.get_gener(wait)]

			def get_gener(self, wait):
				"""
				retourne la liste des resultats
				"""
				no_error = True
				for r in self.res:
					if no_error:
						try:
							yield r.get(wait)
						except Exception as e:
							r.stop()
							no_error = False
							erreur = e
					else:
						r.stop()
				if not no_error:
					raise erreur

			def get_all(self, wait=True):
				"""
				retourne la liste des resultats
				"""
				return [r.get_all(wait) for r in self.res]
		
			def stop(self):
				for r in self.res:
					r.stop()

		return Local_Scaner(target, *args, timeout=timeout, job_timeout=job_timeout, local=local, force=force)

	class Pooler_loin:
		"""
		met a jour la base de donnee
		tente d'envoyer le travail sur un serveur
		"""
		def __init__(self, father, target, args, args_hash, job_hash, timeout, job_timeout, force):
			with Printer("work preparation...", signature=father.signature):	#on previent l'utilisateur d'une monopolisation
				#preparation
				self.father = father											#objet "Session"
				self.target = target											#pointeur vers une methode ou une fonction a executer
				self.args = args												#tuple des arguments non serialises
				self.args_hash = args_hash										#le hash des arguments (modifier plus tard)
				self.job_hash = job_hash										#cela permet d'eviter de refaire toute l'analyse du code
				self.timeout = timeout											#temps total d'execution
				self.job_timeout = job_timeout									#temps d'execution du script
				self.interim_is_ok = False										#devient True des que le resultat est poste dans la base de donnees
				self.terminate = False											#si on est ici, c'est que la fonction n'a pas ete executee
				self.force = force												#True si l'on s'acharne a avoir une reponse positive, False si on accepte les erreurs

				#a distance
				self.continuer = True											#est True tant qu'il faut s'acharner a comuniquer avec l'exterieur
				self.emetter = self.Emetter(self)								#envoi du boulot

		def stop(self):
			"""
			arrete le processus en cours
			"""
			self.terminate = True			#on dit que c'est fini
			self.continuer = False			#arret de l'envoi du travail

		def get_all(self, wait=True):
			"""
			retourne le resultat sous forme de dictionaire, contenant le plus d'infrmations possibles
			si le resultat n'est pas arrive, retourne {}
			'wait' est un boolen:
				-True => attente que le resultat arrive, avec ou sans echec
				-False => retourne imediatement
			"""
			with Printer("get result", signature=self.father.signature):
				while not self.interim_is_ok:									#tant que le programme n'est pas enregistre dans la base de donnee
					time.sleep(0.1)												#on arrete tout

				while 1:
					try:
						self.interim = self.father.Interim.update_interim({"sending_date": self.interim["sending_date"]})#recuperation de l'etat du resultat
					except:
						continue
					if self.interim["state"] == "waiting":						#si rien n'est encore arrive
						time.sleep(1)											#attente
					else:														#si il y a quelque chose
						if self.interim["state"] == "finish":					#et que c'est meme un joli resultat
							res = self.father.Interim.update_res({"res_hash":self.interim["res_hash"]})#recuperation du resultat enrregistre
							self.stop()											#on arrete tout
							return {**self.interim, **res}						#on retourne la totale
						elif not type(self.interim.get("error", None)) in [KeyboardInterrupt, ImportError, MemoryError, type(None)]:#si l'erreur et mortelle
							if self.force:										#si on shouaite a tout pris eliminer les erreurs
								with Printer("IGNORE AN ERROR...", signature=self.father.signature) as p:
									p.show(str(self.interim.get("error", None)))#on affiche en partie l'erreur quand meme
									self.terminate = False
									self.interim_is_ok = False
									self.father.Interim.del_interim(self.interim["sending_date"], signature=self.father.signature)
									self.emetter.run()
									continue
							self.stop()											#on s'arrete alors
							return self.interim									#on retourne ce que l'on peu
						else:													#dans le cas ou l'erreur est mineure
							if wait:											#si l'on a le droit d'attendre
								time.sleep(1)									#pause de liberation du cpu
								continue										#et bien l'on se troune les pouce
							else:												#a l'inverse, si on diot fire vite
								return self.interim								#on retourne ce que l'on peut

		def get(self, wait=True):
			"""
			retourne imediatement un resultat sauf si wait=True
			on lance le calcul localement
			"""
			res = self.get_all(wait)
			if res.get("state","waiting") == "finish":
				if res["display"] != "":
					print(res["display"])
				return res["res"]
			elif res.get("state","waiting") == "fail":
				raise res["error"]
			raise Exception("the result has not arrived yet!")

		def is_alive(self):
			if self.terminate:
				return False
			try:
				self.interim = self.father.Interim.update_interim({"sending_date": self.interim["sending_date"]})#recuperation de l'etat du resultat
				if self.interim["state"] in ["waiting", "working"]:
					return True
				else:
					return False
			except:
				return True

		def ready(self):
			return not self.is_alive()

		class Emetter:
			"""
			poste le travil a faire
			"""
			def __init__(self, father):
				self.father = father											#objet 'Pooler_loin'
				self.signature = self.father.father.signature					#creation d'une signature personelle
				self.is_coming = False											#devient True des que l'on soccupe personellement de la reception
				self.run()														#on se lance

			def run(self):
				"""
				poste et recupere le travail a faire
				retourne aussitot que le travail est pris en charge
				"""
				'''
				try:
					sys.settrace(self.trace)										#met en place le tracage par la fonction testarret()
					self.courir()													#execution des infos
					sys.settrace(None)												#arret normal du tracage
				except Exception as e:
					raise e
					sys.settrace(None)												#arret du tracage en cas d'exception
				'''
				self.courir()

			def courir(self):
				"""
				permet de faire une seule definition pour une bonne gestion des erreur
				"""
				with Lock("employement_bdd", timeout=60, local=True, display=False):#pour eviter qu'il y ai des conflits avec trop d'acces en meme temps
					with Printer("post all the employement in dataset...", signature=self.signature):
						self.Interim = Interim(signature=self.signature)
						if self.father.ready():
							return None
						if not self.father.continuer:
							return None
						self.father.interim = self.post_all()
						self.father.interim_is_ok = True

			def post_all(self):
				"""
				met l'emploi dans la base de donnee et retourne le dictionaire interim propre a ce dernier
				"""
				with Printer("post args...", signature=self.signature):				#on met l'argument en premier
					args_hash = []													#c'est la liste de la reference des arguments
					for i,pedofile in enumerate(self.father.args):					#pour chaque arguments
						arg = {"arg":pedofile}										#on le prepare
						if i < len(self.father.args_hash):							#si on connait deja le hash de l'argument
							arg["arg_hash"] = self.father.args_hash[i]				#on gagne du temps en enlevant des etapes
						arg = self.Interim.update_arg(arg, signature=self.signature)#on pose alors les arguments
						args_hash.append(arg["arg_hash"])							#on ajoute le hash de cet argument pour le garder par la suite

				with Printer("post code...", signature=self.signature):				#on met le code en deuxieme afin de ne pas crer de conflits
					job = {"target":self.father.target, "job_timeout":self.father.job_timeout}#initialisation du boulot
					if self.father.job_hash != None:								#si on connait l'identifiant du job
						job["job_hash"] = self.father.job_hash						#on l'ajoute affin de s'en servir
					job = self.Interim.update_job(job, signature=self.signature)	#on le met a jour

				with Printer("post interim...", signature=self.signature):			#il est enfin possible de poster l'offre dans sa globalitee
					interim = {"job_hash":job["job_hash"], "args_hash":args_hash, "timeout":self.father.timeout}#la partie principale
					interim = self.Interim.update_interim(interim, signature=self.signature)#enregistrement de ce dernier

				return interim

			def trace(self, frame, event, arg):
				"""
				permet de gerer la mort du thread
				"""
				if event == "line":
					if not self.father.continuer:
						with Printer("I'm killed!", signature=self.signature):
							raise SystemExit()
				return self.trace

	class Pooler_cpu:
		"""
		execute le travail imediatement, au coeur de cette machine
		n'interagit pas avec la base de donnees
		"""
		def __init__(self, father, target, args, timeout, job_timeout):
			self.father = father												#lien vers l'objet parent affin de pouvoir afficher les informations
			self.target = target												#pointeur vers une methode ou une fonction a executer
			self.args = args													#tuple des arguments non serialises
			self.timeout = timeout												#temps total d'execution
			self.job_timeout = job_timeout										#temps d'execution du script
			self.sending_date = time.time()										#date de creation de cet emploi
			self.res = self.start()												#execution imediate de l'emploi
			self.result = {}													#c'est le resultat complet

		def start(self, timeout=None):
			"""
			timeout est seulement la pour une question d'homogeneite avec Pooler_loin
			"""
			with Printer("give work to the CPU...", signature=self.father.signature):#affichage de l'action en cours
				if self.father.pool == True:
					self.father.pool = multiprocessing.Pool()					#on recre un pool avoir l'environement en entier
				self.res = self.father.pool.apply_async(func=self.target, args=self.args)#preparation du travail sur un autre cpu
				return self.res													#le travail est desormais pret

		def get_all(self, wait=True):
			"""
			retourne le dictionaire de reponsse
			"""
			if self.result != {}:												#si on a deja le resultat
				return self.result												#on ne le calcul pas en plus
			while not self.res.ready():											#si le resultat n'est pas encore pret
				if not wait:													#si il faut imediatement rendre la main
					return self.result											#on retourne rien, mais cela est fait imediatement
				if time.time() > self.sending_date+self.timeout:				#si le temps critique est atteind
					raise TimeoutError("Processing time was too long")			#une erreur est retournee	
			try:
				self.result["res"] = self.res.get()
				self.result["state"] = "finish"
				self.result["blacklisted"] = []
				self.result["error"] = None
			except Exception as e:
				self.result["blacklisted"] = [raisin.id]
				self.result["error"] = e
				self.result["state"] = "fail"
			self.result["worker"] = raisin.id
			self.result["display"] = ""
			del self.res
			return self.result													#le resultalt est donc retourne

		def get(self, wait=True):
			"""
			retourne imediatement un resultat sauf si wait=True
			on lance le calcul localement
			"""
			if self.get_all(wait) == {}:
				raise Exception("the result has not arrived yet!")
			if "res" in self.result:
				return self.result["res"]
			raise self.result["error"]

		def stop(self):
			"""
			tue instentanement le processus
			"""

		def is_alive(self):
			"""
			retourne True si le processus travail encore
			"""
			try:
				return not self.res.ready()
			except:
				return False

		def ready(self):
			"""
			retourne False quand le travail est termine
			"""
			return not self.is_alive()

	class Pooler_thread(threading.Thread):
		"""
		execute le travail en local sur cette machine
		simule un faut paralelisme qui n'exploite pas les capacitees de l'ordinateur
		n'interagit pas avec la base de donnee
		"""
		def __init__(self, father, target, args, timeout, job_timeout):
			threading.Thread.__init__(self)										#initialisation du thread
			self.father = father												#lien vers l'objet parent affin de pouvoir afficher les informations
			self.target = target												#pointeur vers une methode ou une fonction a executer
			self.args = args													#tuple des arguments non serialises
			self.timeout = timeout												#temps total d'execution
			self.job_timeout = job_timeout										#temps d'execution du script
			self.sending_date = time.time()										#date de creation de cet emploi
			self.res = None														#valeur du resultat
			self.result = {}													#le resultat complet
			self.start()

		def run(self):
			"""
			execute le travail en le hachant
			"""
			with Printer("give work to the active CPU...", signature=self.father.signature):#affichage de l'action en cours
				self.res = self.target(*self.args)								#execution de la fonction	

		def get_all(self, wait=True):
			"""
			retourne le dictionaire de reponsse
			"""
			if self.result != {}:												#si on a deja le resultat
				return self.result												#on ne le calcul pas en plus
			while self.is_alive():												#si le resultat n'est pas encore pret
				if not wait:													#si il faut imediatement rendre la main
					return self.result											#on retourne rien, mais cela est fait imediatement
				if time.time() > self.sending_date+self.timeout:				#si le temps critique est atteind
					raise TimeoutError("Processing time was too long")			#une erreur est retournee	
			self.result["state"] = "finish"
			self.result["res"] = self.res
			self.result["worker"] = raisin.id
			self.result["error"] = None
			self.result["blacklisted"] = []
			self.result["display"] = ""
			return self.result													#le resultalt est donc retourne

		def get(self, wait=True):
			"""
			retourne imediatement un resultat sauf si wait=True
			on lance le calcul localement
			"""
			if self.get_all(wait) == {}:
				raise Exception("the result has not arrived yet!")
			return self.result["res"]

		def stop(self):
			"""
			tue instentanement le processus
			"""

class Signature:
	"""
	est un objet qui change momentanement la variable
	self.signature de l'objet 'father'
	"""
	def __init__(self, father, signature):
		self.father = father			#cela permet de pouvoir en changer la valeur
		self.signature = signature		#nouvelle signature a implenter sur 'father'
		if self.signature == None:		#si il s'agit d'une signature par defaut
			self.signature = self.father.signature#on ne change rien du tout

	def __enter__(self):
		self.ancienne = self.father.signature#memorisation de l'anciene signature pour povoir revenir en arriere
		self.father.signature = self.signature#remplacement de la signature de 'father' par la nouvelle
		return None

	def __exit__(self, *args):
		self.father.signature = self.ancienne#on remet la valeur d'avant

class Timeout:
	"""
	permet d'executer des fonctions avec un temps limite
	"""
	class Timeout(Exception):
		pass

	def __init__(self, timeout):
		self.timeout = timeout

	def __enter__(self):
		if "win" in sys.platform:
			raise Exception("passés sous linux!")
		else:
			signal.signal(signal.SIGALRM, self.raise_timeout)
			signal.alarm(self.timeout)

	def __exit__(self, *args):
		if "win" in sys.platform:
			pass
		else:
			signal.alarm(0)

	def raise_timeout(self, *args):
		raise Timeout.Timeout()

class Worker:
	"""
	execute le travail a distance
	"""
	def __init__(self, cpu=None, dt=6, compresslevel=2, signature=None, boss=False, laborer=False):
		self.signature = signature												#pour faire un affichage coherent
		self.Interim = Interim(signature=self.signature)						#lien vers la base de donnee
		self.cpu = cpu															#c'est le taux maximum acceptable de cpu, peut etre un nombre ou un dictionaire ex {20.5:20, '6:50', 12:100} = 20% à partir de 20h30, 50% apres 6h...
		if self.cpu == None:
			self.cpu = {"6h30":75, "8h":50, "21h":30, "1h":100}
		self.dt = dt															#temps de lecture du cpu, ie temps de reaction de l'asservissement
		self.compresslevel = compresslevel										#taux de compression du resultat envoyer
		self.boss = boss														#si True, ne s'ocupe que de gerer tout ce qui est autre que le travail
		self.laborer = laborer													#si True, s'occupe uniquement d'executer du travail
		self.frequency = 10/dt													#c'est la frequance de hachage pour les pause des ouvriers en Hz
		self.l_workers = []														#c'est la liste qui contient tous les objets multiprocessing et leurs informations relatives
		self.nbr_cpu = multiprocessing.cpu_count()								#c'est le nombre de cpu sur cette machine
		self.whip = self.__init__event()										#initialise le fichier qui va contenir le fait que l'on doit bosser ou non
		self.one_more = False													#devient True lorsque l'on peu se permettre d'embocher un travailleur
		self.forbidden = []														#c'est la liste des 'sending_date' sur laquelle on ne doit meme pas essayer de bosser
		self.commun = Global_var("partage_boulot", local=True, signature=self.signature)#permet de ne pas bosser a 2 sur le meme emploi
		try:
			self.commun.read()
		except:
			self.commun.write([])
		if self.boss:															#si il faut juste diriger
			self.run_boss()														#on chapotte le tout
		elif self.laborer:														#si il faut seulement bosser
			self.run_laborer()													#on appelle la methode qui cherche du boulot et l'execute
		else:																	#si il faut tout faire a la fois
			threading.Thread(target=self.listen_servers).start()				#fait un pont avec les serveurs
			self.run()															#demarrage du travailleur

	def __init__event(self):
		"""
		ouvre le fichier et lui met la valeur par default
		"""
		whip = os.path.join(raisin.rep, "raisin_whip.txt")
		with open(whip, "w") as file:
			file.write("stop")
		return whip

	def autorize_cpu(self, motif=None):
		"""
		retourne le taux d'utilisation autorise maximum de cpu
		retourne un entier entre 0 et 100
		en cas d'erreur, retourne 100
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

		if motif == None:														#si on est pas entrain de faire du recursif
			motif = self.cpu													#on recopi la variable de base
		if type(motif) == str:
			try:
				motif = eval(motif)
			except:
				return 100
		if type(motif) == int:													#si le taux est donne en entier
			return max(0, min(100, motif))										#on le renvoi tel qu'elle
		elif type(motif) == float:												#si il est deja dans le bon format
			return max(0, min(100, int(motif)))									#on se contente de verifier sa valeur
		elif type(motif) == dict:												#dans le cas ou il faut etre plus precis
			date = datetime.datetime.now()										#on regarde l'heure actuelle
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
				return 100
		else:
			return 100

	def equalize(self):
		"""
		fait de l'equilibre sur les serveurs
		"""
		with Printer("balancing files betwen servers...", signature=self.signature):
			pass
			#dbx.users_get_space_usage()

	def execute(self, interim, job, args):
		"""
		execute le travail demander
		retourne l'objet multiprocessing qui execute ce boulot
		"""
		def prudence(interim, job, args, frequency, signature, compresslevel):
			"""
			execute localement le travail
			"""
			import os															#cette fonction n'aura pas acces a l'environnement
			import raisin														#il faut donc importer les modules qui vont bien
			import uuid															#permet de generer un code uniqe
			raisin_answer = None												#le resultat du calcul
			raisin_display = ""													#tout ce qu'affiche la fonction 'fonction'
			path_file = os.path.join(raisin.temprep, str(uuid.uuid4()))
			try:
				with raisin.raisin.Printer("I'm working...", signature=signature):
					fonction = raisin.raisin.deserialize(job["target_data"], signature=signature, frequency=frequency, modules=job["modules"])
					args = tuple([raisin.raisin.deserialize(arg["arg_path"], signature=signature) for arg in args])
					with raisin.raisin.Timeout(job["job_timeout"]):
						raisin_answer = fonction(*args)
					with open(path_file, "wb") as f:
						for pack in raisin.raisin.serialize(raisin_answer, compresslevel=compresslevel, generator=True, signature=signature):
							f.write(pack)
					return {"answer":path_file, "display":raisin_display, "error":None}
			except Exception as e:
				return {"answer":None, "display":raisin_display, "error":e}

		signature = str(uuid.uuid4())
		with Printer("real copy of environement...", signature=signature):
			func = raisin.copy(prudence, signature=signature)
		pool = multiprocessing.Pool()
		signature_dico = {"rep":raisin.temprep, "signature":signature}
		worker = pool.apply_async(func=func, args=(interim, job, args, self.frequency, signature_dico, self.compresslevel))#execution du code
		return worker

	def get_cpu(self):
		"""
		retourne le pourcentage de cpu entre 0 et 100
		le pourcentage retourne est le pourcentage moyen sur une periode de 'dt' secondes
		"""
		try:
			import psutil
			cpu = psutil.cpu_percent(self.dt)
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
				return cpu
			except:
				try:
					i = os.subprocess.Popen("top -d "+str(self.dt).replace(".",",")+" -n 2").read()
					cpu = float(i.split("%Cpu(s):")[-1].split("us,")[0].replace(",",".").replace("  "," ").split(" ")[1])
					return cpu
				except:
					time.sleep(self.dt)
					return 0.0

	def get_work(self):
		"""
		affiche dans la colone principale
		retourne None en cas d'echec
		et (interim, job, args) en cas de reussite
		"""
		with Printer("get job...", signature=self.signature):
			
			#recuperation des donnee en ligne
			with Printer("organisation of inline data...", signature=self.signature):
				d_on_line_waiting, d_on_line_fail, d_on_line_working = {}, {}, {}#a chaque identifiant de server, associ la liste des elements
				random.shuffle(raisin.servers.servers)
				for i, server in enumerate(raisin.servers.servers):			#pour chaque serveur
					try:													#mais pour cela, on doit prendre milles et une precautions
						with raisin.Timeout(10):
							l = server.ls(signature=self.signature)			#tentative de recuperations des infos
						l = [e for e in l if "interim&" in e]				#epurage de ce qui ne nous concerne pas
						random.shuffle(l)									#on le melange pour eviter les conflits
						d_on_line_waiting[i] = [float(e.split("&")[1]) for e in l if e.split("&")[2] == "waiting"]#recuperation de la 'sending_date' seulement
						d_on_line_fail[i] = [float(e.split("&")[1]) for e in l if e.split("&")[2] == "fail"]#on separe selon la categorie
						d_on_line_working[i] = [float(e.split("&")[1]) for e in l if e.split("&")[2] == "working"]
					except:													#si sa rate
						d_on_line_waiting[i] = []							#ignore ce serveur
						d_on_line_fail[i] = []								#afin de ne pas plus le surbouquer
						d_on_line_working[i] = []							#on fait donc croire qu'il n'y a rien dessus

			#analyse des donnees
			for exigency in range(3):										#nous allons proceder par ordre croissant d'exigeance
				for i, server in enumerate(raisin.servers.servers):			#pour chaque serveur
					for sending_date in {0:d_on_line_waiting, 1:d_on_line_fail, 2:d_on_line_working}[exigency][i]:#pour chaque sending dans le bon etat et dans le bon serveur
						if sending_date in self.forbidden:					#si ce boulot n'est pas fait pour nous
							continue										#on passe au suivant
						try:												#il est temps de tenter un telechargement
							interim = deserialize(server.load("interim&"+str(sending_date)+"&"+{0:"waiting", 1:"fail", 2:"working"}[exigency], signature=self.signature), signature=self.signature)#tentative de telechargement
						except:												#si c'est rate
							continue										#on va directement voire l'offre suivante
						if raisin.id in interim.get("blacklisted", []):		#si on a deja echoue sur ce job
							self.forbidden.append(sending_date)				#il est important d'apprendre de nos erreurs
							continue										#on va voir le suivant
						if sending_date in self.commun.read():				#si notre voisin bosse deja dessus
							continue										#on ne va pas aussi bosser dessus, un seul suffit
						interim["receivers"] = interim.get("receivers", [])	#si ce champs n'existe pas, on le cre
						if (interim["receivers"] != []) and (not raisin.id in interim["receivers"]):#si il ne nous est pas destine
							self.forbidden.append(sending_date)				#memorisation pour ne pas s'y reprendre
							continue										#on le laisse a la bonne machine					
						if not type(interim.get("error", None)) in [KeyboardInterrupt, ImportError, MemoryError, type(None)]:#si on va echouer dessus
							self.forbidden.append(sending_date)				#memorisation pour ne pas s'y reprendre
							continue										#on ne prend meme pas le risque

						#recuperation de tout le boulot
						with Printer("downloading of the integrality...", signature=self.signature):
							interim["last_support"] = time.time()			#on met a jour la date de derniere visite
							interim["state"] = "working"					#on dit que l'on est entrain de s'en charger
							interim_data = serialize(interim, compresslevel=0, generator=False, signature=self.signature)#on serialise le paquet
							if exigency != 1:
								while 1:									#on l'envoi a tout pris
									try:									#mais en prenant 1001 precautions
										server.send(interim_data, "interim&"+str(sending_date)+"&working", signature=self.signature)#on tente d'envoyer ce petit paquet
										break								#et on sort de la boucle
									except:									#si on a echouer, on va tenter de recomencer
										try:								#car les erreurs ne sont pas gerees par le serveur
											server.remove("interim&"+str(sending_date)+"&working", signature=self.signature)#tant que l'envoi ne fonctionne pas, on s'y acharne
										except:								#si on en arrive la
											continue						#c'est qu'il faut recomencer
								try:										#on va essaiyer de degommer le code existant
									server.remove("interim&"+str(sending_date)+"&"+{0:"waiting", 1:"fail", 2:"working"}[exigency], signature=self.signature)#tentative de suppression
								except:										#mais l'on insiste pas tres fort
									pass									#car on s'y aucupe mieu apres, c'est juste une histoire de gain de temps

							with Printer("download job...", signature=self.signature):
								if "job_data" in interim:					#si le boulot n'est pas dans une autre fonction
									job = deserialize(interim["job_data"], signature=self.signature)#on l'extrait localement
								else:										#si il figure dans un autre fichier
									while 1:								#on va tenter sans relache de recuperer le boulot
										try:								#toujours, la meme histoire
											job_data = server.load("job&"+interim["job_hash"], signature=self.signature)#tentative de telechargement
											job = deserialize(job_data, signature=self.signature)#on le rend exploitable
											break							#il faut faire attention
										except:								#et donc retenter si on echou
											continue						#ainsi, on repart en haut de la boucle
								job["modules"] = deserialize(job["modules_data"], signature=self.signature)#recuperations des modules

							with Printer("download arguments...", signature=self.signature):
								while 1:									#on va tenter sans relache de recuperer le boulot
									try:									#toujours, la meme histoire
										args = [server.load("arg&"+arg_hash, signature=self.signature) for arg_hash in interim["args_hash"]]#telechargement des information sur les arguments#tentative de telechargement
										args = [deserialize(a, signature=self.signature) for a in args]#deserialisation des arguments
										break								#il faut faire attention
									except:									#et donc retenter si on echou
										continue							#ainsi, on repart en haut de la boucle
								for n, arg in enumerate(args):				#pour chacun des fichiers potentiellement gros
									arg_path = os.path.join(raisin.temprep, "arg_"+arg["arg_hash"]+".rais")#on recupere le nom qu'il est cence avoir
									arg["arg_path"] = arg_path				#on le sauvegarde pour creer un pont avec multiprocessing
									if arg.get("arg_data", b"") != b"":		#si l'argument est present localement
										with open(arg_path, "wb") as file:	#on ouvre le fichier en mode ecrasement, pour que ca fonctionne aussi la deuxieme fois
											file.write(arg["arg_data"])		#on y ajoute le bout de fichier fraichement recupere
									else:									#si c'est un peu plus complique que cela
										try:								#nous allons tenter de recuperer
											size = os.path.getsize(arg_path)#la taille du fichier
										except:								#si l'on arrive a rien
											size = 0						#c'est que le fichier n'existe pas
										rang = size//arg["chunk_size"]		#c'est l'endroit a partir du quel il faut continuer le fichier
										for i in range(rang, len(arg["torrent"])):#pour chaque elements qui n'est pas encore telecharge
											while 1:						#tant que l'on arrive pas a le telecharger
												try:						#on essay en boucle
													data = server.load(arg["torrent"][i], signature=self.signature)#on tente sans fin de telecharger la suite du fichier
													break					#si le telechargement est efectuer, on ne le fait qu'une seule fois
												except:						#dans le cas ou il y a un probleme
													continue				#on retente notre chance
											with open(arg_path, "ab") as file:#on ouvre le fichier en mode ajout
												file.write(data)			#on y ajoute le bout de fichier fraichement recupere
						
							self.forbidden.append(interim["sending_date"])
							self.commun.append(interim["sending_date"])
							return interim, job, args

		with Printer("wait to pain servers...", signature=self.signature):
			time.sleep(900)													#on fait une longue pause (environ 15min) si il n'y a rien

	def hibernate(self):
		"""
		donne l'ordre aux ouvriers de s'arretter
		"""
		with open(self.whip, "w") as file:										#c'est bon, il ont enfin droit a leur tee-break!
			file.write("stop")
	
	def listen_servers(self, signature="valeur par defaut"):
		"""
		permet de faire un pont entre la base de donnee et les differents serveurs
		tourne continuellement afin de recuperer les resultat si il y en a
		ne retourne rien
		"""
		def genere_res(server, ress_hash):
			"""
			est un generateur qui cede peu a peu chaque bout de resultat
			"""
			for res_hash in ress_hash:											#pour chaque sous paquet de resultat
				while 1:														#on va s'acharner a le telecharger
					try:														#mais en etant tres prudent
						yield server.load("res&"+str(res_hash), signature=signature)#on essai alors de retourne le petit bout de resultat
						break													#si ca a fonctionne, c'est bon, on passe au suivant
					except:														#si ca a merdoye
						continue												#on refait un tour de manege

		if signature == "valeur par defaut":
			signature = str(uuid.uuid4())										#signature de ce Thread en local
		with Printer("stay alert from servers...", signature=signature):		#on indique le demarage du thread
			Interim_local = Interim(signature=signature)						#on cre un objet Interim afin de ne pas avoir de souci avec l'ecriture dans la base de donnees
			last_time_cleen = time.time()										#dernier moment ou le serveur peu etre netoyer
			compteur = 0														#il permet d'eviter de faire trop de requette sur le serveur
			d_on_line_waiting, d_on_line_fail, d_on_line_working, d_on_line_finish = {}, {}, {}, {}#a chaque identifiant de server, associ la liste des elements
			while 1:															#on entame une grande boucle infinie
				#organisation donnees locales
				with Printer("organisation of local data...", signature=signature) as p:
					with Lock("bdd", signature=signature):						#pour comencer, il faut deja regarder ce qu'il y a dans la base de donnee
						with Lock("interim_bdd", timeout=10, signature=signature):
							curseur = Interim_local.bdd.cursor()
							r = curseur.execute("""SELECT sending_date FROM interim WHERE state = 'finish'""")#qui va lire ceux qui sont termine
							l_finish = r.fetchall()								#lencement de la requette
							r = curseur.execute("""SELECT sending_date, error FROM interim WHERE state = 'fail'""")#recuperation de ceux qui ont echoue
							l_fail = [(e[0], deserialize(e[1], signature=signature)) for e in r.fetchall()]#lancement de cette deuxieme requette
							r = curseur.execute("""SELECT sending_date FROM interim WHERE state = 'working'""")#ca c'est ceux qui sont normalement deja pris en charge
							l_working = r.fetchall()							#recuperation de ce resultat
							r = curseur.execute("""SELECT sending_date FROM interim WHERE state = 'waiting'""")#enfin, les petits derniers
							l_waiting = r.fetchall()							#sont ceux qui ne sont pas encore envoye
					l_terinate = [e[0] for e in l_finish]						#extraction de la partie principale des offres d'emploi qui ne doivent pas figurer sur le serveur
					l_terinate.extend([e[0] for e in l_fail if not type(e[1]) in [KeyboardInterrupt, ImportError, MemoryError]])#on y ajoute celle ou il n'y a plus d'espoir
					l_active = [e[0] for e in l_working] + [e[0] for e in l_waiting] + [e[0] for e in l_fail if type(e[1]) in [KeyboardInterrupt, ImportError, MemoryError]]#elles, ce sont les offres d'emploi qui doivent ou qui sont entrain d'etre traitees
				p.show("terminate :"+str(len(l_terinate)))
				p.show("no terminate :"+str(len(l_active)))
				if (l_active == []) and compteur <= 720:						#si il n'y a rien a faire
					time.sleep(5)												#on attend un peu
					compteur += 1												#on incremente le compteur pour q'au minimum, on aille voir la suite une fois par heure
					continue													#on recomence la boucle
				compteur = 0													#il est remis a 0

				#organisation des donnes en lignes
				with Printer("organisation of inline data...", signature=signature):
					for i, server in enumerate(raisin.servers.servers):			#pour chaque serveur
						while 1:												#on va recuperer ce qu'il y a dessus
							try:												#mais pour cela, on doit prendre milles et une precautions
								with raisin.Timeout(10):
									l = server.ls(signature=signature)			#tentative de recuperations des infos
								l = [e for e in l if "interim&" in e]			#epurage de ce qui ne nous concerne pas
								d_on_line_waiting[i] = [float(e.split("&")[1]) for e in l if e.split("&")[2] == "waiting"]#recuperation de la 'sending_date' seulement
								d_on_line_fail[i] = [float(e.split("&")[1]) for e in l if e.split("&")[2] == "fail"]#on separe selon la categorie
								d_on_line_working[i] = [float(e.split("&")[1]) for e in l if e.split("&")[2] == "working"]
								d_on_line_finish[i] = [float(e.split("&")[1]) for e in l if e.split("&")[2] == "finish"]
								break											#dans le cas ou l'operation est un succes, la place est laisse au suivant
							except:												#si sa rate
								pass											#on fait une pause dans l'espoir que ca se remete en place
				
				#suppression des doublons
				with Printer("deleting duplicates...", signature=signature):
					actualize = False											#devient True si il y a du changement
					for i, l in d_on_line_waiting.items():						#on y va peu a peu
						for rang, s in enumerate(l):							#pour chaque services
							tuer = False										#devien True si il faut faire mourir cet emploi
							if True in [(s in v) for k,v in d_on_line_working.items()]:#si il ne sert plus a rien
								tuer = True										#on le bute
							elif True in [(s in v) for k,v in d_on_line_fail.items()]:#on fait le test avec tout les etats plus interressant
								tuer = True										#de meme, si un ordi a deja echoue dessus
							elif True in [(s in v) for k,v in d_on_line_finish.items()]:#enfin, c'est le dernier niveau de verification
								tuer = True										#si le travail est termine, on extermine son mauvais clone
							if tuer:											#si il doit etre bute
								try:											#on va tenter de lui metre le coup fatal
									raisin.servers.servers[i].remove("interim&"+str(s)+"&waiting", signature=signature)#la, on l'acheve
									del d_on_line_fail[i][rang]
									actualize = True							#on marque le fait qu'il y a eu un changement
								except:											#si c'est vraiment un dur a cuire
									continue									#tant pis, on adandone
					for i, l in d_on_line_working.items():						#on y va peu a peu
						for rang, s in enumerate(l):							#pour chaque service
							tuer = False										#devient True si il faut faire mourir cet emploi
							if True in [(s in v) for k,v in d_on_line_fail.items()]:#on fait le test avec tout les etats plus interressant
								tuer = True										#de meme, si un ordi a deja echoue dessus
							elif True in [(s in v) for k,v in d_on_line_finish.items()]:#enfin, c'est le dernier niveau de verification
								tuer = True										#si le travail est termine, on extermine son mauvais clone
							if tuer:											#si il doit etre bute
								try:											#on va tenter de lui metre le coup fatal
									raisin.servers.servers[i].remove("interim&"+str(s)+"&working", signature=signature)#la, on l'acheve
									del d_on_line_fail[i][rang]
									actualize = True							#on marque le fait qu'il y a eu un changement
								except:											#si c'est vraiment un dur a cuire
									continue									#tant pis, on adandone
					for i, l in d_on_line_fail.items():							#on y va peu a peu
						for rang, s in enumerate(l):							#pour chaque services
							if True in [(s in v) for k,v in d_on_line_finish.items()]:#enfin, c'est le dernier niveau de verification
								try:											#on va tenter de lui metre le coup fatal
									raisin.servers.servers[i].remove("interim&"+str(s)+"&working", signature=signature)#la, on l'acheve
									del d_on_line_fail[i][rang]
									actualize = True							#on marque le fait qu'il y a eu un changement
								except:											#si c'est vraiment un dur a cuire
									continue									#tant pis, on adandone
					if actualize:												#si des emploi viennent d'etres postee
						continue												#on repart en haute du "while 1:"

				#suppression des travaux termines
				with Printer("removing of terminate employement...", signature=signature) as p:
					actualize = False											#devient True si il y a du changement
					for etat, d in [("waiting", d_on_line_waiting), ("fail", d_on_line_fail), ("working", d_on_line_working), ("finish", d_on_line_finish)]:#parcours de l'integralite des boulots
						for i in d.keys():										#dans chaqun des differents serveurs
							for s in d[i]:										#pour chaque interim qu'il comporte
								if s in l_terinate:								#si il ne sert a rien
									p.show("remove "+str(s))
									try:										#il faut tenter de le supprimer
										server = raisin.servers.servers[i]		#il faut bien evidement prendre le bon serveur
										server.remove("interim&"+str(s)+"&"+etat, signature=signature)#la on tente de le supprime
										actualize = True						#quand on en est la, c'est qu'il y a eu du changement
									except:										#si ca a cafouille
										pass									#pas d'affolement, c'est pas dramatique
					if actualize:												#si des emploi viennent d'etres postee
						continue												#on repart en haute du "while 1:"

				#actualisation des traveaux en cours
				with Printer("recovery of results...", signature=signature) as p:
					actualize = False											#devient True si il y a du changement
					for s in l_active:											#pour chaque boulot qui est entrain d'etre traite
						for i in d_on_line_finish.keys():						#on tente de voir sur quel serveur il se trouve
							if s in d_on_line_finish[i]:						#lorsque l'on localise enfin le bon serveur
								server = raisin.servers.servers[i]				#on le recupere
								try:											#puis on se prepare a telecharger le boulot
									interim = deserialize(server.load("interim&"+str(s)+"&finish", signature=signature), signature=signature)#on le telecharge
									for k,v in interim.items():					#on affiche la ou l'on en est
										p.show(str(k)+":"+str(v))				#pour savoir ce qui est recupere
								except:											#si on arrive pas a recuperer ce boulot
									continue									#il est temps de passer au suivant sans plus s'y attarder
								res = {"res_hash":interim["res_hash"], "compresslevel":interim["compresslevel"], "res_data":genere_res(server, interim["ress_hash"])}
								Interim_local.update_res(res)					#on recupere le resultat
								Interim_local.update_interim(interim)			#dans tout les cas, on met a jour cet interim
								actualize = True								#il y a donc du changement
						for i in d_on_line_fail.keys():							#on va faire la meme chose pour les boulot qui semble avoir echoues
							if s in d_on_line_fail[i]:							#on regarde sur quel serveur il se trouve
								server = raisin.servers.servers[i]				#affin de pouvoir selectionner le bon
								try:											#comme d'habitude, plein de precautions sont prises
									interim = deserialize(server.load("interim&"+str(s)+"&fail", signature=signature), signature=signature)#telechargement pour plus de details
									for k,v in interim.items():					#on affiche la ou l'on en est
										p.show(str(k)+":"+str(v))				#pour savoir ce qui est recupere
								except:											#si le telechargement rate
									continue									#on n'insiste pas, tant pis
								if not type(Interim_local.update_interim(interim).get("error", None)) in [KeyboardInterrupt, ImportError, MemoryError, type(None)]:#si l'erreur n'est pas une erreur mineure
									actualize = True							#on considere alors un vrai changement
					if actualize:												#si des emplois viennent d'etres postes
						continue												#on repart en haute du "while 1:"

				#envoi des travaux pas encore presents sur le serveur
				with Printer("sending missing interims...", signature=signature) as p:
					actualize = False											#devient True si il y a du changement
					for s in l_active:											#pour chaque boulot qui est cence etre sur un serveur
						if not True in [(True in v) for v in [[(s in l) for k,l in d.items()] for d in (d_on_line_waiting, d_on_line_fail, d_on_line_working, d_on_line_finish)]]:	#si il n'est sur aucun d'entre aux
							p.show(str(s))
							interim = Interim_local.update_interim({"sending_date":s})#on va l'envoyer pour qu'il y soit
							Interim_local.send(interim)							#mais avant cela il faut recuperer les infos relative a ce boulot
							actualize = True									#quand on en est la, c'est que des choses ont changees
					if actualize:												#si des emploi viennent d'etres postee
						continue												#on repart en haute du "while 1:"

				#epurage du serveur
				with Printer("clean the serveur...", signature=signature):
					clean = False
					for i in range(len(raisin.servers.servers)):				#il faut dabord scruter chaque serveur en profondeur
						if d_on_line_waiting[i]+d_on_line_fail[i]+d_on_line_working[i]+d_on_line_finish[i] == []:#si il n'y a plus rien d'interressant sur le serveur										#si l'un d'entre eux est vide
							try:												#on lui enleve tout ce qu'il lui reste
								server = raisin.servers.servers[i]				#recuperation du serveur concerne par l'evenement
								if not Interim_local.is_lock(server, signature=signature):#dans le cas ou le serveur est libre
									if last_time_cleen + 3600*6 < time.time():	#si cela fait suffisement longtemps que l'on est pret a effacer
										[server.remove(e, signature=signature) for e in [e for e in server.ls(signature=signature) if "&" in e]]#ca, c'est tout les elements a supprimer
										clean = True
							except:												#si ca rate
								pass											#tant pi, on passe a la suite
					if clean:
						last_time_cleen = time.time()							#on remet les compteur a zero
				
				if len(l_active) == 0:
					time.sleep(30)

	def regulator(self):
		"""
		hache le travail de facon a ne pas exeder le taux autorise de cpu
		actualise la variable 'self.one_more'
		"""
		def chopper():
			"""
			hache le travail des ouvriers
			c'est ici que l'on ordone de faire des pose ou de se remetre au boulot
			"""
			while 1:															#on ne s'arrete jamais, on hache en continue
				if self.cyclical_report >= 1:									#si il faut les faire bosser a fond
					self.resurrect()											#on les fouette pour qu'ils aillent plus vite
					time.sleep(1/self.frequency)								#on refait tout de meme un test juste apres
				elif self.cyclical_report <= 0:									#dans le cas contraire, si il doivent roupiller
					self.hibernate()											#on leur donne des somniferes
					time.sleep(1/self.frequency)								#il sont laisser tranquil un petit bout de temps
				else:															#si le travail doit etre hache
					self.resurrect()											#pandant la premiere periode
					time.sleep(self.cyclical_report/self.frequency)				#il sont actif et c'est seulement
					self.hibernate()											#durant la deuxieme partie du temps
					time.sleep((1-self.cyclical_report)/self.frequency)			#qu'il profite de leur congees

		def calculator():
			"""
			c'est ici que l'on fait les calculs d'asservisement de CPU
			au passage, met aussi a jour la variable 'self.one_more'
			"""
			signature = str(uuid.uuid4())										#creation d'un identifiant unique
			temps = 0															#dernier moment a partir duquel le rapport cyclique est rester bloque a 1
			with Printer("cpu usage regulation...", signature=signature):
				while 1:														#le calcul va etre fait en boucle
					with Printer("calculing cyclical...", signature=signature) as p:
						e = self.autorize_cpu(self.cpu)							#voici le taux maximum de cpu autorise que l'on va tenter d'atteindre
						p.show("autorized max cpu: "+str(round(e))+" %")
						s = self.get_cpu()										#taux actuele d'utilisation du cpu (notre processs + les autres)
						p.show("mesured cpu: "+str(round(s))+" %")
						if self.boss == True:									#si les travailleur sont dans un autre processus
							self.cyclical_report = min(1.0, max(0.0, self.cyclical_report-.01*(s-e)))
						else:
							k = float(len(self.l_workers))/float(100*self.nbr_cpu)#c'est le coefficient d'amplification de rapport cyclyque
							if k == 0:											#si il n'y a aucun ouvrier sur le terrain
								self.cyclical_report = 1.0						#et on s'apprette a les faire bosser plein pot
							else:												#dans le cas ou il y a deja quelques ouvriers
								self.cyclical_report = min(1.0, max(0.0, self.cyclical_report+k*(e-s)))#une nouvelle loie sur leur horaires est pondue
						p.show("chopper rate: "+str(round(100*self.cyclical_report))+" %")
					if self.cyclical_report < 1.0:								#si tout le monde n'est pas a fond
						temps = time.time()										#c'est que la boite n'est pas prete a embocher une nouvelle personne
						self.one_more = False									#on ferme donc les portes
						continue												#on repart donc pour une nouvelle estimation des temps de conges
					if time.time()-temps > 10*self.dt:							#si tout est calcm depuis un moment
						self.one_more = True									#c'est qu'on est fin pret a etandre nos effectifs
					
		self.cyclical_report = 0.0												#on commence par fixer le rapport cyclique a 0

		threading.Thread(target=chopper).start()								#preparation du hacheur et demarrage de ce dernier
		threading.Thread(target=calculator).start()								#mise au boulot de celui que calcule le rapport cyclyque
		return None

	def resurrect(self):
		"""
		relance tous les processus en veille
		"""
		with open(self.whip, "w") as file:										#on change l'evenement affin qu'il soit vu par les travailleurs
			file.write("run")

	def run(self):
		"""
		le reveil du patron sonne,
		il se met en branle
		"""
		def send_resultat(server, res_generator):
			"""
			envoi le resultat sur les serveurs
			retourne la liste des res_hash
			"""
			with Printer("sending result...", signature=self.signature):
				ress_hash = []													#au debut, cette liste est vide
				for data in res_generator:										#pour chaque paquets de bytes
					ress_hash.append(self.Interim.get_hash(data, signature=self.signature))#on recupere la signature du resultat
					name = "res&"+ress_hash[-1]									#c'est le nom de ce paquet sur les serveurs
					while 1:													#on va tenter de l'envoyer en jusqu'a ce que mort s'en suive
						try:													#on prend plain de precautions
							while not name in server.ls(signature=self.signature):#tant que le paque n'est pas sur le serveur
								server.send(data, name, signature=self.signature)#on tente d'y remedier
							break
						except:
							continue
			return ress_hash

		self.regulator()													#travail en arriere plan pour asservir le cpu

		with Printer("it is working...", signature=self.signature):
			while 1:														#a partir du moment que l'on est lance, l'on ne s'arette jamais
				if self.one_more and (len(self.l_workers) < self.nbr_cpu):		#si il est temps d'aller chercher du boulot
					with Printer("employ a new worker..."):
						work = self.get_work()									#recuperation du travail a faire
					if work != None:											#si cela n'a pas echoue
						interim, job, args = work								#on le separe en plusieurs parties
						travailleur = {}										#c'est lui qui contient le pool et les infos relative a ce dernier
						travailleur["worker"] = self.execute(interim, job, args)#le travailleur est depose sur le chantier
						travailleur["interim"] = interim						#recuperation de l'interim
						travailleur["job"] = job								#recuperation du boulot
						travailleur["args"] = args								#recuperation des arguments
						self.l_workers.append(travailleur)						#et on tente de l'executer
					if self.autorize_cpu() < 100:								#si l'utilisateur nous impose d'etre parcimonieux avec les resources de l'ordinateur
						time.sleep(2*self.dt)									#une petite pause s'impose le temps que la nouvelle loi sur les conges soit calculee

				for i, travailleur in enumerate(self.l_workers):				#pour chaque travailleurs:
					worker = travailleur["worker"]								#on regarde seulement si le pool lui meme
					if worker.ready():											#est pret, c'est a dire si son execution est terminee
						with Printer("send the result...", signature=self.signature):#appretation a avoyer le resulatat
							interim = travailleur["interim"]					#initialisation de l'interim
							name = "interim&"+str(interim["sending_date"])		#c'est le nom d'interim dans le bon serveur
							server = [s for s in raisin.servers.servers if s.id == interim["server_id"]][0]#recuperation du serveur qui contient ce boulot
							result = worker.get()
							if result["answer"] != None:						#si le travailleur a bien fait son boulot
								with Printer("send the body of the result...", signature=self.signature):
									with open(result["answer"], "rb") as f:		#on recupere le resultat
										res_generator = self.Interim.generateur(f)
										ress_hash = send_resultat(server, res_generator)#on envoi ce resultat
							with Printer("update the interim on server...", signature=self.signature):
								try:
									interim = deserialize(server.load(name+"&working", signature=self.signature), signature=self.signature)#tentative de telecharger l'offre d'emploi telle qu'elle apparait sur le serveur
								except:											#dans le cas ou le telechargement ne donne rien
									pass										#on garde l'interim par defaut
								if interim["state"] != "finish":				#si ce travail n'est pas deja fait par un autre
									if result["error"] == None:					#si le resultat ne contient pas d'erreur
										interim["state"] = "finish"				#cette tache est totalement terminee
										interim["error"] = None					#il n'y a pas d'erreur
										interim["res_hash"] = self.Interim.get_hash(result["answer"], signature=self.signature)
										interim["ress_hash"] = ress_hash		#evidement, on met a jour la liste des resultats
										interim["display"] = result["display"]	#ajout de l'affichage graphique
										interim["compresslevel"] = self.compresslevel#ajout du taux de compression de ce resultat
										interim["blacklisted"] = interim["blacklisted"]#on ne s'ajoute pas a la liste noir
										interim["last_support"] = time.time()	#on met a jour ce moment
										interim["worker"] = raisin.id			#on dit qui est le dernier a avoir bosse
									else:										#dans le cas ou une erreur est suspicieuse
										interim["state"] = "fail"				#on marque le fait que quelque chose n'est pas propre
										interim["error"] = result["error"]		#dictionaire des differentes erreurs
										interim["res_hash"] = None				#il n'y a pas des resultat
										interim["ress_hash"] = []				#donc encore moin un gros resultat
										interim["display"] = result["display"]	#des choses ont pu etre affichee avant que l'erreur ne surviene
										interim["compresslevel"] = self.compresslevel#le taux de compression est celui
										interim["blacklisted"].append(raisin.id)#on se note dans la liste des ordinateurs qui ont echoues afin de ne pas refaire la meme erreur
										interim["last_support"] = interim["last_support"]#on ne met surtout pas a jour le fait qu'on ai intervenu
										interim["worker"] = raisin.id			#on dit qui est le dernier a avoir bosse
									data = serialize(interim, compresslevel=0, generator=False, signature=self.signature)#serialisation de l'interim
									while 1:									#il est temps d'envoyer le resultat
										try:									#on tente d'envoyer la reponse
											server.send(data, name+"&"+interim["state"], signature=self.signature)#avec son etat actuel
											try:
												server.remove(name+"&working", signature=self.signature)
											except:
												pass
											try:
												if interim["state"] == "finish":
													server.remove(name+"&fail", signature=self.signature)
											except:
												pass
											try:
												server.remove(name+"&waiting", signature=self.signature)
											except:
												pass
											break								#si c'est un succes, on en fini la
										except:									#si c'est un echec
											try:								#on va essayer de faire en sorte que ca fonctionne au prochain coup
												server.remove(name+"&"+interim["state"], signature=self.signature)#aisin on supprime ce qui serait suceptible de generer une erreur
											except:								#si c'est l'acces a internet qui fait defaut
												time.sleep(10)					#on attend un moment le temps que la conection revienne
								del worker										#on va forcer sa destruction pour liberer la memoire
								del self.l_workers[i]							#on supprime la ligne affin de ne pas refaire la meme chose la boucle juste apres
								break											#il est important de na pas continuer car un decalage dans le for vien d'apparaitre
				if self.autorize_cpu() < 100:									#si on est pas trop presse
					time.sleep(2*self.dt)										#on fait une petite pause qui libere les resources

	def run_boss(self):
		"""
		n'execute pas le travail mais gere le cpu, l'envoi des boulot et la recuperations des travaux termines
		"""
		self.upgrade()														#on regarde si il y a des mises a jour
		self.equalize()														#tente d'équilibre la place sur les serveurs
		self.regulator()													#asservissement du cpu
		self.listen_servers(self.signature)									#fait un pont avec les serveurs

	def run_laborer(self):
		"""
		se charge de recuperer du travail et de l'executer
		"""
		def send_resultat(server, res_generator):
			"""
			envoi le resultat sur les serveurs
			retourne la liste des res_hash
			"""
			with Printer("sending result...", signature=self.signature):
				ress_hash = []													#au debut, cette liste est vide
				for data in res_generator:										#pour chaque paquets de bytes
					ress_hash.append(self.Interim.get_hash(data, signature=self.signature))#on recupere la signature du resultat
					name = "res&"+ress_hash[-1]									#c'est le nom de ce paquet sur les serveurs
					while 1:													#on va tenter de l'envoyer en jusqu'a ce que mort s'en suive
						try:													#on prend plain de precautions
							while not name in server.ls(signature=self.signature):#tant que le paque n'est pas sur le serveur
								server.send(data, name, signature=self.signature)#on tente d'y remedier
							break
						except:
							continue
			return ress_hash

		with Printer("I want to work!...", signature=self.signature):
			while 1:														#on va sans cese chercher du travail
				work = self.get_work()										#recuperation du travail a faire
				if work != None:											#si cela n'a pas echoue
					interim, job, args = work								#on le separe en plusieurs parties
					
					"""execution du travail"""
					raisin_answer = None									#le resultat du calcul
					raisin_display = ""										#tout ce qu'affiche la fonction 'fonction'
					path_file = os.path.join(raisin.temprep, str(uuid.uuid4()))
					stdout_principal = sys.stdout
					try:
						with raisin.raisin.Printer("I'm working...", signature=self.signature) as p:
							f_display = open(os.path.join(raisin.temprep, 'stdout.txt'), 'w', encoding='utf-8')
							with raisin.raisin.Timeout(job["job_timeout"]):
								fonction = raisin.raisin.deserialize(job["target_data"], signature=self.signature, frequency=self.frequency, modules=job["modules"])
								args = tuple([raisin.raisin.deserialize(arg["arg_path"], signature=self.signature) for arg in args])
								sys.stdout = f_display
								sys.stderr = f_display
								raisin_answer = fonction(*args)
							sys.stdout = stdout_principal
							sys.stderr = stdout_principal
							f_display.close()
							with open(path_file, "wb") as f:
								for pack in raisin.raisin.serialize(raisin_answer, compresslevel=self.compresslevel, generator=True, signature=self.signature):
									f.write(pack)
							with open(os.path.join(raisin.temprep, 'stdout.txt'), 'r', encoding='utf-8') as f_display:
								result = {"answer":path_file, "display":f_display.read(), "error":None}
					except Exception as e:
						try:
							sys.stdout = stdout_principal
							sys.stderr = stdout_principal
							f_display.close()
							with open(os.path.join(raisin.temprep, 'stdout.txt'), 'r', encoding='utf-8') as f_display:
								result = {"answer":None, "display":f_display.read(), "error":e}
						except Exception as e:
							result = {"answer":None, "display":None, "error":e}
					
					"""envoi du resultat"""
					with Printer("send the result...", signature=self.signature):#appretation a avoyer le resultat
						name = "interim&"+str(interim["sending_date"])		#c'est le nom d'interim dans le bon serveur
						server = [s for s in raisin.servers.servers if s.id == interim["server_id"]][0]#recuperation du serveur qui contient ce boulot
						if result["answer"] != None:						#si le travailleur a bien fait son boulot, qu'il n'a pas echoue
							with Printer("send the body of the result...", signature=self.signature):
								with open(result["answer"], "rb") as f:		#on recupere le resultat
									res_generator = self.Interim.generateur(f)#on met en forme le resultat
									ress_hash = send_resultat(server, res_generator)#on envoi ce resultat
						with Printer("update the interim on server...", signature=self.signature):#une fois les donnees du resultat envoyees
							try:											#il est desormais tant de metre l'offre d'emploi a jour
								interim = deserialize(server.load(name+"&working", signature=self.signature), signature=self.signature)#tentative de telecharger l'offre d'emploi telle qu'elle apparait sur le serveur
							except:											#dans le cas ou le telechargement ne donne rien
								pass										#on garde l'interim par defaut
							if interim["state"] != "finish":				#si ce travail n'est pas deja fait par un autre
								if result["error"] == None:					#si le resultat ne contient pas d'erreur
									interim["state"] = "finish"				#cette tache est totalement terminee
									interim["error"] = None					#il n'y a pas d'erreur
									interim["res_hash"] = self.Interim.get_hash(result["answer"], signature=self.signature)
									interim["ress_hash"] = ress_hash		#evidement, on met a jour la liste des resultats
									interim["display"] = result["display"]	#ajout de l'affichage graphique
									interim["compresslevel"] = self.compresslevel#ajout du taux de compression de ce resultat
									interim["blacklisted"] = interim["blacklisted"]#on ne s'ajoute pas a la liste noir
									interim["last_support"] = time.time()	#on met a jour ce moment
									interim["worker"] = raisin.id			#on dit qui est le dernier a avoir bosse
								else:										#dans le cas ou une erreur est suspicieuse
									interim["state"] = "fail"				#on marque le fait que quelque chose n'est pas propre
									interim["error"] = result["error"]		#dictionaire des differentes erreurs
									interim["res_hash"] = None				#il n'y a pas des resultat
									interim["ress_hash"] = []				#donc encore moin un gros resultat
									interim["display"] = result["display"]	#des choses ont pu etre affichee avant que l'erreur ne surviene
									interim["compresslevel"] = self.compresslevel#le taux de compression est celui
									interim["blacklisted"].append(raisin.id)#on se note dans la liste des ordinateurs qui ont echoues afin de ne pas refaire la meme erreur
									interim["last_support"] = interim["last_support"]#on ne met surtout pas a jour le fait qu'on ai intervenu
									interim["worker"] = raisin.id			#on dit qui est le dernier a avoir bosse
								data = serialize(interim, compresslevel=0, generator=False, signature=self.signature)#serialisation de l'interim
								while 1:									#il est temps d'envoyer le resultat
									try:									#on tente d'envoyer la reponse
										server.send(data, name+"&"+interim["state"], signature=self.signature)#avec son etat actuel
										try:
											server.remove(name+"&working", signature=self.signature)
										except:
											pass
										try:
											if interim["state"] == "finish":
												server.remove(name+"&fail", signature=self.signature)
										except:
											pass
										try:
											server.remove(name+"&waiting", signature=self.signature)
										except:
											pass
										break								#si c'est un succes, on en fini la
									except:									#si c'est un echec
										try:								#on va essayer de faire en sorte que ca fonctionne au prochain coup
											server.remove(name+"&"+interim["state"], signature=self.signature)#aisin on supprime ce qui serait suceptible de generer une erreur
										except:								#si c'est l'acces a internet qui fait defaut
											time.sleep(10)					#on attend un moment le temps que la conection revienne
								self.commun.remove(interim["sending_date"])	#on fait un peu de place sur la variable partagee

				if self.autorize_cpu() < 100:								#si l'utilisateur nous impose d'etre parcimonieux avec les resources de l'ordinateur
					time.sleep(2*self.dt)									#une petite pause s'impose le temps que la nouvelle loi sur les conges soit calculee

	def upgrade(self):
		"""
		fait et poste les mises a jour si nessesaire
		"""
		def put_on_line(version_var):
			"""
			depose cette version de raisin sur un serveur
			"""
			with Printer("put this version of raisin in line...", signature=self.signature):
				with Printer("make link with upgrade data...", signature=self.signature):
					while 1:												#on va sans relache essayer de se conecter au serveur
						try:												#pour cela, on encapsule le tout dans un try
							upgrade_var = raisin.Variable("upgrade_data")	#on tente de se connecter a la bonne variable
							break											#si la connection est bonne, on passe a la suite
						except:												#si sa a foire
							continue										#on retente notre chance
				parent = os.path.dirname(__file__)							#on se met au bon endroit, pour lire les fichiers utiles
				dico = {f:open(os.path.join(parent, f), "r", encoding="utf-8").read() for f in os.listdir(parent) if (not f in ["__pycache__", "data"]) and (f[-4:] != ".pyc")}
				with Printer("send new version on the server...", signature=self.signature):
					while 1:												#on va tenter d'envoyer les fichiers sur le serveur
						try:												#mais evidement, on prend mille et une precautions
							upgrade_var.write(dico)							#envoi des donnees
							version_var.write(raisin.__version__)			#et l'info qui va avec
							break											#quand c'est fait, on passe a la suite
						except:												#en cas d'echec
							continue										#on recomence

		def superieur(version1, version2):
			"""
			retourne True si la version1 > version2
			retourne False le cas echeant
			"""
			if version1.count(".") < version2.count("."):
				version1 += ".0"*(version2.count(".")-version1.count("."))
			elif version1.count(".") > version2.count("."):
				version2 += ".0"*(version1.count(".")-version2.count("."))
			for v1, v2 in zip(map(int, version1.split(".")), map(int, version2.split("."))):
				if v1 > v2:
					return True
				elif v1 < v2:
					return False
			return False

		def install_upgrade():
			"""
			fait la mise a jour de raisin sur ce poste
			"""
			with Printer("upgrading of raisin...", signature=self.signature):
				with Printer("make link with upgrade data...", signature=self.signature):
					while 1:												#on va sans relache essayer de se conecter au serveur
						try:												#pour cela, on encapsule le tout dans un try
							upgrade_var = raisin.Variable("upgrade_data")	#on tente de se connecter a la bonne variable
							dico = upgrade_var.read()						#et de lire son contenu
							break											#si la connection est bonne, on passe a la suite
						except:												#si sa a foire
							continue										#on retente notre chance
				parent = os.path.dirname(__file__)							#on se met au bon endroit, pour ecrir les fichiers
				for name, content in dico.items():
					with open(os.path.join(parent, name), "w", encoding="utf-8") as f:
						f.write(content)

		with Printer("looking for upgrade...", signature=self.signature) as p:
			while 1:														#on va sans relache essayer de se conecter au serveur
				try:														#pour cela, on encapsule le tout dans un try
					version_var = raisin.Variable("upgrade_version")		#on tente de se connecter
					break													#si la connection est bonne, on passe a la suite
				except:														#si sa a foire
					continue												#on retente notre chance
			try:															#cette fois, on va essayer de savoir de quelle version il s'agit
				l_version = version_var.read()								#recuperation de la version
				p.show("inline version: "+l_version)						#on affiche la version disponible
				p.show("local version: "+raisin.__version__)				#et la version locale
				if raisin.__version__ == l_version:							#si les versions sont les memes
					return None												#on arrete la
				if superieur(raisin.__version__, l_version):				#si on est plus en avance
					put_on_line(version_var)								#on en fait profiter les autre
				else:														#au contraire, si on est a la traine
					install_upgrade()										#c'est sur cet ordi que l'on fait la mise a jour
			except:															#si on echou a telecharger
				p.show("no upgrade on line")								#on en fait par au lecteur
				put_on_line(version_var)

def deserialize(data, psw=None, frequency=0, signature=None, modules={}, rep=None):
	"""
	deserialise l'objetsous sa forme primitive
	'psw' est le mot de passe pour le dechiffrage des donnees cryptees
	'rep' est le repertoire dans lequel apparait l'archive finale
	'data' peut etre:
		-un 'bytes' objet
		-un generateur de bytes sequences
		-un 'io.BufferedReader'
		-un path vers un fichier binaire
	'frequency' est un flotant (en Hz): lorsqu'il est > 0, l'objet retourne est pret a etre hache
	retourne l'objet sous sa forme primitive
	"""
	def generateur(data):
		"""
		genere les donnees par paquets comme elles arrivent
		"""
		if len(str(data)) < 32767:										#protection pour windaube
			if os.path.isfile(str(data)):								#si un path est envoye
				data = open(str(data), "rb")							#il est transorme en fichier binaire
		if type(data) == io.BufferedReader:								#si il s'agit d'un pointeur vers un fichier
			while 1:													#on retourne tout petit a petit
				pack = data.read(10**7)									#on lit la suite
				if pack == b"":											#si tout le fichier est lu
					break												#on arrette la
				yield pack												#sinon on retourne le petit bout de fichier que l'on vient de lire
		elif type(data) == bytes:										#si les donnees sont directement en binaire
			yield data													#c'est le plus simple pour nous
		else:															#si il s'agit d'un generateur
			for pack in data:											#on va directement le vider
				yield pack												#petit a petit

	def uncipher(data):
		"""
		dechiffre 'data'
		retourne les donnees dechiffrees de type 'bytes'
		"""
		kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=psw.encode("utf-8"), iterations=100000, backend=default_backend())
		key = base64.urlsafe_b64encode(kdf.derive(psw.encode("utf-8")))	#on utilise un module tout fait qui fait ca tres bien
		coder = Fernet(key)												#creation de la clef de chiffrement
		return coder.decrypt(data) 

	def put_between(file, lignes):
		"""
		insere tout le contenu nescessaire au hachage
		'file' est un fichier en ecriture
		'lignes' est un iterable qui reflete chaques lignes du code a executer
		retourne le fichier rempli
		"""
		#import des modules
		for module, list_import in modules.items():							#pour chaque module
			for importation in list_import:									#pour chaque ligne d'import
				file.write(importation+"\n")								#on l'ajoute en entete du programme

		#gestion exterieur
		file.write("\n")													#pour plus de visibilitee
		file.write("import os\n")											#pour pouvoir changer le repertoire par defaut
		file.write("import pickle\n")										#au debut du fichier, pour metre les signature au bon endroit
		file.write("import raisin\n")										#pour communiquer avec l'exterieur
		file.write("import sys\n")											#pour changer printer dans un fichier
		file.write("local_signature = pickle.loads("+str(pickle.dumps(signature))+")\n")#on ajoute la signature pour la suite
		file.write("os.chdir(raisin.decompress('"+raisin.compress(raisin.temprep, compresslevel=0, signature=signature, copy_file=False)+"', signature=local_signature))\n")#affin que tout ce qu'ecrive l'utilisateur finisse par disparaitre

		#insertion des pauses
		file.write("\n")													#on allege le code pour le rendre un peu plus lisible
		file.write("iter_raisin = 0\n")										#initialisation du compteur
		file.write("path_whip = raisin.decompress('"+raisin.compress(os.path.join(raisin.rep, "raisin_whip.txt"), compresslevel=0, signature=signature, copy_file=False)+"', signature=local_signature)\n")
		file.write("def pause_raisin():\n")									#c'est la fonction qui va permetre de faire une pause si necessaire
		file.write("\tglobal iter_raisin\n")								#la variable 'iter_raisin' est globale affin d'etre incrementee de partout
		file.write("\titer_raisin += 1\n")									#il faut incrementer le compteur
		file.write("\tif iter_raisin == "+str(max(1, int(math.pow(10.0, 6.0-math.log10(frequency*20)))))+":\n")#on met un == et non pas un >= de facon a optimiser la vitesse du test
		file.write("\t\titer_raisin = 0\n")									#on remet le compteur a 0
		file.write("\t\twhile 1:\n")										#on rentre dans une longue boucle si amais il faut faire une pause
		file.write("\t\t\twith open(path_whip, 'r') as file:\n")			#il faut ouvrir le fichier qui contient les informations relative aux pauses permises
		file.write("\t\t\t\tif file.read() == 'run':\n")					#si le fichier nous dit qu'il faut tracer
		file.write("\t\t\t\t\treturn None\n")								#c'est parti, on y va a fond
		file.write("\t\t\t\telse:\n")										#si c'est autre chose qui y est ecrit
		file.write("\t\t\t\t\ttime.sleep("+str(1/frequency/20)+")\n")		#on fait une petite pause

		file.write("\n")													#le fait d'ajouter un saut de ligne permet d'aleger le code
		for ligne in lignes:												#pour chaque ligne de code
			alinea = 0														#on se prepare  compter les alineas present dans cette ligne
			lbis = ligne													#comme l'on va escinter la ligne, on en fait une sauvegarde
			while lbis[0] == "\t":											#tant que la premiere ligne possede un alinea
				alinea+=1													#on incremente ce nombre de 1
				lbis = lbis[1:]												#suppression de cet alinea
			file.write(ligne)												#cette ligne est ecrite
			if alinea >= 1:													#dans le cas ou l'on est dans une fonction
				if ligne[-2] == ":":										#si il y a un alinea de plus a faire
					alinea += 1												#on le fait afon d'eviter les erreurs de sytaxe
				file.write("\t"*alinea+"pause_raisin()\n")					#on intercale plein de verifications entre chaques lignes

		return file

	with Printer("deserialization...", signature=signature):
		gen = generateur(data)
		with Printer("header reading...", signature=signature):				#pour le moment, l'entete est vide
			entete = ""														#creation de la variable
			pack = next(gen)												#recuperation du premier paquet
			while 1:														#on va le lire petit a petit
				if pack == b"":												#affin de recuperer l'entete de fichier
					pack = next(gen)										#si l'entet est coupee, on va voir la suite
				car = pack[0:1].decode("utf-8")								#on recupere le premier caractere
				pack = pack[1:]												#on le suprime de la suite du fichier
				if car == "/":												#si l'entete est fini
					break													#on sort ici
				entete+=car													#si le caractere fait parti de l'entete, on le rajoute
			entete = entete.split(".")										#on rend l'entete utilisable
			entete.reverse()												#et oui, toute les operations faites lors de la serialisation doivent etre faitenet en sens inverse

		with Printer("file_creation...", signature=signature):				#il faut ecrire ces 'bytes' dans un fichier
			source = os.path.join(raisin.temprep, "_raisin"+str(uuid.uuid4())+".rais")#cela va etre le nom du fichier
			with open(source, "wb") as f:									#creation du fichier
				f.write(pack)												#on ecrit deja ce bout la pour ne pas l'oublier
				for pack in gen:											#pour chaque paquets restant
					f.write(pack)											#on l'ajoute dans le fichier

		with Printer("reverse protocol: ",",".join(entete),"...", signature=signature):#nous pouvons desormais passer aux choses serieuses
			objet = None
			for i, protocole in enumerate(entete):							#pour chacunes des operations a faire en sens inverse
				cible = os.path.join(raisin.temprep, "_raisin"+str(uuid.uuid4())+".rais")#on avance d'un pas en creant un fichier un peu plus proche de l'original
				if protocole == "xz":										#si il s'agit d'une archive lzma
					with Printer("xz decompression...", signature=signature):
						with lzma.open(source ,"rb") as src:				#on l'ouvre avec lzma
							with open(cible, "wb") as dest:					#c'est dans ce fichier que l'archive va etre decompressee
								shutil.copyfileobj(src, dest)				#on l'extrait
				elif protocole == "gz":										#si il s'agit d'une archive gzip
					with Printer("gz decompression...", signature=signature):
						with gzip.open(source ,"rb") as src:				#on l'ouvre avec gzip
							with open(cible, "wb") as dest:					#c'est dans ce fichier que l'archive va etre decompressee
								shutil.copyfileobj(src, dest)				#on l'extrait
				elif protocole == "bz2":									#si il s'agit d'une archive bzip2
					with Printer("bz2 decompression...", signature=signature):
						with bz2.open(source ,"rb") as src:					#on l'ouvre avec bz2
							with open(cible, "wb") as dest:					#c'est dans ce fichier que l'archive va etre decompressee
								shutil.copyfileobj(src, dest)				#on l'extrait
				elif protocole == "cry":									#si il s'agit de fichier a decrypter
					with Printer("cry decryption...", signature=signature):
						with open(cible, "wb") as dest:						#c'est dans ce fichier que l'on va ajouter chaque fichier decripte
							with tarfile.open(source, "r") as file:			#on ouvre l'archive car en realite, .cry est une archive
								for nom in file.getnames():					#pour tous les fichiers presents dans l'archive
									dest.write(uncipher(file.extractfile(nom).read()))#on les dechiffre et on les raboutes dans la destination
				elif protocole == "tar":									#si il faut extraire l'archive
					with Printer("tar extraction...", signature=signature):
						with tarfile.open(source, "r") as archive:			#deja on commence par l'ouvrir
							if (i+1 == len(entete)) and (rep != None):
								archive.extractall(rep)						#extraction de l'archive dans le repertoire de raisin
								objet = archive.getnames()[0]				#recuperation du nom du fichier ou du repertoire
								objet = os.path.join(rep, objet)			#c'est un chemin absolu que l'on retourne
							else:
								archive.extractall(raisin.temprep)
								objet = archive.getnames()[0]				#recuperation du nom du fichier ou du repertoire
								objet = os.path.join(raisin.temprep, objet)	#c'est un chemin absolu que l'on retourne
				elif protocole == "pk":										#si il s'agit d'un fichier serialise
					with Printer("pk reading...", signature=signature):
						with open(source, "rb") as f:						#on ouvre le fichier
							objet = pickle.load(f)							#extraction de l'objet
				elif protocole == "txt":									#si il s'agit d'un pointeur vers un fichier txt
					with Printer("txt TextIOWrapper...", signature=signature):
						objet = open(source, "r", encoding="utf-8")			#on cree un lien vers le pointeur
						source = cible										#affin qu'il ne soit pas supprime
				elif protocole == "bytes":									#si il s'agit d'un pointeur vers un fichier bytes
					with Printer("bytes io.BufferedReader...", signature=signature):
						objet = open(source, "rb")							#on cree un lien vers le pointeur
						source = cible										#afin qu'il ne soit pas supprime
				elif protocole == "imp":									#si il s'agit d'une classe
					with Printer("user python object...", signature=signature):
						name = str(uuid.uuid4())							#voici le nom du module
						with open(os.path.join(raisin.temprep, name+".py"), "w", encoding="utf-8") as module:#ouverture du module
							if frequency > 0:								#si il faut intercaller l'artillerie de hachage
								module = put_between(module, objet)			#on fait en sorte qu'elle y soit
								
							else:											#si ce n'est pas la peine
								objet.insert(0, "import pickle\n")			#au debut du fichier
								objet.insert(1, "local_signature = pickle.loads("+str(pickle.dumps(signature))+")\n")#on ajoute la signature
								for ligne in objet:							#pour chaque ligne de code
									module.write(ligne)						#elle est ecrite dans le module

						try:
							if not raisin.temprep in sys.path:
								sys.path.insert(0, raisin.temprep)
							mod = __import__(name)
						except:
							mod = imp.load_source(name, os.path.join(raisin.temprep, name+".py"))#import du module fraichement cree
						try:
							shutil.rmtree(os.path.join(raisin.temprep, "__pycache__"))#suppression de toutes les traces
						except:
							pass
						objet = mod.get_raisin_answer()						#on retourne la fonction
				elif protocole == "sym":									#si il s'agit d'une expression sympy
					with Printer("sympy_expr interpretation...", signature=signature):
						objet = sympy.sympify(objet)						#et le reste, c'est sympy qui s'en charge

				try:
					os.remove(source)										#faire du menage ne fait pas de mal
				except:
					pass
				source = cible												#pour la suite, on est bien oblige de metre le nom du fichier a jour

			return objet

def deserialize_bis(data, signature, psw):
	"""
	'data' peut etre:
		-un 'bytes' objet
		-un generateur de bytes sequences
		-un 'io.BufferedReader'
	'signature' permet d'afficher au bon endroit
	"""
	def deserialize_filename(pack, generator):
		"""
		si le fichier d'origine avait pour nom un chemin absolu,
		alors toute une arboresance va etre construite a partir du repertoir
		courant de facon a retourne exactement la meme chaine que celle definie par
		l'utilisateur qui a prealablement enregistre le fichier
		si le fichier d'origine avait pour nom un chemin relatif,
		alors, un nouveau fichier nome par ce meme nom est cree dans le repertoir courant
		ne prend aucune precaution, peu donc ecraser un fichier si un fichier de meme nom etait deja present
		dans le repertoir par defaut
		retourne le nom de ce fichier, relatif par rapport au repertoir courant
		"""
		def split_directories(directories):
			"""
			retourne une liste avec chaques dossier
			les un apres les autres
			"""
			liste = []													#initialisation de la liste vide
			directories = os.path.normpath(directories)
			while directories != "":									#tant que l'on a pas parcouru la totalite du chemin
				directories, e = os.path.split(directories)				#on extrait le dossier du bout
				if e == "":												#si jamais on frole la boucle infinie
					break												#on ne s'y aventure pas plus que ca
				liste.insert(0, e)										#ajout de cet element dans la liste
			return liste

		#lecture entete
		taille = 0														#cette variable reflete la taille du nom du fichier
		while not b"-" in pack:											#tant que le debut de l'entete ne contient pas asser d'info
			pack += next(generator)										#alors on va voir ce qu'il y a juste apres
		while pack[0:1] != b"-":										#a ce niveau la, on lit l'entete pour connaitre la longueur
			taille = 10*taille+int(pack[0:1])							#du nom du fichier
			pack = pack[1:]												#une fois le chiffre lu, on le supprime
		pack = pack[1:]													#supression du b"-" de fon de balise
		while len(pack) < taille:										#on s'attarde mintenant a la lecture du nom du fichier
			pack += next(generator)										#ainsi, on va chercher le nom en entier
		filename = pack[:taille].decode("utf-8")						#le nom du fichier est desormais accessible
		pack = pack[taille:]											#voila, il ne reste plus que le contenu
		
		#preparation du terrain
		if os.path.isabs(filename):										#si il s'agit d'un chemin absolu vers un fichier
			filename = os.path.basename(filename)						#alors on ne s'embete pas, on le transforme en chemin relatif
		directories, file = os.path.split(filename)						#separation entre le nom du fichier et le chemin qui y mene
		if directories != "":
			chemin_complet = ""											#cela va etre le chemin complet qui mene au dossier
			for directory in split_directories(directories):			#pour chaque dossier a parcourir
				chemin_complet = os.path.join(chemin_complet, directory)#on l'ajoute a la pile
				if not os.path.exists(chemin_complet):					#si ce chemin n'est pas deja sur le disque
					os.mkdir(chemin_complet)							#alors on l'ajoute
			filename = os.path.join(chemin_complet, file)				#quitte afaire quelque modification, on retourne un path valide

		#restitution du fichier
		with open(filename, "wb") as f:									#ouverture du fichier
			f.write(pack)												#puis on ecrit dedans son contenu
			for pack in generator:										#pour chaque packet restant
				f.write(pack)											#on y vide aussi le contenu du generateur
		return filename

	def deserialize_file_bytes(pack, generator):
		"""
		'pack' est un bout de bit
		'generator' cede la continuite de 'pack'
		"""
		#lecture entete
		while not b"</>" in pack:										#l'entete est tres complexe ici puisque
			pack += next(generator)										#qu'elle contient de nombreuses informations
		position = pack.index(b"</>")									#position du separateur
		mode = pack[0:position].decode("utf-8")							#comme par example le mode ou le fichier est enregistre
		pack = pack[position+3:]										#on supprime cette partie la de la terre
		while not b"</>" in pack:										#tant que l'on a pas la suite
			pack += next(generator)										#on va la chercher
		position = pack.index(b"</>")									#on regarde ou est-ce que ca s'arrette
		stream_position = int(pack[0:position])							#position du pointeur dans le fichier
		pack = pack[position+3:]										#ça y est, toute l'entete est lu
		filename = filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".txt")#creation du fichier temporaire
		if ("w" in mode) or ("x" in mode):								#si il est en simple mode ecriture
			f = open(filename, mode=mode)								#ouverture du fichier
			f.write(pack)												#on y ecrit le contenu
			for pack in generator:										#sans passer par la rame
				f.write(pack)											#on ecrit tout
			f.seek(stream_position, 0)									#on place le curseur la ou il etait
			return f
		with open(filename, "wb") as f:									#on ouvre une premiere fois le fichier pour y ecrire le contenu
			f.write(pack)												#ecriture du premier packet
			for pack in generator:										#puis on va lire tous les autre paquets
				f.write(pack)											#pour les y ecrir un a un
		f = open(filename, mode=mode)									#ouverture du fichier final
		f.seek(stream_position, 0)										#on place le curseur la ou il etait
		return f

	def deserialize_file_text(pack, generator):
		"""
		'pack' est un bout de bit
		'generator' cede la continuite de 'pack'
		"""
		#lecture entete
		while not b"</>" in pack:										#l'entete est tres complexe ici puisque
			pack += next(generator)										#qu'elle contient de nombreuses informations
		position = pack.index(b"</>")									#position du separateur
		mode = pack[0:position].decode("utf-8")							#comme par example le mode ou le fichier est enregistre
		pack = pack[position+3:]										#on supprime cette partie la de la terre
		while not b"</>" in pack:										#tant que l'on a pas la suite
			pack += next(generator)										#on va la chercher
		position = pack.index(b"</>")									#on regarde ou est-ce que ca s'arrette
		encoding = pack[0:position].decode("utf-8")						#c'est la maniere dons le fichier est encode
		pack = pack[position+3:]										#on va voir la suite
		while not b"</>" in pack:										#tant que l'on a pas la suite
			pack += next(generator)										#on va la chercher
		position = pack.index(b"</>")									#on regarde ou est-ce que ca s'arrette
		stream_position = int(pack[0:position])							#position du pointeur dans le fichier
		pack = pack[position+3:]										#ça y est, toute l'entete est lu
		filename = filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".txt")#creation du fichier temporaire
		if ("w" in mode) or ("x" in mode):								#si il est en simple mode ecriture
			f = open(filename, mode=mode, encoding=encoding)			#ouverture du fichier
			f.write(pack.decode(encoding))								#on y ecrit le contenu
			for pack in generator:										#sans passer par la rame
				f.write(pack.decode(encoding))							#on ecrit tout
			f.seek(stream_position, 0)									#on place le curseur la ou il etait
			return f
		with open(filename, "wb") as f:									#on ouvre une premiere fois le fichier pour y ecrire le contenu
			f.write(pack)												#ecriture du premier packet
			for pack in generator:										#puis on va lire tous les autre paquets
				f.write(pack)											#pour les y ecrir un a un
		f = open(filename, mode=mode, encoding=encoding)				#ouverture du fichier final
		f.seek(stream_position, 0)										#on place le curseur la ou il etait
		return f

	class Deserialize_class:
		"""
		deserialise une classe
		"""
		def __init__(self, pack, gen, signature):
			"""
			initialisation de l'objet
			"""
			self.pack = pack
			self.gen = gen
			self.signature = signature

		def read_name(self):
			"""
			retourne le nom de la classe
			met a jour self.pack
			"""
			nom = b""		#nom de l'entete
			while 1:		#ce n'est pas une vrai boucle infinie
				if not self.pack:#si le reservoir est vide
					self.pack = next(self.gen)#on le rempli
				if self.pack[:3] == b"</>":#si le nom est complet
					self.pack = self.pack[3:]#on enleve la balise
					return nom.decode("utf-8")#puis on retourne
				nom += self.pack[0:1]#si ce n'est pas la fin
				self.pack = self.pack[1:]#on va voir le caractere suivant

		def read_length(self):
			"""
			retourne la longeur du packet qui suit
			"""
			longueur = b""	#longueur de ce qui suit
			while 1:		#ce n'est pas une vrai boucle infinie
				if not self.pack:#si le reservoir est vide
					self.pack = next(self.gen)#on le rempli
				if self.pack[0:1] == b"d":#si le nom est complet
					self.pack = self.pack[1:]#on enleve la balise
					return int(longueur)#puis on retourne la longueur
				longueur += self.pack[0:1]#si ce n'est pas la fin
				self.pack = self.pack[1:]#on va voir le caractere suivant

		def read_info(self):
			"""
			retourne 2 choses:
				-un INT qui correspond a la longueur en octet du packet restant
				-"d" ou "m" ou "f" pour "debut" ou "milieu" ou "fin"
			"""
			entier = 0													#on initialise l'entier a 0, meme si il ne va pas y rester longtemps
			while 1:
				if len(self.pack) < 1:									#si le paquet est trop court pour y lire quoi que ce soit
					self.pack += next(self.gen)							#on commence par aller lire la suite
				if self.pack[0:1].isdigit():							#si l'on est encore entrain de lire le nombre de l'entete
					entier = 10*entier+int(self.pack[0:1])				#et bien on va jusqu'au bout
					self.pack = self.pack[1:]							#puis on supprime ce que l'on vient de faire pour eviter une boucle infinie
				else:													#si on est enfin au bout de l'entete
					lettre = self.pack[0:1].decode()
					self.pack = self.pack[1:]
					return entier, lettre								#enfin, l'entete est entierement lu et supprimee

		def generator_intermediaire(self):
			"""
			cede une succession de donnee qui correspond a une seule methode
			'pack' et 'generateur' doivent contenir la premiere entete
			"""
			taille, balise = self.read_info()							#on commence par lire l'entete une premiere fois
			while balise != "f":										#tant que l'on a pas atteind la fin
				taille_cede = 0											#c'est le nombre d'octet que l'on a envoye
				while taille_cede < taille:								#tant que l'on est pas encore a la future balise
					delta = taille-taille_cede							#c'est le nombre d'octet qu'il nous reste a recuprer avant la prochaine balise
					if len(self.pack) <= delta:							#si on a de la marge:
						yield self.pack									#on retourne deja ce que l'on a
						taille_cede += len(self.pack)					#puis on incremente le compteur pour ne pas aller trop loin
						self.pack = next(self.gen)						#on va lire la suite du generateur
					else:												#dans le cas ou l'on est proche de la balise
						yield self.pack[:delta]							#on retourne juste ce qu'il faut: on s'arret devant la balise
						self.pack = self.pack[delta:]					#puis on supprime ce que l'on vient de retourner
						taille_cede += delta							#comme d'habitude, on precise ce que l'on vient de faire
				taille, balise = self.read_info()						#on lit alors la balise devant laquelle on vient de s'arretter

		def generator_methodes(self):
			"""
			cede une a une les methodes caches dans 'pack' et 'generator'
			"""
			while 1:													#tant que l'erreur StopIterationError n'est pas interceptee
				yield deserialize_bis(self.generator_intermediaire(), signature=self.signature, psw=None)#on deserialise une methode de plus

		def get(self):
			with raisin.Printer("class extraction...") as p:			#affichage de l'operation en cours
				nom = self.read_name()									#nom de l'objet
				code = "class "+nom+":\n"								#c'est le code source qui va etre complete au fur a meusure
				for dico in self.generator_methodes():					#pour chaque methode de l'objet
					signature = []										#c'est la liste qui va contenir chaque parametre de l'entete
					for par in  dico["signature"]:						#on parcours ainsi chaque elements de l'entete
						if par[0] == "empty":							#si le parametre n'a pas de valeur par defaut
							signature.append(par[2]+par[1])				#on met juste le nom du parametre
						else:											#si le parametre a une valeur par defaut
							signature.append(par[1]+"="+"pickle.loads(bytes("+str(list(pickle.dumps(par[2])))+"))")#on fait passer cette valeur la
					signature = "("+", ".join(signature)+")"			#on met l'entete en forme
					methode = "\tdef "+dico["name"]+signature+":\n"		#affin qu'elle soit compilable
					methode += "\t\t"+"\t\t".join(dico["code"])			#code brute de la methode
					code += methode										#on ajoute cette methode a l'objet principal
				code += "self.objet = "+nom								#pour avoir acces a l'objet, on le rend global
				exec(code)												#compilation de l'objet
				return self.objet

	class Deserialize_function:
		"""
		deserialise une fonction
		"""
		def __init__(self, pack, gen, signature, psw):
			"""
			initialisation de l'objet
			"""
			self.pack = pack
			self.gen = gen
			self.signature = signature
			self.psw = psw

		def generator(self):
			"""
			cede pack pui gen
			"""
			yield self.pack
			for pack in self.gen:
				yield pack

		def get(self):
			dico = deserialize_bis(self.generator(), self.signature, self.psw)
			return dico
	
	class Deserialize_list:
		"""
		'pack' est un bout de bit
		'generator' cede la continuite de 'pack'
		retourne une liste
		"""
		def __init__(self, pack, generator, signature, psw):
			self.pack = pack
			self.generator = generator
			self.signature = signature
			self.psw = psw

		def read_info(self):
			"""
			retourne 2 choses:
				-un INT qui correspond a la longueur en octet du packet restant
				-"d" ou "m" ou "f" pour "debut" ou "milieu" ou "fin"
			"""
			entier = 0													#on initialise l'entier a 0, meme si il ne va pas y rester longtemps
			while 1:
				if len(self.pack) < 1:									#si le paquet est trop court pour y lire quoi que ce soit
					self.pack += next(self.generator)					#on commence par aller lire la suite
				if self.pack[0:1].isdigit():							#si l'on est encore entrain de lire le nombre de l'entete
					entier = 10*entier+int(self.pack[0:1])				#et bien on va jusqu'au bout
					self.pack = self.pack[1:]							#puis on supprime ce que l'on vient de faire pour eviter une boucle infinie
				else:													#si on est enfin au bout de l'entete
					lettre = self.pack[0:1].decode()
					self.pack = self.pack[1:]
					return entier, lettre								#enfin, l'entete est entierement lu et supprimee

		def generator_intermediaire(self):
			"""
			cede une succession de donnee qui correspond a un seul element de la liste
			'pack' et 'generateur' doivent contenir la premiere entete
			"""
			taille, balise = self.read_info()							#on commence par lire l'entete une premiere fois
			while balise != "f":										#tant que l'on a pas atteind la fin
				taille_cede = 0											#c'est le nombre d'octet que l'on a envoye
				while taille_cede < taille:								#tant que l'on est pas encore a la future balise
					delta = taille-taille_cede							#c'est le nombre d'octet qu'il nous reste a recuprer avant la prochaine balise
					if len(self.pack) <= delta:							#si on a de la marge:
						yield self.pack									#on retourne deja ce que l'on a
						taille_cede += len(self.pack)					#puis on incremente le compteur pour ne pas aller trop loin
						self.pack = next(self.generator)				#on va lire la suite du generateur
					else:												#dans le cas ou l'on est proche de la balise
						yield self.pack[:delta]							#on retourne juste ce qu'il faut: on s'arret devant la balise
						self.pack = self.pack[delta:]					#puis on supprime ce que l'on vient de retourner
						taille_cede += delta							#comme d'habitude, on precise ce que l'on vient de faire
				taille, balise = self.read_info()						#on lit alors la balise devant laquelle on vient de s'arretter

		def generator_elements(self):
			"""
			cede un a un les elements caches dans 'pack' et 'generator'
			"""
			while 1:													#tant que l'erreur StopIterationError n'est pas interceptee
				yield deserialize_bis(self.generator_intermediaire(), signature=self.signature, psw=self.psw)#on tente de deserialiser un objet de plus

		def get(self):
			"""
			retourne la liste
			"""
			return [e for e in self.generator_elements()]

	class Deserialize_module:
		"""
		'pack' est un bout de bit
		'generator' cede la continuite de 'pack'
		retourne un module ou une erreur en cas d'echec d'importation
		"""
		def __init__(self, pack, generator, signature, psw):
			self.pack = pack
			self.generator = generator
			self.signature = signature
			self.psw = psw

		def read_info(self):
			"""
			retourne 2 choses:
				-un INT qui correspond a la longueur en octet du packet restant
				-"d" ou "m" ou "f" pour "debut" ou "milieu" ou "fin"
			"""
			entier = 0													#on initialise l'entier a 0, meme si il ne va pas y rester longtemps
			while 1:
				if len(self.pack) < 1:									#si le paquet est trop court pour y lire quoi que ce soit
					self.pack += next(self.generator)					#on commence par aller lire la suite
				if self.pack[0:1].isdigit():							#si l'on est encore entrain de lire le nombre de l'entete
					entier = 10*entier+int(self.pack[0:1])				#et bien on va jusqu'au bout
					self.pack = self.pack[1:]							#puis on supprime ce que l'on vient de faire pour eviter une boucle infinie
				else:													#si on est enfin au bout de l'entete
					lettre = self.pack[0:1].decode()
					self.pack = self.pack[1:]
					return entier, lettre								#enfin, l'entete est entierement lu et supprimee

		def generator_bloc(self):
			"""
			cede une succession de donnee qui correspond a un seul element de la liste
			'pack' et 'generateur' doivent contenir la premiere entete
			"""
			try:
				taille, balise = self.read_info()						#on commence par lire l'entete une premiere fois
			except:														#si on n'arrive pas a la lire
				yield True												#c'est que c'est termine, on peu donc arretter
			yield False													#par contre, on precise que ce n'est pas fini si il y a bien une entete
			while balise != "f":										#tant que l'on a pas atteind la fin
				taille_cede = 0											#c'est le nombre d'octet que l'on a envoye
				while taille_cede < taille:								#tant que l'on est pas encore a la future balise
					delta = taille-taille_cede							#c'est le nombre d'octet qu'il nous reste a recuprer avant la prochaine balise
					if len(self.pack) <= delta:							#si on a de la marge:
						yield self.pack									#on retourne deja ce que l'on a
						taille_cede += len(self.pack)					#puis on incremente le compteur pour ne pas aller trop loin
						self.pack = next(self.generator)				#on va lire la suite du generateur
					else:												#dans le cas ou l'on est proche de la balise
						yield self.pack[:delta]							#on retourne juste ce qu'il faut: on s'arret devant la balise
						self.pack = self.pack[delta:]					#puis on supprime ce que l'on vient de retourner
						taille_cede += delta							#on precise ce que l'on vient de faire
				taille, balise = self.read_info()						#on lit alors la balise devant laquelle on vient de s'arretter

		def gener_gener(self):
			"""
			est un generateur de generateur
			"""
			while 1:
				g = self.generator_bloc()
				fin = next(g)
				if fin:
					break
				yield g

		def build_graph(self, graph, path):
			"""
			cree une arborescence de dossier dans le dossier temporaire
			de raisin
			"""
			for dossier, enfant in graph.items():
				nouveau = os.path.join(path, dossier)
				if not os.path.isdir(nouveau):
					os.mkdir(nouveau)
				self.build_graph(enfant, nouveau)

		def get(self):
			"""
			retourne la liste
			"""
			with raisin.Printer("module extraction...") as p:
				for i, e in enumerate(self.gener_gener()):
					if i == 0:
						modulename = deserialize_bis(e, signature=self.signature, psw=self.psw)
						p.show("modulename: "+modulename)
					elif i == 1:
						dependences = deserialize_bis(e, signature=self.signature, psw=self.psw)
						with raisin.Printer("dependences:"):
							for d in dependences:
								p.show(d)
					elif i == 2:
						graph = deserialize_bis(e, signature=self.signature, psw=self.psw)
						with raisin.Printer("build graph..."):
							self.build_graph(graph, raisin.temprep)
					elif (i+1)%2 == 0:
						end = deserialize_bis(e, signature=self.signature, psw=self.psw)
						path = os.path.join(raisin.temprep, *end)
					else:
						with raisin.Printer("writing "+path+"..."):
							with open(path, "wb") as f:
								for data in e:
									f.write(data)

			with raisin.Printer("importation..."):
				path = os.path.join(raisin.temprep, "/".join(modulename.split("."))+".py")
				if os.path.exists(path):
					return imp.load_source(modulename, path)
				return imp.load_source(modulename, os.path.join(raisin.temprep, "/".join(modulename.split(".")), "__init__.py"))

	def file_to_json(filename):
		"""
		'filename' est le chemin absolu d'un fichier ecrit en binaire
		ce fichier doit etre compatible avec le format json
		retourne l'objet deserialise et supprime le fichier une fois l'operation terminee
		"""
		with open(filename, "r") as f:
			obj = json.load(f)
		os.remove(filename)
		return obj

	def file_to_pickle(filename):
		"""
		'filename' est le chemin absolu d'un fichier ecrit en binaire
		ce fichier a ete cree par pickle
		retourne l'objet deserialise et supprime le fichier une fois l'operation terminee
		"""
		with open(filename, "rb") as f:
			obj = pickle.load(f)
		os.remove(filename)
		return obj

	def generator_to_file(pack, gen, data):
		"""
		cree un fichier en binaire qui contient les paquets de generator
		prend un racourci si 'data' est deja un pointeur vers un fichier en mode lecture
		retourne le chemin absolu de ce fichier
		"""
		if type(data) == io.BufferedReader:								#si le fichier est deja enregistre
			return os.path.abspath(data.name)							#on va pas en faire un nouveau!
		filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".pkl")#creation du fichier temporaire
		with open(filename, "wb") as f:									#que l'on rempli peu a peu
			f.write(pack)												#le generateur a deja subit une iteration
			for pack in gen:											#en vidant le generateur
				f.write(pack)											#dans le disque dur
		return filename													#fermeture du fichier et on renvoi son nom

	def generator_to_generator(pack, generator, buff):
		"""
		'generator' est un generateur qui cede des paquets de taille tres variable
		les paquet doivent etre de type 'bytes'
		le but est ici, d'uniformiser la taille des packet affin de renvoyer des pakets de 
		'buff' octet
		cede donc les paquets au fur a meusure apres avoir cede 'pack'
		"""																#initialisation du paquet
		for data in generator:											#on va lentement vider le generateur
			pack += data												#pour stocker peu a peu les paquets dans cette variable
			while len(pack) >= buff:									#si le packet est suffisement gros
				yield pack[:buff]										#on le retourne avec la taille reglementaire
				pack = pack[buff:]										#puis on le racourci et on recomence le test
		yield pack														#enfin, on retourne le bout restant

	def generator_bytes(data):
		"""
		prend les donnes sous sa forme primitive
		pour en faire un generateur de sequence de 'bytes'
		"""
		if type(data) == io.BufferedReader:								#si il s'agit d'un pointeur vers un fichier
			while 1:													#on retourne tout petit a petit
				pack = data.read(1024*1024)								#on lit la suite
				if pack == b"":											#si tout le fichier est lu
					break												#on arrette la
				yield pack												#sinon on retourne le petit bout de fichier que l'on vient de lire
		elif type(data) == bytes:										#si les donnees forment une chaine de d'octets
			for i in range(0, len(data), 1024*1024):					#on va les decouper en petit bout
				yield data[i:i+1024*1024]								#pour la restituer peu a peu
		else:															#si l'objet est deja un generateur
			try:
				for pack in data:
					yield pack
			except Exception as e:
				raise TypeError("'data' must be a 'bytes' object or a bytes sequences generator object or an 'io.BufferedReader'")	

	def uncipher_data(data, psw):
		"""
		'data' est une sequence de bytes
		retourne la sequence de byte decriptee
		"""
		psw = psw.encode("utf-8")										#on fait la convertion avant que l'algorithme ne la fasse tout seul et but sur l'ascii
		if len(psw) <= 16:												#la clef doit faire
			psw = (psw+b" "*16)[:16]									#16 bit
		elif len(psw) <= 24:											#ou bien
			psw = (psw+b" "*8)[:24]										#24 bit
		else:															#on bien meme
			psw = (psw+b" "*8)[:32]										#32 octets au maximum
		n = int(data[0:1], 16)											#c'est le nombre de bytes ajoutee pour faire un multiple de 16
		iv = data[1:17]													#c'est un bout de la clef de dechiffrage
		data = AES.new(psw, AES.MODE_CBC, iv).decrypt(data[17:])		#decriptage des donnees
		data = data[:len(data)-n]										#supression des ajouts artificiel
		return data

	def uncipher_generator(pack, generator, psw):
		"""
		'pack' est une sequence de bytes
		'generator' est un generateur qui cede les sequances suivante de 'pack'
		est un generateur qui cede les paquets deserialise
		"""
		#preparation
		psw = psw.encode("utf-8")										#on fait la convertion avant que l'algorithme ne la fasse tout seul et but sur l'ascii
		if len(psw) <= 16:												#la clef doit faire
			psw = (psw+b" "*16)[:16]									#16 bit
		elif len(psw) <= 24:											#ou bien
			psw = (psw+b" "*8)[:24]										#24 bit
		else:															#on bien meme
			psw = (psw+b" "*8)[:32]										#32 octets au maximum
		while len(pack) < 16:											#tant que le generateur ne nous donne pas asser de longeur
			pack += next(generator)										#on va en chercher nous meme
		iv = pack[:16]													#recuperation de l'iv
		pack = pack[16:]												#on met la chaine a jour
		#lecture et dechiffrage des packets
		while 1:														#c'est le StopIterationError qui va nous faire sortir de la
			while not b"_" in pack:										#tant que l'on a pas suffisement d'informations pour la suite
				pack += next(generator)									#on va les recuperer
			n = int(pack[0:1], 16)										#c'est le nombre de bytes ajoutee pour faire un multiple de 16
			debut = pack.index(b"_")+1									#c'est la ou commence le message code
			taille = int(pack[1:debut-1])								#ca, c'est la longeur du message code
			pack = pack[debut:]											#maintenant que les informations sont recuperes
			while len(pack) < taille:									#il faut aller chercher le packet a decoder
				pack += next(generator)									#on prend le nessecaire pour le decodage
			data = AES.new(psw, AES.MODE_CBC, iv).decrypt(pack[:taille])#le decriptage des donnees est enfin possible
			data = data[:len(data)-n]									#supression des ajouts artificiel
			pack = pack[taille:]										#supression des parties traitees
			yield data

	text = {b"00":"data->small int",
			b"01":"data->pikle->large int",
			b"02":"data->json->small str",
			b"03":"data->json->medium str",
			b"04":"file->json->large str",
			b"05":"data->float",
			b"06":"data->small bytes",
			b"07":"data->medium bytes",
			b"08":"file->large bytes",
			b"09":"data->io.TextIOWrapper",
			b"10":"data->io.BufferedReader",
			b"11":"data->list",
			b"12":"data->tuple data",
			b"13":"data->file",
			b"14":"data->standard_module",
			b"15":"data->module",
			b"16":"data->class",
			b"17":"data->json->dict",
			b"18":"data->list->dict",
			b"19":"data->function",
			b"96":"encrypted generator data->data",
			b"97":"encrypted data->data",
			b"98":"file->pickle->obj",
			b"99":"data->pickle->obj",}

	gen = generator_bytes(data)											#homogeneisation des donnes entrantes
	pack = next(gen)													#on va lire le premier bout du generateur
	with Printer("deserialization...", signature=signature) as p:		#pour le moment, l'entete est vide
		if (pack[:3] != b"</>") or (not pack[3:7].isdigit()) or (pack[7:10] != b"</>"):#si il n'y a pas d'entete
			raise ValueError("the header is all brocken!")				#on envoi bouler
		p.show(text[pack[3:5]])											#on affiche ce que l'on fait
		protocol = pack[5:7]											#c'est le protocol pour la deserialisation
		pack = pack[10:]												#suppression de l'entete
		if protocol == b"00":											#dans le cas ou l'on doit faire un simple int
			return int(pack+b"".join(gen))								#on vide le generateur et on retourne l'entier
		elif protocol == b"99":											#si il s'agit d'une simple serialisation avec pickle
			return pickle.loads(pack+b"".join(gen))						#on les retourne telle qu'elle
		elif protocol == b"98":											#si c'est tout un fichier qui est pickelise
			return file_to_pickle(generator_to_file(pack, gen, data))	#on retourne l'objet deserialise
		elif protocol == b"97":											#si les donnees sont cryptees
			return deserialize_bis(uncipher_data(pack+b"".join(gen), psw), signature, psw)#dechiffrage puis deserialisation des donnees
		elif protocol == b"96":											#si les donnes sont cryptees mais a la volle par un generateur
			return deserialize_bis(uncipher_generator(pack, gen, psw), signature, psw)#decriptage puis deserialisation
		elif protocol == b"01":											#si le protocol est un simple json
			return json.loads((pack+b"".join(gen)).decode("utf-8"))		#on le decode simplement
		elif protocol == b"02":											#pour dejsoniser les fichiers
			return file_to_json(generator_to_file(pack, gen, data))		#on retourne l'objet deserialise
		elif protocol == b"03":											#si c'est un simple flotant
			return float((pack+b"".join(gen)).decode())					#on le decode simplement
		elif protocol == b"04":											#si il s'agit d'une simple sequence de bytes
			return pack+b"".join(gen)									#on la retourne directement
		elif protocol == b"05":											#si il faut faire un pointeur de fichier text
			return deserialize_file_text(pack, gen)						#on ecrit le fichier et on le retourne
		elif protocol == b"07":											#si il faut faire un pointeur vers un fichier binaire
			return deserialize_file_bytes(pack, gen)					#on ecrit le fichier avant de le retourner
		elif protocol == b"08":											#si il s'agit d'une liste
			return Deserialize_list(pack, gen, signature, psw).get()	#on la deserialise
		elif protocol == b"09":											#si on deserialize un tuple
			return tuple(deserialize_bis(generator_to_generator(pack, gen, 1024*1024), signature, psw))#on deserialise en fait une liste
		elif protocol == b"10":											#si il s'agit d'un fichier
			return deserialize_filename(pack, gen)						#on ecrit alors le fichier puis on retourne son nom
		elif protocol == b"11":											#si il s'agit d'un module standard
			return __import__((pack+b"".join(gen)).decode("utf-8"))		#on l'import puis on le retourne directement
		elif protocol == b"12":											#si il s'agit de la copie d'un module
			return Deserialize_module(pack, gen, signature, psw).get()	#on passe par un objet puisque la deserialisation est complique
		elif protocol == b"13":											#si l'objet est une class
			return Deserialize_class(pack, gen, signature).get()		#on l'interprete
		elif protocol == b"14":											#si l'objet est un dictionaire
			return {c:v for c,v in Deserialize_list(pack, gen, signature, psw).get()}#on le deserialise via une liste
		elif protocol == b"15":											#si l'objet est une fonction
			return Deserialize_function(pack, gen, signature, psw).get()#on le transforme en fonction
		else:															#dans le cas ou ce n'est rien de tout ca
			raise Exception("the protocol "+str(protocol)+" is unknown")#on renvoi une erreur

def get_id():
	"""
	retourne l'identifiant propre a cette ordinateur
	il s'agit d'un dictionnaire non serialise
	en cas d'erreur, retourne un identifiant quelconque dependant du temps
	"""
	def get_ip_local():
		"""
		retourne l'ip sur le reseau local
		"""
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#un socket en mode UDP (DGRAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)		#broadcast
			s.connect(('<broadcast>', 0))								#le mot-cle python pour INADDR_BROADCAST
			ip_local, port = s.getsockname()							#renvoi de l'adresse source
			return ip_local												#on retourne donc la vrai adresse
		except:															#mais l'on est pas certain que cette methode fonctionne a tous les coups
			try:														#c'est pour cela que l'on met aussi en place une deuxieme methode
				return socket.gethostbyname_ex(socket.gethostname())[2]	#qui renvoi n'importe quoi sous linux
			except:														#si rien ne marche car l'ordinateur n'est pas connecte a aucun resau
				return None

	def get_ip_internet():
		"""
		tente de retourner l'ip d'internet
		"""
		try:
			with Timeout(30):
				dic = eval(urllib.request.urlopen("https://api.ipify.org/?format=json").read().decode())
			return dic["ip"]
		except:
			try:
				with Timeout(30):
					dic = eval(urllib.request.urlopen("http://ipinfo.io/json").read().decode())
				return dic["ip"]
			except:
				try:
					with Timeout(30):
						dic = eval(urllib.request.urlopen("http://freegeoip.net/json").read().decode())
					return dic["ip"]
				except:
					return None

	def get_mac():
		"""
		retourne l'adress mac du pc
		"""
		try:
			return uuid.getnode()										#renvoi un entier
		except:
			return None

	identifiant = {}
	identifiant["hostname"] = socket.gethostname()
	identifiant["ip_wan"] = get_ip_internet()
	identifiant["ip_lan"] = get_ip_local()
	identifiant["mac"] = get_mac()

	return identifiant

def open_extend(file, mode, buffering, encoding, errors, newline, closefd, opener):
	"""
	extension de la fonction open de base
	"""
	class TextIOWrapper_py(io.TextIOWrapper):
		"""
		permet de lire les fichier python
		c'est a dire:
			-supprime tous les retours a la ligne inutils
			-supprime les comentaires et la documentation
		"""
		def __init__(self, *args, **kargs):
			io.TextIOWrapper.__init__(self, *args, **kargs)

	if re.match(r"\w+\.py$", file):
		return TextIOWrapper_py(buffer=buffering)

	return open(file, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener)

def serialize(obj, psw=None, buff=1024*1024, compresslevel=2, generator=False, copy_file=True, signature=None):
	"""
	'obj' peut etre:
		-un objet python de base ex: int, float, str, list, dict, set...
		-un path vers un fichier ou un dossier (str)
		-un fichier (le pointeur vers un fichier)
	'psw' est la clef de chiffrement (facultative) (en STR)
	'buff' est la tailles des paquets retournes en octets (100 Mo par defaut)
	'compresslevel' est compris entre 0 et 3, 0 pour pas de compression et 3 pour la meilleur compression possible (mais plus lente)
	'generator' est True si l'on retourne un generateur est False pour directement retourner le 'bytes'
	'copy_file' True => copie du fichier dans l'objet retourne si l'objet pointe un fichier ou un dossier
	retourne l'objet serialise
	"""
	class mkdir:
		"""
		cre un dossier temporaire
		allonge 'rep' pour l'inserer dans ce dossier
		"""
		def __init__(self, generator):
			self.remove = not(generator)
			self.rep = os.path.join(raisin.temprep, str(uuid.uuid4()))

		def __enter__(self):
			os.mkdir(self.rep)
			return self.rep

		def __exit__(self, *args):
			if self.remove:
				try:
					shutil.rmtree(self.rep)
				except:
					pass

	def compress(file):
		"""
		compresse au maximum le fichier 'file'
		'file' est le nom du fichier en relatif (sans basename)
		retourne le nom relatif
		"""
		def compresseur(file, algo):
			"""
			compress le fichier 'file' relatif (sans basename)
			avec l'algo lzma, gzip ou bz2
			retourne le nom relatif du fichier comresse
			"""
			path = os.path.join(rep, file+{lzma:".xz", gzip:".gz", bz2:".bz2"}[algo])#on ajoute la bonne extension pour pouvoir revenir en arriere
			with Printer(path.split(".")[-1]+" processing...", signature=signature) as p:#on informe quel algorithme est entrain de tourner
				init_size = os.path.getsize(os.path.join(rep, file))		#taille initiale du fichier
				with open(os.path.join(rep, file), "rb") as f:				#celui la, c'est le fichier de lecture
					t_init = time.time()									#demarrage du chronometre pour connaitre le temps de compression
					if algo != gzip:										#l'algo gzip est emerdant
						with algo.open(path, "wb") as archive:				#car il stoque des metadatas
							shutil.copyfileobj(f, archive)					#qui le rend instable
					else:													#c'est pour cela qu'on le traite a part
						with algo.GzipFile(path, "wb", mtime=0) as archive:	#afin de lui fixer les metadonee
							shutil.copyfileobj(f, archive)					#on copy avec shutil afin d'eviter les erreurs memoire
				t_final = int(time.time()-t_init)							#temps de compression
				p.show("runing time: "+str(t_final)+"s",0)					#affichage du temps de compression
				comp_purc = 100*(init_size-os.path.getsize(path))/init_size	#pourcentage de fichier compresse
				p.show("reduced percentage: "+str(round(comp_purc,2))+"%",0)#affichage de ce pourcentage
				return os.path.basename(path)								#et c'est tout

		def comparateur(file):
			"""
			compare les 3 algorithmes et garde celui qui retourne le meilleur resultat
			compress le fichier 'file' relatif (sans basename)
			retourne le nom du fichier relatif le plus petit entre les 4
			"""
			with Printer("comparison of one layer...", signature=signature):#comparaison d'une couche
				files = [file]+[compresseur(file, algo) for algo in (gzip, bz2, lzma)]#creation du test
				size = [os.path.getsize(os.path.join(rep, file)) for file in files]#test de comparraisin entre les differents fichiers
				file = files[size.index(min(size))]							#recuperation du meilleur
				[os.remove(os.path.join(rep, f)) for f in files if f != file]#on fait du menage mais en concervant tout de meme le fichier a garder
				return file													#on peut desormais recuperer le plus compact des fichiers

		if compresslevel == 0:												#si la compression n'est pas demandee
			return file														#on ne compress rien du tout et on passe a la suite
		elif compresslevel == 1:											#si une compression legere est demandee
			with Printer("light compression...", signature=signature):#on ne va faire qu'une seule passe
				out = compresseur(file, gzip)								#l'algo gzip est le plus rapide
				os.remove(os.path.join(rep, file))							#on fait un peu de menage
				return out													#arret ici
		elif compresslevel == 2:											#si il faut tester les 3 algorithmes
			with Printer("one compression layer...", signature=signature):#et garder le meilleur
				out = comparateur(file)										#on compare les differents algorithmes
				return out													#il est donc judicieux de ne pas continuer
		else:																#dans le cas on l'on reclame le meilleur
			with Printer("heavy compression...", signature=signature) as p:#taux de compression, on fait plein de couches de compressions
				init_size = os.path.getsize(os.path.join(rep, file))		#taille du fichier d'origine
				while 1:													#il faut donc commencer!
					new_file = comparateur(file)							#c'est parti pour l'etude d'une couche
					if new_file == file:									#si aucun des algos n'arrive plus a compresser le fichier
						break												#c'est que c'est fini, on sort donc de cette boucle sans fin
					file = new_file											#c'est reparti pour un tour!
				final_size = os.path.getsize(os.path.join(rep, file))		#on recupere la taille du fichier compresse
				comp_purc = 100*(init_size-final_size)/init_size			#pourcentage de fichier compresse
				p.show("total reduced: "+str(round(comp_purc, 4))+"%",0)	#affichage du taux total de compression		
				return file													#c'est pourquoi tout s'arrette ici

	def path_to_archive(path, name):
		"""
		met le repertoire specifier dans une archive
		de nom '_raisin.tar'
		'path' est le chemin du dossier ou du fichier a archiver
		'name' est le nom a donner a l'archive (sans 'dirname')
		retourne le nom de l'archive (sans 'dirname')
		"""
		with Printer("path->file...", signature=signature):					#on copie le lien dans une archive
			with tarfile.open(os.path.join(rep, name+".tar"),"w") as archive:#ouverture de l'archive dans le bon repertoire
				archive.add(path)											#on y ajoute le repertoire en y conservant toute l'arboressance
			return name+".tar"												#on retourne le nom de l'archive en relatif

	def cipher(file):
		"""
		'file' est le nom du fichier en relatif (sans basename)
		retourne le nom relatif du fichier crypte
		"""
		if psw == None:														#si il n'y a rien a crypter
			return file														#on ne le chiffre pas, on retourne donc le fichier tel qu'il est
		with Printer("coding...", signature=signature):						#si on doit le chiffrer
			kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=psw.encode("utf-8"), iterations=100000, backend=default_backend())
			key = base64.urlsafe_b64encode(kdf.derive(psw.encode("utf-8")))	#on utilise un module tout fait qui fait ca tres bien
			coder = Fernet(key)												#creation de la clef de chiffrement
			with tarfile.open(os.path.join(rep, file+".cry"),"w") as archive:#on ouvre l'archive avec la bonne extension
				with open(os.path.join(rep, file), "rb") as f:				#on ouvre aussi le fichier
					i=0														#initialisation du compteur
					while 1:												#pour chaque petit fragments du fichier source
						i+=1												#incrementation de ce compteur
						data = f.read(buff)									#on va en prendre un bout ni trop gros, ni trop petit
						if data == b"":										#si on est arrive a la fin du fichier
							break											#on s'arrete ici			
						data = coder.encrypt(data)							#si on a du boulot, on se charge du bout de ce fichier
						info = tarfile.TarInfo(str(i))						#affin de pouvoir ajouter dans l'archive
						info.size = len(data)								#un type 'bytes' et non pas un fichier ('path')
						archive.addfile(info, io.BytesIO(data))				#on est obliger de lui faire croire qu'il s'agit d'un fichier ('path')
			os.remove(os.path.join(rep, file))								#on fait du menage
			return compress(file+".cry")									#on fait une derniere petite compression

	def file_generator(file, header, buff):
		"""
		est un generateur qui retourne peu a peu
		l'integralite du fichier
		'header' est un STR qui sera colle en entete des donnes retournees
		'file' est le nom du fichier (sans dirname)
		"""
		header+="/"															#ajout d'un separateur pour pouvaire separrer l'entete du reste
		header = header.encode()											#on met de suite l'entete en binaire
		with open(os.path.join(rep, file), "rb") as f:						#on ouvre le fichier en binaire
			yield header+f.read(buff-len(header))							#on met l'entete
			while 1:														#tant que l'on a pas lu l'integralite du fichier
				pack = f.read(buff)											#si il reste un bout de fichier
				if pack == b"":												#si on est arrive au bout
					break													#on s'arrete
				yield pack													#on retourne le petit bout qu'il reste		
		shutil.rmtree(rep)													#et on fait du menage quand c'est fini

	def remove_indentation(code):
		"""
		retir les indentations en trop
		retir les comentaires
		retir les saut de lignes
		'code' est une liste de chaine de caractere ou chaque chaine represente une ligne de code
		retourne la liste avec les alineas en moin
		"""
		#suppression des indentations
		indentation = 0															#recuperation des indentations en trop
		tete = code[0]
		while tete[0] in " \t":
			indentation += 1
			tete = tete[1:]
		code = [l for l in code if l != "\n"]									#supression des espaces
		code = [l[indentation:] for l in code]									#supression des indentations
		
		#supressions des commentaires
		for i, ligne in enumerate(code):										#chaque ligne va subir ce sort
			parenthese = 0														#nombre de parenthes ouvertes
			crochet = 0															#nombre de crochets ouverts
			acolade = 0															#nombre d'acolades ouverts
			guillemet_simple = 0												#1 si on est dedans
			guillemet_double = 0												#de meme 1 si on est dedans
			for rang, caractere in enumerate(ligne):							#on verifi parcours la ligne de gauche a droite
				if (caractere == "#") and (parenthese+crochet+acolade+guillemet_simple+guillemet_double == 0):#si on arrive sur un comentaire
					code[i] = ligne[:rang]+"\n"									#supression du comentaire
					break														#passage a la ligne d'apres
				parenthese += {"(":1, ")":-1}.get(caractere, 0)					#on incremente ou decremente le nombre de parentheses
				crochet += {"(":1, ")":-1}.get(caractere, 0)					#celon qu'on va plus en profondeur ou qu'on en sort
				acolade += {"{":1, "}":-1}.get(caractere, 0)					#ce procede est valide pour les trois
				guillemet_simple += {"'":1-guillemet_simple}.get(caractere, 0)	#si il est ouvert, alors c'est qu'il se ferme
				guillemet_double += {'"':1-guillemet_double}.get(caractere, 0)	#si il etait ferme, alors il s'agit d'un ouverture

		#supressions des espaces a la fin
		for i, ligne in enumerate(code):										#chaque ligne est traitee
			for rang in range(len(ligne)-2, -1, -1):							#pour chaque caractere de droite a gauche
				if not ligne[rang] in " \t":									#si ce n'est plus un caractere inimprimable
					code[i] = ligne[:rang+1]+"\n"								#supression des espaces
					break														#on passe a la ligne suivante

		return code

	name = "_raisin"															#on fait une entete legere

	with Printer("serialisation...", signature=signature) as p:
		with mkdir(generator) as rep:											#ajout temporaire d'un repertoire
			if type(obj) == dict:												#si il s'agit d'un dictionnaire
				p.show("obj=dict->obj")											#on va faire du recursif a fond
				code = []														#c'est un code qui reconstitu le dictionaire
				code.append("import raisin\n")									#import du module de base
				code.append("dico = {"+"}\n")									#initialisation du dictionaire
				clef = sorted(obj.keys(), key=str)								#on tri les clefs pour avoir unicite du dictionaire
				for key, value in zip(clef, (obj[k] for k in clef)):			#pour chaque clef et chaque valeur
					if type(key) in [int, float, bool]:
						key = str(key)
					else:
						key = "raisin.decompress('"+raisin.compress(key, compresslevel=0, copy_file=False, signature=signature)+"', signature=local_signature)"
					if type(value) in [int, float, bool]:
						value = str(value)
					else:
						value = "raisin.decompress('"+raisin.compress(value, compresslevel=0, signature=signature)+"', signature=local_signature)"
					code.append("dico["+key+"] = "+value+"\n")
				code.append("def get_raisin_answer():\n")						#ajout d'une ligne d'appelle a la fin
				code.append("\treturn dico\n")									#qui retourne le dictionaire
				obj = code														#on dit que le nouvel objet est desormais un code
				name+=".imp"
			elif type(obj) == list:												#si l'objet est une liste
				p.show("obj=list->obj")											#on le dit a l'utilisateur
				if False in [type(e) in (int, float, bool, bytes) for e in obj]:#si il y a un interet a faire une serialisation recursive
					code = []													#c'est un code qui reconstitu le dictionaire
					code.append("import raisin\n")								#import du module de base
					message = "liste = ["										#initialisation de la liste
					for e in obj:												#pour chaque element
						if type(e) in [int, float, bool]:						#si il est inutile de serialise l'element
							e = str(e)											#on ne le serialise pas
						else:
							e = "raisin.decompress('"+raisin.compress(e, compresslevel=0, signature=signature)+"', signature=local_signature)"
						message += (e+",")										#la liste est peu a peu complete
					code.append(message[:-1]+"]\n")
					code.append("def get_raisin_answer():\n")					#ajout d'une ligne d'appelle a la fin
					code.append("\treturn liste\n")								#qui retourne le dictionaire
					obj = code													#on dit que le nouvel objet est desormais un code
					name+=".imp"
			elif type(obj) == tuple:											#si l'objet est un tuple
				p.show("obj=tuple->obj")										#on le dit a l'utilisateur
				if False in [type(e) in (int, float, bool, bytes) for e in obj]:#si il y a un interet a faire une serialisation recursive
					code = []													#c'est un code qui reconstitu le tuple
					code.append("import raisin\n")								#import du module de base
					message = "objet = ("										#initialisation du tuple
					for e in obj:												#pour chaque element
						if type(e) in [int, float, bool]:						#si il est inutile de serialise l'element
							e = str(e)											#on ne le serialise pas
						else:
							e = "raisin.decompress('"+raisin.compress(e, compresslevel=0, signature=signature)+"', signature=local_signature)"
						message += (e+",")										#le tuple est peu a peu complete
					code.append(message[:-1]+")\n")
					code.append("def get_raisin_answer():\n")					#ajout d'une ligne d'appelle a la fin
					code.append("\treturn objet\n")								#qui retourne le tuple complete
					obj = code													#on dit que le nouvel objet est desormais un code
					name+=".imp"
			elif ("sympy" in str(type(obj))) or ("sympy" in str(type(type(obj)))):#si il s'agit d'une expression sympy
				p.show("obj=sympy_expr->str")
				obj = str(sympy.srepr(obj))										#on le transforme betement en str, sympy gere le reste
				name+=".sym"
			elif inspect.isfunction(obj):										#si l'element est une fonction definie par l'utilisateur
				try:
					with Printer("obj=function->obj...", signature=signature):	#on en informe l'utilisateur
						code = inspect.getsourcelines(obj)[0]					#recuperation du code source
						code = remove_indentation(code)							#supression des indentations en trop
						
						#gestion de l'affichage
						code.append("def get_raisin_answer():\n")				#ajout d'une ligne d'appelle a la fin
						entete = code[0]										#recuperation du nom de la fonction
						entete = entete.split("(")[0]							#supression de toute la partie de droite
						entete = "def".join(entete.split("def")[1:])			#et de celle de gauche aussi
						while entete[0] in " \t":								#affin de seulement garder le nom de la fonction
							entete = entete[1:]									#qui peut desormai etre appellee
						code.append("\treturn "+entete+"\n")					#ce fonctionement permet d'uniformiser la sytaxe
						obj = code												#l'objet est transforme en fonction
						name+=".imp"											#memorisation pour le retour inverse
				except:
					pass
			elif inspect.isclass(obj):											#si l'element est une classe
				try:
					with Printer("obj=class->obj...", signature=signature):		#l'utilisateur en est informe
						code = inspect.getsourcelines(obj)[0]					#recuperation du code source
						sign = inspect.signature(obj).__str__()					#recuperation des parametres de la fonction
						code = remove_indentation(code)							#supression des indentations en trop
						code.append("def get_raisin_answer():\n")				#ajout d'une ligne d'appelle a la fin
						entete = code[0]										#recuperation du nom de la methode
						entete = ":".join(entete.split(":")[:-1])
						entete = "class".join(entete.split("class")[1:])
						while entete[0] in " \t":
							entete = entete[1:]
						code.append("\treturn "+entete)
						obj = code
						name+=".imp"
				except:
					pass
			elif inspect.ismethod(obj):											#si c'est une methode d'un objet
				try:
					with Printer("obj=method->obj...", signature=signature):#l'utilisateur est informe de ce qu'il en est
						parent = raisin.dumps(obj.__self__, signature=signature)#serialisation de l'objet parent
						entete = inspect.getsourcelines(obj)[0][0]
						entete = entete.split("(")[0]
						entete = "def".join(entete.split("def")[1:])
						while entete[0] in " \t":
							entete = entete[1:]				
						code = ["import raisin\n"]								#import du module qui va permetre de tout deserialiser
						code.append("def get_raisin_answer():\n")				#ajout d'une ligne d'appelle a la fin
						code.append("\treturn raisin.loads("+str(parent)+", signature=local_signature)."+entete+"\n")
						obj = code
						name+=".imp"					
				except:
					pass
			elif ("__main__." in str(type(obj))) or ("bound method" in str(obj.__init__) and (not type(obj) in (int, float, str, set, type(Exception), type(None), bytes, frozenset)) and (not "Error" in str(type(obj)))):#si l'element semble etre une classe deja parmetree
				try:															#c'est a dire ou la methode __init__ a deja ete appellee
					with Printer("obj=",str(type(obj))[8:-2],"->obj...", signature=signature):#on prend plein de precautions car on en est pas vraiment certain
						variables = obj.__dict__								#recuperation de variables internes
						code = inspect.getsourcelines(obj.__class__)[0]			#recuperation du code source
						init = inspect.getsourcelines(obj.__init__)[0]			#et en particulier de la methode __init__()
						for i in range(len(code)-len(init)+1):					#car cette derniere va changer
							if code[i:i+len(init)] == init:						#on cherche la position ou cette methode apparait
								del code[i:i+len(init)]							#suppression de cette methode afin de la reecrire
								break											#i correspond donc au rang de l'apparition de la methode
						init = ["	def __init__(self):\n"]						#c'est partit pour la reecrire entierement
						for var, value in variables.items():					#dans le but de redefinir imediatement chaque objet
							init.append("\t\tself."+var+"=raisin.decompress('"+str(raisin.compress(value, compresslevel=0, signature=signature))+"', signature=local_signature)\n")#on lui ajoute sa variable
						code = remove_indentation(code)							#suppression des alineas dans le code source
						code = [code[0]]+init+code[1:]							#on intercale la methode fraichement ecrite
						code.append("def get_raisin_answer():\n")				#pour plus d'uniformeseite
						entete = code[0]										#recuperation du nom de la classe
						entete = entete.split(":")[0]							#supression de toute la partie de droite
						entete = "class".join(entete.split("class")[1:])		#et de celle de gauche aussi
						while entete[0] in " \t":								#affin de seulement garder le nom de la fonction
							entete = entete[1:]									#qui peut desormai etre appellee
						code.append("\treturn "+entete+"()\n")					#ce fonctionement permet d'uniformiser la sytaxe					
						code.insert(0, "import raisin\n")						#ajout d'une ligne d'import
						obj = code												#l'objet a serialiser est desormai la liste qui represente l'objet
						name+=".imp"											#c'est pourquoi il faudra faire un traitement particulier a cette liste
				except Exception as e:
					raise e
					pass

			is_path = False														#on considere dans un premier temps que l'objet n'est pas un chemin
			if (len(str(obj)) < 32767) and copy_file:							#si la chaine est trop longue, elle ne risque pas d'etre un path
				if os.path.exists(str(obj)):									#si il s'agit d'un fichier ou d'un repertoire
					p.show("obj=path")											#on annonce que c'est bien un chemin d'acces
					name = path_to_archive(str(obj), name)						#on en fait une archive
					is_path = True												#on memorise qu'il s'agit bien d'un chemin
			if type(obj) == io.TextIOWrapper:									#si il s'agit d'un pointeur vers un txt
				p.show("obj='io.TextIOWrapper'")								#on ouvre un fichier nouveau
				name+=".txt"													#on y met la bonne extension
				with open(os.path.join(rep, name), "w", encoding=obj.encoding) as f:#afin de pourvoir l'exploiter
					shutil.copyfileobj(obj, f)									#on le copie dans le fichier fraichement cree
			elif type(obj) == io.BufferedReader:								#si il s'agit d'un pointeur vers un fichier binaire
				p.show("obj='io.BufferedReader")								#on ouvre un fichier nouveau
				name+=".bytes"													#on y met la bonne extension
				with open(os.path.join(rep, name), "wb") as f:					#afin de pourvoir l'exploiter
					shutil.copyfileobj(obj, f)									#on le copie dans le fichier fraichement cree
			elif not is_path:													#dans tous les autres cas
				p.show("obj->pickle->file")										#on serialise l'objet avec pickle
				name+=".pk"														#on y met la bonne extension
				with open(os.path.join(rep, name),"wb") as f:					#on ouvre un fichier en binaire
					pickle.dump(obj, f)											#on y ecrit l'objet python

			name = compress(name)												#on compresse les donnees
			name = cipher(name)													#on chiffre les donnees si cela est demande
			entete = ".".join(name.split(".")[1:])								#recuperation des donnees importante en entete
			gen = file_generator(name, entete, buff)							#c'est un generateur que l'on retourne
			if generator:
				return gen
			data = b""
			for pack in gen:
				data+=pack
			return data

def serialize_bis(obj, signature, buff, compresslevel, copy_file, psw):
	"""
	serialize l'objet 'obj'. Cet objet peut etre:
		-un entier (int)
		-une chaine de caractere (str)
		-un flotant (float)
		-du binaire (bytes)
		-un pointeur de fichier texte (io.TextIOWrapper)
		-un pointeur vers un fichier binaire (io.BufferedReader ou io.BufferedWriter)
		-une liste (list)
		-un tuple (tuple)
		-un dictionaire (dict)
		-un nom de fichier, relatif ou absolu, si 'copy_file' == True (str)
		-un module (module)
		-une classe (class)

	'signature' est l'identifiant pour gerer l'affichage (STR)
	'buff' est environ la taille des paquets retournes en octets (100 Mo par defaut) (INT)
	'compresslevel' est le taux de compression a appliquer 0 pour sauter cette etape (INT)
	'copy_file' permet d'autoriser ou non la copie de fichier si l'objet est un str qui correspond a un chemin (BOOL)
	'psw' est un mot de passe pour crypter les donnees de facon symetriques (STR)
	est un generateur qui renvoi des paquets de buff octets	(BYTES)
	"""
	def cipher_data(data, psw, signature):
		"""
		'data' est une sequence de bytes
		retourne la nouvelle sequence data mais cryptee (l'entete et retourne avec)
		"""
		if psw == None:
			return data
		with raisin.Printer("encryption sequences...", signature=signature):
			entete = "</>9797</>"										#entete pour le chiffrement basic
			psw = psw.encode("utf-8")									#on fait la convertion avant que l'algorithme ne la fasse tout seul et bute sur l'ascii
			if len(psw) <= 16:											#la clef doit faire
				psw = (psw+b" "*16)[:16]								#16 octets
			elif len(psw) <= 24:										#ou bien
				psw = (psw+b" "*8)[:24]									#24 octets
			else:														#on bien meme
				psw = (psw+b" "*8)[:32]									#32 octets au maximum
			iv = Crypto.Random.new().read(AES.block_size)				#c'est pour mettre un peu d'aleatoire dans le tas
			n = 16-len(data)%16											#'data' doit etre un multiple de 16 octets
			data = AES.new(psw, AES.MODE_CBC, iv).encrypt(data+b" "*n)	#on peut enfin passer au chiffrement
			data = entete.encode()+hex(n)[2].encode()+iv+data			#ajout des informations necessaire a la bijection
			return data

	def cipher_file(filename, psw, signature, remove=True):
		"""
		'filename' est le chemin absolu vers le fichier binaire a encrypter
		supprime le fichier une fois l'operation terminee si 'remove' == True
		retourne le nouveau 'filename' du fichier encrypte (l'entete figure au debut du fichier)
		"""
		if psw == None:
			return filename
		with raisin.Printer("encryption file...", signature=signature):
			new_filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".cry")
			with open(new_filename, "wb") as f:
				for pack in cipher_generator(generator_file(filename, buff, remove=remove), psw, signature):
					f.write(pack)
		os.remove(filename)
		return new_filename

	def cipher_generator(generator, psw, signature):
		"""
		'generator' est un generateur de paquet de bytes
		cede ces memes paquets mais criptes (l'entete est presente sur le premier packet)
		"""
		if psw == None:
			for pack in generator:
				yield pack
		else:
			with raisin.Printer("encryption generator...", signature=signature):
				entete = "</>9696</>"									#on ne va pas utiliser cipher_data
				psw = psw.encode("utf-8")								#car il fait des operations a chaque fois
				if len(psw) <= 16:										#qui ne necessite pas d'etre faites plusieurs fois
					psw = (psw+b" "*16)[:16]							#comme cette operation par exemple, elle consiste a
				elif len(psw) <= 24:									#mettre la clef de chiffrement a la bonne longueur
					psw = (psw+b" "*8)[:24]								#car la clef doit imperativement faire
				else:													#16, 24 ou 32 octets
					psw = (psw+b" "*8)[:32]								#sinon l'algorithme AES ne fonctionne pas
				iv = Crypto.Random.new().read(AES.block_size)			#c'est pour mettre un peu d'aleatoire
				i = 0													#cette variable permet juste de savoir si l'on est a la premiere boucle ou pas
				for pack in generator:									#une fois ces operations faites, on peut lancer le chiffrement
					n = 16-len(pack)%16									#encore une fois la longueur de ce que l'on doit coder se doit d'etre un multiple de 16
					pack = AES.new(psw, AES.MODE_CBC, iv).encrypt(pack+b" "*n)#on peut enfin passer au chiffrement
					pack = hex(n)[2].encode()+str(len(pack)).encode()+b"_"+pack#on y ajoute les informations necessaires au decryptage
					if i == 0:											#si on est a la premiere boucle
						pack = entete.encode()+iv+pack					#on insert subtilement l'entete
						i = 1											#on change la valeur du detecteur pour n'etre qu'une seule fois dans la premiere boucle
					yield pack

	def compress_data(data, compresslevel, signature):
		"""
		'data' est une sequence de bytes
		retourne la nouvelle sequence data mais compressee (l'entete est retourne avec)
		"""
		if compresslevel == 0:
			return data
		with raisin.Printer("compressing sequences...", signature=signature):
			raise NotImplementedError()

	def compress_file(filename, compresslevel, signature, remove=True):
		"""
		'filename' est le chemin absolu vers le fichier binaire a compresser
		supprime le fichier une fois l'operation terminee si 'remove' == True
		retourne le nouveau 'filename' du fichier compresse (l'entete figure au debut du fichier)
		"""
		if compresslevel == 0:
			return filename
		with raisin.Printer("compressing file...", signature=signature):
			raise NotImplementedError()

	def compress_generator(generator, compresslevel, signature):
		"""
		'generator' est un generateur de paquet de bytes
		cede ces memes paquets mais encodees (l'entete est presente sur le premier paquet)
		passe tout de meme par un fichier pour que la compression finale soit meilleure
		"""
		if compresslevel == 0:
			for pack in generator:
				yield pack
		else:
			with raisin.Printer("compressing generator...", signature=signature):
				raise NotImplementedError()

	def generator_file(filename, buff, remove=True, entete=""):
		"""
		'filename' est le chemin absolu vers un fichier binaire
		supprimme le fichier une fois qu'il est totalement restitue si remove == True
		cede peu a peu le fichier avec des packets de 'buff' octets
		"""
		with open(filename, "rb") as f:									#on ouvre le fichier en binaire
			i = 0														#on met un detecteur de premiere boucle
			while 1:													#tant que l'on a pas lu l'integralite du fichier
				pack = f.read(buff)										#on va lire le bout suivant
				if i == 0:												#si on en est a la premiere boucle
					pack = entete.encode("utf-8")+pack					#on insere l'entete
					i = 1												#on change la valeur du detecteur pour faire cela une fois seulement
				if pack == b"":											#si on est arrive au bout
					break												#on s'arrete
				yield pack												#sinon on cede le bout qui vient d'etre lu
		if remove:
			os.remove(filename)											#suppression definitive du fichier desormais lu

	def generator_data(data, buff):
		"""
		c'est tout simplement un generateur qui permet de ceder peu a peu des paquets de buff octets
		'data' doit imperativement etre une sequence de type bytes
		"""
		for i in range(0, len(data), buff):
			yield data[i:i+buff]

	def generator_to_generator(pack, generator, buff):
		"""
		'generator' est un generateur qui cede des paquets de taille tres variable
		les paquet doivent etre de type 'bytes'
		le but est ici, d'uniformiser la taille des packet affin de renvoyer des pakets de 
		'buff' octet
		cede donc les paquets au fur a meusure
		"""
		for data in generator:											#on va lentement vider le generateur
			pack += data												#pour stocker peu a peu les paquets dans cette variable
			while len(pack) >= buff:									#si le packet est suffisement gros
				yield pack[:buff]										#on le retourne avec la taille reglementaire
				pack = pack[buff:]										#puis on le racourci et on recomence le test
		yield pack														#enfin, on retourne le bout restant

	def get_installed_modules():
		"""
		retourne le dictionaire qui a chaque module
		associ son chemin absolu dans l'ordinateur
		"""
		def analyse_dir(path, header):
			"""
			fouille recursivement le dossier pour retourner le dictionaire des modules
			qui se cachent a l'interieur
			"""
			dico = {}													#initialisation du dictionaire
			for element in os.listdir(path):							#on fouille chaque elements
				mod = os.path.abspath(os.path.join(path, element))		#recuperation du chemin absolu qui mene a cet element
				if element == "__init__.py":							#si l'element nous prouve la presence d'un module
					dico[header] = path									#alors on ajoute le nom du dossier
				elif os.path.isdir(mod):								#si c'est un dossier
					dico = {**dico, **analyse_dir(mod, header+"."+element)}#on le parcour recursivement
				elif element.split(".")[-1] in ("py", "so", "egg-info"):#si il s'agit d'un fichier en lien avec le module
					dico[header+"."+".".join(element.split(".")[:-1])] = dico.get(header+"."+".".join(element.split(".")[:-1]), mod)#on l'ajoute au dictionaire		
			return dico

		with raisin.Printer("referencing all modules..."):
			dico = {}													#initialisation du dictionaire
			for path in sys.path:										#pour chaque endroit ou sons stocke les modules
				if os.path.isdir(path):									#si c'est un dossier
					for mod in os.listdir(path):						#pour chaque elements du dossier
						mod = os.path.abspath(os.path.join(path, mod))	#recuperation du chemin absolu qui mene a cet element
						if os.path.isdir(mod):							#si l'element semble etre un module dans un repertoire
							for module, chemin in analyse_dir(mod, os.path.basename(mod)).items():#pour chaque elements
								dico[module] = dico.get(module, chemin)	#si il n'y est pas deja, on l'ajoute a la liste
						elif mod.split(".")[-1] in ("py", "so", "egg-info"):#si il s'agit d'un fichier en lien avec le module
							dico[".".join(os.path.basename(mod).split(".")[:-1])] = dico.get(".".join(os.path.basename(mod).split(".")[:-1]), mod)#on l'ajoute au dictionaire
						else:
							pass
			return dico

	def get_module_dependence(modulename, installed_modules):
		"""
		cherche les dependances du module 'modulename'
		retourne l'ensemble qui contient le nom de tous les modules dons
		'modulename' depend
		"""
		def is_space(chaine):
			"""
			retourn True si la chaine est exclusivement composee de caracteres non imprimables
			"""
			for c in chaine:
				if not re.search(r"\s", c):
					return False
			return True

		def analyse(file_path):
			"""
			lit le fichier 'file_path' pour rechercher les lignes
			d'import de module
			cede le nom de chacun de ces modules
			"""
			with open(file_path, "r", encoding="utf-8") as f:			#ouverture du fichier designe
				expression1 = r"\s*(from){1}\s+(?P<module>[a-zA-Z0-9._]+)\s+(import)\s+"#recupere les lignes du type 'from ... import '
				expression2 = r"\s*(import){1}\s+(?P<modules>[a-zA-Z0-9, ._]+)"#recupere les ligne du type 'import ...'
				uni = Uniformizer(f.readlines())
				for ligne in uni.del_facultative():						#on parcours chaque ligne du module principal
					if not "import " in ligne:							#si le mot "import" n'apparait meme pas
						continue										#alors on ne cherche pas a passer plus de temps a l'analyse
					if ligne:											#si la ligne n'est pas une chaine vide
						ligne = clean_codeligne([ligne])				#on en leve les comentaire de la ligne si il y en a
					if ligne:											#si la ligne n'est pas vide
						ligne = ligne[0]								#on transforme la liste en chaine de caractere
					else:												#si apres netoyage, il ne reste plus rien
						continue										#on passe a la ligne suivante
					found = re.search(expression1, ligne)				#si une des ligne est de la forme from module import ...
					if found:											#alors dans ce cas
						if not is_space(ligne.split("from")[0]):
							continue
						yield found.group("module").split(".")[0]		#on recupere le nom de ce module
					else:												#si la ligne n'est pas de cette forme
						found = re.search(expression2, ligne)			#alors on regarde si elle ne serait pas du genre import module
						if found:										#si effectivement la ligne
							if not is_space(ligne.split("import")[0]):
								continue
							chaine = found.group("modules")				#c'est la chaine d'import
							while " " in chaine:						#tant qu'il y a des espaces dans la chaine
								chaine = chaine.replace(" ", ",")		#on remplace les esplace par des virgules
							while ",," in chaine:						#du coup on a pu cree plusieur occureces de virgule
								chaine = chaine.replace(",,", ",")		#que l'on supprime donc peu a peu
							alias = False								#devient True si le mot qui suit est un alias
							for m in chaine.split(","):					#on recupere alors le nom de tous les modules
								if m == "":								#si il n'y a rien
									pass								#c'est ignore
								elif m == "as":							#si c'est un alias
									alias = True						#alors on le precise
									pass								#puis on ne s'y attarde pas
								elif alias:								#si il faut sauter ce mot
									alias = False						#alors on le saute mais pas l suivant
									pass								#on ne s'y attarde donc pas non plus
								else:									#si ce n'est rien de tout ca
									yield m.split(".")[0]				#alors on a surement affaire a un nom de module

		path = installed_modules[modulename]							#recuperation du path du module
		if os.path.isfile(path):										#si le module n'est qu'un fichier
			if os.path.basename(path)[-3:] == ".py":					#et que ce fichier est analysable
				return set(analyse(path))								#alors on n'analyse que lui
			return set()												#sinon, on ne fait rien
		total = []														#va contenir toutes les dependances
		for path, dirs, files in os.walk(path):							#dans le cas ou c'est un repertoire
			if "__init__.py" in files:									#on verifi tout de meme une derniere fois qu'il s'agit bien d'un module python
				for file in files:										#on parcours tout le dossier recursivement
					if file[-3:] == ".py":								#si il s'agit bien d'un fichier text
						total.extend(list(analyse(os.path.join(path, file))))#on le fouille en profondeur
		return set(total)												#on renvoi l'ensemble de tous les modules depandants

	def serialize_class(obj, signature, buff):
		"""
		'obj' est le pointeur vers la class a serialiser
		cede peu a peu la classe avec ses methodes, les packets cede sont de tailles tres variables
		mais n'exede pas buff, si celui-ci est suffisement grand
		"""
		def serialise_fonction(pointeur):
			"""
			retourne le code normalise pointe par 'pointeur'
			retourne aussi l'ensemble des parametres presents dans la signature
			"""
			code = {}
			code["name"] = pointeur.__name__							#c'est le nom de la methode
			signature = inspect.signature(pointeur)						#signature de la methode
			code["default"] = {}										#ca va etre tout les parametres par defaut
			code["signature"] = []										#c'est ce qui se trouve dans l'entete
			for parametre in signature.parameters.values():				#pour chaque parametre
				if parametre.default == inspect._empty:					#si ce n'est pas un parametre par defaut
					code["signature"].append(["empty", parametre.name, {parametre.VAR_POSITIONAL:"*", parametre.VAR_KEYWORD:"**"}.get(parametre.kind, "")])#on l'ajoute tel quel
				else:													#si il s'agit d'un parametre avec une valeur pas defaut
					code["signature"].append(["default", parametre.name, parametre.default])#on serialise aussi ce parametre
			lignes = inspect.getsourcelines(pointeur)[0]				#voila toutes les lignes de code			
			while True:													#tant que l'on est pas au vrai debut
				copie = lignes[0].replace(" ","").replace("\t","")		#on vire les caracteres inimprimables
				if len(copie) < 4:										#si il y a moin de 4 caracteres
					del lignes[0]										#c'est mort, on en est pas au debut
				elif copie[0:3] == "def":								#si il s'agit bien de la premiere ligne
					break												#on ne fait pas plus de menage
				del lignes[0]											#si c'est pas la premiere ligne, on la supprime
			uni = Uniformizer(lignes)									#et bien-sur, le code source normalise
			uni.del_end_line()											#dons on commence par enlever les retour a la ligne
			uni.code = uni.code[1:]										#et de pouvoir retirer la ligne de definition
			code["code"] = uni.normalize()								#et dont on met tout bien
			return code													#on retourne le code source

		with raisin.Printer("serialization of "+obj.__name__+"...") as p:
			entete = "</>1513</>"										#balise de debut
			yield entete.encode()										#on cede cette balise
			yield (obj.__name__+"</>").encode()							#on cede aussi le nom la classe
			for nom, pointeur in sorted(inspect.getmembers(obj), key=lambda t: t[0]):#pour chaque methode de cet objet et son heritage
				if inspect.isfunction(pointeur):						#si l'on s'aprette bien a serialiser une methode
					p.show(nom)											#on affiche ou l'on en est
					for i, pack in enumerate(serialize_bis(serialise_fonction(pointeur), signature=signature, buff=buff, compresslevel=0, copy_file=False, psw=None)):#code source dans un dictionaire
						if i == 0:										#dans le cas ou l'on en est au premier packet a poster
							yield str(len(pack)).encode()+b"d"			#on pose une balise
						else:											#si ce n'est pas le premier packet
							yield str(len(pack)).encode()+b"m"			#on poste une balise intermediaire
						yield pack										#puis on retourne le contenu
					yield b"f"											#on indique que l'on est arrive a la fin

	def serialize_dict(dico, signature, copy_file, buff):
		"""
		'dico' est le dictionaire (dict)
		genere le dictionaire avec des packets de taille environ buff
		"""
		if is_jsonisable(dico, copy_file):								#si il existe un algorithme performant pour serialiser ce dictionaire
			if sys.getsizeof(dico) < buff:								#si il ne prend pas trop de place en memoire
				entete = "</>1701</>"									#alors on le serialize directement dans la ram
				yield (entete+json.dumps(dico)).encode("utf-8")			#c'est a dire avec json
			else:														#si l'objet est un peu trop gros
				entete = "</>1702</>"									#on passe par un fichier
				filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".json")#generation du nom du fichier temporaire
				with open(filename, "w") as f:							#creation phisique du fichier
					f.write(entete)										#on y ecrit l'entete
					json.dump(liste, f)									#puis la liste en json
				for pack in generator_file(filename, buff):				#pour chaque petit bout du fichier que l'on vient d'ecrire
					yield pack											#on envoi ce petit packet
		else:															#si le dictionaire contient des parties non jsonisables
			entete = "</>1814</>"										#on va passer par une liste
			yield entete.encode("utf-8")								#on previent de ce qui arrive
			for pack in serialize_list([[klef, value] for klef, value in dico.items()], signature, copy_file, buff, header=False):
				yield pack

	def serialize_function(fonc, signature, buff):
		"""
		'fonc' est le pointeur vers la fonction
		cede peu a peu des packets d'environ 'buff' octets
		"""
		class Analiser:
			"""
			analyse et traite un bout de code qui represente une fonction
			"""
			def __init__(self, filename, start_line, signature):
				self.filename = filename				#nom du fichier source
				self.start_line = start_line			#numero de la ligne a partir de laquelle l'objet commence
				self.signature = signature				#signature pour afficher dans la bonne colone
				self.is_uniformize = False				#devient True des que les lignes de code sont uniformises
				self.other_objects = {}					#ce sont toutes les fonctions, modules, classes, definies au dessus de la fonction en cours d'analyse

			def decompose(self, ligne):
				"""
				retourne les differents elements de la ligne
				'ligne' doit representer une ligne de code COMPLETE (pas de retour a la ligne)
				et doit se finir par "\n"
				retourne un dictionaire qui contient:
				-'indentation':
					l'ensemble de touts les premiers caracteres inimprimable consecutifs (str)
				"""
				dico = {"indentation":""}		#initialisation du dictionaire a remplir
				zonne = 0						#c'est la zonne dans laquelle on se trouve
				for caractere in ligne[:-1]:	#pour chaque caractere
					#indentation
					if zonne == 0:				#si il est dans la zone d'indentation
						if caractere in " \t":	#et que c'est un espace ou une tabulation:
							dico["indentation"]+=caractere#alors ce caractere fait partie integrante de l'indentation de cette ligne
							continue			#on passe alors au caractere suivant
						else:					#si ce n'est pas un caractere de ce type la
							zonne = 1			#on passe alors dans la premiere zonne interessante

				return dico

			def is_end_ligne(self, ligne):
				"""
				analyse la ligne de code 'ligne'
				retourne True, ligne si la ligne est complete
				retourne False, None si la ligne de code n'est pas terminee
				"""
				#preparation
				try:									#dans le cas ou les variables ne sont pas cree
					self.profondeur						#pour cela il faut faire un petit test
					self.old_line
				except AttributeError:					#alors on va les initialiser
					self.profondeur = {"parentheses":0, "crochets":0, "accolades":0, "guillemets":[0, 0, 0, 0]}#afin de savoir ou l'on se situe
					self.old_line = ""

				#reperage
				for rang_car, caractere in enumerate(ligne):#on va voir chaque caractere
					if (self.profondeur["parentheses"]+self.profondeur["crochets"]+self.profondeur["accolades"]+sum(self.profondeur["guillemets"]) == 0) and (caractere == "#"):#si on entre sur un comentaire
						break							#on passe a la suite
					if sum(self.profondeur["guillemets"]) == 0:#si l'on est pas dans une chaine de caractere ou un commentaire
						self.profondeur["parentheses"] += {"(":1, ")":-1}.get(caractere, 0)#on incremente ou decremente le nombre de parentheses
						self.profondeur["crochets"] += {"[":1, "]":-1}.get(caractere, 0)#selon qu'on va plus en profondeur ou qu'on en sort
						self.profondeur["accolades"] += {"{":1, "}":-1}.get(caractere, 0)#ce procede est valide pour les trois
					for i in range(4):					#on s'attarde maintenant aux 4 types de guillemets
						if sum((g for j,g in enumerate(self.profondeur["guillemets"]) if j != i)) == 0:#si il n'y a pas d'autres guillemets
							if ligne[rang_car:rang_car+3-2*(i%2)] == ["'''", "'", '"""', '"'][i]:#et que ce type de guillemet est present
								self.profondeur["guillemets"][i] = 1-self.profondeur["guillemets"][i]#alors on change ca valeur
								break					#puis on sort imediatement de la boucle avant d'introduire une erreur

				#passage a l'acte
				if self.profondeur["parentheses"]+self.profondeur["crochets"]+self.profondeur["accolades"] != 0:#si on est en plein dans une ligne de def
					if ligne[-2] == "\\":				#et que l'avant dernier caractere impose un saut de ligne
						ligne = ligne[:-2]				#on en enleve la bonne quantite
					else:								#dans le cas ou ce caractere n'est pas explicite
						ligne = ligne[:-1]				#on supprime juste le retour a la ligne mais pas plus
					self.old_line += ligne				#extension de la ligne suivante avec celle-ci
					return False, None					#on dit alors que ce n'est pas fini
				if self.profondeur["guillemets"][1] or self.profondeur["guillemets"][3]:#si on est en plein dans un guillemet simple
					self.old_line += ligne[:-1]			#on supprime seulement le saut de ligne
					return False, None					#ce n'est donc pas termine non plus
				if self.profondeur["guillemets"][0] or self.profondeur["guillemets"][2]:#si il y a des guillememets triples
					if ligne[-2] == "\\":				#et que l'avant dernier caractere impose un saut de ligne
						ligne = ligne[:-2]				#on en enleve la bonne quantite
					else:								#dans le cas ou ce caractere n'est pas explicite
						ligne = ligne[:-1]				#on supprime juste le retour a la ligne mais pas plus
					self.old_line += ligne				#extension de la ligne suivante avec celle-ci
					return False, None					#on dit alors que ce n'est pas fini

				ligne = self.old_line+ligne				#on concatene toutes ces lignes
				self.old_line = ""						#afin de pouvoir les reinitialiser
				return True, ligne						#on retourne alors la ligne complette

			def normalize(self):
				"""
				cede chaque ligne de code normalise, avec toutes les dependances inscrites dans la fonction elle meme
				"""
				self.uniformize()						#on commence par unifomiser le code si ce n'est pas deja fait
				yield ""

			def uniformize(self):
				"""
				uniformise le ligne de code
				"""
				if self.is_uniformize:					#si cette opperation a deja ete faite
					return None							#on ne la refait pas a nouveau
				with raisin.Printer("source lines analization...", signature=self.signature) as p:#on dit ce que l'on fait
					new_filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".py")#nom du fichier dans lequel on va ecrir le nouveau code
					with open(new_filename, "w", encoding="utf-8") as new_file:#on ouvre ce fichier
						with open(self.filename, "r", encoding="utf-8") as old_file:#c'est l'ancien fichier dans lequel on va extraire les donnee primaires
							
							#analyse du contexte
							for rang, ligne in enumerate(old_file):#on lit chaque ligne du nouveau ficher
								if rang == self.start_line:#si on arrive aux ligne qui definissent la fonction elle meme
									break				#on passe a la suite
								booleen, complete_line = self.is_end_ligne(ligne)#on recupere le ligne
								if not booleen:			#si la ligne n'es pas complete
									continue			#on la complete
								print(complete_line)



				self.is_uniformize = True		#on marque le fait que l'on vien de faire un travail consequent
				return None						#on sort de cette methode

		entete = "</>1915</>"											#mise en place de l'entete
		code = {}														#c'est le dictionaire qui va etre retourne
		code["code"], start_line = inspect.getsourcelines(fonc)			#recuperation du code brut
		sig = inspect.signature(fonc)									#recuperartion de l'entete
		code["signature"] = []											#c'est ce qui se trouve dans l'entete
		for parametre in sig.parameters.values():						#pour chaque parametre
			if parametre.default == inspect._empty:						#si ce n'est pas un parametre par defaut
				code["signature"].append(["empty", parametre.name, {parametre.VAR_POSITIONAL:"*", parametre.VAR_KEYWORD:"**"}.get(parametre.kind, "")])#on l'ajoute tel quel
			else:														#si il s'agit d'un parametre avec une valeur pas defaut
				code["signature"].append(["default", parametre.name, parametre.default])#on serialise aussi ce parametre	
		if ("lambda" in code["code"][0]) and ("=" in code["code"][0]) and (len(code["code"]) == 1):#si il s'agit d'une expression avec lambda
			code["name"] = "lambda"										#on precise qu'il s'agit d'une expression lambda
			code["code"] = Uniformizer([":".join(code["code"][0].split(":")[1:])]).normalize()#on ne garde que le contenu
		else:															#si c'est une code normal
			code["name"] = fonc.__name__								#recuperation du nom de la fonction
			filename = inspect.getsourcefile(fonc)
			code["code"] = list(Analiser(filename, start_line, signature).normalize())
		
		yield entete.encode()
		for pack in serialize_bis(obj=code, signature=signature, buff=buff, compresslevel=0, copy_file=False, psw=None):
			yield pack

	def serialize_list(liste, signature, copy_file, buff, header=True):
		"""
		'liste' est une liste (LIST)
		genere la liste peu a peu avec autant de paquets que d'elements
		l'entete est contenu dans les paquets retournee
		cette algorithme est faux mathematiquement mais les probabilitees montrent que
		la probabilitee qu'une balise de longueur k apparraise spontanement dans une chaine de n octets vaux:
		P = (n-k+1)/(256**k) qui vaut 10⁻⁶ pour 100 Go (n=10¹¹)
		"""
		if is_jsonisable(liste, copy_file):								#et qu'il existe un algorithme performant pour serialiser cette liste
			if sys.getsizeof(liste) < buff:								#si la liste ne prend pas trop de place
				if header:
					entete = "</>1101</>"									#alors on va la serializer dans la ram
				else:
					entete = ""
				yield (entete+json.dumps(liste)).encode("utf-8")		#on retourne alors le packet directement
			else:														#dans le cas ou l'objet est un peu plus gros
				if header:
					entete = "</>1102</>"									#on va passer par le disque dur pour eviter toute surcharge de memoire
				else:
					entete = ""
				filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".json")#generation du nom du fichier temporaire
				with open(filename, "w") as f:							#creation phisique du fichier
					f.write(entete)										#on y ecrit l'entete
					json.dump(liste, f)									#puis la liste en json
				for pack in generator_file(filename, buff):				#pour chaque petit bout du fichier que l'on vient d'ecrire
					yield pack											#on envoi ce petit packet
		else:
			if header:
				entete = "</>1108</>"									#balise de debut
				yield entete.encode()									#on retourne deja ca, comme ca c'est fait
			for element in liste:										#pour chaque element qu'il y a dans la liste
				for i,pack in enumerate(serialize_bis(element, signature=signature, buff=buff, compresslevel=0, copy_file=copy_file, psw=None)):
					if i == 0:											#si l'on s'apprete a envoyer un sous element
						yield str(len(pack)).encode()+b"d"				#cette balise signe le debut et nous renvoi a la fin du packet
					else:												#dans le cas ou l'on est en plein milieu de l'objet
						yield str(len(pack)).encode()+b"m"				#balise qui signe le milieu
					yield pack											#on delivre de cette facon les fichiers petit a petit
				yield b"f"												#on marque la fin du packet (pour plus de vitesse a la deserialisation)

	def serialize_module(modulename, signature, module_path, dependences, buff):
		"""
		permet de retourner peu a peu l'ensemble d'un dossier
		ce dossier correspond a un module python
		au moment de la deserialisation, le module est retourne
		"""
		def graph_maker(path, first=True):
			"""
			retourne un dictionaire qui a chaque dossier, associ le dictionaire
			de tous les dossiers enfant
			si le dossier est vide de dossier, on lui ascossi {}
			"""
			if first:
				if "__init__.py" in os.listdir(os.path.dirname(path)):
					return graph_maker(os.path.dirname(path), first=True)
				elif os.path.isfile(path):
					return {}
			dico = {}
			for rep in os.listdir(path):
				nouv = os.path.join(path, rep)
				if os.path.isdir(nouv) and rep != "__pycache__":
					dico[rep] = graph_maker(nouv, first=False)
			if first:
				return {os.path.basename(path):dico}
			return dico

		def file_found(path, liste_primaire=[], first=True):
			"""
			cede chaque fichier et la liste de son arborescence
			"""
			if first:
				if "__init__.py" in os.listdir(os.path.dirname(path)):
					for path, liste in file_found(os.path.dirname(path), first=True):
						yield path, liste
					raise StopIteration
				elif os.path.isfile(path):
					yield path, [os.path.basename(path)]
					raise StopIteration
			if liste_primaire == []:
				liste_primaire = [os.path.basename(path)]
			for rep in os.listdir(path):
				nouv = os.path.join(path, rep)
				if os.path.isdir(nouv) and rep != "__pycache__":
					for npath, liste in file_found(nouv, liste_primaire+[rep], first=False):
						yield npath, liste
				elif (rep[-4:] != ".pyc") and (rep != "__pycache__"):
					yield nouv, liste_primaire+[rep]

		entete = "</>1512</>"											#balise du debut
		yield entete.encode()											#on le retourne de suite comme ca c'est fait
		
		#nom du module
		for i,pack in enumerate(serialize_bis(modulename, signature, buff=buff, compresslevel=0, copy_file=False, psw=None)):#serialisation rapide du nom du module
			if i == 0:													#si l'on s'apprete a envoyer un sous element
				yield str(len(pack)).encode()+b"d"						#cette balise signe le debut et nous renvoi a la fin du packet
			else:														#dans le cas ou l'on est en plein milieu de l'objet
				yield str(len(pack)).encode()+b"m"						#balise qui signe le milieu
			yield pack													#on delivre de cette facon les donnees petit a petit
		yield b"f"
		
		#liste des depandances
		for i,pack in enumerate(serialize_list(list(dependences-{modulename}), signature, copy_file=False, buff=buff)):
			if i == 0:													#si l'on s'apprete a envoyer un sous element
				yield str(len(pack)).encode()+b"d"						#cette balise signe le debut et nous renvoi a la fin du packet
			else:														#dans le cas ou l'on est en plein milieu de l'objet
				yield str(len(pack)).encode()+b"m"						#balise qui signe le milieu
			yield pack													#on delivre de cette facon les donnees petit a petit
		yield b"f"
		
		#creation du graph
		for i,pack in enumerate(serialize_bis(graph_maker(module_path), signature, buff=buff, compresslevel=0, copy_file=False, psw=None)):#serialisation rapide du nom du module
			if i == 0:													#si l'on s'apprete a envoyer un sous element
				yield str(len(pack)).encode()+b"d"						#cette balise signe le debut et nous renvoi a la fin du packet
			else:														#dans le cas ou l'on est en plein milieu de l'objet
				yield str(len(pack)).encode()+b"m"						#balise qui signe le milieu
			yield pack													#on delivre de cette facon les donnees petit a petit
		yield b"f"

		for path, l in file_found(module_path):
			for i, pack in enumerate(serialize_list(l, signature, copy_file=False, buff=buff)):
				if i == 0:												#si l'on s'apprete a envoyer un sous element
					yield str(len(pack)).encode()+b"d"					#cette balise signe le debut et nous renvoi a la fin du packet
				else:													#dans le cas ou l'on est en plein milieu de l'objet
					yield str(len(pack)).encode()+b"m"					#balise qui signe le milieu
				yield pack
			yield b"f"
			for i, pack in enumerate(generator_file(path, buff, remove=False, entete="")):
				if i == 0:												#si l'on s'apprete a envoyer un sous element
					yield str(len(pack)).encode()+b"d"					#cette balise signe le debut et nous renvoi a la fin du packet
				else:													#dans le cas ou l'on est en plein milieu de l'objet
					yield str(len(pack)).encode()+b"m"					#balise qui signe le milieu
				yield pack
			yield b"f"														#on marque la fin du packet (pour plus de vitesse a la deserialisation)

	def is_file(obj, copy_file):
		"""
		retourne True si l'objet est un chemin vers un fichier
		et qu'il faut copier les fichiers
		"""
		if not copy_file:												#si l'utilisateur ne nous autorise pas d'interpreter l'objet comme un fichier
			return False												#alors on ne fait meme pas la suite du test
		if type(obj) == str:											#deja il faut que l'objet soit une chaine de caractere
			if len(obj) < 32767:										#et qu'il ne soit pas trop gros, sinon windaube plante
				return os.path.isfile(obj)								#alors on fait le test
		return False													#si ces conditions ne sont pas verifies, alors ce n'est pas un chemin vers un fichier

	def is_jsonisable(obj, copy_file):
		"""
		retourne True si l'objet peu etre serialise avec json
		retourne False le cas echeant
		"""
		if type(obj) in (int, float, bool, type(None)):					#si l'objet est vraiment basique
			return True													#alors json sait le serialiser
		elif type(obj) == str:											#dans le cas ou c'est une chaine de caractere
			if not is_file(obj, copy_file):
				return True
		elif type(obj) == list:											#dans le cas ou l'objet est une liste
			for element in obj:											#on a pas d'autre choix que de parcourir la liste
				if not is_jsonisable(element, copy_file):				#si l'un des elements n'est pas compatible avec json
					return False										#alors la liste n'est pas jsonisable
			return True													#par contre, si tout est ok, allors on le jsonisifi
		elif type(obj) == dict:											#de meme, dans le cas ou l'objet est un dictionnaire
			for key, value in obj.items():								#pour faire la verification, on s'y prend comme pour les listes
				if not is_jsonisable(value, copy_file):					#si l'un des elements du dictionnaire fait tout capoter
					return False										#on ne va pas plus loin
				elif not is_jsonisable(key, copy_file):					#meme si c'est moin probable, mais si la clef n'est pas satisfesante
					return False										#tant pis, ça fait tout arreter quand meme
			return True													#si tout semble ok, et bien on dit qu'il est jsonalisable
		return False													#dans tous les autres cas, json ne fait pas bien le boulot

	#entete: </>message protocol</>
	try:																#pour un affichage plus parlant
		message = "serialization of "+obj.__name__+"..."				#on tente de recuperer le nom de l'objet
	except:																#sinon
		message = "serialization of "+str(obj)+"..."					#on affiche un message pas tres explicite
	with raisin.Printer(message, signature=signature) as p:
		if type(obj) == int:											#si l'objet est un entier
			if abs(obj) < 10**2000:										#si l'entier n'est pas bien gros
				p.show("small int->bytes")								#alors on va prendre des racourcis
				entete = "</>0000</>"									#precision de l'id et du protocol
				return generator_data(cipher_data((entete+str(obj)).encode(), psw, signature), buff)#on l'envoi vite fait bien fait
			else:														#si l'entier est gros
				p.show("large int->bytes")								#on le dit a l'utilisateur
				entete = "</>0199</>"									#on met le bon texte mais avec le protocol pickle
				data = entete.encode()+pickle.dumps(obj)				#serialisation directe avec pickle
				return cipher_generator(generator_data(compress_data(data, compresslevel, signature), buff), psw, signature)#on retourne ces donnes la

		elif is_file(obj, copy_file):									#si l'objet est un nom de fichier
			if compresslevel != 0:										#dans le cas ou une compression est requiere
				raise NotImplementedError()
			else:														#sinon, si on ne demande pas specialement de compresser
				p.show("file->bytes")									#on y va directement
				entete = "</>1310</>"									#comme d'habitude on met l'entete
				suite_entete = str(len(obj.encode("utf-8")))+"-"+obj	#sauf que la on y ajoute le nom du fichier
				return cipher_generator(generator_file(obj, buff, remove=False, entete=entete+suite_entete), psw, signature)#puis on lit directement le fichier pour l'envoyer

		elif type(obj) == str:											#maintenant, si c'est une chaine de caractere que l'on serialise
			if len(obj) < 100:											#si la chaine est rikiki
				p.show("small str->json->bytes")						#on va sauter des etapes
				entete = "</>0201</>"									#precision du protocol et du message
				return generator_data(cipher_data((entete+json.dumps(obj)).encode("utf-8"), psw, signature), buff)#on le serialise avec json pour aller plus vite
			elif len(obj) < buff:										#on essay d'optimiser et la ram, et la compression ainsi:
				p.show("medium str->json->bytes")						#si la chaine est suffisement petite pour rester en RAM
				entete = "</>0301</>"									#on garde le meme protocol, mais on ajoute une compression eventuelle
				return cipher_generator(compress_generator(generator_data((entete+json.dumps(obj)).encode("utf-8"), buff), compresslevel, signature), psw, signature)
			else:														#bon, si il est suffisement gros pour etre compresse
				p.show("large str->json->file")							#si la chaine est grosse, on passe par un fichier
				entete = "</>0402</>"									#entete propre a json
				filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".json")#generation du nom du fichier temporaire
				with open(filename, "w") as f:							#creation phisique du fichier
					f.write(entete)										#on y ecrit l'entete
					json.dump(obj, f)									#puis la chaine de caractere
				return generator_file(cipher_file(compress_file(filename, compresslevel, signature), psw, signature), buff)#on fait les operations de bases

		elif type(obj) == float:										#si c'est un flotant
			p.show("float->bytes...")									#on trace
			entete = "</>0503</>"										#avec un protocol specifique du coup
			return generator_data(cipher_data(entete.encode()+str(obj).encode(), psw, signature), buff)#on le passe juste en str

		elif type(obj) == bytes:										#si l'objet est deja serialiser
			if len(obj) < 100:											#mais que c'est suffisement petit pour ne pas subir de compression
				p.show("small bytes->bytes")							#on va sauter des etapes
				entete = "</>0604</>"									#precision du protocol et du message
				return generator_data(cipher_data(entete.encode()+obj, psw, signature), buff)#on l'encripte juste si nessecaire
			elif len(obj) < buff:										#on essay d'optimiser et la ram, et la compression ainsi:
				p.show("medium bytes->bytes")							#si la chaine est suffisement petite pour rester en RAM
				entete = "</>0704</>"									#on garde le meme protocol, mais on ajoute une compression eventuelle
				return cipher_generator(compress_generator(generator_data(entete.encode()+obj, buff), compresslevel, signature), psw, signature)
			else:														#bon, si il est suffisement gros pour etre compresse
				p.show("large bytes->file")								#si la chaine est grosse, on passe par un fichier
				entete = "</>0804</>"									#entete propre a cette serialisation
				filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".json")#generation du nom du fichier temporaire
				with open(filename, "wb") as f:							#creation phisique du fichier
					f.write(entete.encode())							#on y ecrit l'entete
					f.write(obj)										#puis la sequence de bytes
				return generator_file(cipher_file(compress_file(filename, compresslevel, signature), psw, signature), buff)#on fait les operations de bases

		elif type(obj) == io.TextIOWrapper:								#si il s'agit d'un fichier binaire en lecture
			filename = os.path.abspath(obj.name)						#on recupere son nom et son emplacement sur la machine
			mode = obj.mode												#son mode ("r", "w", "a", ...)
			encoding = obj.encoding										#le format dans lequel il est encode
			closed = obj.closed											#True si l'objet est ferme
			if not closed:												#si le fichier n'est pas ferme
				stream_position = obj.tell()							#position du pointeur
				if compresslevel != 0:									#dans le cas ou le fichier doit etre un minimum compresse
					raise NotImplementedError()
				else:													#dans le cas ou la compression n'est pas exigee
					p.show("io.TextIOWrapper->file")					#on dit ce que l'on fait
					entete = "</>0905</>"+mode+"</>"+encoding+"</>"+str(stream_position)+"</>"#on met les infos dans l'entete
					return cipher_generator(generator_file(filename, buff, remove=False, entete=entete), psw, signature)#on renvoi alors le fichier
			raise NotImplementedError()

		elif (type(obj) == io.BufferedReader) or (type(obj) == io.BufferedWriter):#si il s'agit d'un fichier binaire
			filename = os.path.abspath(obj.name)						#on recupere son nom et son emplacement sur la machine
			mode = obj.mode												#son mode ("rb", "wb", "ab", ...)
			closed = obj.closed											#True si l'objet est ferme
			if not closed:												#si le fichier n'est pas ferme
				stream_position = obj.tell()							#position du pointeur
				if compresslevel != 0:									#dans le cas ou le fichier doit etre un minimum compresse
					raise NotImplementedError()
				else:													#dans le cas ou la compression n'est pas exigee
					p.show("io.BufferedReader->file")
					entete = "</>1007</>"+mode+"</>"+str(stream_position)+"</>"#on met les infos dans l'entete
					return cipher_generator(generator_file(filename, buff, remove=False, entete=entete), psw, signature)#on renvoi alors le fichier
			raise NotImplementedError()

		elif type(obj) == list:											#si l'objet est une liste, alors on met en place un systeme de balise
			p.show("list->bytes")										#ainsi, l'entete est incluse dedans
			return cipher_generator(compress_generator(generator_to_generator(b"", serialize_list(obj, signature, copy_file, buff), buff), compresslevel, signature), psw, signature)#on la retourne recursivement taux d'erreur de 1/1000000 pour 100 Go de data
		
		elif type(obj) == tuple:										#si l'objet est un tuple
			p.show("tuple->list")										#on le transforme en liste
			entete = "</>1209</>"										#permet de dire que l'on passe par une liste
			return cipher_generator(compress_generator(generator_to_generator(entete.encode(), serialize_bis(list(obj), signature, buff, compresslevel=0, copy_file=copy_file, psw=None), buff), compresslevel, signature), psw, signature)

		elif type(obj) == dict:											#si l'objet est un dictionaire
			p.show("dict->bytes")
			return cipher_generator(compress_generator(generator_to_generator(b"", serialize_dict(obj, signature, copy_file, buff), buff), compresslevel, signature), psw, signature)

		elif inspect.ismodule(obj):										#si l'objet est un module
			modulename = obj.__name__									#c'est le nom du module
			standard_list = [
				"abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore", "atexit", "audioop",
				"base64", "bdb", "binascii", "binhex", "bisect", "builtins", "bz2",
				"calendar", "cgi", "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys", "compileall", "concurrent", "configparser", "contextlib", "copy", "copyreg", "cProfile", "csv", "ctypes",
				"datetime", "dbm", "decimal", "difflib", "dis", "distutils", "doctest", "dummy_threading",
				"email", "encodings", "enum", "errno",
				"faulthandler", "filecmp", "fileinput", "fnmatch", "formatter", "fractions", "ftplib", "functools",
				"gc", "getopt", "getpass", "gettext", "glob", "gzip",
				"hashlib", "heapq", "hmac", "html", "http",
				"imaplib", "imghdr", "imp", "importlib", "inspect", "io", "ipaddress", "itertools",
				"json",
				"keyword",
				"lib2to3", "linecache", "locale", "logging", "lzma",
				"macpath", "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder", "multiprocessing",
				"netrc", "nntplib", "numbers",
				"operator", "optparse", "os",
				"parser", "pathlib", "pdb", "pickle", "pickletools", "pkgutil", "platform", "plistlib", "poplib", "pprint", "profile", "pstats", "py_compile", "pyclbr", "pydoc",
				"queue", "quopri",
				"random", "re", "reprlib", "rlcompleter", "runpy",
				"sched", "select", "selectors", "shelve", "shlex", "shutil", "signal", "site", "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "sqlite3", "ssl", "stat", "statistics", "string", "stringprep", "struct", "subprocess", "sunau", "symbol", "symtable", "sys", "sysconfig",
				"tabnanny", "tarfile", "telnetlib", "tempfile", "test", "textwrap", "threading", "time", "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc", "turtle", "types", "typing",
				"unicodedata", "unittest", "urllib", "uu", "uuid",
				"venv",
				"warnings", "wave", "weakref", "webbrowser", "wsgiref",
				"xdrlib", "xml", "xmlrpc",
				"zipapp", "zipfile", "zipimport", "zlib"]
			if modulename in standard_list:								#si le module a serialise est standard et donc present sur toutes les machines
				p.show("standard_module->bytes")						#bien evidement, on dit ce que l'on fait
				entete = "</>1411</>"									#puis on met en place la bonne entete
				return generator_data(cipher_data(entete.encode()+modulename.encode("utf-8"), psw, signature), buff)#et l'on retourne directement le nom du module

			p.show("module->bytes")
			with raisin.Printer("search dependences of "+modulename+"..."):
				installed_modules = get_installed_modules()				#c'est le dictionaire qui recence tous les modules installes
				dependences_ok = set()									#l'ensemble de tous les modules dependant deja cherches
				dependences_to_do = {modulename}						#les modules dons on doit encore chercher les dependances
				while dependences_to_do:								#tant que la recherche n'est pas finie
					m = dependences_to_do.pop()							#recuperation d'un module a traiter
					if (m in installed_modules) and not(m in standard_list):#si ce module existe bien
						dependences_ok.add(m)							#alors on le traite une seule fois puis on n'y revient plus
						p.show(m)										#pour faire pascienter, on dit de quelle dependance il s'agit 
						dependences_to_do = dependences_to_do | get_module_dependence(m, installed_modules) - dependences_ok#puis on fait de recherches sur cette derniere
			return cipher_generator(compress_generator(generator_to_generator(b"", serialize_module(modulename, signature, installed_modules[modulename], dependences_ok, buff), buff), compresslevel, signature), psw, signature)

		elif inspect.isclass(obj):										#si l'objet est une classe, qu'elle soit integree ou creee dans du code python
			p.show("class->bytes")
			return cipher_generator(compress_generator(generator_to_generator(b"", serialize_class(obj, signature, buff), buff), compresslevel, signature), psw, signature)

		elif inspect.isfunction(obj):									#si l'objet est une fonction python, qui inclut des fonctions creees par une expression lambda
			p.show("function->bytes")									#on va les serialiser comme on peut
			return cipher_generator(compress_generator(generator_to_generator(b"", serialize_function(obj, signature, buff), buff), compresslevel, signature), psw, signature)

		elif inspect.isgeneratorfunction(obj):							#si l'objet est une fonction generatrice python
			p.show("generatorfunction->bytes")
			raise NotImplementedError()

		elif inspect.isgenerator(obj):									#si l'objet est un generateur
			p.show("generator->bytes")
			raise NotImplementedError()

		elif inspect.iscoroutinefunction(obj):							#si l'objet est une fonction coroutine (une fonction definie avec une syntaxe async def)
			p.show("coroutinefunction->bytes")
			raise NotImplementedError()

		elif inspect.iscoroutine(obj):									#si l'objet est une coroutine creee par une fonction async def
			p.show("coroutine->bytes")
			raise NotImplementedError()

		elif inspect.isawaitable(obj):									#si l'objet peut etre utilise dans une expression await
			p.show("awaitable->bytes")
			raise NotImplementedError()

		elif inspect.istraceback(obj):									#si l'objet est une traceback
			p.show("traceback->bytes")
			raise NotImplementedError()

		elif inspect.isframe(obj):										#si l'objet est un cadre
			p.show("frame->bytes")
			raise NotImplementedError()

		elif inspect.iscode(obj):										#si l'objet est un code
			p.show("code->bytes")
			raise NotImplementedError()

		elif inspect.isbuiltin(obj):									#si l'objet est une fonction integree ou une methode integree liee
			p.show("builtin->bytes")
			raise NotImplementedError()

		elif inspect.isroutine(obj):									#si l'objet est une fonction ou une methode définie par l'utilisateur ou integree
			p.show("routine->bytes")
			raise NotImplementedError()

		elif inspect.isabstract(obj):									#si l'objet est une classe de base abstraite
			p.show("absstract->bytes")
			raise NotImplementedError()

		elif inspect.ismethoddescriptor(obj):							#si l'objet est un descripteur de methode, mais pas si ismethod() , isclass() , isfunction() ou isbuiltin() sont vrais
			p.show("methoddescriptor->bytes")
			raise NotImplementedError()

		elif inspect.isdatadescriptor(obj):								#si l'objet est un descripteur de donnees
			p.show("datadescriptor->bytes")
			raise NotImplementedError()

		elif inspect.isgetsetdescriptor(obj):							#si l'objet est un descripteur de getset
			p.show("getsetdescriptor->bytes")
			raise NotImplementedError()

		elif inspect.ismemberdescriptor(obj):							#si l'objet est un descripteur de membre
			p.show("memberdescriptor->bytes")
			raise NotImplementedError()

		else:															#dans le cas ou l'objet est inconnu
			if sys.getsizeof(obj) > buff:								#si l'objet est tres lourd en memoire
				p.show("large unknown object->pickle->file")			#on va passer par un fichier
				entete = "</>9898</>"									#mais avant, on specifi le protocole
				filename = os.path.join(raisin.temprep, str(uuid.uuid4())+".pkl")#que l'on met par precaution dans un repertoir temporaire
				with open(filename, "wb") as f:							#afin d'eviter toute surcharge dans la memoire
					f.write(entete.encode())							#on y ecrit l'entete
					pickle.dump(obj, f)									#on utilise pickle, qui serialise pas mal de choses
				return generator_file(cipher_file(compress_file(filename, compresslevel, signature), psw, signature), buff)#le reste, c'est des formalitees
			else:														#si le fichier est suffisement petit pour pouvoir tout faire dans la RAM
				p.show("little unknown object->pickle->bytes")			#l'utilisateur est averti de l'opperation iminente
				entete = "</>9999</>"									#ajout de l'entete
				data = entete.encode()+pickle.dumps(obj)				#serialisation directe avec pickle
				return generator_data(cipher_data(compress_data(data, compresslevel, signature), psw, signature), buff)#on retourne ces donnes la

class Uniformizer:
	"""
	uniformise des lignes de code
	"""
	def __init__(self, code):
		"""
		'code' est une liste de lignes de codes
		"""
		self.code = code
		self.end_line = False											#devient True des que les retours chariots inutils sont supprimes
		self.indentation = False										#devient True des que les indentations sont normalisees
		self.factultative = False										#devient True des que toutes les ligne facultatives sont enlevees

	def del_end_line(self, start=0):
		"""
		supprime les retours a la ligne inutiles
		'start' est le rang a partir du quel on annalise
		"""
		while not self.end_line:										#si l'operation est deja faite
			parentheses = 0												#nombre de parentheses ouvertes
			crochets = 0												#nombre de crochets ouverts
			accolades = 0												#nombre d'accolades ouvertes
			guillemets = [0, 0, 0, 0]									#c'est touts les tipe de guillemets [''', ', """, "]
			self.end_line = True
			for rang_ligne in range(start, len(self.code)):				#pour chaque ligne
				for rang_car, caractere in enumerate(self.code[rang_ligne]):#pour chacun des caracteres de la ligne
					if (parentheses+crochets+accolades+sum(guillemets) == 0) and (caractere == "#"):#si on entre sur un comentaire
						break											#on passe a la ligne suivante
					if sum(guillemets) == 0:							#si l'on est pas dans une chaine de caractere ou un commentaire
						parentheses += {"(":1, ")":-1}.get(caractere, 0)#on incremente ou decremente le nombre de parentheses
						crochets += {"[":1, "]":-1}.get(caractere, 0)	#selon qu'on va plus en profondeur ou qu'on en sort
						accolades += {"{":1, "}":-1}.get(caractere, 0)	#ce procede est valide pour les trois
					for i in range(4):									#on s'attarde maintenant aux 4 types de guillemets
						if sum((g for j,g in enumerate(guillemets) if j != i)) == 0:#si il n'y a pas d'autres guillemets
							if self.code[rang_ligne][rang_car:rang_car+3-2*(i%2)] == ["'''", "'", '"""', '"'][i]:#et que ce type de guillemet est present
								guillemets[i] = 1-guillemets[i]			#alors on change ca valeur
								break									#puis on sort imediatement de la boucle avant d'introduire une erreur
				if parentheses+crochets+accolades != 0:					#si on est en plein dans une ligne de def
					if self.code[rang_ligne][-2] == "\\":				#et que l'avant dernier caractere impose un saut de ligne
						self.code[rang_ligne] = self.code[rang_ligne][:-2]#on en enleve la bonne quantite
					else:												#dans le cas ou ce caractere n'est pas explicite
						self.code[rang_ligne] = self.code[rang_ligne][:-1]#on supprime juste le retour a la ligne mais pas plus
					self.code = self.code[:rang_ligne]+[self.code[rang_ligne]+self.code[rang_ligne+1]]+self.code[rang_ligne+2:]#on joint alors ces 2 lignes
					start=rang_ligne									#on reanalise recursivement ce nouveau code
					self.end_line = False
					break												#on recomence l'analyse du code
				if guillemets[1] or guillemets[3]:						#si on est en plein dans un guillemet simple
					self.code = self.code[:rang_ligne]+[self.code[rang_ligne][:-2]+self.code[rang_ligne+1]]+self.code[rang_ligne+2:]#alors on enleve le saut de ligne
					start=rang_ligne									#puis on relance une analyse
					self.end_line = False
					break												#on recomence l'analyse du code
				if guillemets[0] or guillemets[2]:						#si il y a des guillememets triples
					if self.code[rang_ligne][-2] == "\\":				#et que l'avant dernier caractere impose un saut de ligne
						self.code[rang_ligne] = self.code[rang_ligne][:-2]#on en enleve la bonne quantite
					else:												#dans le cas ou ce caractere n'est pas explicite
						self.code[rang_ligne] = self.code[rang_ligne][:-1]+"\\n"#on supprime juste le retour a la ligne mais pas plus
					self.code = self.code[:rang_ligne]+[self.code[rang_ligne]+self.code[rang_ligne+1]]+self.code[rang_ligne+2:]#on joint alors ces 2 lignes
					start=rang_ligne									#on reanalise recursivement ce nouveau code
					self.end_line = False
					break												#on recomence l'analyse du code					
		return self.code												#si on en arrive la, c'est que le traitement est termine

	def del_indentation(self):
		"""
		retire le maximum d'indentations au code
		remplace toutes les indentation restantes par des tabulations
		"""
		if not self.indentation:										#si l'on ne s'en est pas deja occupe
			#preparation
			self.del_end_line()											#on commence d'abord par supprimer les retours a la ligne qui vont nous enbeter
			graph = {}													#c'est le dictionaire qui a chaque numero de ligne va associer les indentations
			for i, text in enumerate(self.code):						#on parcours donc chaque ligne du code
				indentation = ""										#c'est la partie inimprimable (indentation) de la ligne en cours d'analyse
				for caractere in text:									#on regarde chaque caractere de la ligne
					if caractere in " \t":								#si le caractere est un espace ou une tabulation
						indentation += caractere						#alors il fait partie de l'indentation
					elif caractere in ("#", "\n"):						#si c'est un commentaire ou un retour a la ligne
						break											#alors on ignore cette ligne
					else:												#dans le cas ou c'est une ligne de commande normale
						graph[i] = indentation							#alors on y memorise l'indentation
						self.code[i] = self.code[i][len(indentation):]	#puis on l'enleve de suite pour mieu l'ajouter apres
						break											#puis on ne va pas lire le reste de la ligne
			#analyse
			while not "" in (indentation for i, indentation in graph.items()):#tant que l'on est pas tout a gauche
				graph = {i:indentation[1:] for i, indentation in graph.items()}#on se decale legerement
			clefs = [i for i in graph]									#la liste de clefs
			i_ref = [i for i in graph if graph[i] == ""][0]				#c'est la ou il n'y a pas d'indentations
			rang_ref = clefs.index(i_ref)								#c'est l'endroit de depart
			graph[i_ref] = []											#on va metre les tabulations dans une liste a plusieurs elements
			for rang in range(rang_ref+1, len(clefs)):					#pour chaque clef
				precedent = graph[clefs[rang-1]]						#les indentations de la ligne du dessus (list) e: [" ", "\t", "    "]
				courant = graph[clefs[rang]]							#l'indentation de la ligne en cours de traitement (str)
				graph[clefs[rang]] = []									#on va peu a peu completer dans une liste les frontiere des indentation de la ligne en cours de traitement
				for e in precedent:										#on va regarder chaque element de la ligne du dessus
					if len(courant) >= len(e):							#et le comparer a la ligne juste en dessous
						if courant[:len(e)] == e:						#si l'element se retrouve a la ligne en dessous
							graph[clefs[rang]].append(e)				#alors on le prend en compte
							courant = courant[len(e):]					#et on va voir la suite
						else:											#si ce n'est pas le cas
							raise SyntaxError("bug in the indentations")#et bien normalement c'est toujours le cas
					else:												#si l'element est plus petit
						if courant != "":								#si c'est pas une chaine vide
							raise SyntaxError("bug in the indentations")#et bien c'est pas cence arriver
						break											#bref si on est arrive au bout de la comparaison, on s'arrette ici
				if courant != "":										#si la ligne courante est plus grande que la precedente
					graph[clefs[rang]].append(courant)					#alors on a evolue d'une indentation

			#remplacement
			graph = {i:"\t"*len(l_ind) for i,l_ind in graph.items()}	#on remplace les listes par des tabulations
			self.code = [graph.get(i, "")+text for i, text in enumerate(self.code)]#que l'on injecte dans le code de depart
			for i in range(i_ref):										#pour chaque ligne qui se trouve avant la ligne de reference
				del self.code[0]										#et bien on la supprime
		self.indentation = True
		return self.code

	def del_facultative(self):
		"""
		supprime toutes les lignes facultatives
		c'est a dire les ligne vides et touts les commentaires
		"""
		if not self.factultative:
			self.del_end_line()											#tout d'abord, on ommets touts les retourne a la ligne inutiles

			#suppression des commentaire suivant un "#"
			parentheses = 0												#nombre de parentheses ouvertes
			crochets = 0												#nombre de crochets ouverts
			accolades = 0												#nombre d'accolades ouvertes
			guillemets = [0, 0, 0, 0]									#c'est touts les tipe de guillemets [''', ', """, "]
			for rang_ligne in range(len(self.code)):					#pour chaque ligne
				for rang_car, caractere in enumerate(self.code[rang_ligne]):#pour chacun des caracteres de la ligne
					if (parentheses+crochets+accolades+sum(guillemets) == 0) and (caractere == "#"):#si on entre sur un commentaire
						self.code[rang_ligne] = self.code[rang_ligne][:rang_car]+"\n"
						break											#on passe a la ligne suivante
					if sum(guillemets) == 0:							#si l'on est pas dans une chaine de caractere ou un commentaire
						parentheses += {"(":1, ")":-1}.get(caractere, 0)#on incremente ou decremente le nombre de parentheses
						crochets += {"(":1, ")":-1}.get(caractere, 0)	#selon qu'on va plus en profondeur ou qu'on en sort
						accolades += {"{":1, "}":-1}.get(caractere, 0)	#ce procede est valide pour les trois
					for i in range(4):									#on s'attarde maintenant aux 4 types de guillemets
						if sum((g for j,g in enumerate(guillemets) if j != i)) == 0:#si il n'y a pas d'autres guillemets
							if self.code[rang_ligne][rang_car:rang_car+3-2*(i%2)] == ["'''", "'", '"""', '"'][i]:#et que ce type de guillemet est present
								guillemets[i] = 1-guillemets[i]			#alors on change ca valeur
								break									#puis on sort imediatement de la boucle avant d'introduire une erreur

			#suppression de ligne en entieres
			a_supprimer = []											#liste qui comporte le rang de chaque ligne de code qui doit etre supprimee
			for i, ligne in enumerate(self.code):						#pour chaque ligne de code
				for j, c in enumerate(ligne):							#pour chaque caractere de la ligne
					if c in " \t":										#si il s'agit d'un espace
						continue										#on va voir le caractere suivant
					elif c in ("'", '"', "\n"):							#si cette ligne est inutile
						a_supprimer.append(i)							#alors elle va etre exterminee
						break											#puis on passe de suite voir la ligne suivante
					else:												#si cette ligne est potentiellement utile
						break											#on la laise tranquille pour le moment
			self.code = [l for i,l in enumerate(self.code) if not i in a_supprimer]#on abat toutes les ligne en trop

		self.factultative = True										#on fois l'opperation terminnee, on se prepare a ne plus la refaire
		return self.code

	def normalize(self):
		"""
		retourne le code completement normalize
		"""
		self.del_facultative()											#on enleve alors les ligne factultatives
		self.del_indentation()											#puis on met des indentations standards
		return self.code

class Code_Analyser:
	"""
	cet objet permet d'analiser des lignes de code
	"""
	class Function_text:
		"""
		permet de reperer les definitions de fonctions dans
		une chaine de caractere qui represente une ligne complete de code
		"""
		def __init__(self, code_line:str):
			self.code_analyser = Code_Analyser()
			self.group_var_re = self.code_analyser.group_var_re			#format regex d'une variable
			self.code_line = code_line									#une ligne complete du code source
			self.regex = re.compile(r"^\s*def\s+"+self.group_var_re+r"\s*(?P<parametres>\(.*\))\s*:")#format regex pour valider que le code represente bien une definition de fonction
			self.is_ok = None											#booleen qui vaut True si il s'agit bien d'une definition de fonction ou False le cas echeant
			self.decompose_ok = False									#booleen prenant l'etat True lorsque la methode decompose a etet appelle

		def __bool__(self):
			"""
			renvoi True si 'self.code_line' est bien une ligne de definition de fonction
			"""
			if self.is_ok == None:										#si l'analyse n'a pas ete faite
				self.res_group = self.regex.search(self.code_line)
				if self.res_group:										#si c'est bon c'est ok
					self.is_ok = True
				else:
					self.is_ok = False
			return self.is_ok

		def decompose(self):
			"""
			renvoi un dictionaire contenant:
				'name' : le nom de la fonction (STR)
				'var_positional' : le parametre avec * puis sa classe [LIST] or None
				'var_keyword' : le parametre avec ** puis sa classe [LIST] or None
				'vars_default' : les parametres avec = (LIST), chaque element contient le nom, la valeur et le type
				'vars_normal' : les parametres de base sans infos (LIST), chaque elements contient le nom et le type
			"""
			if not self:												#si de base on pedale a cote du velo
				raise SyntaxError(self.code_line+" does not define a function defining")#on ne va pas plus loin
			if not self.decompose_ok:									#si on n'a pas fait l'effort de decomposer cette ligne
				self.dico = {}											#initialisation du dictionaire
				self.dico["name"] = self.res_group.group("variable")	#recuperation du nom de la fonction
				parametres = self.res_group.group("parametres")			#paquet qui constitu les parametres
				print("parametres:",parametres)
				for argument in self.code_analyser.generator_tuple_list_content_str(parametres):#pour chaque paquets
					print("argument brut:",argument)

				#input("suite")

			return self.dico

	def __init__(self):
		self.var_re = r"[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*"#modele d'une variable python
		self.group_var_re = r"(?P<variable>"+self.var_re+r")"

	def generator_tuple_list_content_str(self, chaine:str):
		"""
		cede chaque contenu d'un tuple ou d'une liste representee par une chaine de caractere.
		chaque paquet cede est la chaine comprise entre les virgule de separations
		la chaine doit etre encadree par () ou []
		"""
		content = re.compile(r"\((?P<content>.*)\)").search(chaine).group("content")
		chaine_inter = ""												#va peu a peu se charger
		while 1:														#fausse boucle infinie pour un faux recursif
			if content == "":											#si il ne reste plus rien
				if chaine_inter != "":									#on retourne les stock
					yield chaine_inter									#si on a du stock
				break													#car c'est un tuple ou une liste vide
			if content[0] == ",":										#si on en est a l'endroit de la separation
				yield chaine_inter										#on renvoi le stock
				chaine_inter = ""										#puis on le reinitialise de si-tot
				content = content[1:]									#puis on passe a la suite
				continue												#on recommence le test
			saut = self.jump(content)									#on saute le bloc qui ne nous interresse pas
			if saut == -1:												#sauf bien sur si on est a la fin
				yield chaine_inter+content								#au quel cas, on va droit au but
				break													#puis on sort de la
			chaine_inter+=content[:saut]								#mais on le memorise tous de meme
			content = content[saut:]									#c'est seulement ici que l'on saute veritablement le bloc

	def jump(self, chaine, start_rank=0):
		"""
		'chaine' est une ligne de code ou un bout de ligne de code (STR)
		'start_rank' est le rang a partir d'ou l'analise commence
		retourne le rang du dernier caractere qui fait parti du groupe
		en cas de paquet posiblement incomplet, retourne -1
		ex:
		>>>self.jump("les (orties sont belles) et verte", 4)
		24
		>>>chaine[4:24]
		'(orties sont belles et vertes)'
		>>>self.jump("les (orties sont belles) et verte", 5)
		23
		>>>chaine[5:23]
		'orties sont belles et vertes'
		"""
		parentheses = 0													#nombre de parentheses ouvertes
		crochets = 0													#nombre de crochets ouverts
		accolades = 0													#nombre d'accolades ouvertes
		guillemets = [0, 0, 0, 0]										#c'est touts les types de guillemets [''', ', """, "]

		#verif
		if start_rank < 0:
			raise ValueError("the start rank must to be >= 0")
		if start_rank >= len(chaine):
			raise ValueError("the start rank must to be < len(chaine)")

		#cas (...), [...], {...}, "...", '...', """...""", '''...'''
		if chaine[start_rank] in ("'", '"', "(", "[", "{"):				#dans le cas ou l'on est sur le debut d'un paquet on ne peu plus clair
			ref_ouvrante = chaine[start_rank]
			if ref_ouvrante == "'":
				if chaine[start_rank:start_rank+3] == "'''":
					ref_ouvrante = "'''"
			elif ref_ouvrante =='"':
				if chaine[start_rank:start_rank+3] == '"""':
					ref_ouvrante = '"""'

			i_veritable = start_rank+len(ref_ouvrante)-1				#on se place bien pour le debut de l'analyse
			while i_veritable+1 < len(chaine):							#on va analyser chaque caractere
				i_veritable += 1										#c'est le rang a partir du tout debut de la chaine
				if (ref_ouvrante in ("'", '"', "'''", '"""')) and (chaine[i_veritable:i_veritable+len(ref_ouvrante)] != ref_ouvrante):#si on est pas au bout
					continue
				elif (ref_ouvrante in ("'", '"', "'''", '"""')) and (chaine[i_veritable:i_veritable+len(ref_ouvrante)] == ref_ouvrante) and (chaine[i_veritable-1] != "\\"):
					return i_veritable+len(ref_ouvrante)
				elif (ref_ouvrante in ("(", "[", "{")) and (chaine[i_veritable] in "([{'\""):#si on rentre dans un autre bloc
					i_veritable = self.jump(chaine, i_veritable)-1
					continue
				elif (ref_ouvrante in ("(", "[", "{")) and (chaine[i_veritable] == {"(":")", "[":"]", "{":"}"}.get(ref_ouvrante, "")):
					return i_veritable+1
			return -1

		#cas de caractere inimprimable, si on est
		if chaine[start_rank] in " \t\n\r\f\v":							#si ca semble bien parti
			for i_veritable in range(start_rank+1, len(chaine)):		#pour tous les caractere suivants
				if not(chaine[i_veritable] in " \t\n\r\f\v"):			#si le caractere en cours n'est pas un espace
					return i_veritable									#alors le dernier en etait un
			return -1													#si il y a que des espaces, on ne peu pas dire avoir trouver la fin de la chaine

		#cas d'un mot clef ou d'un nom de variable
		if re.match(r"[a-zA-Z_\x7f-\xff]", chaine[start_rank]):			#si ca semble bien parti pour une variable
			for i_veritable in range(start_rank+1, len(chaine)):		#on va regarder les caracteres suivants
				if re.match(r"[a-zA-Z0-9_\x7f-\xff]", chaine[i_veritable]):#si on est encore dans la variable
					continue											#et bien on avance
				return i_veritable										#si le caractere n'est plus un caractere de variable, on s'en arrete la
			return -1

		#cas + - * / % // += -= *= /= //= %= @ == != > < >= <= ** | . :
		if re.match(r"[\+\-\*/%=!%@\|<>.:]", chaine[start_rank]):		#si il s'agit d'un symbol
			for i_veritable in range(start_rank+1, len(chaine)):		#on va regarder les caracteres suivants
				if re.match(r"[\+\-\*/%=!%@\|<>.:]", chaine[i_veritable]):#si on est encore dans la variable
					continue											#et bien on avance
				return i_veritable										#si le caractere n'est plus un caractere de variable, on s'en arrete la
			return -1

		#cas des nombres
		if re.match(r"^[\.][0-9]+", chaine[start_rank:]) or re.match(r"[0-9]", chaine[start_rank]):#si il s'agit d'un nombre
			i_veritable = re.match(r"^[0-9]*[\.]?[0-9]*[eE]*[\+\-]*[0-9]*", chaine[start_rank:]).end()#on l'extrait
			return i_veritable											#puis on le retourne aussi-tot





		raise Exception("the position of depature is not correct")









		







