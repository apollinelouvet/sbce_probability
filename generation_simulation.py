# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 17:16:41 2018

@author: apolline l
"""

#import matplotlib.pyplot as plt
#import numpy as np
import random as rd
from decimal import * 

### Caution ###
#Pay attention to the potential use of capital letters in function and class names, especially regarding PRM/prm, as the code doesn't consistently use one or the other.

class PiedArbre(object):
	"""Class defining a 'tree base' object, characterized by the geographical location of its center, standing vegetation presence and seed bank presence."""
    
	def __init__(self, abs, ord, plante, graine): #Generator of the class
		"""Takes as arguments the coordinates of the center, the presence or absence of standing vegetation and of seeds.
		Caution : center coordinates can not be modified after patch creation.
		Example : PiedArbre(1, 2, 0, 1) represents a patch whose center is at (1,2), containing seeds but not standing vegetation."""   
		try:
			if plante != 0 and plante != 1:
				raise Warning("Warning : standing vegetation status was not entered at the desired format (0/1). Tree base will not be created.")
			elif graine != 0 and graine != 1:
				raise Warning("Warning : standing vegetation status was not entered at the desired format (0/1). Tree base will not be created.")
		except Warning as e:
			print(e)
		else:
			self._x = abs
			self._y = ord
			self.plante = plante
			self.graine = graine
    
	#Methods blocking coordinates modification
	def get_x(self):
		return self._x
    
	def set_x(self, new):
		print("Error : tree base coordinates are not modifiable")
            
	def get_y(self):
		return self._y
    
	def set_y(self, new):
		print("Error : tree base coordinates are not modifiable")    
    
	x = property(get_x, set_x)
	y = property(get_y, set_y)
    
	def affiche(self):
		"""Prints tree base charateristics in a readable way. Returns a list containing center coordinates, standing vegetation status and seed bank status.
		Ex : PiedArbre(1, 2, 0, 1).affiche returns
		=> [1, 2, 0, 1] """
		return([self.x, self.y, self.plante, self.graine])
    
	#(french speaking) user-friendly methods for updating standing vegetation and seed bank status
	def nais_plante(self):
		self.plante = 1
    
	def mort_plante(self):
		self.plante = 0
    
	def nais_graine(self):
		self.graine = 1
    
	def mort_graine(self):
		self.graine = 0

class Milieu(PiedArbre):
	"""Class defining a set of tree bases. """
    
	def __init__(self, liste): #Generator of the class
		"""Takes as arguments a list of PiedArbre objects. A list of tree base coordinates is automatically created and associated to the object."""
		self.liste = liste
		coords = []
		for elem in liste:
			coords.append([elem.x, elem.y])
		self._coord = coords
    
	#Method blocking patch coordinates modification
	def get_coord(self):
		return self._coord
    
	def set_coord(self, new):
		print("Error : tree base coordinates are not modifiable") 
    
	coord = property(get_coord, set_coord)
    
	def patch(self,indice):
		"""Extracts the tree base of indice i from the list."""
		return self.liste[indice]
    
	def repres_patch(self, indice):
		"""Extracts the tree base of indice i from the list, and prints it in a readable way."""
		return self.liste[indice].affiche()
    
	#Methods giving the number of tree bases
	#Method using how tree bases are represented as part of the Milieu object
	def __len__(self):
		return len(self.liste)
 
	#Another method more user-friendly
	def nbr(self):
		"""Returns the number of tree bases."""
		return len(self.liste)

	def esp(self):
		"""Returns the list of standing vegetation status for each tree base."""
		espece = []
		for pied in self.liste:
			espece.append(pied.plante)
		return espece
    
	def bg(self):
		"""Returns the list of seed bank status for each tree base."""
		bgraine = []
		for pied in self.liste:
			bgraine.append(pied.graine)
		return bgraine

class ModPRM(object):
	"""Class defining a parameter set for a PRM model with a seed bank. 
	The parameter set comprises colonization probability, persistance probability, germination probability and seed bank death probability. Initial proportion of seeds can also be added as a supplementary argument. 
	Persistance probability is to be set to 1 to get the PRM model with seed bank used in the article.
	A model without seed bank can be encoded setting persistance probability and seed bank death probability to 1.
	Caution : probabilities should be entered using the cdecimal format."""

	def __init__(self, col, per, germ, mor, pro = 'na'):
		try:
			#Check that parameter values entered really correspond to probabilities
			assert 0 <= col <= 1
			assert 0 <= per <= 1
			assert 0 <= germ <= 1
			assert 0 <= mor <= 1
			if type(pro) != str:
				assert 0 <= pro <= 1
			#Check that float module wasn't used instead of cdecimal module. Otherwise, a warning is raised, and the float is converted to a cdecimal (raising a warning).
			if type(col) == float:
				raise Warning("Warning : rounding errors are likely to happen. Cdecimal module should be prefered to float one.")
				col = Decimal(col)
			elif type(per) == float :
				raise Warning("Warning : rounding errors are likely to happen. Cdecimal module should be prefered to float one.")
				per = Decimal(per)
			elif type(germ) == float :
				raise Warning("Warning : rounding errors are likely to happen. Cdecimal module should be prefered to float one.")
				germ = Decimal(germ)
			elif type(mor) == float :
				raise Warning("Warning : rounding errors are likely to happen. Cdecimal module should be prefered to float one.")
				mor = Decimal(mor)
			elif type(pro) != 'na':
				if type(pro) == float :
					raise Warning("Warning : rounding errors are likely to happen. Cdecimal module should be prefered to float one.")
					pro = Decimal(pro)
		except AssertionError :
			print('Errors : probabilities are to be in [0,1]')
		except Warning as e :
			print(e)
		else :
			self._c = col
			self._p = per
			self._g = germ
			self._d = mor
			self._pi = pro
    
	#Methods for blocking parameter modification
	def get_c(self):
		return self._c
    
	def set_c(self, new):
		print('Error : model parameters are not modifiable.')
    
	c = property(get_c, set_c)
    
	def get_p(self):
		return self._p
    
	def set_p(self, new):
		print('Error : model parameters are not modifiable.')
    
	p = property(get_p, set_p)
    
	def get_g(self):
		return self._g
        
	def set_g(self, new):
		print('Error : model parameters are not modifiable.')
    
	g = property(get_g, set_g)
    
	def get_d(self):
		return self._d
    
	def set_d(self, new):
		print('Error : model parameters are not modifiable.')
    
	d = property(get_d, set_d)
    
	def get_pi(self):
		return self._pi
    
	def set_pi(self, new):
		print('Error : model parameters are not modifiable.')
    
	pi = property(get_pi, set_pi)
    
	def affiche(self):
		"""Prints PRM model parameter in a readable way."""
		return([self.c, self.p, self.g, self.d, self.pi])
    
	def matrice_transition_prm(self):
		"""Return the transition matrix associated to the PRM model with seed bank."""
		mat = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		mat[0][0] = 1 - self.c
		mat[0][1] = self.c*(1-self.g)
		mat[0][2] = self.g*self.c
		mat[1][0] = self.d*(1-self.c)
		mat[1][1] = ((1 - self.d + self.d*self.c)*(1-self.g))
		mat[1][2] = self.g*(self.d*self.c + 1 - self.d)
		mat[2][0] = self.d*(1-self.c)*(1-self.p)
		mat[2][1] = (1 - self.d + self.d*self.p + self.d*self.c*(1-self.p))*(1-self.g)
		mat[2][2] = self.g*(1 - self.d + self.d*self.p + (1-self.p)*self.d*self.c)
		return mat
       
class ReproPRM(PiedArbre):
	"""Class modelling reproduction process."""
	def __init__(self, param, conditions_initiales):
		self.mod = param
		self.ci = conditions_initiales
    
	def germ_exp(self):
		"""Makes each tree base germinate independently with the same germination probability, irrelevant of seed bank age."""
		nbr_pieds = len(self.ci)
		for i in range(nbr_pieds):
			pied = self.ci.patch(i)
			if pied.graine == 1:
				if rd.uniform(0,1) <= self.mod.g:
					pied.nais_plante() #Remark : no need to make the seed bank die since standing vegetation will refill it anyway
    
	def reproprm(self):
		"""Makes seed bank die and standing vegetation produce new seeds."""
		nbr_pieds = len(self.ci)
		for i in range(nbr_pieds):
			pied = self.ci.patch(i)
			if pied.graine ==1:
				if rd.uniform(0,1) <= self.mod.d: #Seed bank dies with probability d
					pied.mort_graine()
			if pied.plante == 1:
				pied.mort_plante() #Plants die after one year
				if rd.uniform(0,1) <= self.mod.p: #(here p = 1) standing vegetation produce new seeds
					pied.nais_graine()
			if rd.uniform(0,1) <= self.mod.c: #New seeds come from outside with probability c
				pied.nais_graine()
    
	def prm_generation(self):
		"""Models complete reproductive cycle according to the PRM model with seed bank."""
		self.reproprm()
		self.germ_exp()

#The following class is used for initial condition generation, but is not to be used alone - the function below is to be preferred
class GenerateurCI():
	"""Class allowing automatic generation of a set of tree bases. Takes as arguments the tree base number, the initial proportion of seeds, and two extra arguments.
	The two extra arguments are not used here, they can be set to $0$ (or whatever value)."""
	def __init__(self, npatch, pgraines, pasx, pasy):
		self.N = npatch
		self.pg = pgraines
		self.dx = pasx
		self.dy = pasy
    
	def generation_unif(self):
		"""Generates a set of tree bases where each tree base is assigned or not a seed bank, uniformly and independently."""
		liste = []
		for i in range(self.N):
			etat_g = rd.uniform(0,1)
			if etat_g <= self.pg:
				liste.append(PiedArbre(self.dx*i, self.dy*i, 0, 1))
			else:
				liste.append(PiedArbre(self.dx*i, self.dy*i, 0, 0))
		return liste

	#Note that since there is no spatial structure in the PRM model, no need initial condition needs to be tested.

#Function to use in order to generate initial conditions
def generation_CI_complet_prm(n_patch, prop_init, dx, dy, modele):
	"""Generates automatically a set of tree bases with standing vegetation and seed bank already present."""
	try :
		if type(modele.pi) != type('hello world'): #Check if an initial proportion of seeds was indicated in the PRM model or not
			assert modele.pi == prop_init
	except AssertionError :
		print("Warning : PRM model initial proportion of seeds differs from the one indicated in argument. Only the PRM model one will be used.")
		prop_init = modele.pi #If there is a conflict, then the PRM model one is to be used
	finally: 
		gen_CI = GenerateurCI(n_patch, prop_init, dx, dy)
		milieu = Milieu(gen_CI.generation_unif()) 
		pop = ReproPRM(modele, milieu)
		pop.germ_exp()
		return(pop)

if __name__ == "__main__":
	modele = ModPRM(Decimal('0.6'), Decimal('0.4'), Decimal('0.7'), Decimal('0.8'), Decimal('0.7'))
	pop = generation_CI_complet_prm(50, Decimal('0.5'), Decimal('0.1'), Decimal('0.5'), modele)
	pop.prm_generation()
    
