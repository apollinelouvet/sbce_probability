# -*- coding: utf-8 -*-
"""
Created on Thu Oct 08 09:35:09 2020

@author: apolline l
"""

import random as rd
import os
import csv
from representation_simulation import *
from algo_EM_PRM import *

#Indicate below the name of the file to be used for analysis, without 
#indicating the .csv extension
#(Warning : the file has to be in the same folder as the code)

name_file_without_extension = 'test'

#Indicate below the observation year missing. The first observation year is numberered as 0.
year = 4

#########################
#Part not to be modified#
#########################

data = lire_colonne_csv(lire_csv(name_file_without_extension))
mod_avec_BGS = ModPRM(Decimal(rd.uniform(0,1)), 1, Decimal(rd.uniform(0,1)), Decimal(rd.uniform(0,1)), Decimal(rd.uniform(0,1))) #Tirage des CI

print('Parameter estimation')

try :
	for i in range(200): 
		resultat = etape_EM_PRM_BGS_na(data,mod_avec_BGS,year)
		mod_avec_BGS = resultat[0]

	val1 = 1 - (1-resultat[0].d)*(1-resultat[0].c)*(1-resultat[0].g)

	if val1 > 0:
		val2 = resultat[0].g*(1-resultat[0].d)*(1-resultat[0].c)*(1-resultat[0].g)/val1
   
	else :
		val2 = 0
		
	print('Estimated SBCE probability = '+str(val2))
	print('AIC on parameter estimation ='+str(resultat[2]))

except :
	print('Error : Estimation could not be carried out')

