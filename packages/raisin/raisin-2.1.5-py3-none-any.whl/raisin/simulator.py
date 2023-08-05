#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sympy.core.relational import Equality
from math import *
import raisin
import sympy
import time

#environement

class node:
	def __init__(self, id=None):
		self.id = id						#identifiant de ce noeud
		self.U = 0							#potentiel du noeud

	def change_voltage(self, new=None):
		"""
		change la valeur courante de la tension par cette nouvelle valeur
		retourne la valeur actuelle de la tension
		"""
		if new == None:
			return self.U
		self.U = new
		return self.U

class pin:
	def __init__(self, node, id=None, current_id=None):
		"""
		c'est une pate de composant
		elle permet de faire un lien entre les noeuds et les composants
		c'est l'objet a partir du quel va etre construit la loie des mailles et des noeuds
		"""
		self.node = node					#objet noeud
		self.id = id						#identifiant de la pate, un numero ou un nom en str, peu importe
		self.current_id = current_id		#l'identifiant du courrant, pour les simplifications

class Compiler:
	def __init__(self, *components):
		"""
		contient en trotre, les equations:
			-self.invariant_equations
			-self.differencial_equations
			-self.surplus_equations
		"""
		self.components = components
		self.vars = self.get_vars()							#recuperations des variables qui interviennent dans les equations
		self.compile()

	def get_vars(self):
		"""
		retourne la liste des variables sympy
		"""
		with raisin.Printer("get variables..."):
			variables = []									#la liste est tout d'abord vide
			for component in self.components:				#pour chaque composant, comme ca on est certain de ne pas sauter de variables
				for var in component.get_vars():			#pour chaque variables de chaque composant
					if not var in variables:				#si elle n'est pas deja dans le lot
						variables.append(var)				#on l'ajoute aux autres variables
			return variables								#la liste des variables sans doublet est donc retournee

	def update(self, t, dt, solution):
		"""
		met a jour tous les parametres internes des composant
		c'est par ici que l'on peu faire griller les composants
		ou changer en profondeur leus proprietes
		"""
		with raisin.Printer("update components..."):
			for comp in self.components:					#pour chaque composant
				comp.update(t, dt, solution)				#il est mis a jour

	def get_invariant_equations(self):
		"""
		retourne la liste des equations simple qui ne changent pas dans le temps
		ces equations contienne la loie des noeuds
		le systeme forme par ces equations ne sera donc resolu qu'une seule fois
		"""
		with raisin.Printer("get intemporal equations..."):
			eqs = {}										#c'est la liste qui va contenir les equations lineaires
			for component in self.components:				#pour chaques composants
				for eq in component.invariant_equations():	#on recupere les equations qui lui sont propres
					g,d = eq.args							#on disconecte le menbre de droite et de gauche
					eqs[g] = d								#affin de les ajouter au lot global
			nodes = {}										#mais jusque ici, la loie des noeuds a ete delaissee
			for component in self.components:				#c'est donc reparti pour un tour
				for pin in component.get_pins():			#chaque pate de chaque composant
					node = pin.node							#est relier a un potentiel
					nodes[pin.node.id] = nodes.get(pin.node.id, [])+[sympy.Function(pin.current_id)(sympy.Symbol("t"))]#a chaque potentiel, on recence les pate qui lui rentre dedans
			for node in nodes:								#une fois le recencement fini, il faut metre en place les equations de la loie des noeuds
				eq = nodes[node][0]							#chaque courant qui rentre dans un meme noeud
				for I in nodes[node][1:]:					#est donc somme au precedent
					eq = eq+I								#l'equation reflette la somme de tous les courants
				eqs[eq] = sympy.sympify("0")				#la somme des courants entrant dans le noeud fait 0
			return eqs										#toutes ces equations sont renvoyer affin d'etre resolues

	def get_differencial_equations(self):
		"""
		retourne la liste des equations non lineaires et ou differencielles
		sous forme integrale (pour eviter d'avoir recours aux condition initiales)
		qui ne change pas de forme dans le temps
		"""
		with raisin.Printer("get differencial equations..."):
			eqs = {}										#la liste des equations a retourner
			for component in self.components:				#pour chaque composant
				for eq in component.differencial_equations():#chaque equations complexes
					g,d = eq.args							#separation du menbre de gauche et de droite
					eqs[g] = d								#est recuperree
			return eqs										#puis renvoyer au lot global

	def get_variant_equations(self):
		"""
		retourne les equations qui regissent un systeme trop complexe pour pouvoir
		etre totalement explicitee, c'est equations peuvent contenir des tests logics
		ou peuvent elles-meme resulter d'une interpolation non lineaire...
		bref, elle ne sont valide qu'a t fixer et pour un dt suffisement petit
		"""
		with raisin.Printer("get mooving equations..."):
			eqs = {}										#la liste bientot retournee
			for component in self.components:				#on fouille chaque composant
				for eq in component.variant_equations():	#pour lui extraire les equations les plus profondes
					g,d = eq.args							#separation des 2 menbres
					eqs[g] = d								#et les garder un tout petit moment
			return eqs										#avant qu'elles ne soient plus valides

	def compile(self):
		"""
		compile les informations minimums
		"""
		with raisin.Printer("node and basic law..."):
			self.invariant_equations = self.get_invariant_equations()#recuperations des equations gentilles
			self.surplus_equations, self.invariant_equations = self.simplify(self.invariant_equations)#petite tentative de simplification

		with raisin.Printer("temporal integration law..."):
			self.differencial_equations = self.get_differencial_equations()#recuperations des mechantes equations
			self.differencial_equations = self.replace(self.differencial_equations, self.surplus_equations)#epurage maximum

		with raisin.Printer("derivate forme..."):
			variables = self.get_specific_vars(self.differencial_equations)#recuperation des variables qui interviennent dans ces equations
			equations = {list(dico.items())[0][0]:list(dico.items())[0][1] for dico in [self.substituer(self.differencial_equations, var) for var in variables]}#on fait une substitution des equation du systeme pour se ramener a des equation independantes
			equations = {g:d for g,d in equations.items() if len(self.get_specific_vars({g:d})) == 1}#on ne garde que les meilleur, c'est a dire celle qui ne font intervenir qu'un seule variable
			self.variables = [self.get_specific_vars({g:d})[0] for g,d in equations.items()]#c'est la liste de chaque variable qui intervient dans chaque equations
			equations = {var:sympy.solve(sympy.Eq(g,d), var, list=True)[0] for (g,d),var in zip(equations.items(), self.variables)}#on la met sous une jolie form
			self.derivate_equations, self.initial_conditions = self.find_initial_conditions(equations)#on derive mais en gardant une trace pour pouvoir plus tard, virrer les variables

		with raisin.Printer("searching parameters..."):
			self.parameters = self.get_parameters()

	def get_specific_vars(self, differencial_equations):
		"""
		retourne la liste de toutes les fonctions presentes dans le systemes
		"""
		variables = set()
		for packet in [(k-v).atoms(sympy.Function) for k,v in differencial_equations.items()]:
			variables = variables | packet
		variables = variables & set(self.get_vars())
		return list(variables)

	def substituer(self, differencial_equations, variable):
		"""
		fait des substitutions sucessives afin d'avoir une seule equation celon la variable
		'variable'
		"""
		with raisin.Printer("substitution..."):
			while len(differencial_equations) > 1:
				for i,(g,d) in enumerate(differencial_equations.items()):	#on parcours chaque equations
					solution = sympy.solve(sympy.Eq(g,d), variable, list=True)#on tente pour chaque d'entre elle, d'en isoler la variable qui nous interresse
					if solution != []:										#si on a reussi a extraire la variable
						differencial_equations = {g.subs(variable, solution[0]):d.subs(variable, solution[0]) for j,(g,d) in enumerate(differencial_equations.items()) if j!=i}
			return differencial_equations

	def find_initial_conditions(self, equations):
		"""
		derive les equation pour en faire un systeme d'equation sous forme derivee
		trouve les conditions initiales
		retroune ces 2 dictionaires
		"""
		initial = {}												#au debut c'est un dictionaire vide
		is_not_differencial = True 									#devient False des qu'il n'y a plus d'integrales
		while is_not_differencial:									#tant que l'on a pas fini
			is_not_differencial = False
			initial = {**initial, **{g.subs("t", 0):d.subs("t", 0).doit() for g,d in equations.items()}}#on recupere les conditions initiales
			equations = {g.diff("t"):d.diff("t").doit().simplify() for g,d in equations.items()}#on derive tout d'un coup
			for var in equations:									#pour chaque clef
				if equations[var].atoms(sympy.Integral) != set():
					is_not_differencial = True
		return equations, initial

	def simplify(self, system):
		"""
		'system' est un dictionaire d'equation sympy
		retourne 2 dictionaires
		-le dictionaire associe a chaque variables, l'expression de la variable seule
		-la liste est le systeme simplifier avec des equations et des variables en moin
		"""
		with raisin.Printer("system simplification...") as p:
			a_suprime = []									#liste des elements a supprimer
			dico_vars = {}									#dictionaire qui va contenir les variables simplifiees
			for var in self.vars:							#pour chaque variable, on va essayer de l'isoler
				for g,d in system.items():					#on prend chaque expression une par une
					sol = sympy.solve(sympy.Eq(g,d), var, dict=True)#tentative de resolution
					if sol == []:							#si le solveur echoue
						continue							#on passe a la suite
					elif sol == sympy.true:					#si l'equation est un doublon d'une autre
						a_suprime.append(g)					#elle sera supprime
						continue							#et on s'arrette la
					elif sol == sympy.false:				#si cette equation en contredit une autre
						raise Exception("any equations are opposits")#on fait tout plenter
					v, expression = list(sol[0].items())[0]	#on recupere la variable isolee et son expression
					if var in expression.atoms(sympy.Function):#si il s'agit d'une equa-diff
						continue							#on abandone aussi
					dico_vars = self.replace(dico_vars, {var: expression})#substitution
					del system[g]							#le systeme est un peu simplifier
					system = self.replace(system, {var: expression})#substitution dans le systeme global
					dico_vars[var] = expression				#memorisation de ce resultat
					p.show(str(var))
					break									#on ne cherche pas plus a supprimer de variables
			system = {g:d for g,d in system.items() if not g in a_suprime}#retirage des equations inutiles
			return dico_vars, system

	def replace(self, system1, system2):
		"""
		remplace tous les elements remplacable du syteme1 par ceux du systeme2
		retourne le systeme 1 aleger
		les systemes sont des dictionaires d'equation sympy
		"""
		for var, expr in system2.items():					#pour chaque variable qui doit disparaitre
			system1 = {g.subs(var, expr).doit():d.subs(var, expr).doit() for g,d in system1.items()}
		return system1

	def get_parameters(self):
		"""
		retourne la liste des parametre inconu
		ces parametres ne contiennent pas les fonction inconu que l'on cherche,
		seulement des variables comme R, x, qui ne dependent pas du temps
		"""
		parametres = set()								#on initialise la liste a vide
		for g,d in self.invariant_equations.items():
			parametres = parametres | g.atoms(sympy.Symbol) | d.atoms(sympy.Symbol)
		for g,d in self.surplus_equations.items():
			parametres = parametres | g.atoms(sympy.Symbol) | d.atoms(sympy.Symbol)
		for g,d in self.differencial_equations.items():
			parametres = parametres | g.atoms(sympy.Symbol) | d.atoms(sympy.Symbol)
		for g,d in self.get_variant_equations().items():
			parametres = parametres | g.atoms(sympy.Symbol) | d.atoms(sympy.Symbol)
		parametres = parametres - {sympy.Symbol("t")}
		return list(parametres)

