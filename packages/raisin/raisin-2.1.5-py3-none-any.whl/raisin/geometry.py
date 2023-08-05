#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#https://docs.python.org/fr/3.7/library/operator.html
#https://docs.python.org/fr/3/reference/datamodel.html

"""
ax = plt.axes(projection='3d')
ax.plot_trisurf(x, y, z, cmap='cubehelix', edgecolor='none')
avec x, liste, y liste z=f(x,y)
"""

import logging
try:
	import matplotlib.pyplot as plt
	from mpl_toolkits.mplot3d import Axes3D
	import numpy
except ImportError:
	logging.warning("'matplotlib' failed to import. It will be impossible to show a graphic representation.")
import copy
import raisin
import sympy
from sympy.core.function import count_ops

#objets geometriques

class Function:
	"""
	est une fonction allant de R**n dans R**k
	"""
	def __init__(self, *args, id=None):
		"""
		on defini ici les 'sous fonctions de la fonction principale'
		en effet, self est de la forme:
			f : (x1,x2,...,xn) -> (f1(x1,x2,...,xn), ..., fk(x1,x2,...,xn))
		on a donc *args = f1, ..., fk
		"""
		self.coords = []			#initialisation des coordonnees avec une liste vide
		self.__init__render(*args)	#que l'on remplit aussitot
		self.point = Point(*self.coords)#on cree un point proche de cette fonction pour eviter des redondances
		self.expr_free_symbols = set(self.get_expr_free_symbols())#toutes les variables
		self.free_symbols = set(self.get_free_symbols())#seulement les variables visible, excluant les variables muettes
		self.id = id				#si il ne vaut pas None, c'est ce qu'affichera cet objet

	def __init__render(self, *args, first=True):
		"""
		converti l'argument ou l'ensemble d'argument en tuple de coordonnees reelles
		"""
		if len(args) == 0:								#si le point n'est pas defini
			if first:
				raise Exception("the function is not definied")#on releve un erreur
			return None
		if (len(args) == 1) and first:					#si il n'y a qu'un seul argument
			try:										#on va essayer de l'iterer
				if type(args[0]) == str:				#sauf si c'est une chaine de caractere
					raise TypeError						#car il ne faut surtout pas la decompose en caractere elementaire
				for e in iter(args[0]):					#ainsi, pour chaque parametre
					self.__init__render(e, first=False)	#on lui reapplique une verification
				return None
			except TypeError:							#si ce n'est pas un iterable
				if type(args[0]) == complex:			#dans le cas ou c'est un complexe natif
					self.coords.append(sympy.sympify(args[0].real))#on met la partie reelle sur x
					self.coords.append(sympy.sympify(args[0].imag))#et la partie imaginaire sur y
					return None
				self.coords.append(sympy.sympify(args[0]))#on n'y touche pas
				return None

		for el in args:									#si il y a plusieur arguments, on les regardes un a un
			try:										#on va essayer de l'iterer
				if type(el) == str:						#sauf si c'est une chaine de caractere
					raise TypeError						#car il ne faut surtout pas la decomposer en caractere elementaire
				for e in iter(el):						#ainsi, pour chaque parametre
					self.__init__render(e, first=False)	#on lui reapplique une verification
			except TypeError:							#si ce n'est pas un iterable
				self.coords.append(sympy.sympify(el))	#alors on considere directement que c'est un reel

	def __abs__(self):
		"""
		retourne une fonction ou chaque argument est sous une valeur absolue. (appelle par 'abs(self)')
		"""
		return Function(*(abs(e) for e in self))

	def __add__(self, function):
		"""
		retourne une fonction ou chaque coordonnee vaut l'ancienne plus la somme des coordonnees de self.
		c'est a dire f(...)+g(...) = (f1(...)+g1(...), ..., fn(...)+gn(...)). (appelle par 'self + function')
		garde les variables de self. par exemple f(x,y)+g(a,b) donne (f1(x,y)+g1(x,y), ...)
		"""
		f = function(*self.expr_free_symbols())
		if type(f) != list:
			f = [f]
		return Function(*(e1+e2 for e1, e2 in zip(self, f)))

	def __bool__(self):
		"""
		retourne True si la fonction est non nulle. (appelle par 'if objet:')
		"""
		return bool(self.point)

	def __call__(self, *args, **kargs):
		"""
		evalue la fonction aux points donnes
		retourne une liste de coordonnees si la fonction va de R**k dans R**n avec n>1
		ou bien retourne la valeur seule si la fonction va de R**k dans R tout cours
		"""
		parametres = self.free_symbols
		
		if kargs and (not args):			#si le dictionnaire est non vide
			ncoords = [c for c in self]		#copie des coordonnees
			for var, values in kargs.items():#on parcours toutes celles qui doivent changer
				f = Function(values).coords	#les parametre peuvent etre des fonctions de R**n dans R ou des expressions
				if len(f) != 1:				#si c'est une fonction de R**n dans R**k avec k>1
					raise Exception("Dimension error. The parameter "+str(var)+" must to be replace by an expression or a function of R**n to R. "+str(f)+" have return in R**"+str(len(f))+".")#alors on releve une exception
				ncoords = [c.replace(sympy.sympify(var), f[0]) for c in ncoords]#sinon, on remplace cette variable dans toutes les coordonees
			if len(ncoords) == 1:			#si il n'y a qu'une seule coordonnee
				return ncoords[0]			#on la retourne telle quelle
			return ncoords					#sinon, c'est la liste des coordonnees qui est retournee
		
		elif args and (not kargs):			#si il y a des arguments
			if len(args) == 1:				#enfin, si il n'y en a qu'un seul
				arg = args[0]				#on en simplifie l'acces
				if type(arg) == Function:	#si cet argument est une fonction
					if len(parametres) != len(arg):#on verifie que les dimensions pour la loi rond soient correctes
						raise Exception("Dimension error. "+str(self)+" takes "+str(len(parametres))+". So, only "+str(arg)+" gives only "+str(len(arg))+" values.")#si ce n'est pas le cas, une exception est relevee
					return Function(*(c.xreplace({var:exp for var,exp in zip(parametres, arg)}) for c in self))#on retourne donc la composee de fonction
				if type(arg) == str:		#si l'argument est une chaine de caractere
					arg = sympy.sympify(arg)#on lui enleve son iterabilite
				try:
					args = tuple(arg)		#dans le cas ou l'argument unique est finalement un iterable, on explicite chaque argument
				except TypeError:
					args = (arg,)
			if len(args) == len(parametres):#si il y a autant d'arguments que de variables
				return self.__call__(**{str(par):arg for par,arg in zip(parametres, args)})#alors on associe un argument a chaque variables
			else:							#si il y a encore un probleme de dimension
				raise Exception("This function takes "+str(len(parametres))+" parameters: "+str(parametres)+". But "+str(len(args))+" were given.")
		
		elif len(parametres) == 0:			#si on ne donne ni argument ni parametre, mais que la fonction est une constante
			if len(self) == 1:
				return self.coords[0]
			return self.coords

		raise Exception("The __call__ methode can not take a mixing of args and kargs.")

	def __delitem__(self, index):
		"""
		supprimme la coordonee d'index 'index'. (appelle par 'del objet[index]')
		"""
		c = self.coords.pop(index)
		if len(self.coords) == 0:
			raise Exception("the point can not be empted")#on releve une erreur
		self.point = Point(*self.coords)
		self.expr_free_symbols = set(self.get_expr_free_symbols())
		self.free_symbols = set(self.get_free_symbols())
		return c

	def __eq__(self, other):
		"""
		retourne True si self et le 'other' sont egaux.
		retourne False si l'une des coordonnees au moins differe.
		retourne un systeme d'equation si des variables sont en jeux. (appelle par '==')
		"""
		return self.equals(other)

	def __getitem__(self, index):
		"""
		recupere et retourne la coordonnee de rang 'index'. (appelle par 'objet[index]')
		"""
		return self.coords[index]

	def __hash__(self):
		"""
		retourne le hash entier de cet objet
		afin qu'un point soit un hashable. (appelle par 'hash(objet)')
		"""
		return hash(self.coords)

	def __iter__(self):
		"""
		genere chacune des coordonnees de sortie. (appelle par 'for coordonnees in self:')
		"""
		for c in self.coords:
			yield c

	def __len__(self):
		"""
		retourne le nombre de coordonnee que renvoie cette fonction,
		c'est a dire le k de R**n dans R**k. (appelle par 'len(self)')
		"""
		return len(self.coords)

	def __mul__(self, factor):
		"""
		retourne la fonction ou chaque coordonnee est multipliee par 'factor'. (appelle par 'objet*factor')
		"""
		return Function(*(e*factor for e in self))

	def __neg__(self):
		"""
		retourne la fonction dons chaque coordonnee sont
		l'oppose des coordonnees de self. (appelle par '-objet')
		"""
		return Function(*(-e for e in self))

	def __pos__(self):
		"""
		retourne la valeur positive de cette fonction, c'est a dire elle meme. (appelle par '+objet')
		"""
		return self

	def __truediv__(self, divisor):
		"""
		retourne le point ou chaque coordonnee se retrouve divisee par 'divisor'. (appelle par 'objet/divisor')
		"""
		return Function(*(e/divisor for e in self))

	def __repr__(self):
		"""
		permet un affichage graphique un peu meilleur
		"""
		if self.id:
			return str(self.id)
		symbols = self.get_free_symbols()
		if len(self) == 1:
			if len(symbols) == 1:
				return "Function:"+str(symbols[0])+"->"+str(self.coords[0])
			elif len(symbols) == 0:
				return "Function constant: "+str(self.coords[0])
			return "Function:"+str(tuple(symbols))+"->"+str(self.coords[0])
		if len(symbols) == 1:
			if len(self) == 1:
				return "Function:"+str(symbols[0])+"->"+str(self.coords[0])
			return "Function:"+str(symbols[0])+"->"+str(tuple(self.coords))
		return "Function constant: "+str(tuple(self.coords))

	def __rmul__(self, factor):
		"""
		retourne la fonction ou chaque coordonnee se retourve multipliee par 'factor'. (appelle par 'factor*objet')
		"""
		return Function(*(factor*e for e in self))

	def __setitem__(self, index, coord):
		"""
		permet de remplacer la coordonnee de rang 'index' par la valeur 'coord'. (appelle par 'objet[index] = coord')
		"""
		coords = copy.copy(self.coords)		#on fait une copie vraie des coordonnees courantes
		coords[index] = coord				#on modifit cette copie afin de mieux gerer les exceptions
		self.coords = []					#et les slices
		self.__init__render(coords)			#mais c'est effectivement un peu plus lourd
		self.point = Point(*self.coords)
		self.expr_free_symbols = set(self.get_expr_free_symbols())
		self.free_symbols = set(self.get_free_symbols())

	def __sub__(self, function):
		"""
		retourne une fonction ou chaque coordonnee vaut l'ancienne moins la somme des coordonnees de self.
		c'est a dire f(...)+g(...) = (f1(...)-g1(...), ..., fn(...)-gn(...)). (appelle par 'self - function')
		garde les variables de self. par exemple f(x,y)-g(a,b) donne (f1(x,y)-g1(x,y), ...)
		"""
		f = function(*self.expr_free_symbols())
		if type(f) != list:
			f = [f]
		return Function(*(e1-e2 for e1, e2 in zip(self, f)))

	def are_associative(law):
		"""
		retourne True si toutes les fonctions sont associatives dans un cas general
		"""
		return Point.are_associative(law)

	def are_commutative(law):
		"""
		retourne True si toutes les fonctions sont commutatives avec la loi 'law'
		"""
		return Point.are_commutative(law)

	def are_distributive(law1, law2):
		"""
		returne True si pour toutes les fonctions, la loi 'law1' est distributive par rapport a la loi 'law2'
		"""
		return Point.are_distributive(law1, law2)

	def atoms(self, *types):
		"""
		retourne l'union de tout les ensembles
		generes par cette methode applique a chacune des coordonnees
		"""
		ensemble = set()
		for e in self:
			ensemble = ensemble | e.atoms(*types)
		return ensemble

	def copy(self):
		"""
		retourne une copie vrai de self
		"""
		try:
			return Function(*(e.copy() for e in self))
		except:
			return Function(*(raisin.copy(e) for e in self))

	def diff(*symbols, **assumptions):
		"""
		retourne la fonction derivee
		"""
		raise NotImplementedError

	def dim(self):
		"""
		retourne la dimension de la fonction, c'est a dire la dimension
		de l'espace dans lequel un affichage graphique de la fonction ait du sens
		"""
		return len(self)+len(self.free_symbols)
	
	def doit(self):
		"""
		applique la methode doit a chacune des coordonnees
		retourne la nouvelle coordonnees doite
		"""
		return Function(*(e.doit() for e in self))

	def equals(self, other):
		"""
		retourne True si self et la fonction sont egales.
		retourne False si l'une des coordonnees au moins differe.
		retourne un systeme d'equation si des variables sont en jeux. (appelle par '==')
		"""
		raise NotImplementedError

	def _eval_simplify(self, ratio=1.7, measure=count_ops, rational=False, inverse=False):
		"""
		methode appelle par sympy.simplify
		"""
		return Function(*(sympy.simplify(e, ratio, measure, rational, inverse) for e in self))

	def evalf(n=15, subs=None, maxn=1000, chap=False, strict=False, quad=None, verbose=False):
		"""
		retourne le point ou cette fonction est appliquee a chacune des coordonnees
		"""
		return Function(*(e.evalf(n=n, subs=subs, maxn=maxn, chap=chap, strict=strict, quad=quad, verbose=verbose) for e in self))

	def get_expr_free_symbols(self):
		"""
		retourne la liste de tous les parametres, symbol, que ce soit des lettres, des mots ou des chiffres...
		la liste est triee par ordre alphabetique
		"""
		symbols = []
		for e in self:
			symbols.extend(list(e.expr_free_symbols))
		symbols = {str(s):s for s in set(symbols)}
		return [symbols[t] for t in sorted([c for c in symbols])]

	def get_free_symbols(self):
		"""
		retourne la liste de tous les parametres non muets, c'est a dire les variables
		la liste est triee par ordre alphabetique
		"""
		return self.point.get_free_symbols()

	def is_associative(self, law):
		"""
		retourne True si cette fonction est associative
		"""
		self.point.is_associative(law)

	def is_commutative(self, law):
		"""
		retourne True si cette fonction est commutative
		"""
		self.point.is_commutative(law)

	def is_distributive(self, law1, law2):
		"""
		retourne True si cette fonction est distributive
		"""
		return self.point.is_distributive(law1, law2)
	
	def is_number(self):
		"""
		retourne True si il n'y a pas de symbols ou de truc bizzare
		en gros, retourne True si chaque coordonnees peut etre vu comme un flottant
		"""
		return self.point.is_number()

	def limit(x, xlim, dir="+"):
		"""
		applique cette methode a toutes le coordonnees
		retourne une nouvelle instance de l'objet
		"""
		return Function(*(c.limit(x, xlim, dir) for c in self))

	def n(*args, **kargs):
		"""
		applique la methode evalf
		"""
		return self.evalf(*args, **kargs)

	def plot(self, ax, label=None, color=None, border={}, dim=None):
		"""
		prepare l'affichage graphique de cette fonction
		'ax' est l'objet matplotlib qui permet de tout plotter au meme endroit
		'label' est la legende de cette fonction
		'color' est le code rgb de la forme '#ffee00'
		'border' est le dictionnaire qui a chaque variables associe au minimum la valeur minimum, maximum du parametre,
		et accessoirement le nombre de point qu'il doit balayer.
		"""
		border = {str(v):info for v,info in border.items()}
		if len(self.free_symbols) == 0:		#si il n'y a qu'une seule valeur et aucune variable, que la fonction est constante
			xmin, xmax = -10, 10
			ymin, ymax = -10, 10
			if border:
				for i, (var, info) in enumerate(border.items()):
					if (i == 0) and (var != "y"):
						xmin, xmax = info[0], info[1]
					elif (i == 1) and (var != "x"):
						ymin, ymax = info[0], info[1]
				if "x" in border:
					xmin, xmax = border["x"][0], border["x"][1]
				if "y" in border:
					ymin, ymax = border["y"][0], border["y"][1]
			if self.dim() == 1:				#si f: -> cst
				value = self[0].evalf()
				if (dim == None) or (dim == 2):
					ax.plot([xmin, xmax], [value, value], label=label, color=color)
				elif dim == 3:
					X = [[numpy.float(xmin), numpy.float(xmax)],[numpy.float(xmin), numpy.float(xmax)]]
					Y = [[numpy.float(ymin), numpy.float(ymin)],[numpy.float(ymax), numpy.float(ymax)]]
					Z = [[numpy.float(value), numpy.float(value)],[numpy.float(value), numpy.float(value)]]
					surf = ax.plot_surface(numpy.array(X), numpy.array(Y), numpy.array(Z), label=label, color=color)
					surf._facecolors2d=surf._facecolors3d
					surf._edgecolors2d=surf._edgecolors3d
				else:
					raise LookupError("'dim' can only takes None, 2 or 3, no "+str(dim))
			elif self.dim() == 2:			#si f: -> cst1, cst2
				if dim == 2:
					ax.scatter(self[0].evalf(), self[1].evalf(), label=label, color=color)
				elif (dim == None) or (dim == 3):
					ax.plot([xmin, xmax], [self[0].evalf()]*2, [self[1].evalf()]*2, label=label, color=color)
				else:
					raise LookupError("'dim' can only takes None, 2 or 3, no "+str(dim))
			elif self.dim() == 3:			#si f: -> cst1, cst2, cst3
				if (dim == None) or (dim == 3):
					ax.scatter(self[0].evalf(), self[1].evalf(), self[2].evalf(), label=label, color=color)
				else:
					raise LookupError("on a 3d function, I can only plot in 3d")

		elif len(self.free_symbols) == 1:	#si il y a une seule variable
			if self.dim() == 2:				#si f: x->f(x)
				if (dim == None) or (dim == 2):
					Point(list(self.free_symbols)[0], self[0]).plot(ax, label=label, color=color, border=border, dim=2)
				elif dim == 3:
					if "y" != str(list(self.free_symbols)[0]):
						Point(list(self.free_symbols)[0], "y", self[0]).plot(ax, label=label, color=color, border=border, dim=3)
					else:
						Point(list(self.free_symbols)[0], "y'", self[0]).plot(ax, label=label, color=color, border=border, dim=3)
			elif self.dim() == 3:			#si f: x->f1(x), f2(x)
				Point(list(self.free_symbols)[0], self[0], self[1]).plot(ax, label=label, color=color, border=border, dim=3)
			else:
				raise LookupError("can only plot a 3d function in a 3d space")

		elif len(self.free_symbols) == 2:	#si f: x,y->f(x,y)
			if self.dim() == 3:
				Point(list(self.free_symbols)[0], list(self.free_symbols)[1], self[0]).plot(ax, label=label, color=color, border=border, dim=3)
			else:
				raise LookupError("can only plot a 3d function in a 3d space")

		else:								#si la fonction est en 4d ou plus
			raise LookupError("show only on dimension 1, 2 or 3, no "+str(self.dim()))

	def pprint(self):
		"""
		affiche joliment l'objet
		"""
		raise NotImplementedError

	def project(self, a, b):
		"""
		retourne la projection de self sur 'a' parallelement a 'b'
		"""
		raise NotImplementedError

	def replace(self, query, value, map=False, simultaneous=True, exact=False):
		"""
		retourne la nouvelle fonction ou chaque coordonnees subit cette methode
		"""
		return Function(*(e.replace(query, value, map, simultaneous, exact) for e in self))

	def round(p=0):
		"""
		retourne la fonction arrondi
		"""
		return Function(*(e.round(p) for e in self))

	def show(self, label="automatic", color=None, border={}, dim=None):
		"""
		affiche la fonction dans un graphique en 2d ou 3d
		'label' est la legende de cette fonction (par defaut le str de cet objet)
		'color' est le code rgb de la forme '#ffee00'
		'border' est le dictionnaire qui a chaque variable associe au minimum la valeur minimum, maximum du parametre,
		et le nombre de point qu'il doit balayer.
		"""
		if self.dim() > 3:					#si la fonction est en 4d ou plus
			raise LookupError("show only on dimension 1, 2 or 3, no "+str(self.dim()))
		if label == "automatic":
			label = self.__repr__()
		
		if len(self.free_symbols) == 0:		#si il n'y a aucun parametre d'entree
			if self.dim() == 1:				#si f: -> cst
				if (dim == None) or (dim == 2):#alors on l'affiche en 2d
					self.plot(plt, label, color, border, dim)
					plt.legend()
					plt.xlabel("x")
					plt.ylabel("f(x)")
					plt.show()
				elif dim == 3:				#sauf si la 3d nous est imposee
					fig = plt.figure()
					ax = fig.gca(projection='3d')
					self.plot(ax, label, color, border, dim)
					plt.legend()
					ax.set_xlabel("x")
					ax.set_ylabel("y")
					ax.set_zlabel("f(x,y)")
					plt.show()
				else:
					raise LookupError("'dim' can only takes None, 2 or 3, no "+str(dim))
			elif self.dim() == 2:			#si f: -> cst1, cst2
				if dim == 2:
					self.plot(plt, label, color, border, dim)
					plt.legend()
					plt.xlabel("f1(x)")
					plt.ylabel("f2(x)")
					plt.show()
				elif (dim == None) or (dim == 3):
					fig = plt.figure()
					ax = fig.gca(projection='3d')
					self.plot(ax, label, color, border, dim)
					plt.legend()
					ax.set_xlabel("x")
					ax.set_ylabel("f1(x)")
					ax.set_zlabel("f2(x)")
					plt.show()
				else:
					raise LookupError("'dim' can only takes None, 2 or 3, no "+str(dim))
			elif self.dim() == 3:			#si f: -> cst1, cst2, cst3
				if (dim == None) or (dim == 3):
					fig = plt.figure()
					ax = fig.gca(projection='3d')
					self.plot(ax, label, color, border, dim)
					plt.legend()
					ax.set_xlabel("f1(x)")
					ax.set_ylabel("f2(x)")
					ax.set_zlabel("f3(x)")
					plt.show()
				else:
					raise LookupError("on a 3d function, I can only plot in 3d")
		if len(self.free_symbols) == 1:		#si il y a un parametre en entree
			if self.dim() == 2:				#si f: x->f1(x)
				if (dim == None) or (dim == 2):
					self.plot(plt, label, color, border, dim)
					plt.legend()
					plt.xlabel(str(list(self.free_symbols)[0]))
					plt.ylabel("f("+str(list(self.free_symbols)[0])+")")
					plt.show()
				elif dim == 3:
					fig = plt.figure()
					ax = fig.gca(projection='3d')
					self.plot(ax, label, color, border, dim)
					plt.legend()
					if "y" != str(list(self.free_symbols)[0]):
						ax.set_xlabel(str(list(self.free_symbols)[0]))
						ax.set_ylabel("y")
						ax.set_zlabel("f("+str(list(self.free_symbols)[0])+",y)")
					else:
						ax.set_xlabel(str(list(self.free_symbols)[0]))
						ax.set_ylabel("y'")
						ax.set_zlabel("f("+str(list(self.free_symbols)[0])+",y')")
					plt.show()
				else:
					raise LookupError("'dim' can only takes None, 2 or 3, no "+str(dim))
			if self.dim() == 3:				#si f: x->f1(x), f2(x)
				if (dim == None) or (dim == 3):
					fig = plt.figure()
					ax = fig.gca(projection='3d')
					self.plot(ax, label, color, border, dim)
					plt.legend()
					ax.set_xlabel(str(list(self.free_symbols)[0]))
					ax.set_ylabel("f1("+str(list(self.free_symbols)[0])+")")
					ax.set_zlabel("f2("+str(list(self.free_symbols)[0])+")")
					plt.show()
				else:
					raise LookupError("can only plot a 3d function in a 3d space")
		if len(self.free_symbols) == 2:		#si f: x,y->f(x,y)
			if self.dim() == 3:
				fig = plt.figure()
				ax = fig.gca(projection='3d')
				self.plot(ax, label, color, border, dim)
				plt.legend()
				ax.set_xlabel(str(list(self.free_symbols)[0]))
				ax.set_ylabel(str(list(self.free_symbols)[1]))
				ax.set_zlabel("f("+str(list(self.free_symbols)[0])+", "+str(list(self.free_symbols)[1])+")")
				plt.show()
			else:
				raise LookupError("can only plot a 3d function in a 3d space")

	def subs(self, *args, **kwargs):
		"""
		retourne la nouvelle fonction ou la methode subs a ete applique a chaque coordonnees
		"""
		return Function(*(e.subs(*args, **kwargs) for e in self))

	def translate(self, vector):
		"""
		retourne la nouvelle fonction ayant subit une translation
		du vecteur 'vector'
		"""
		raise NotImplementedError

	def trigsimp(self, **args):
		"""
		applique cette fonction a chacune des coordonnees, retourne la fonction simplifiee
		"""
		return Function(*(e.trigsimp(**args) for e in self))

	def xreplace(self, rule):
		"""
		Replace occurrences of objects within the expression
		"""
		return Function(*(e.xreplace(rule) for e in self))

