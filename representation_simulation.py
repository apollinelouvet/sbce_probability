# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 15:17:24 2018

@author: apolline l
"""

from generation_simulation import *
import os
import csv

def simulation_prm_csv(population, T, nom_du_csv):
	"""Given initial conditions and a parameter set, simulates population evolution according to the associated PRM model with seed bank.
	The number of simulated generation is entered by the user. 
	Presence/absence simulated data is recorded in a csv file.
	Caution : the first few lines of the generated csv file are the coordinates of the different tree bases, which are irrelevant in a PRM model."""
	file_name = nom_du_csv+".csv"
	file = open(file_name, 'wt')
	N = len(population.ci)
	try:
		writer = csv.writer(file, delimiter = ';')
		liste_str1 = []
		for i in range(N):
			liste_str1.append(str(population.ci.patch(i).x)+' ')
		writer.writerow(liste_str1)
		liste_str2 = []
		for i in range(N):
			liste_str2.append(str(population.ci.patch(i).y)+' ')
		writer.writerow(liste_str2)
		liste_plante = []
		for i in range(N):
			liste_plante.append(population.ci.patch(i).plante)
		writer.writerow(liste_plante)
		for j in range(T):
			population.prm_generation() 
			liste_plante = []
			for i in range(N):
				liste_plante.append(population.ci.patch(i).plante)
			writer.writerow(liste_plante)
	finally:
		file.close()

def lire_csv(nom_du_csv):
	"""Reads csv files containing standing vegetation presence/absence data. Each tree base have to be associated to a column, and the first two rows have to contain tree bases coordinates. 
	From the third row onwards, a row = a year. The timestep between two rows is of one year."""
	lecture_csv = []
	compteur = 0
    
	if type(nom_du_csv) == type('Hello world'):
		file_name = nom_du_csv+'.csv'
		file = open(file_name, 'rt')
	else :
		file = nom_du_csv
    
	reader = csv.reader(file, delimiter = ';')
	for row in reader :
		if compteur == 0:
			abs = row
			compteur += 1
		elif compteur == 1:
			ord = row
			compteur += 1
		else :
			lecture_csv.append(row)
            
	file.close()
	return(lecture_csv, abs, ord)
      
if __name__ == "__main__":
	modele = ModPRM(Decimal('0.1'), Decimal('0.5'), Decimal('0.8'), Decimal('0.8'), Decimal('1'))
	pop = generation_CI_complet_prm(50, Decimal('0.5'), Decimal('0.1'), Decimal('0.5'), modele)
	simulation_prm_csv(pop, 20, 'test1')
    