class Function_sympy:
	"""
	c'est un courant, une tension... et tout l'environement qui va avec
	"""
	def __init__(self, id, eq, duration):
		self.id = id				#c'est le nom de la grandeur mis en jeu (ex: current_pin2_condensateur(t))
		self.eq = eq				#c'est l'equation sympy qui regit cette grandeur
		self.duration = duration	#le temps de la simulation en s
		self.values = {}			#a chaque instant t, y est associe la valeur de la fonction
		self.t = ([t for t in self.eq.atoms(sympy.Symbol) if str(t) == "t"]+["t"])[0]#c'est la variable temporelle

	def eval(self, t):
		"""
		retourne la valeur de la fonction a l'instant t
		"""
		if t in self.values:
			return self.values[t]
		try:
			exec("from math import *\nt = "+str(t)+"\nself.values[t] = eval('''"+str(self.eq)+"''')")
		except:
			self.values[t] = self.eq.subs(self.t, t).evalf()
		return self.values[t]

	def show(self, plt):
		"""
		affiche la courbe
		"""
		self.plot(plt)
		plt.xlabel("temps en (s)")
		plt.show()

	def plot(self, plt):
		"""
		prepare la courbe a l'affichage
		"""
		T = [self.duration*i/400 for i in range(400)]
		Y = [self.eval(t) for t in T]
		plt.plot(T, Y)
		plt.legend((str(self.id),))