class Group:
	"""
	represente un groupe au sens algebre
	"""
	def __init__(self, *elements, law="+"):
		with raisin.Printer("group initialization..."):
			self.law = law						#c'est la loi du groupe (+, *, °, @, **, &, |)
			self.elements = elements
			self.__init__verification(*elements)#verification qu'il s'agit bien d'un groupe

	def __init__verification(self, *elements):
		"""
		verifie que les elements forment bien un groupe avec la loi 'self.loi'
		"""
		#verification des types
		for e in elements[1:]:					#on prend le premier element comme reference
			if type(elements[0]) != type(e):	#on compare cette reference a chaque autres entites
				raise TypeError("the elements must have the same type. "+str(type(elements[0]))+" and "+str(type(e))+" are different!")#si ils ne sont pas du meme type, on releve une exception

		#associatif
		if not is_associative(elements[0], self.law):
			raise Exception("the type "+str(type(elements[0]))+" is not associative with the law "+self.law)

		#neutre
		with raisin.Printer("is the neutral element in the group ?") as p:
			neutre = self.neutral()
			if type(neutre) != type(elements[0]):
				raise Exception("the group is not stable!")
			for e in elements[1:]:
				if not(self.operation(self.inverse(e), e) == self.operation(e, self.inverse(e)) == neutre):
					raise Exception("the neutral is not unique!")
			p.show("yes")

	def operation(self, a, b):
		"""
		returne 'a self.law b'
		"""
		if self.law == "+":
			return a + b
		if self.law == "*":
			return a * b
		if self.law == "°":
			return a(b)
		if self.law == "@":
			return a @ b
		if self.law == "&":
			return a & b
		if self.law == "|":
			return a | b
		raise TypeError("the law "+self.law+" is not registered")

	def inverse(self, a):
		"""
		retourne le symetrique tel que 'a law inverse(a) = neutre'
		"""
		if self.law == "+":
			try:
				return -a
			except:
				return a.inv("+")
		if self.law == "*":
			try:
				return a**-1
			except:
				try:
					return 1/a
				except:
					return a.inv("*")
		if self.law == "°":
			try:
				return a.bijection()
			except:
				return a.inv("°")
		if self.law == "@":
			return a.inv("@")
		if self.law == "&":
			return a.inv("&")
		if self.law == "|":
			return a.inv("|")
		raise TypeError("the law "+self.law+" is not registered")

	def neutral(self):
		"""
		retourne l'element neutre du groupe
		"""
		return self.operation(elements[0], inverse(elements[0]))

	def is_abelien(self):
		"""
		renvoi True si le groupe est abelien
		"""
		return self.is_commutative()

	def is_commutative(self):
		"""
		retourne True si le groupe est un groupe abelien
		"""
		with raisin.Printer("is it an abelian group ?") as p:
			for e in self.elements:
				if not is_commutative(e, self.law):
					p.show("no")
					return False
			p.show("yes")
			return True

