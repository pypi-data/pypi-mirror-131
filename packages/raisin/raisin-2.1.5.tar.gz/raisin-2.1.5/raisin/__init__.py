#!/usr/bin/env python3
#-*- coding: utf-8 -*-

__version__ = "2.1.5.3"
__author__ = "Robin RICHARD <serveurpython.oz@gmail.com>"

import os
from raisin import geometry
from raisin import raisin
from raisin import install
from raisin import servers
import tempfile

def compress(obj, compresslevel=3, psw=None, copy_file=True, signature=None):
	"""
	serialise l'objet
	retourne une chaine de caractere
	"""
	f = {**{i:str(i) for i in range(10)}, **{i+10:chr(i+97) for i in range(26)}, **{i+36:chr(i+65) for i in range(26)}, **{62:"@", 63:"_"}}
	g_dico = {}
	def g(tree_bytes):
		"""
		permet de convertir 3 octets en 4 caracteres
		"""
		if tree_bytes in g_dico:
			return g_dico[tree_bytes]
		x,y,z = tuple((tree_bytes+b"00")[:3])
		s = 65536*x+256*y+z
		d = f[s%64]
		s //= 64
		c = f[s%64]
		s //= 64
		b = f[s%64]
		a = f[s//64]
		g_dico[tree_bytes] = a+b+c+d
		return g_dico[tree_bytes]

	data = dumps(obj, compresslevel=compresslevel, psw=psw, copy_file=copy_file, signature=signature)
	return "".join([g(data[i:i+3]) for i in range(0, len(data), 3)])+"."*((3-(len(data)%3))%3)

def copy(obj, signature=None):
	"""
	fait une copie vrai de l'objet en recursif
	retourne la copie de l'objet
	"""
	with raisin.Printer("copy...", signature=signature):
		return raisin.deserialize(raisin.serialize(obj, generator=True, compresslevel=0, signature=signature), signature=signature)

def decompress(chaine, psw=None, signature=None):
	"""
	deserialise 'data' en STR
	retourne l'objet deserialise
	"""
	f = {**{str(i):i for i in range(10)}, **{chr(i+97):i+10 for i in range(26)}, **{chr(i+65):i+36 for i in range(26)}, **{"@":62, "_":63}}
	g_dico = {}
	def g(four_str):
		"""
		converti 4 str en 3 bytes
		"""
		if four_str in g_dico:
			return g_dico[four_str]
		a,b,c,d = four_str
		s = 262144*f[a]+4096*f[b]+64*f[c]+f[d]
		z = s%256
		s //= 256
		y = s%256
		x = s//256
		g_dico[four_str] = bytes([x,y,z])
		return g_dico[four_str]

	data = b''.join([g(chaine[i:i+4]) for i in range(0, 4*(len(chaine)//4), 4)])[:3*(len(chaine)//4)-(len(chaine)%4)]
	return loads(data, psw, signature)

def deserialize(data, signature=None, psw=None):
	"""
	retourne l'objet natif
	"""
	return raisin.deserialize_bis(data, signature=signature, psw=psw)

def dump(obj, file, compresslevel=3, psw=None, copy_file=True, signature=None):
	"""
	fonctione comme pickle.dump
	'file' doit avoir un atribut "write binary"
	"""
	for data in raisin.serialize(obj, psw=psw, compresslevel=compresslevel, generator=True, copy_file=copy_file, signature=signature):#pour chaques paquets
		file.write(data)					#on inscrit ce bout de donnee dans le fichier passe en parametre
	file.write(b"<end_pack>")				#on inscrit un separateur afin de separer les differents objets serialises
	return None

def dumps(obj, compresslevel=1, psw=None, copy_file=True, signature=None):
	"""
	fonctionne comme pickle.dumps
	"""
	return raisin.serialize(obj, psw=psw, compresslevel=compresslevel, generator=False, copy_file=copy_file, signature=signature)

def load(file, psw=None, signature=None, rep=None):
	"""
	fonctionne comme pickle.load
	'file' doit avoir un atribut "read binary"
	"""
	def generator(file):
		"""
		genere des paquets de bytes jusqu'a rencontrer "<end_pack>"
		place le curseur au bon endroit pour la prochaine fois
		"""
		buff = 1024*1024
		while 1:							#tant que le separateur n'est pas rencontre
			position = file.tell()			#recuperation de la valeur du curseur
			data = file.read(buff)			#on lit le paquet suivant
			if (not b"<end_pack>" in data) and (data != b""):#tant que le separateur de fin n'est pas present
				yield data[:-9]				#on retourne le packet lu pour aller voir la suite
				file.seek(-9, 1)			#retour de 9 en arriere par rapport a la position actuelle
			elif buff >= 11:
				file.seek(position)
				buff = min(max(10, buff//2-10), len(data))
			else:
				break

	return raisin.deserialize(generator(file), psw=psw, signature=signature, rep=rep)

def loads(data, psw=None, signature=None):
	"""
	fonctionne comme pickle.loads
	"""
	return raisin.deserialize(data, psw=psw, signature=signature)

def map(target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, in_order=True, force=False):
	"""
	applique a 'target', les parametre '*args'
	retourne une liste
	"""
	session_raisin = raisin.Session()			#on initialise l'objet session afin qu'il soit unique
	return session_raisin.map(target, *args, timeout=timeout, job_timeout=job_timeout, local=local, in_order=in_order, force=force)#on utilise la methode map de session

def Map(target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, force=False):
	"""
	retourne un objet qui a pour methode get() et get_all()
	"""
	session_raisin = raisin.Session()			#on initialise l'objet session afin qu'il soit unique
	return session_raisin.map_object(target, *args, timeout=timeout, job_timeout=job_timeout, local=local, force=force)#on utilise la methode map de session

def open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
	"""
	extension de la methode '<built-in function open>'
	"""
	return raisin.open_extend(file, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, closefd=closefd, opener=opener)

def process(target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, force=False):
	"""
	execute la fonction 'target' et retourne le resultat
	"""
	session_raisin = raisin.Session()			#on initialise l'objet session afin qu'il soit unique
	return session_raisin.process_object(target, *args, timeout=timeout, job_timeout=job_timeout, local=local, force=force).get()#on retourne l'objet

def Process(target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, force=False):
	"""
	retourne un objet qui a pour methode get() et get_all() pour recuperer le resultat
	'target' est un pointeur vers une methode ou une fonction
	'timeout' est le temps maximum acceptable en seconde avant avant de retourner une erreur (temps total)
	'job_timeout' est le temps maximum acceptable pour l'execution du job (temps de l'execution seulement sans l'attente)
	'local' permet de forcer une execution locale sans passer par les serveurs
	"""
	session_raisin = raisin.Session()			#on initialise l'objet session afin qu'il soit unique
	return session_raisin.process_object(target, *args, timeout=timeout, job_timeout=job_timeout, local=local, force=force)#on retourne l'objet

def serialize(obj, signature=None, buff=1024*1024, compresslevel=0, copy_file=True, psw=None):
	"""
	cede des paquets de bytes de taille environ egale a buff
	"""
	return raisin.serialize_bis(obj, signature=signature, buff=buff, compresslevel=compresslevel, copy_file=copy_file, psw=psw)

def scan(target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, force=False):
	"""
	fait un balayage de 'target' par les iterables '*args'
	retourne une liste de liste de liste de ... de liste
	on accede au resultat de la facon suivante:
		resultat = scan(...)[arg0][arg1][arg2]
	"""
	return Scan(target, *args, timeout=timeout, job_timeout=job_timeout, local=local, force=force).get(wait=True)

def Scan(target, *args, timeout=3600*24*31, job_timeout=3600*48, local=False, force=False):
	"""
	retourne un objet Scan qui a pour methode get et get_all
	"""
	session_raisin = raisin.Session()			#on initialise l'objet session afin qu'il soit unique
	return session_raisin.scanner_object(target, *args, timeout=timeout, job_timeout=job_timeout, local=local, force=force)#on retourne l'objet

Lock = raisin.Lock								#import du verrou
Printer = raisin.Printer						#import de l'affichage
Timeout = raisin.Timeout						#import de l'objet timeout
Variable = raisin.Global_var					#est une variable visible a travers les differents processus

id = raisin.get_id()							#identifiant propre a cet ordinateur
rep = os.path.join(os.path.dirname(__file__), "data")#le repertoire par defaut
temprep = tempfile.mkdtemp()					#le repertoire dans lequel on fait les etapes intermediaires
garbage_collector = raisin.Garbage_collector(temprep)#suppression de ce repertoire a la fin