def solve(*components, duration=10, parameters_values={}):
	"""
	genere au fur a meusure les fonctions
	"""
	#recuperations des equations
	def genere_dico_parameters(parameters, dico={}):
		"""
		cede un dictionaire qui a chaque parametre, associe ca valeur
		"""
		if len(parameters) == 1:		#si il n'y a qu'un seul balayage a faire
			for value in [10**i for i in range(-9, 7)]:
				yield {**dico, **{parameters[0]:value}}
		else:
			for value in [10**i for i in range(-9, 7)]:
				for d in genere_dico_parameters(parameters[1:], {**dico, **{parameters[0]:value}}):
					yield d

	def subs_fix_parameters(equation, parameters_values):
		"""
		retourne l'equation 'equation' totalement evaluer, sans les variables d'integration
		"""
		with raisin.Printer("replace fixed parameters..."):
			for par, value in parameters_values.items():
				equation = {k.subs(par, sympy.simplify(value)):v.subs(par, sympy.simplify(value)) for k,v in equation.items()}
			return equation

	def sympy_solve(derivate_equations, initial_conditions):
		"""
		tente de formellement resoudre le systeme
		'variables' est la liste des variables qui compose les equations 'derivate equations'
		"""
		def replace_initial_condition(equation, initial_conditions, integration_vars):
			"""
			retourne l'equation 'equation' totalement evaluer, sans les variables d'integration
			l'equation est retourne dans un dictionaire
			"""
			with raisin.Printer("replace initial condition in the result..."):
				with raisin.Printer("successiv differentials..."):
					systeme = [equation]						#c'est le systeme qui va permetre de trouver les sonditions initiales
					for i in range(len(integration_vars)-1):
						systeme.append(sympy.Eq(systeme[-1]._args[0].diff("t"), systeme[-1]._args[1].diff("t")))#afin d'avoir le bon nombre d'equations
				with raisin.Printer("evaluation in t=0..."):
					systeme = [sympy.Eq(s._args[0].subs("t",0), s._args[1].subs("t",0)) for s in systeme]
				with raisin.Printer("insertion of initials values..."):
					for fonc, value in initial_conditions.items():
						systeme = [s.subs(fonc, value) for s in systeme]
				with raisin.Printer("resolution..."):
					solution = sympy.solve(systeme, integration_vars - {sympy.Symbol("t")}, dict=True)[0]
				with raisin.Printer("injection of the result..."):
					for par, value in solution.items():
						equation = sympy.Eq(equation._args[0].subs(par, value), equation._args[1].subs(par, value))
				with raisin.Printer("simplification..."):
					equation = sympy.Eq(equation._args[0], equation._args[1].simplify())
				return {equation._args[0]:sympy.re(equation._args[1].replace("t", sympy.Symbol("t", real=True))).doit()}

		erreur = Exception("fail to solve")
		for g,d in derivate_equations.items():
			with raisin.Printer("try to solve the folowing equation...") as p:
				try:
					p.show(str(sympy.Eq(g,d)))
					sympy.pprint(sympy.Eq(g,d))
					avant = (g-d).free_symbols
					equation = sympy.dsolve(sympy.Eq(g,d))
					sympy.pprint(equation)
					apres = equation.free_symbols
					return replace_initial_condition(equation, initial_conditions, apres-avant)
				except Exception as e:
					erreur = e
		raise erreur

	def iterative_solve(derivate_equation, initial_conditions, eq_vars, parameters_values, duration):
		"""
		resoult pas a pas le systeme
		retourne le dictionaire qui a chaque fonctions, associ un objet 'fonction'
		plus en detail la resolution se fait de la facon suivante:
		on a : f(g'', g', g)=0 (ca c'est "derivate_equation")
		pour avancer pas a pas on pose g(t) = at²+bt+c
		il faut donc resoudre:
			a_vieu*t0²+b_vieu*t0+c_vieu = a_nouveau*t0²+b_nouveau*t0+c_nouveau	(la fonction est continue)
			2*a_vieu*t0+b_vieu = 2*a_nouveau*t0+b_nouveau						(et meme de classe C1)
			f(2*a_nouveau, 2*a_nouveau*(t0+dt)+b_nouveau, a_nouveau*(t0+dt)²+b_nouveau*(t0+dt)+c_nouveau) (l'equation differenciele est verifier au nouveau point)
		de ce systeme on isole a, b et c de la facon suivante:
			a_nouveau = u(a_vieu, b_vieu, c_vieu, t0, dt)
			b_nouveau = v(a_vieu, b_vieu, c_vieu, t0, dt)
			c_nouveau = w(a_vieu, b_vieu, c_vieu, t0, dt)
		grace a "initial_conditions", on en deduit a_nouveau(t=0), b_nouveau(t=0), c_nouveau(t=0)
		c'est bon on a notre relation de recurence
		"""
		def polinomial_replacement(system, eq_vars):
			"""
			remplace toutes les fonctions par un polinome de degres 2
			"""
			with raisin.Printer("searching fonction..."):
				variables = set()
				for packet in [(k-v).atoms(sympy.Function) for k,v in system.items()]:
					variables = variables | packet
				var = variables & set(eq_vars)
				var = list(var)[0]

			with raisin.Printer("polinomial replacement..."):
				t = sympy.Symbol("t")
				t0 = sympy.Symbol("t0")
				dt = sympy.Symbol("dt")
				an = sympy.Symbol("an")
				bn = sympy.Symbol("bn")
				cn = sympy.Symbol("cn")
				system = {g.subs(var, an*t**2+bn*t+cn):d.subs(var, an*t**2+bn*t+cn) for g,d in system.items()}
				system = {g.subs(t, t0+dt):d.subs(t, t0+dt) for g,d in system.items()}
				system = {g.doit():d.doit() for g,d in system.items()}
			return system
		
		def chec_is_numerical(system, parameters_values):
			"""
			"system" est un dictionaire d'expression sympy
			retourne une erreur si d'autre symboles que 't' apparaissent dans au moins une des expressions
			"""
			with raisin.Printer("chec all is numerical..."):
				for g,d in system.items():					#pour chaque expression
					for s in map(str,(g-d).atoms(sympy.Symbol)):#pour chaque symbol present dans l'expression
						if s != "t":						#si jamais ce symbol n'a rien a faire la
							raise Exception("the numerical aplication is not complete:\nno value found for "+s+"\nthey have: "+str(parameters_values))

		def append_jointure_conditions(system):
			"""
			ajoute aux syteme d'equations, les conditions qui vont permetre que le nouveau bout de
			fonction calcule soit continu avec le precedent, et que leur tangantes coincides
			"""
			with raisin.Printer("appening the junction conditions..."):
				t0 = sympy.Symbol("t0")														#c'est le temps de la jointure
				an = sympy.Symbol("an")														#a(n+1)
				bn = sympy.Symbol("bn")														#b(n+1)
				cn = sympy.Symbol("cn")														#c(n+1)
				av = sympy.Symbol("av")														#a(n)
				bv = sympy.Symbol("bv")														#b(n)
				cv = sympy.Symbol("cv")														#c(n)
				system = {**system, **{av*t0**2+bv*t0+cv:an*t0**2+bn*t0+cn, 2*av*t0+bv:2*an*t0+bn}}#derive et valeur en t0 sont egales
			return system

		def shortify_recurrence(system):
			"""
			simplifi la relation de recurence de facon
			a ce que U(n) ne soit pas exprime en fonction de U(n-1) mais de U(n)
			pour eviter de devoir changer les variable et donc gagner du temps au coeur du calcul
			"""
			with raisin.Printer("simplification of the relation..."):
				remplacent = {sympy.Symbol(v):sympy.Symbol(n) for v,n in [("an","a"),("bn","b"),("cn","c"),("av","a"),("bv","b"),("cv","c")]}#chaque U(n-1) est exprime en fonction de U(n)
				system = {g.subs(remplacent):d.subs(remplacent) for g,d in system.items()}	#on remplace tout les U(n-1) par les U(n)
				system = {g:d.simplify() for g,d in system.items()}							#on en fait une evaluation numerique
				return system

		def initial_conditions_replacement(initial_conditions, eq_vars):
			"""
			retourne le systeme mais dont les conditions initiales ont ete remplacees par a, b et c
			"""
			with raisin.Printer("searching fonction..."):
				variables = set()
				for packet in [(k-v).atoms(sympy.Function) for k,v in initial_conditions.items()]:
					variables = variables | packet
				var = variables & set(eq_vars)
				var = list(var)[0]

			with raisin.Printer("initial condiction replacement..."):
				t = sympy.Symbol("t")
				a = sympy.Symbol("a")
				b = sympy.Symbol("b")
				c = sympy.Symbol("c")
				system = {g.subs(var.subs(t,0), c):d.subs(var.subs(t,0), c) for g,d in initial_conditions.items()}#remplacement de f(0) par c
				system = {g.subs(var.diff(t).subs(t,0), b):d.subs(var.diff(t).subs(t,0), b) for g,d in system.items()}#remplacement de f'(0) par b
				system = {g.subs(var.diff(t).diff(t).subs(t,0), c):d.subs(var.diff(t).diff(t).subs(t,0), 2*a) for g,d in system.items()}#remplacement de f''(0) par 2a
				system = {g:d for g,d in system.items() if g in [a,b,c]}					#on eleve les conditions initiales qui ne nous concernent pas
				return system

		def append_default_conditions(system):
			"""
			ajoute aux conditions initiales, la valeur 0 pour les variables qui ne sont pas definies
			"""
			with raisin.Printer("append defaul initial conditions..."):
				a = sympy.Symbol("a")
				b = sympy.Symbol("b")
				c = sympy.Symbol("c")
				system = {var:system.get(var,0) for var in [a,b,c]}				#on fixe a 0 les variables indeterminees
				return system

		def run(initial_conditions, duration, recurrence_relation):
			"""
			calcul les termes de la suite
			"""
			def epure(temps, variables, teta, rang):
				"""
				parcours toute la fonction et supprime beaucoup de points
				les points sont suprimes de facon a ce que l'angle forme
				par 2 tangantes consecutives soit <= teta (en degre), quand cela est possible
				"""
				if rang == 0:										#si on est sur le bord:
					rang = 1										#on se decale un peu pour pouvoir faire un taux d'acroisement
				suivant = rang+1									#'suivant' est le rang du point en questionnement de suppression
				while suivant < len(temps)-1:						#tant que l'on est pas arrive au bout
					angle_init = atan((variables[rang]-variables[rang-1])/(temps[rang]-temps[rang-1]))*180/pi#angle de 'gauche' = artan(f')
					while suivant < len(temps)-1:					#on remet cette condition, mais pour une etape seulement
						angle_courant = atan((variables[suivant]-variables[rang])/(temps[suivant]-temps[rang]))*180/pi#calcul de l'angle
						if abs(angle_init-angle_courant) > teta:	#si on atteind les limites
							break									#on sort de cette boucle
						suivant += 1								#si on et en dessous de la limite, ce point va etre igore
					del temps[rang:suivant]							#tous les points en trop sont extermines
					del variables[rang:suivant]						#bien sur, sur l'axe des Y aussi
					rang+=1											#il est donc temps de passer au rang suivant
					suivant = rang+1								#pour pouvoir refair la meme manipulation
				return temps, variables

			with raisin.Printer("solvation...") as p:
				a = float(initial_conditions[sympy.Symbol("a")])		#c'est a(t=0)
				b = float(initial_conditions[sympy.Symbol("b")])		#c'est b(t=0)
				c = float(initial_conditions[sympy.Symbol("c")])		#c'est c(t=0)
				u = str(recurrence_relation[sympy.Symbol("a")])			#c'est u(t0, dt, a, b, c)
				v = str(recurrence_relation[sympy.Symbol("b")])			#c'est v(t0, dt, a, b, c)
				w = str(recurrence_relation[sympy.Symbol("c")])			#c'est w(t0, dt, a, b, c)
				t0 = 0													#on commence a t=0 secondes
				dt = 10**-10											#avec un pas de temps de 10**-10 secondes (ce pas est variable)
				variables = [c]											#variables contient les valeurs de la fonction de l'equation differencielle
				temps = [t0]											#c'est la liste du temps, initialise a t=0
				rang = 0												#c'est a partir de la que l'on fait l'epuration

				iterations = 0											#entier qui va s'incrementer pour faire du menage au fur a meusure
				while t0 < duration:									#tant que la simulation n'est pas terminee
					av, bv, cv = a, b, c								#sauvegarde des valeurs actuelles pour pouvoir revenir en arriere
					a, b, c = eval(u), eval(v), eval(w)					#calcul du rang suivant
					value = a*(t0+dt)**2+b*(t0+dt)+c					#evaluation du polinome a t=t0+dt
					if (bv-b)**2 < 10**-7:								#si les tengentes en t=t0 et t=t0+dt sont vraiment tres proches
						variables.append(value)							#alors on considere que l'ecart est tout petit
						t0 += dt										#on se permet donc d'avencer au rang suivant
						temps.append(t0)								#bien sur, pour savoir ou on en est, il faut aussi enregister le temps
						dt = min(60, dt*2)								#l'erreur etant tellement petite, on autorize une augmentation du pas
						iterations += 1									#comme on vien d'enregistrer une valeur, le compteur est incremente de 1
					elif (bv-b)**2 > 10**-6:							#au contraire, si l'erreur est trop grande
						if dt <= 10**-10:								#mais qu'on ne peu pas faire mieu
							variables.append(value)						#tant pis, il faut tout de meme avancer
							t0 += dt									#en esperant que ca va s'arranger au rang suivant
							temps.append(t0)							#bref, on fait comme si tout allait bien
							iterations += 1								#et donc on increment le compteur
						else:											#par contre, si on peu reduire cette erreur
							dt = max(10**-10, dt/2)						#on reduit l'intervalle de temps
							a, b, c = av, bv, cv						#puis on se replace a t=t0 pour retenter notre chance
					else:												#si l'erreur n'est ni trop grande, ni trop petite
						variables.append(value)							#on enregistre la valeur courante
						t0 += dt										#on passe tranquillement de t=t0 a t=t0+dt
						temps.append(t0)								#le temps est important pour faire un lien entre le X et l Y de la fonction
						iterations += 1									#puis enfin le compteur est incremente

					if iterations == 100000:							#si cela fait trop lomgtemps que l'on stock des valeurs sans les traiter
						p.show(str(round(100*t0/duration,2))+"%")		#affichage du pourcentage accompli
						temps, variables = epure(temps, variables, 0.1, rang)#liberation de l'espace dans la ramme
						rang = len(temps)-1								#preparation pour la prochaine liberation de memoire
						iterations = 0									#le compteur est remis a zero
				temps, variables = epure(temps, variables, 0.1, rang)	#a la fin, il faut aussi liberer de l'espace
				return temps, variables

		t = sympy.Symbol("t")
		t0 = sympy.Symbol("t0")
		delta_t = sympy.Symbol("dt")

		with raisin.Printer("searching recurence relation..."):
			system = {g.subs(parameters_values):d.subs(parameters_values) for g,d in derivate_equation.items()}#on commence par l'aplication numerique
			chec_is_numerical(system, parameters_values)									#il est important que l'on ne soit plus en literal mais purement en numerique
			system = polinomial_replacement(system, eq_vars)								#on remplace la fonction par a(t0+dt)²+b(t0+dt)+c
			system = append_jointure_conditions(system)										#ajout des conditions pour que la fonction soit de classe C1
			with raisin.Printer("deduction of recurence relation..."):						#resolution pour trouver u, v et w
				recurrence_relation = sympy.solve([sympy.Eq(g,d) for g,d in system.items()], [sympy.Symbol(car) for car in ("an","bn","cn")])#on tente d'en deduire une relation de recurence
			recurrence_relation = shortify_recurrence(recurrence_relation)					#expression plus simple seulement avec a,b et c

		with raisin.Printer("searching initial values..."):
			system = {g.subs(parameters_values):d.subs(parameters_values) for g,d in initial_conditions.items()}#on commence la aussi par l'application numerique
			chec_is_numerical(system, parameters_values)									#il est important que l'on ne soit plus en literal mais purement en numerique
			system = initial_conditions_replacement(system, eq_vars)						#la aussi on remplace les variables par des polinomes
			system = append_default_conditions(system)										#on fixe a 0 les variables qui n'ont pas de conditions initiales

		with raisin.Printer("calculation of the function value...") as p:
			temps, variables = run(system, duration, recurrence_relation)					#resolution de l'equation differencielle
			return temps, variables															#on retourne le nuage de point epure

	c = Compiler(*components)
	parameters_values = {g:sympy.simplify(d) for g,d in parameters_values.items()}
	if c.get_variant_equations() == {}:							#si on a toutes les equations
		remaining_functions = c.get_vars()						#la liste de toutes les fonctions qui ne sont as encore retournee
		with raisin.Printer("send different type of equations..."):#on va les resoudre au loin
			sympy_proc = [raisin.Process(sympy_solve, {g:d}, c.initial_conditions) for g,d in c.derivate_equations.items()]#on tente une resolution formelle
			iterative_proc = [raisin.Process(iterative_solve, {g:d}, c.initial_conditions, c.get_vars(), parameters_values, duration) for g,d in c.derivate_equations.items()]
		with raisin.Printer("recuperation of the work..."):		#une fois que les calculs sont exposes
			while len(sympy_proc) and len(iterative_proc):		#tant que tous les resultats ne sont pas la, on tente de les recuperer
				for sympy_proc_rank, p in enumerate(sympy_proc):#on commence d'abord par s'occuper des equations formelles
					res = p.get_all(wait=False)					#on recupere le resultat
					if res["state"] == "finish":				#si le resultat est un bon resultat
						with raisin.Printer("injection of this result in the overs..."):#il va etre exploite au maximum
							#substitution du resultat
							c.surplus_equations = {var:e.subs(res["res"]) for var, e in c.surplus_equations.items()}#on injecte la solution de partout
							c.differencial_equations = {g.subs(res["res"]):d.subs(res["res"]) for g,d in c.differencial_equations.items()}#y compris dans les equations differencielles
							c.surplus_equations = {**c.surplus_equations, **res["res"]}#dans les equations potentiellement resolues, on y ajoute la solution fraichement trouvee
							
							rank_of_resolved_equations = []		#liste qui contient les rangs des equations a enlever
							for rank,(var, equation) in enumerate(c.surplus_equations.items()):#une fois la substitution terminee
								if equation.atoms(sympy.Function) & set(c.get_vars()) == set():#si la fonction est totalement determinee
									if var in remaining_functions:
										f_object = raisin.geometry.Function(equation.subs(parameters_values), id=var)
										#f_object = Function_sympy(var, equation.subs(parameters_values), duration)#on la met en forme dans un objet, pour plus d'uniformisation
										remaining_functions.remove(var)#on fait comprendre que cette fonction n'a plus lieu d'etre traitee
										yield f_object			#on cede l'objet
									rank_of_resolved_equations.append(rank)#comme elle est terminee, on ne veux plus quelle nous encombre
							c.surplus_equations = {g:d for i,(g,d) in enumerate(c.surplus_equations.items()) if not i in rank_of_resolved_equations}#les equations qui doivent mourir meur
							del sympy_proc[sympy_proc_rank]		#le resultats vien d'etre exploite, une fois suffit

				for iterative_proc_rank, p in enumerate(iterative_proc):#on regarde si des resultats moin formel seraient arrives
					res = p.get_all(wait=False)
					print(res)
					time.sleep(10)