class Vect:
	"""
	represente un espace vectoriel au sens algebre en dimension finie
	"""
	def __init__(self, *vectors):
		self.vectors = list(vectors)			#ensemble de tous les vecteurs qui engendrent cet espace vectoriel
		self.__init__verification(*vectors)

	def __init__verification(self, *vectors):
		"""
		verifie plusieurs choses:
			-que tous les vecteurs soient de meme type
			-qu'ils aient une loi "+" de composition interne
				-qui soit commutative
				-associative
				-admettent un element neutre
				-tout element admette un oppose
			-qu'ils aient une loi "*" avec un corps externe
				-distributive par rapport a "+"
					-a droite
					-a gauche
				-distibutive a droite par rapport a la loi "+" du corps K
				-l'element neutre multiplicatif du corps K, note '1', est neutre a gauche pour *
		"""
		#verification des types
		for v in vectors[1:]:					#on prend le premier vecteur comme reference
			if type(vectors[0]) != type(v):		#on compare cette reference a chaque autres vecteurs
				raise TypeError("the vectors must have the same type. "+str(type(vectors[0]))+" and "+str(type(v))+" are different!")#si ils ne sont pas du meme type, on releve une exception

		#exclusion des cas usuels
		if type(vectors[0]) in (Vector, Point): #si il s'agit d'un n-uplet:
			for v in vectors[1:]:				#on verifie qu'ils ont tous la meme taille
				if len(vectors[0]) != len(v):	#si l'un d'eux n'a pas la meme taille que les autres
					raise Exception("all the n-uplets must to have the same len.")#on releve une erreur


		raise NotImplementedError

class Point:
	"""
	Represente un point dans R**n, qui contient donc n coordonnees en geometrie cartesienne
	"""
	def __init__(self, *args, id=id):
		"""
		les 'args' peuvent etre:
			-plusieurs coordonnees reelles (INT, FLOAT ...)
			-un seul complexe (COMPLEX ...)
			-un seul vecteur au sens geometrique (Vector)
			-une seule matrice colonne
		"""
		self.coords = []			#initialisation des coordonnees avec une liste vide
		self.__init__render(*args)	#que l'on rempli aussi tot
		self.expr_free_symbols = set(self.get_expr_free_symbols())#toutes les variables
		self.free_symbols = set(self.get_free_symbols())#seulement les variables visibles, excluant les variables muettes
		self.id = id

	def __init__render(self, *args, first=True):
		"""
		converti l'argument ou l'ensemble d'argument en tuple de coordonnees reelles
		"""
		if len(args) == 0:								#si le point n'est pas defini
			if first:
				raise Exception("the point is not definied")#on releve un erreur
			return None
		if (len(args) == 1) and first:					#si il n'y a qu'un seul argument
			try:										#on va essayer de l'iterer
				if type(args[0]) == str:				#sauf si c'est une chaine de caractere
					raise TypeError						#car il ne faut surtout pas la decomposer en caractere elementaire
				for e in iter(args[0]):					#ainsi, pour chaque parametre
					self.__init__render(e, first=False)	#on lui reaplique une verification
				return None
			except TypeError:							#si ce n'est pas un iterable
				if type(args[0]) == complex:			#dans le cas ou c'est un complex natif
					self.coords.append(sympy.sympify(args[0].real))#on met la partie reelle sur x
					self.coords.append(sympy.sympify(args[0].imag))#et la partie imaginaire sur y
					return None
				self.coords.append(sympy.re(sympy.sympify(args[0])))#on n'y touche pas
				self.coords.append(sympy.im(sympy.sympify(args[0])))#enfin, on s'assure juste que ce soit bien des reels
				return None

		for el in args:									#si il y a plusieur arguments, on les regarde un a un
			try:										#on va essayer de l'iterer
				if type(el) == str:						#sauf si c'est une chaine de caractere
					raise TypeError						#car il ne faut surtout pas la decomposer en caractere elementaire
				for e in iter(el):						#ainsi, pour chaque parametre
					self.__init__render(e, first=False)	#on lui reaplique une verification
			except TypeError:							#si ce n'est pas un iterable
				self.coords.append(sympy.re(sympy.sympify(el)))#alors on considere directement que c'est un reel

	def __abs__(self):
		"""
		Returns the distance between this point and the origin. (appelle par 'abs(obj)')
		"""
		somme = 0
		for e in self:
			somme += e**2
		return sympy.sqrt(somme)

	def __add__(self, point):
		"""
		retourne le point qui a chaque coordonne, associe la somme des coordonnees de
		self et de 'point'. (appelle par 'objet + point')
		"""
		return Point(*(e1+e2 for e1,e2 in zip(self, point)))

	def __bool__(self):
		"""
		retourne True si le point est non nul. (appelle par 'if objet:')
		"""
		for e in self:
			if e:
				return False
		return True

	def __contains__(self, item):
		"""
		retourne la condition pour que 'item' soit contenu dans self. (appelle par 'item in objet')
		"""
		raise NotImplementedError

	def __delitem__(self, index):
		"""
		supprimme la coordonnee d'index 'index'. (appelle par 'del objet[index]')
		"""
		c = self.coords.pop(index)
		if len(self.coords) == 0:
			raise Exception("the point can not be empted")#on releve une erreur
		self.expr_free_symbols = set(self.get_expr_free_symbols())#toutes les variables
		self.free_symbols = set(self.get_free_symbols())
		return c

	def __eq__(self, other):
		"""
		retourne True si self et le point sont egaux.
		retourne False si l'une des coordonnees au moins differe.
		retourne un systeme d'equation si des variables sont en jeux. (appelle par '==')
		"""
		return self.equals(other)

	def __getitem__(self, index):
		"""
		recupere et retourne la coordonnee de rang 'index'. (appelle par 'objet[index]')
		"""
		return self.coords[index]

	def __hash__(self):
		"""
		retourne le hash entier de cet objet
		afin qu'un point soit un hashable. (appelle par 'hash(objet)')
		"""
		return hash(self.coords)

	def __len__(self):
		"""
		retourne le nombre de coordonnees qui constituent le point. (appelle par 'len(objet)')
		"""
		return len(self.coords)

	def __mul__(self, factor):
		"""
		retourne le point ou chaque coordonnee est multipliee par 'factor'. (appelle par 'objet*factor')
		"""
		return Point(*(e*factor for e in self))

	def __neg__(self):
		"""
		retourne le point dont chaque coordonnee est
		l'oppose des coordonnees de self. (appelle par '-objet')
		"""
		return Point(*(-e for e in self))

	def __pos__(self):
		"""
		retourne la valeur positive de ce point, c'est a dire lui meme. (appelle par '+objet')
		"""
		return self

	def __truediv__(self, divisor):
		"""
		retourne le point ou chaque coordonee se retrouve divisee par 'divisor'. (appelle par 'objet/divisor')
		"""
		return Point(*(e/divisor for e in self))

	def __repr__(self):
		"""
		permet un affichage graphique un peu mieux
		"""
		if self.id:
			return str(self.id)
		if 0 <= len(self) <= 3:						#si on est dans une dimension visualisable
			return "Point"+str(len(self))+"D("+", ".join(map(str, self))+")"#on colle a la representation de sympy
		return "Point("+", ".join(map(str, self))+")"#afin d'uniformiser les codes

	def __rmul__(self, factor):
		"""
		retourne le point ou chaque coordonnee se retrouve multipliee par 'factor'. (appelle par 'factor*objet')
		"""
		return Point(*(factor*e for e in self))

	def __setitem__(self, index, coord):
		"""
		permet de remplacer la coordonnee de rang 'index' par la valeur 'coord'. (appelle par 'objet[index] = coord')
		"""
		coords = copy.copy(self.coords)		#on fait une copie vraie des coordonnees courantes
		coords[index] = coord				#on modifit cette copie afin de mieux gerer les exceptions
		self.coords = []					#et les slices
		self.__init__render(coords)			#mais c'est effectivement un peu plus lourd
		self.expr_free_symbols = set(self.get_expr_free_symbols())
		self.free_symbols = set(self.get_free_symbols())

	def __sub__(self, point):
		"""
		retourne le point ou chaque coordonnee vaut les coordonnees
		de self, moins celles de point. (appelle par 'objet - point')
		"""
		return Point(*(e1-e2 for e1,e2 in zip(self, point)))

	def are_associative(law):
		"""
		retourne True si tous les points sont associatifs dans un cas general
		"""
		if law == "+":
			return True
		if law == "*":
			return True
		raise TypeError

	def are_commutative(law):
		"""
		retourne True si tous les points sont commutatifs avec la loi 'law'
		"""
		if law == "+":
			return True
		if law == "*":
			return True
		raise TypeError

	def are_distributive(law1, law2):
		"""
		retourne True si pour tous les points, la loi 'law1' est distributive par rapport a la loi 'law2'
		"""
		if (law1 == "*") and (law2 == "+"):
			return True
		raise TypeError

	def are_coplanar(*points):
		"""
		retourne une condition pour que tous les points
		soient cooplanaires
		"""
		points = [Point(point) for point in points]	#on s'assure que les objets soient bien des points
		if len(points) <= 3:						#si il y a trois points ou moins
			return True								#alors ils sont obligatoirement cooplanaires
		len_max = max(map(len, points))				#et que chacun de ces points
		points = [Point(list(point)+[0]*(len_max-len(point))) for point in points]#aient tout autant de coordonnees, on ajoute des 0 si nescessaire
		space = Vect([point-points[0] for point in points])#pour verifier qu'ils soient cooplanaire, on regarde si, en se fixant un point comme origine arbitraire
		return Equation(space.dim(), 2, "<=").solve()#tous les vecteurs n'engendrent pas un espace plus grand qu'un plan

	def are_collinear(*points):
		"""
		retourne une condition pour que tous les points
		soients collineaires
		"""
		points = [Point(point) for point in points]	#on s'assure que les objets soient bien des points
		if len(points) <= 2:						#si il y a trois points ou moins
			return True								#alors ils sont obligatoirement cooplanaires
		len_max = max(map(len, points))				#et que chacun de ces points
		points = [Point(list(point)+[0]*(len_max-len(point))) for point in points]#aient tout autant de coordonnees, on ajoute des 0 si nescessaire
		space = Vect([point-points[0] for point in points])#pour verifier qu'ils soient cooplanaire, on regarde si, en se fixant un point comme origine arbitraire
		return Equation(space.dim(), 1, "<=").solve()#tous les vecteurs n'engendrent pas un espace plus grand qu'un plan

	def are_concyclic(*points):
		"""
		retourne une condition pour qu'un meme cercle
		passe par tous les points
		"""
		raise NotImplementedError

	def atoms(self, *types):
		"""
		retourne l'union de tous les ensembles
		generes par cette methode appliquee a chacune des coordonnees
		"""
		ensemble = set()
		for e in self:
			ensemble = ensemble | e.atoms(*types)
		return ensemble

	def canberra_distance(self, point):
		"""
		The Canberra Distance from self to point p.
		Returns the weighted sum of horizontal and vertical distances to point 'point'.
		"""
		raise NotImplementedError

	def copy(self):
		"""
		retourne une copie vraie de self
		"""
		try:
			return Point(*(e.copy() for e in self))
		except:
			return Point(*(raisin.copy(e) for e in self))

	def diff(self, *symbols, **assumptions):
		"""
		retourne le point ou chaque coordonnee est derivee
		"""
		return Point(*(c.diff(*symbols, **assumptions) for c in self))

	def dim(self):
		"""
		retourne la dimension du point:
		si la dimension est 0, alors il s'agit d'un veritable point
		si la dimension est 1, alors le point forme une vraie une courbe, etc
		"""
		def dim_rec(symbols, dimension, excluded):
			"""
			'symbols' est une liste dont chaque element est la liste des parametres qui intervienent dans la coordonnee
			'dimension' est la dimension en plus de celle du point
			'excluded' est la liste qui a chaque coordonnee, prend la valeur False si elle na pas ete traitee, True sinon
			retourne la dimension de ce point
			"""
			if len(symbols) == 0:					#si il n'y a plus aucune coordonnee
				return dimension					#alors la dimension ne va pas augmenter
			for nbr in range(1+max((len(e) for e in symbols))):
				for i,l in enumerate(symbols):		#on parcourt la liste
					if len(l) == nbr:
						if l == []:					#si l'un des elements est une constante
							return dim_rec([s for j,s in enumerate(symbols) if j!=i], dimension, [e for j,e in enumerate(excluded) if j!=i])#alors on ignore totalement ce point
						if not excluded[i]:			#si ce point n'est pas deja traite
							return dim_rec([[v for v in li if v!=l[0]] for li in symbols], {True:dimension, False:dimension+1}[excluded[i]], [{True:True, False:b}[j==i] for j,b in enumerate(excluded)])
			return dimension						#si tous les points on ete traites, on s'arrete la

		return dim_rec([list(e.free_symbols) for e in self], 0, [False for i in range(len(self))])#on retourne la dimension de ce point

	def distance(self, point):
		"""
		The Euclidean distance from self to point p.
		return this distance
		"""
		return abs(self-point)

	def doit(self):
		"""
		applique la methode doit a chacune des coordonnees
		retourne le nouveau point ou la methode doit a ete appliquee
		"""
		return Point(*(e.doit() for e in self))

	def equals(self, other):
		"""
		retourne True si self et le point sont egaux.
		retourne False si l'une des coordonnees au moins differe.
		retourne un systeme d'equation si des variables sont en jeux. (appelle par '==')
		"""
		return System(self.__contains__(other), other.__contains__(self)).solve()#les 2 entitees sont egales si elles sont incluses l'une dans l'autre

	def _eval_simplify(self, ratio=1.7, measure=count_ops, rational=False, inverse=False):
		"""
		methode appelle par sympy.simplify
		"""
		return Point(*(sympy.simplify(e, ratio, measure, rational, inverse) for e in self))

	def evalf(n=15, subs=None, maxn=1000, chap=False, strict=False, quad=None, verbose=False):
		"""
		retourne le point ou cette fonction est appliquee a chacune des coorconnees
		"""
		return Point(*(e.evalf(n=n, subs=subs, maxn=maxn, chap=chap, strict=strict, quad=quad, verbose=verbose) for e in self))

	def get_expr_free_symbols(self):
		"""
		retourne la liste de tous les parametres, symbol, que ce soit des lettre, des mot ou des chiffres...
		la liste et triee par ordre alphabetique
		"""
		symbols = []
		for e in self:
			symbols.extend(list(e.expr_free_symbols))
		symbols = {str(s):s for s in set(symbols)}
		return [symbols[t] for t in sorted([c for c in symbols])]

	def get_free_symbols(self):
		"""
		retourne la liste de tous les parametres non muet, c'est a dire les variables
		la liste et triee par ordre alphabetique
		"""
		symbols = []
		for e in self:
			symbols.extend(list(e.free_symbols))
		symbols = {str(s):s for s in set(symbols)}
		return [symbols[t] for t in sorted([c for c in symbols])]

	def intersection(self, other):
		"""
		The intersection between this point and another GeometryEntity.
		"""
		raise NotImplementedError

	def is_collinear(self, *points):
		"""
		Returns `True` if there exists a line
		that contains `self` and `points`.  Returns `False` otherwise.
		A trivially True value is returned if no points are given.
		"""
		return Point.are_collinear(self, *points)

	def is_associative(self, law):
		"""
		retourne True si ce point est associatif
		"""
		with raisin.Printer("it is associative with the law "+law+"?") as p:
			for e in self:
				if not is_commutative(e, law):
					p.show("no")
					return False
			p.show("yes")
			return True

	def is_commutative(self, law):
		"""
		retourne True si ce point est commutatif
		"""
		with raisin.Printer("it is commutative with the law "+law+"?") as p:
			for e in self:
				if not is_commutative(e, law):
					p.show("no")
					return False
			p.show("yes")
			return True

	def is_distributive(self, law1, law2):
		"""
		retourne True si ce point est distributif
		"""
		with raisin.Printer("Is it distributive with the laws "+law1+" and "+law2+"?") as p:
			for e in self:
				if not is_distributive(e, law1, law2):
					p.show("no")
					return False
			p.show("yes")
			return True
	
	def is_concyclic(self, *points):
		"""
		Do `self` and the given sequence of points lie in a circle?
		Returns True if the set of points are concyclic and
		False otherwise. A trivial value of True is returned
		if there are fewer than 2 other points.
		"""
		return Point.are_concyclic(self, *points)

	def is_number(self):
		"""
		retourne True si il n'y a pas de symbole ou de trucs bizarres
		en gros, retourne True si chaque coordonnee peu etre vu comme un flotant
		"""
		for e in self:
			if not e.is_number():
				return False
		return True

	def limit(x, xlim, dir="+"):
		"""
		applique cette methode a toutes les coordonnees
		retourne une nouvelle instance de l'objet
		"""
		return Point(*(c.limit(x, xlim, dir) for c in self))

	def midpoint(self, point):
		"""
		retourne le point equidistant de self est de point
		"""
		return (self+point)/2

	def n(*args, **kargs):
		"""
		applique la methode evalf
		"""
		return self.evalf(*args, **kargs)

	def taxicab_distance(self, point):
		"""
		The Taxicab Distance from self to point 'point'.
		Returns the sum of the horizontal and vertical distances to point 'point'.
		"""
		distance = 0
		for e1, e2 in zip(self, point):
			distance += sympy.abs(e1-e2)
		return distance

	def plot(self, ax, label=None, color=None, border={}, dim=None):
		"""
		prepare l'affichage graphique de ce point
		'ax' est l'objet matplotlib qui permet de tout preparer a l'affichgage au meme endroit
		'label' est la legende de ce point
		'color' est le code rgb de la forme '#ffee00'
		'border' est le dictionnaire qui a chaque variable associe au minimum : la valeur minimum, maximum du parametre,
		'dim' est la dimenssion dans laquelle afficher le point
		et le nombre de point qu'il doit balayer.
		"""
		def evaluate(coord, border, symbols):
			"""
			retourne le 'tenseur' (liste de liste de liste n fois) avec n le nombre de parametres
			les parametres varient entre vmin et vmax.
			retourne environ 'nbr' de point en tout
			'order est l'ordre dans lequel les parametres on etes balayes
			'free_symbols' est la liste qui ressence tous les parametres dans l'ordre
			"""
			if len(symbols) == 0:					#si c'est une constante
				return float(coord.evalf())			#on la retourne en flotant
			border = {str(k):v for k,v in border.items()}#afin d'interpreter les chaines de caracteres
			symbol = symbols[0]						#c'est le parametre que l'on va iterer
			liste = border.get(str(symbol), [-10, 10, 100])#tentative de recuperation des informations
			if len(liste) == 3:						#mais comme il y a un parametre qui
				vmin, vmax, nbr = liste				#est succeptible de ne pas exister
			elif len(liste) == 2:					#on prend des precautions
				vmin, vmax = liste					#en faisant des test
				nbr = 101							#si jamais le test donne un resultat absurde
			else:									#on renvoie une erreur
				raise ValueError("the dictionary 'border' must associate 2 or three parametrers: (min, max and nbr)")#plutot que de la corriger pour en creer une plus indetectable
			vmin, vmax = sympy.sympify(vmin), sympy.sympify(vmax)#dont on permet des constantes comme pi...
			return [evaluate(coord.subs(symbol, (vmax-vmin)*i/(nbr-1)+vmin), border, symbols[1:]) for i in range(nbr)]

		if len(self) > 3:		#si il n'est pas possible d'en faire une representation graphique
			raise LookupError("plot only on dimenssion 1, 2 or 3, no "+str(len(self)))#on retourne une erreur
		
		if dim == None:
			pass
		elif dim == 2:
			if len(self) > 2:
				if self[2:] == [0]*(len(self)-2):
					return Point(self[0], self[1]).plot(ax, label, color, border, dim)
				else:
					raise LookupError("can't plot a "+str(len(self))+"d point in a 2d space")
			elif len(self) == 1:
				return Point(self[0], 0).plot(ax, label, color, border, dim)
		elif dim == 3:
			if len(self) == 1:
				return Point(self[0], 0, 0).plot(ax, label, color, border, dim)
			elif len(self) == 2:
				return Point(self[0], self[1], 0).plot(ax, label, color, border, dim)
		else:
			raise LookupError("'dim' can only takes None, 2 or 3, no "+str(dim))

		if self.dim() == 0:		#si il s'agit d'un point
			if len(self) == 1:	#mais qu'on est en dimension 1
				Point(self[0], 0).plot(ax, label, color)#alors on passe en dimension 2
			elif len(self) == 2:#si on est en dimension 2
				ax.scatter(float(self[0]), float(self[1]), label=label, color=color)#alors on affiche le point dans le plan
			else:				#si on est en dimension 3
				ax.scatter(float(self[0]), float(self[1]), float(self[2]), label=label, color=color)#alors on affiche le point dans l'espace
		elif self.dim() == 1:	#si il s'agit d'une courbe
			if len(self) == 1:	#mais qu'on est en dimenssion 1
				Point(self[0], 0).plot(ax, label, color)#on l'affiche en 2d
			elif len(self) == 2:#si on doit tracer en 2d
				X = evaluate(self[0], border, self.get_free_symbols())#on calcul X
				Y = evaluate(self[1], border, self.get_free_symbols())#de meme pour Y
				ax.plot(X, Y, label=label, color=color)#puis on trace
			else:				#si on est en 3d
				X = evaluate(self[0], border, self.get_free_symbols())#on calcule les x
				Y = evaluate(self[1], border, self.get_free_symbols())#puis les y
				Z = evaluate(self[2], border, self.get_free_symbols())#et enfin les z
				ax.plot(X, Y, Z, label=label, color=color)#puis on affiche tout ca
		elif self.dim() == 2:	#si il s'agit d'une surface
			if len(self) == 2:	#et qu'on est en dimension 2
				X = evaluate(self[0], border, self.get_free_symbols())#on calcul x sous forme de tableau
				Y = evaluate(self[1], border, self.get_free_symbols())#on calcul y sous forme de tableau
				for i in range(len(X)-1):#puis on parcourt chaque parametre
					for j in range(len(X[0])-1):#afin de tout balayer
						x = [X[i][j], X[i+1][j], X[i+1][j+1], X[i][j+1]]#on va tracer un polygone
						y = [Y[i][j], Y[i+1][j], Y[i+1][j+1], Y[i][j+1]]#dont on evalue le contour
						if i == j == 0:#si on en est a la premiere boucle
							ax.fill(x, y, label=label, color=color)#on en profite pour mettre la legende
						else:	#mais bon
							ax.fill(x, y, color=color)#on ne l'affiche qu'une seule fois
			else:				#si on est en dimension 3
				X = [[numpy.float(e) for e in liste] for liste in evaluate(self[0], border, self.get_free_symbols())]#on calcule x sous forme de tableau
				Y = [[numpy.float(e) for e in liste] for liste in evaluate(self[1], border, self.get_free_symbols())]#de meme pour y
				Z = [[numpy.float(e) for e in liste] for liste in evaluate(self[2], border, self.get_free_symbols())]#et pour z
				surf = ax.plot_surface(numpy.array(X), numpy.array(Y), numpy.array(Z), label=label, color=color)
				surf._facecolors2d=surf._facecolors3d
				surf._edgecolors2d=surf._edgecolors3d

		else:
			raise NotImplementedError

	def pprint(self):
		"""
		affiche joliment l'objet
		"""
		if len(self) == 0:
			print("point nul")
		elif len(self) == 1:
			print("point ", end="")
			sympy.pprint(self[0])
		else:
			print("point:")
			sympy.pprint(set([sympy.Eq(sympy.sympify({0:"x", 1:"y", 2:"z", 3:"t"}.get(i, "a"+str(i))),e) for i,e in enumerate(self)]))

	def project(self, a, b):
		"""
		retourne la projection de self sur 'a' parrallelement a 'b'
		"""
		raise NotImplementedError

	def replace(self, query, value, map=False, simultaneous=True, exact=False):
		"""
		retourne le nouveau point ou chaque coordonnee subit cette methode
		"""
		return Point(*(e.replace(query, value, map, simultaneous, exact) for e in self))

	def round(p=0):
		"""
		retourne le point arrondi
		"""
		return Point(*(e.round(p) for e in self))

	def scale(self, point, factor):
		"""
		retourne un point. ce nouveau point correspond a self ayant
		subit une homotecie de centre 'point' est de facteur 'factor'
		"""
		return factor*(self-point)+point

	def show(self, label="automatic", color=None, border={}, dim=None):
		"""
		affiche le point dans un graphique en 2d ou 3d
		'label' est la legende de ce point (par defaut le str du point)
		'color' est le code rgb de la forme '#ffee00'
		'border' est le dictionnaire qui a chaque variable associe au minimum la valeur minimum, maximum du parametre,
		et le nombre de point qu'il doit balayer.
		"""
		if dim == None:
			pass
		elif dim == 2:
			if len(self) > 2:
				if self[2:] == [0]*(self.dim()-2):
					return Point(self[0], self[1]).show(label, color, border, dim)
				else:
					raise LookupError("can't plot a "+str(len(self))+"d point in a 2d space")
			elif len(self) == 1:
				return Point(self[0], 0).show(label, color, border, dim)
		elif dim == 3:
			if len(self) == 1:
				return Point(self[0], 0, 0).show(label, color, border, dim)
			elif len(self) == 2:
				return Point(self[0], self[1], 0).show(label, color, border, dim)
		else:
			raise LookupError("'dim' can only takes None, 2 or 3, no "+str(dim))

		if label == "automatic":
			label = self.__repr__()

		if len(self) == 1:
			Point(self[0], 0).show(label, color, border, dim)

		elif len(self) == 2:
			self.plot(plt, label, color, border, dim)
			plt.legend()
			plt.xlabel("x")
			plt.ylabel("y")
			plt.show()

		elif len(self) == 3:
			fig = plt.figure()
			ax = fig.gca(projection='3d')
			self.plot(ax, label, color, border, dim)
			ax.legend()
			ax.set_xlabel("x")
			ax.set_ylabel("y")
			ax.set_zlabel("z")
			plt.show()

		else:
			raise LookupError("show only on dimenssion 1, 2 or 3, no "+str(len(self)))

	def subs(self, *args, **kwargs):
		"""
		retourne le nouveau point ou la methode subs a ete appliquee a chaque coordonnee
		"""
		return Point(*(e.subs(*args, **kwargs) for e in self))

	def translate(self, vector):
		"""
		retourne le nouveau point ayant subit une translation
		du vecteur 'vector'
		"""
		return self+Point(vector)

	def trigsimp(**args):
		"""
		applique cette fonction a chacune des coordonnees, retourne le point simplifie
		"""
		return Point(*(e.trigsimp(**args) for e in self))

	def xreplace(self, rule):
		"""
		Replace occurrences of objects within the expression
		"""
		return Point(*(e.xreplace(rule) for e in self))