#composants

class capacitor:
	def __init__(self, pin1, pin2, id, C="10**-6", U=0):
		with raisin.Printer("capacitor '"+str(id)+"' initializing..."):
			self.pin1 = pin1					#la pate + du condensateur
			self.pin2 = pin2					#la pate - du condensateur
			self.C = sympy.sympify(C)			#la capacite en Farad
			self.U = sympy.sympify(U)			#tension initiale a vide
			self.id = id						#identifiant du condensateur
			if self.pin1.current_id == None:	#si le courrant n'est pas etiquete
				self.pin1.current_id = "current_pin1_"+self.id#un nom lui est attribue
			if self.pin2.current_id == None:	#de meme pour les deux pates
				self.pin2.current_id = "current_pin2_"+self.id#car il est imperatif qu'elles aient un nom
			
			self.t = sympy.Symbol("t")			#temps simuler de la simulation	
			self.u1 = sympy.Function(self.pin1.node.id)(self.t)#potenciel de la premiere pate
			self.u2 = sympy.Function(self.pin2.node.id)(self.t)#potenciel de la deuxieme pate
			self.i1 = sympy.Function(self.pin1.current_id)(self.t)#courant de la premiere pate
			self.i2 = sympy.Function(self.pin2.current_id)(self.t)#courant de la deuxieme pate

			self.eq1 = sympy.Eq(self.i1+self.i2, 0)#loie des noeuds interne du composant
			self.eq2 = sympy.Eq(self.C*(self.u1-self.u2), self.C*self.U+sympy.integrate((self.i1-self.i2)/2, (self.t, 0, self.t)))#equation differencielle sous forme integrale

	def get_pins(self):
		"""
		genere les pins
		"""
		yield self.pin1
		yield self.pin2

	def invariant_equations(self):
		"""
		retourne une equation qui ne depend pas de l'etat du composant
		c'est une equation lineaire non differencielle
		"""
		return [self.eq1]

	def differencial_equations(self):
		"""
		retourne la liste des equations qu sont toujours vrais
		celle qui ne changent pas avec self.update()
		sont exclu les equations lineaires presentent dans self.invariant_equations()
		"""
		return [self.eq2]

	def variant_equations(self):
		"""
		retourne les equations qui changent de forme a chaque fois que self.update
		est appele
		ces equations complettent et ne remplacent pas les equations generees par self.invariant_equations et self.invarient_equations
		"""
		return []

	def get_vars(self):
		"""
		genere la liste des variables sympy
		"""
		yield self.i1
		yield self.i2
		yield self.u1
		yield self.u2

	def update(self, t, dt, solution):
		"""
		met a jour les caracteristique du composant
		cela permet de quantifier l'erreur du aux defaut de la realitee
		"""
		return None

class inductor:
	def __init__(self, pin1, pin2, id, L="10**-3", I=0):
		with raisin.Printer("inductor '"+str(id)+"' initializing..."):
			self.pin1 = pin1					#la pate + de l'inductance
			self.pin2 = pin2					#la pate - de l'inductance
			self.L = sympy.sympify(L)			#l'inductance en H en fonction du temps
			self.I = sympy.sympify(I)			#courant initiale travarssant la bobine
			self.id = id						#identifiant de la bobine
			if self.pin1.current_id == None:	#si le courrant n'est pas etiqueter
				self.pin1.current_id = "current_pin1_"+self.id#un nom lui est attribuer
			if self.pin2.current_id == None:	#de meme pour les deux pates
				self.pin2.current_id = "current_pin2_"+self.id#car il est imperatif qu'elles aient un nom

			self.t = sympy.Symbol("t")			#temps simuler de la simulation
			self.u1 = sympy.Function(self.pin1.node.id)(self.t)#potenciel de la premiere pate
			self.u2 = sympy.Function(self.pin2.node.id)(self.t)#potenciel de la deuxieme pate
			self.i1 = sympy.Function(self.pin1.current_id)(self.t)#courant de la premiere pate
			self.i2 = sympy.Function(self.pin2.current_id)(self.t)#courant de la deuxieme pate

			self.eq1 = sympy.Eq(self.i1+self.i2, 0)#loie des noeuds interne du composant
			self.eq2 = sympy.Eq(self.L*(self.i1-self.i2)/2, -self.L*self.I+sympy.integrate(self.u1-self.u2, (self.t, 0, self.t)))#equation differencielle sous forme integrale

	def get_pins(self):
		"""
		genere les pins
		"""
		yield self.pin1
		yield self.pin2

	def invariant_equations(self):
		"""
		retourne une equation qui ne depend pas de l'etat du composant
		c'est une equation lineaire non differencielle
		"""
		return [self.eq1]

	def differencial_equations(self):
		"""
		retourne la liste des equations qui sont toujours vrais
		celle qui ne changent pas avec self.update()
		sont exclu les equations lineaires presentent dans self.invariant_equations()
		"""
		return [self.eq2]

	def variant_equations(self):
		"""
		retourne les equations qui changent de forme a chaque fois que self.update
		est appele
		ces equations complettent et ne remplacent pas les equations generees par self.invariant_equations et self.invarient_equations
		"""
		return []

	def get_vars(self):
		"""
		genere la liste des variables sympy
		"""
		yield self.i1
		yield self.i2
		yield self.u1
		yield self.u2

	def update(self, t, dt, solution):
		"""
		met a jour les caracteristique du composant
		cela permet de quantifier l'erreur du aux defaut de la realitee
		"""
		return None