class Vector(Point):
	"""
	est un vecteur en n dimensions, heritant de la classe Point
	"""
	def __init__(self, *args, **kwargs):
		Point.__init__(self, *args, **kwargs)

	def __matmul__(self, vector):
		"""
		retourne le produit vectoriel de self par 'vector' dans le cas ou c'est possible. (appelle par 'objet @ vector')
		"""
		if type(vector) != Vector:		#si ce n'est pas un vecteur
			return self.__matmul__(Vector(vector))#on tente de le transformer en vecteur
		if len(self) < 3:				#si le vecteur self n'est pas dans R**3
			return Vector(list(self)+[0]*(3-len(self))).__matmul__(vector)#on le plonge de force
		if len(vector) < 3:				#on fait exactement le meme test avec le vecteur 'vector'
			return self.__matmul__(Vector(list(vector)+[0]*(3-len(self))))#que l'on plonge aussi dans R**3
		if len(self) + len(vector) > 6:	#par contre, si l'un des vecteurs au moins est en 4D ou plus:
			raise Exception("the dimension of the vectors must be <= 3")#on renvoie une erreur
		return Vector(self[1]*vector[2]-self[2]*vector[1], self[2]*vector[0]-self[0]*vector[2], self[0]*vector[1]-self[1]*vector[0])

	def __repr__(self):
		"""
		permet un affichage graphique un peu mieux
		"""
		if 0 <= len(self) <= 3:						#si on est dans une dimension visualisable
			return "Vector"+str(len(self))+"D("+", ".join(map(str, self))+")"#on colle a la representation de sympy
		return "Vector("+", ".join(map(str, self))+")"#afin d'uniformiser les codes

	def are_coplanar(*vectors):
		"""
		retourne une condition pour que tous les vecteurs
		soient cooplanaires
		"""
		vectors = [Vector(vector) for vector in vectors]	#on s'assure que les objets soient bien des vecteurs
		if len(vectors) <= 2:								#si il y a 2 vecteurs ou moins
			return True										#ils sont alors ineluctablement cooplanaires
		space = Vect(*vectors)								#pour voir si ils sont cooplanaires, on regarde la dimmension de l'espace vectoriel
		return Equation(space.dim(), 2, "<=").solve()		#engendre par ces vecteurs. Elle doit donc etre inferieur ou egale a 2

	def are_collinear(*vectors):
		"""
		retourne une condition pour que tous les vecteurs
		soients collineaires
		"""
		vectors = [Vector(vector) for vector in vectors]	#on s'assure que les objets soient bien des vecteurs
		if len(vectors) <= 1:								#si il y n'y a qu'un seul vecteur
			return True										#alors il est coolineaire a lui meme
		space = Vect(*vectors)								#pour voir si ils sont coolineaires, on regarde la dimmension de l'espace vectoriel
		return Equation(space.dim(), 1, "<=").solve()		#engendre par ces vecteurs. Elle doit donc etre inferieur ou egale a 2

	def is_coplanar(self, *vectors):
		"""
		retourne une condition pour que les vecteurs passes en parametre et self
		coexistent sur un meme plan
		"""
		return Vector.are_coplanar(self, *vectors)

	def is_collinear(*vectors):
		"""
		retourne une condition pour que les vecteurs passes en parametre et self
		coexistent sur une meme droite
		"""
		return Vector.are_collinear(self, *vectors)

	def midvector(self, vector):
		"""
		retourne le vecteur equidistant de self est de 'vector'
		"""
		return (self+vector)/2

	def plot(self, ax, label=None, color=None, border={}):
		"""
		prepare l'affichage graphique de ce vecteur
		'ax' est l'objet matplotlib qui permet de tout plotter au meme endroit
		'label' est la legende de ce point
		'color' est le code rgb de la forme '#ffee00'
		'border' est le dictionnaire qui a chaque variable associ au minimum la valeur minimum, maximum du parametre,
		et le nombre de point qu'il doit balayer.
		"""
		if self.dim() == 0:				#si il s'agit d'un vecteur static
			if len(self) == 1:			#si il est en 1D
				Vector(self[0], 0).plot(ax, label, color, border)#on le plonge en 2D
			elif len(self) == 2:		#si il est en 2D
				Point(0, 0).plot(ax, None, color)#on marque fortement l'origine
				ax.quiver(0, 0, float(self[0]), float(self[1]), angles="xy", label=label, color=color)
			elif len(self.coords) == 3:	#de meme, si on est en 3D
				Point(0, 0, 0).plot(ax, None, color)#on marque l'origine
				ax.quiver(0, 0, 0, float(self[0]), float(self[1]), float(self[2]), length=0.1, normalize=True, label=label, color=color)	
			else:
				raise LookupError("plot only on dimenssion 1, 2 or 3, no "+str(len(self)))
		else:
			Point(self).plot(ax, label, color, border)

	def unitary(self):
		"""
		retourne ce vecteur norme. Si le vecteur est nul, le code renvoie une erreur de division par zero.
		equivaut a self/abs(self) mais en plus rapide
		"""
		norme = abs(self)
		return Vector((e/norme for e in self))

class Polyline:
	"""
	Representation d'une ligne brisee, par une succesion de points tous relies entre eux.
	Les points sont des points de R**n.
	Il sont relies par des Segments
	"""
	def __init__(self, *points):
		self.points = points
		self.dim = 1		#une ligne a toujours pour dimension 1
		self.__init__clean()

	def __init__clean(self):
		"""
		fait du tri dans les points
		"""
		#verification du nombre de points
		if len(self.points) < 2:
			raise Exception("Polyline must have a minimum number of 2 Points")
		
		dimenssion = 0
		for p in self:
			if type(p) != Point:
				raise TypeError("Polyline must be uniquely consituted from Point object. no "+str(type(p)))
			if dimenssion == 0:
				dimenssion = len(p)
			elif dimenssion != len(p):
				raise ValueError("All points must to have the same dimenssion "+str(dimenssion)+" and "+str(len(p))+" are differents!")

		#suppression des points inutiles
		nouveau = True						#True quand il y a du changement
		while (len(self) > 2) and nouveau:	#c'est une fausse boucle infinie
			nouveau = False					#cela evite les boucles infinies
			for i in range(len(self)-2):	#on parcours les points 3 a trois
				if abs(Vector(*self[i+2])-Vector(*self[i])) == abs(Vector(*self[i+1])-Vector(*self[i]))+abs(Vector(*self[i+2])-Vector(*self[i+1])):#si les 3 points sont allignes
					self.points = self.points[:i+1]+self.points[i+2:]#alors on supprime celui du milieu
					nouveau = True 			#on indique qu'il y a du changement
					break					#puis on recommence le test

	def __abs__(self):
		"""
		retourne la longeur de la ligne.
		C'est a dire la somme des distances separant chaque point dans l'ordre. (appelle par 'abs(objet)')
		"""
		somme = 0
		for i in range(len(self.points)-1):
			somme += abs(Vector(*self[i])-Vector(*self[i+1]))
		return somme

	def __bool__(self):
		"""
		retourne True si la ligne a une longueur non nulle. (appelle par 'if objet:')
		"""
		for i in range(len(self.points)-1):
			if abs(Vector(*self[i])-Vector(*self[i+1])):
				return True
		return False

	def __contains__(self, item):
		"""
		retourne True si 'item' est un point et que ce point est dans au moins un segment de la ligne.
		retourne aussi True si 'item' est un segment et que ce segment est present dans la courbe.
		(appelle par 'item in objet')
		"""
		if type(item) == Point:						#si l'element est un point
			for segment in self.get_segments():		#on regarde si le point
				if item in segment:					#apparait au moins une fois dans l'un des segments
					return True						#au quel cas, on sait que le point est contenu dans la polyline
			return False							#si il n'apparait nul part, alors il n'est pas contenu dedans

		elif type(item) == Segment:					#si l'objet est un segment
			for segment in self.get_segments():		#on fait comme pour le point
				if item in segment:					#c'est a dire qu'on regarde qu'il soit au moin present
					return True						#dans l'un des segments qui compose la polyline
			return False							#si il n'apparait nul part, alors il n'est pas dans la polyline

		if type(item) in (Polyline, Polygon, Triangle, Quadrilateral, Pentagone, Hexagone, Octogone):#dans tous les autres cas
			for segment in item.get_segments():		#il faut que chaque segment de 'item'
				if not segment in self:				#apparaisse au moins une fois dans la polyline
					return False					#si l'un au moins des segments n'y est pas, alors item
			return True								#n'est pas contenu dans 'polyline'
			
		raise TypeError("'in <Polyline>' requires (Point, Segment, Polyline, Polygon, Triangle, Quadrilateral, Pentagone, Hexagone, Octogone) as left operand, not "+str(type(item)))

	def __delitem__(self, index):
		"""
		supprime le point a l'index 'index'. (appelle par 'del objet[item]')
		"""
		points = list(self.points)
		p = points[index]
		del points[index]
		self.points = tuple(points)
		self.__init__clean()
		return p
	
	def __eq__(self, item):
		"""
		retourne True si self et ligne sont egaux.
		c'est a dire si tous les sommets sont les memes, a une permutation pres. (appelle par '==')
		"""
		if type(item) in (Polyline, Polygon, Point, Segment, Triangle, Quadrilateral, Pentagone, Hexagone, Octogone):
			if (item in self) and (self in item):	#les deux ensembles sont egaux ssi
				return True							#ils sont mutuellement inclus l'un dans l'autre
			return False
		return NotImplemented
		
	def __ge__(self, obj):
		"""
		retourne True si self superieur ou egal a ligne. (appelle par '>=')
		"""
		try:
			return not self.__lt__(obj)
		except:
			return NotImplemented

	def __getitem__(self, index):
		"""
		appelle lorsque qu'on fait ('objet[index]')
		indexe les sommets et pas les aretes
		"""
		return self.points[index]

	def __gt__(self, obj):
		"""
		retourne True si self est strictement superieur a ligne, en terme de longueur. (appelle par '>')
		on compare les modules de ces 2 nombres
		"""
		try:
			return abs(self) > abs(obj)
		except:
			return NotImplemented

	def __hash__(self):
		"""
		retourne le hash entier de cet objet
		afin qu'un point soit un hashable. (appelle par 'hash(objet)')
		"""
		return hash(self.points)

	def __le__(self, obj):
		"""
		retourne True si self inferieur ou egal a ligne. (appelle par '<=')
		"""
		try:
			return not self.__gt__(obj)
		except:
			return NotImplemented

	def __len__(self):
		"""
		renvoie la dimension de la ligne
		c'est a dire le nombre de points qui la compose. (appelle par 'len(obj)')
		"""
		return len(self.points)

	def __lt__(self, obj):
		"""
		retourne True si self est strictement inferieur a P. (appelle par <)
		"""
		try:
			return abs(self) > abs(obj)
		except:
			return NotImplemented

	def __repr__(self):
		"""
		retourne une chaine de caractere pour une plus belle representation de l'objet
		"""
		return "ligne with "+str(len(self.points))+" points at "+str(hash(self))

	def __setitem__(self, index, point):
		"""
		assigne le point 'point' a la position 'index'. (appelle par 'objet[index] = point')
		"""
		if type(point) != Point:
			raise TypeError("'point' must be type Point, no "+str(type(point)))
		points = list(self.points)
		points[index] = point
		self.points = tuple(points)
		self.__init__clean()

	def get_vertices(self):
		"""
		retourne la liste des sommets qui forment
		cette ligne polygonale
		"""
		return list(self.points)

	def get_segments(self):
		"""
		retourne la liste des segments qui forment la ligne
		"""
		return [Segment(self[i], self[i+1]) for i in range(len(self)-1)]

	def is_closed(self):
		"""
		retourne True si la ligne poligonale
		est une ligne fermee, c'est a dire si le premier point est egal au dernier
		"""
		if self[0] == self[-1]:
			return True
		return False

	def is_simple(self):
		"""
		retourne True si la ligne n'est pas une ligne fermee
		"""
		return not self.is_closed()

	def pprint(self):
		"""
		affiche joliment tous les points qui forment la courbe
		"""
		print(self.__repr__())
		for point in self.points:
			point.pprint()

	def plot(self, ax, label=None, color=None):
		"""
		prepare l'affichage en 3 d de ce point
		'color' est le code rgb de la fore '#ffee00'
		"""
		if len(self[0]) == 1:
			Ligne(*(Point(point[0], 0) for point in self)).plot(ax, label, color)
		elif len(self[0]) == 2:
			ax.plot([point[0] for point in self], [point[1] for point in self], label=label, color=color)
		elif len(self[0]) == 3:
			ax.plot([point[0] for point in self], [point[1] for point in self], [point[2] for point in self], label=label, color=color)
		else:
			raise LookupError("plot only on dimenssion 1, 2 or 3, no "+str(len(self[0])))

	def show(self, label="automatic", color=None):
		"""
		affiche le point dans un graphique en 3d
		"""
		if label == "automatic":
			label = self.__repr__()
		
		if len(self[0]) == 1:
			Segment(*(Point(point[0], 0) for point in self)).show(label, color)

		elif len(self[0]) == 2:
			self.plot(plt, label, color)
			plt.legend()
			plt.xlabel("x")
			plt.ylabel("y")
			plt.show()

		elif len(self[0]) == 3:
			fig = plt.figure()
			ax = fig.gca(projection='3d')
			self.plot(ax, label, color)
			ax.legend()
			ax.set_xlabel("x")
			ax.set_ylabel("y")
			ax.set_zlabel("z")
			plt.show()

		else:
			raise LookupError("show only on dimenssion 1, 2 or 3, no "+str(len(self[0])))