class reference:
	"""
	permet de fixer un potenciel a 0v
	de facon a eviter les potentiels flotants
	"""
	def __init__(self, node, id):
		with raisin.Printer("earth reference '"+str(id)+"' initializing..."):
			self.node = node					#la 'fil' qui va etre a 0 v (objet node)
			self.t = sympy.Symbol("t")			#temps simuler de la simulation
			self.u = sympy.Function(self.node.id)(self.t)#potentiel qui va etre a 0
			self.eq = sympy.Eq(self.u, 0)		#l'equation, c'est juste que le potentiel est a 0

	def get_pins(self):
		"""
		genere les pins
		"""
		for e in []:
			yield e

	def invariant_equations(self):
		"""
		retourne une equation qui ne depend pas de l'etat du composant
		c'est une equation lineaire non differencielle
		"""
		return [self.eq]

	def differencial_equations(self):
		"""
		retourne la liste des equations qui sont toujours vrais
		celle qui ne changent pas avec self.update()
		sont exclu les equations lineaires presentent dans self.invariant_equations()
		"""
		return []

	def variant_equations(self):
		"""
		retourne les equations qui changent de forme a chaque fois que self.update
		est appele
		ces equations complettent et ne remplacent pas les equations generees par self.invariant_equations et self.invarient_equations
		"""
		return []

	def get_vars(self):
		"""
		genere la liste des variables sympy
		"""
		yield self.u

	def update(self, t, dt, solution):
		"""
		met a jour les caracteristique du composant
		cela permet de quantifier l'erreur du aux defaut de la realitee
		"""
		return None

class resistor:
	def __init__(self, pin1, pin2, id, R="10**3"):
		with raisin.Printer("resistor '"+str(id)+"' initializing..."):
			self.pin1 = pin1					#la pate + de la resistance
			self.pin2 = pin2					#la pate - de la resistance
			self.R = sympy.sympify(R)			#valeur de la resistance en ohm
			self.id = id						#identifiant de la resistance
			self.t = 0							#temps depuis le debut de la simulation
			if self.pin1.current_id == None:	#si le courrant n'est pas etiqueter
				self.pin1.current_id = "current_pin1_"+self.id#un nom lui est attribuer
			if self.pin2.current_id == None:	#de meme pour les deux pates
				self.pin2.current_id = "current_pin2_"+self.id#car il est imperatif qu'elles aient un nom

			self.t = sympy.Symbol("t")
			self.dt = sympy.Symbol("dt")
			self.u1 = sympy.Function(self.pin1.node.id)(self.t)
			self.u2 = sympy.Function(self.pin2.node.id)(self.t)
			self.i1 = sympy.Function(self.pin1.current_id)(self.t)
			self.i2 = sympy.Function(self.pin2.current_id)(self.t)
			
			self.eq1 = sympy.Eq(self.i1+self.i2, 0)
			self.eq2 = sympy.Eq(self.u1-self.u2, self.R*(self.i1-self.i2)/2)

	def get_pins(self):
		"""
		genere les pins
		"""
		yield self.pin1
		yield self.pin2

	def invariant_equations(self):
		"""
		retourne une equation qui ne depend pas de l'etat du composant
		c'est une equation lineaire non differencielle
		"""
		return [self.eq1, self.eq2]

	def differencial_equations(self):
		"""
		retourne la liste des equations qu sont toujours vrais
		celle qui ne changent pas avec self.update()
		sont exclu les equations lineaires presentent dans self.invariant_equations()
		"""
		return []

	def variant_equations(self):
		"""
		retourne les equations qui changent de forme a chaque fois que self.update
		est appele
		ces equations complettent et ne remplacent pas les equations generees par self.invariant_equations et self.invarient_equations
		"""
		return []

	def get_vars(self):
		"""
		genere la liste des variables sympy
		"""
		yield self.u1
		yield self.u2
		yield self.i1
		yield self.i2

	def update(self, t, dt, solution):
		"""
		met a jour les caracteristique du composant
		cela permet de quantifier l'erreur du aux defaut de la realitee
		"""
		pass