class Segment:
	"""
	represente un segment ferme dans l'espace. defini par 2 points
	"""
	def __init__(self, p1, p2):
		self.p1 = p1		#point 1
		self.p2 = p2		#point 2
		self.dim = 1		#tout segment est de dimension 1
		self.__init__clean()#fait des verifications

	def __init__clean(self):
		"""
		fait les verifications necessaires
		"""
		if type(self.p1) != Point:
			raise TypeError("the point n°1 is not <Point>, it is "+str(type(self.p1)))
		if type(self.p2) != Point:
			raise TypeError("the point n°2 is not <Point>, it is "+str(type(self.p2)))
		if len(self.p1) != len(self.p2):
			raise ValueError("All points must to have the same dimenssion "+str(len(self.p1))+" and "+str(len(self.p2))+" are differents!")

	def __abs__(self):
		"""
		retourne la longueur du segment. (appelle par 'abs(objet)')
		"""
		return abs(Vector(*self.p1)-Vector(*self.p2))

	def __bool__(self):
		"""
		retourne True si le segment n'est pas un point, cas degenere. (appelle par 'if objet:')
		"""
		if self.p1 != self.p2:
			return True
		return False

	def __contains__(self, item):
		"""
		retourne true si l'item se trouve dans ce segment. (appelle par 'item in objet')
		"""
		if type(item) == Point:
			if abs(self) == abs(Vector(*item)-Vector(*self.p1)) + abs(Vector(*self.p2)-Vector(*item)):
				return True
			return False
		elif type(item) == Segment:
			if (item.p1 in self) and (item.p2 in self):
				return True
			return False
		elif type(item) == Polyline:
			for segment in item.get_segments():
				if not segment in self:
					return False
			return True

		raise TypeError("'in <Segment>' requires segment or point as left operand, not "+str(type(item)))

	def __eq__(self, segment):
		"""
		retourne True si self et segment ont les memes extremitees. (appelle par '==')
		"""
		if type(segment) != Segment:
			return NotImplemented
		if ((self.p1 == segment.p1) and (self.p2 == segment.p2)) or ((self.p1 == segment.p2) and (self.p2 == segment.p1)):
			return True
		return False

	def __ge__(self, obj):
		"""
		retourne True si la longueur de self superieur ou egal a celle de obj. (appelle par '>=')
		"""
		try:
			return not self.__lt__(obj)
		except:
			return NotImplemented

	def __getitem__(self, index):
		"""
		permet de recuperer le point 1 ou 2. (appelle par 'objet[index]')
		"""
		return [self.p1, self.p2][index]

	def __gt__(self, obj):
		"""
		retourne True si la longueur de self est strictement superieur a celle de obj. (appelle par '>')
		"""
		try:
			return abs(self) > abs(obj)
		except:
			return NotImplemented

	def __hash__(self):
		"""
		retourne le hash entier de cet objet
		afin qu'un point soit un hashable. (appelle par 'hash(objet)')
		"""
		return hash((self.p1, self.p2))

	def __le__(self, obj):
		"""
		retourne True si la longueur de self inferieur ou egale a celle de segment. (appelle par '<=')
		"""
		try:
			return not self.__gt__(obj)
		except:
			return NotImplemented

	def __lt__(self, obj):
		"""
		retourne True si self est strictement inferieur a obj. (appelle par '<')
		"""
		try:
			return abs(self) > abs(obj)
		except:
			return NotImplemented

	def __repr__(self):
		"""
		permet un affichage graphique un peu meilleur
		"""
		return "segment ("+str(self.p1)+", "+str(self.p2)+")"

	def __setitem__(self, index, point):
		"""
		permet de chager la valeur dune coordonnee. (appelle par 'objet[index] = value')
		"""
		points = [self.p1, self.p2]
		points[index] = point
		self.p1, self.p2 = tuple(points)
		self.__init__clean()

	def get_segments(self):
		"""
		retourne le segment qui compose ce segment
		"""
		return self

	def module_square(self):
		"""
		retourne le carre de la longueur de ce segment
		"""
		return (Vector(*self.p1)-Vector(*self.p2)).module_square()

	def pprint(self):
		"""
		affiche joliment ce segment
		"""
		print("segment:")
		self.p1.pprint()
		self.p2.pprint()

	def plot(self, ax, label=None, color=None):
		"""
		prepare l'affichage en 2d ou 3d de ce segment
		'color' est le code rgb de la fore '#ffee00'
		"""
		if len(self.p1) == 1:
			Segment(Point(self.p1[0], 0), Point(self.p2[0], 0)).plot(ax, label, color)
		elif len(self.p1) == 2:
			ax.plot([self.p1[0], self.p2[0]], [self.p1[1], self.p2[1]], label=label, color=color)
		elif len(self.p1) == 3:
			ax.plot([self.p1[0], self.p2[0]], [self.p1[1], self.p2[1]], [self.p1[2], self.p2[2]], label=label, color=color)
		else:
			raise LookupError("plot only on dimension 1, 2 or 3, no "+str(len(self.p1)))

	def show(self, label="automatic", color=None):
		"""
		affiche le segment dans un graphique en 3d
		"""
		if label == "automatic":
			label = self.__repr__()
		
		if len(self.p1) == 1:
			Segment(Point(self.p1[0], 0), Point(self.p2[0], 0)).show(label, color)

		elif len(self.p1) == 2:
			self.plot(plt, label, color)
			plt.legend()
			plt.xlabel("x")
			plt.ylabel("y")
			plt.show()

		elif len(self.p1) == 3:
			fig = plt.figure()
			ax = fig.gca(projection='3d')
			self.plot(ax, label, color)
			ax.legend()
			ax.set_xlabel("x")
			ax.set_ylabel("y")
			ax.set_zlabel("z")
			plt.show()

		else:
			raise LookupError("show only on dimenssion 1, 2 or 3, no "+str(len(self.p1)))