class voltage_generator:
	def __init__(self, pin1, pin2, id, U=12):
		with raisin.Printer("voltage generator '"+str(id)+"' initializing..."):
			self.pin1 = pin1					#la pate + du generateur
			self.pin2 = pin2					#la pate - du generateur
			self.U = sympy.sympify(U)			#tension du generateur au cours du temps
			self.id = id						#identifiant du generateur
			self.t = 0							#c'est le temps depuis le debut de la simulation
			if self.pin1.current_id == None:	#si le courrant n'est pas etiquete
				self.pin1.current_id = "current_pin1_"+self.id#un nom lui est attribuer
			if self.pin2.current_id == None:	#de meme pour les deux pates
				self.pin2.current_id = "current_pin2_"+self.id#car il est imperatif qu'elles aient un nom

			self.t = sympy.Symbol("t")
			self.dt = sympy.Symbol("dt")
			self.u1 = sympy.Function(self.pin1.node.id)(self.t)
			self.u2 = sympy.Function(self.pin2.node.id)(self.t)
			self.i1 = sympy.Function(self.pin1.current_id)(self.t)
			self.i2 = sympy.Function(self.pin2.current_id)(self.t)
			
			self.eq1 = sympy.Eq(self.i1+self.i2, 0)
			self.eq2 = sympy.Eq(self.u1-self.u2, self.U)

	def get_pins(self):
		"""
		genere les pins
		"""
		yield self.pin1
		yield self.pin2

	def invariant_equations(self):
		return [self.eq1, self.eq2]

	def differencial_equations(self):
		"""
		retourne la liste des equations qu sont toujours vrais
		celle qui ne changent pas avec self.update()
		sont exclu les equations lineaires presentent dans self.invariant_equations()
		"""
		return []

	def variant_equations(self):
		"""
		retourne les equations qui changent de forme a chaque fois que self.update
		est appele
		ces equations complettent et ne remplacent pas les equations generees par self.invariant_equations et self.invarient_equations
		"""
		return []

	def get_vars(self):
		"""
		genere la liste des variables sympy
		"""
		yield self.u1
		yield self.u2
		yield self.i1
		yield self.i2

	def update(self, t, dt, solution):
		"""
		met a jour les caracteristique du composant
		cela permet de quantifier l'erreur du aux defaut de la realitee
		"""
		pass

class coil:
	def __init__(self, pin1, pin2, id, height=0.04, d1=0.008, d2=0.01, wire=0.001):
		"""
		height: longeur de l'inductance
		d1: diametre de la ferrite
		d2: diametre exterieur (fil + ferrite)
		wire: diametre du fil
		"""
		self.femm = __import__("femm")
		self.pin1 = pin1
		self.pin2 = pin2
		self.id = id
		self.height = height
		self.d1 = d1
		self.d2 = d2
		self.wire = wire
		self.turns = 100 #a calculler
		self.I = 10
		self.create_file()

	def create_file(self):
		self.femm.openfemm()
		self.femm.opendocument("inductance.fem")

		#deplacement des points
		self.femm.mi_selectnode(0,1)
		self.femm.mi_movetranslate(0, self.height-1)

		self.femm.mi_selectnode(1,1)
		self.femm.mi_movetranslate(self.d1-1, self.height-1)

		self.femm.mi_selectnode(2,1)
		self.femm.mi_movetranslate(self.d2-2, self.height-1)

		self.femm.mi_selectnode(1,0)
		self.femm.mi_movetranslate(self.d1-1, 0)

		self.femm.mi_selectnode(2,0)
		self.femm.mi_movetranslate(self.d2-2, 0)

		#deplacement de matire
		self.femm.mi_selectlabel(1.5, 0.0001)
		self.femm.mi_movetranslate2(0.5*self.d1+0.5*self.d2-1.5, 0, 2)

		self.femm.mi_setcurrent("bobine", self.I)

		self.femm.mi_selectlabel(0.5*self.d1+0.5*self.d2, 0.0001)
		self.femm.mi_setblockprop("fil", 1, 0, "bobine", 0, 0, self.turns)

		#self.femm.mi_createmesh()
		self.femm.mi_analyse(0)