class Triangle:
	"""
	c'est simplement 3 point relies, dans un espace a n dimensions
	"""
	def __init__(self, p1, p2, p3):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.dim = 2
		self.__init__clean()

	def __init__clean(self):
		"""
		fait des verifications afin de s'assurer que ce triangle soit un vrai triangle
		"""
		if type(self.p1) != Point:
			raise TypeError("the point n°1 is not <Point>, it is "+str(type(self.p1)))
		if type(self.p2) != Point:
			raise TypeError("the point n°2 is not <Point>, it is "+str(type(self.p2)))
		if type(self.p3) != Point:
			raise TypeError("the point n°3 is not <Point>, it is "+str(type(self.p3)))
		if (len(self.p1) != len(self.p2)) or (len(self.p1) != len(self.p3)):
			raise ValueError("All points must to have the same dimenssion "+str(len(self.p1))+", "+str(len(self.p2))+"and "+str(len(self.p3))+" are differents!")

	def __abs__(self):
		"""
		retourne la longueur du perimetre du triangle. (appelle par 'abs(objet)')
		"""
		return abs(Polyline(self.p1, self.p2, self.p3, self.p1))

	def __bool__(self):
		"""
		retourne un booleen qui permet d'affirme si le triangle est un triangle plat ou non
		retourne True si le triangle a une aire non nulle. (appelle par 'if objet')
		"""
		if self.p1 in Segment(self.p2, self.p3):
			return False
		elif self.p2 in Segment(self.p1, self.p3):
			return False
		elif self.p3 in Segment(self.p1, self.p2):
			return False
		return True

	def __eq__(self, obj):
		"""
		retourne True si l'objet 'obj' est egal au triangle 'self'. (appelle par '==')
		"""
		if type(obj) in (Polyline, Polygon, Segment, Triangle, Quadrilateral, Pentagone, Hexagone, Octogone):
			if (self in obj) and (obj in self):
				return True
			return False
		return NotImplemented

	def __ge__(self, obj):
		"""
		retourne True si self superieur ou egal a l'objet. (appelle par '>=')
		"""
		try:
			return not self.__lt__(obj)
		except:
			return NotImplemented

	def __getitem__(self, index):
		"""
		recupere et retourne la coordonnee de rang 'index'. (appelle par 'objet[index]')
		"""
		return [self.p1, self.p2, self.p3][index]

	def __gt__(self, obj):
		"""
		retourne True si self est strictement superieur a obj. (appelle par '>')
		"""
		try:
			return abs(self) > abs(obj)
		except:
			return NotImplemented

	def __hash__(self):
		"""
		retourne le hash entier de cet objet
		afin qu'un point soit un hashable. (appelle par 'hash(objet)')
		"""
		return hash((self.p1, self.p2, self.p3))

	def __le__(self, obj):
		"""
		retourne True si self inferieur ou egal a obj. (appelle par '<=')
		"""
		try:
			return not self.__gt__(obj)
		except:
			return NotImplemented

	def __len__(self):
		"""
		renvoie la dimension de l'espace dans lequel vit ce vecteur. (appelle par 'len(objet)')
		"""
		return len(self.p1)

	def __lt__(self, obj):
		"""
		retourne True si self est strictement inferieur au vecteur. (appelle par '<')
		"""
		try:
			return abs(self) > abs(obj)
		except:
			return NotImplemented

	def __repr__(self):
		"""
		permet un affichage graphique un peu meilleur
		"""
		return "triangle ("+str(self.p1)+", "+str(self.p2)+", "+str(self.p3)+")"

	def __setitem__(self, index, coord):
		"""
		permet de remplacer la coordonnee de rang 'index' par la valeur 'coord'. (appelle par 'objet[index] = coord')
		"""
		coords = [self.p1, self.p2, self.p3]
		coords[index] = coord
		self.p1, self.p2, self.p3 = coords
		self.__init__clean()

	def pprint(self):
		raise NotImplementedError()

#objet pour le calcul

class Equation:
	"""
	modelise une equation, ou une inegalite
	"""
	def __init__(self, element1, element2, comparator="=", formal=None):
		"""
		reflette l'equation:
		'elemment1 comparator element2'
		"""
		self.element1 = self.__init__render(element1)
		self.element2 = self.__init__render(element2)
		self.comparator = comparator	#operateur de comparaison ('=', '==', '!=', '>', '<', '>=', '<=')

	def __init__render(self, element):
		"""
		s'assure que l'element soit pas un systeme mais une expression seule
		"""
		if type(element) == str:		#si c'est une chaine de caractere
			return sympy.sympify(element)#on la transforme en expression sympy

	def __repr__(self):
		return str(self.element1)+" "+self.comparator+" "+str(self.element2)

class System:
	"""
	c'est un ensemble d'equations
	"""

def is_associative(element, law):
	"""
	retourne True si l'element est distributif par rapport a la loi 'law'
	"""
	def test(element, law):
		if type(element) == type:
			return element.are_associative(law)
		return element.is_associative(law)

	with raisin.Printer("are the elements associatives '(a "+law+" b) "+law+" c = a "+law+" (b "+law+" c)'?") as p:#on regarde si les elements sont comutatifs
		if type(element) == type:
			genre = element
		else:
			genre = type(element)
		if law == "+":
			if genre in (int, float, complex, list, tuple, str, sympy.re, sympy.im, type(sympy.sympify("1+x")), type(sympy.sympify("1*x"))):
				p.show("yes")
				return True
			elif genre in (dict, ):
				p.show("no")
				return False
			try:
				if test(element, "+"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		if law == "*":
			if genre in (int, float, complex):
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "*"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		if law == "°":
			if genre in ():
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "°"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		if law == "@":
			if genre in ():
				p.show("yes")
				return True
			elif genre in (Vector,):
				p.show("no")
				return False
			try:
				if test(element, "@"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		if law == "&":
			if genre in (set,):
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "&"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		if law == "|":
			if genre in (set,):
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "|"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		raise TypeError

def is_commutative(element, law):
	"""
	retourne True si l'element est distributif par rapport a la loi 'law'
	"""
	def test(element, law):
		if type(element) == type:
			return element.are_commutative(law)
		return element.is_commutative(law)

	with raisin.Printer("are the elements commutatives 'a "+law+" b = b "+law+" a'?") as p:#on regarde si les elements sont comutatifs
		if type(element) == type:
			genre = element
		else:
			genre = type(element)
		if law == "+":
			if genre in (int, float, complex, sympy.re, sympy.im, type(sympy.sympify("1+x")), type(sympy.sympify("1*x"))):
				p.show("yes")
				return True
			elif genre in (list, tuple, str):
				p.show("no")
				return False
			try:
				if test(element, "+"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		elif law == "*":
			if genre in (int, float, complex):
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "*"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		elif law == "°":
			if genre in ():
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "°"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		elif law == "@":
			if genre in ():
				p.show("yes")
				return True
			elif genre in (Vector,):
				p.show("no")
				return False
			try:
				if test(element, "@"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		elif law == "&":
			if genre in (set,):
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "&"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		elif law == "|":
			if genre in (set,):
				p.show("yes")
				return True
			elif genre in ():
				p.show("no")
				return False
			try:
				if test(element, "|"):
					p.show("yes")
					return True
				p.show("no")
				return False
			except:
				p.show("impossible to know")
				raise TypeError
		raise TypeError

def is_distributive(element, law1, law2):
	"""
	retourne True si l'element est distributif par rapport a la loi 'law'
	"""
	def test(element, law1, law2):
		if type(element) == type:
			return element.are_distributive(law1, law2)
		return element.is_distributive(law1, law2)

	with raisin.Printer("are the elements distrubutives 'a "+law1+" (b "+law2+" c) = (a "+law2+" b) "+law1+" (a "+law2+" c)'?") as p:#on regarde si les elements sont comutatifs
		if type(element) == type:
			genre = element
		else:
			genre = type(element)
		if (law1 == "*") and (law2 == "+"):
			if genre in (int, float, complex):
				p.show("yes")
				return True
		try:
			if test(element, law1, law2):
				p.show("yes")
				return True
			p.show("no")
			return False
		except:
			raise TypeError