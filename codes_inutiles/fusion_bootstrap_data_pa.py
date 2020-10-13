# -*- coding: utf-8 -*-
"""
Created on Mon Sep 07 09:35:09 2020

@author: apolline l
"""

#import numpy as np
#import matplotlib.pyplot as plt
import random as rd
import os
import csv
from representation_simulation import *
from algo_EM_PRM import *

data = 'dataset.csv'

liste_2013 = ['Capsella bursa-pastoris', 'Chenopodium album', 'Hordeum murinum', 'Lactuca serriola', 'Plantago lanceolata', 'Plantago major', 'Polygonum aviculare', 'Senecio inaequidens', 'Senecio vulgaris', 'Stellaria media', 'Taraxacum']

#Liste des rues
def liste_rues() :
	liste_rue = []
	file_data = open(data, 'rt')
	reader = csv.reader(file_data, delimiter = ',')
	for row in reader :
		if row[1] not in liste_rue :
		    liste_rue.append(row[1])
	file_data.close()
	return liste_rue

#Liste des especes presentes 
def liste_especes() :
	liste_espece = []
	file_data = open(data, 'rt')
	reader = csv.reader(file_data, delimiter = ',')
	for row in reader :
		if row[4] not in liste_espece :
		    liste_espece.append(row[4])
	file_data.close()

	return liste_espece

#Liste des pieds d'arbres dans une rue
def liste_pa_rue(nom_rue) :
	liste_pa = []
	file_data = open(data, 'rt')
	reader = csv.reader(file_data, delimiter = ',')
	for row in reader :
		if row[1] == nom_rue and row[3] not in liste_pa :
		    liste_pa.append(row[3])		    
	file_data.close()
	return liste_pa

#Creation des csvs d'observations (critère : au moins 1 patch)

def liste_presence(espece, rue) :
	liste_pa = liste_pa_rue(rue)
	liste_occ_init = [0 for i in range(len(liste_pa))]

	file_data = open(data, 'rt')
	reader = csv.reader(file_data, delimiter = ',')
	for row in reader :
		if row[1] == rue and row[4] == espece :
		    liste_occ_init[liste_pa.index(row[3])] = 1		    
	file_data.close()

	return liste_occ_init, liste_pa

def extraction_presence(espece, rue) :
	liste_occ_init, liste_pa = liste_presence(espece,rue)
	
	liste_occ = []
	
	for i in range(len(liste_occ_init)):
		if liste_occ_init[i] != 0 :
			liste_occ.append(liste_pa[i])
	
	return liste_occ

liste_an = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']	

#Generation de nouveaux jeux de donnees par bootstrap
def generation_bootstrap(espece_gb, rue_gb, liste_pa_interet_gb):
	liste_pa_bootstrap = [liste_pa_interet_gb.index(rd.choice(liste_pa_interet_gb)) for i in range(len(liste_pa_interet_gb))]
	liste_obs_bootstrap = [[] for j in range(len(liste_an))]

	for j in range(len(liste_an)) :
		for pa in liste_pa_bootstrap :
			liste_obs_bootstrap[j].append(liste_obs_fusion[j][pa])	
	str_rue = ''
	for rue in rue_gb :
		str_rue = str_rue + rue
	file_res = open('temp_bs_'+espece_gb+str_rue+'.csv', 'wt')
	writer = csv.writer(file_res, delimiter = ';')
	writer.writerow([0 for i in range(len(liste_pa_interet_gb))])
	writer.writerow([0 for i in range(len(liste_pa_interet_gb))])
	for row in liste_obs_bootstrap :
		writer.writerow(row)
	file_res.close()

################
#Code principal#
################

#Choix de l'espece et de la rue
espece = 'Senecio inaequidens'
liste_complete_rue = [['KESS', 'RAPE', 'CHAR', 'BARO', 'BERC', 'BERY', 'DAUM', 'RBER']]
#liste_complete_rue = [['LACH'], ['MONT'], ['POMM'], ['RAPE'], ['RBER'], ['REUI'], ['TAIN']]
#liste_complete_rue = [['BARO'], ['BATA'], ['BERC'], ['BERY'], ['CHAR'], ['DAUM'], ['KESS']]


for liste_rue in liste_complete_rue :
	liste_obs_fusion = [[] for j in range(len(liste_an))]
	liste_pa_interet_total = []

	#Extraction des paires d'interet
	for rue in liste_rue :
		liste_pa_interet = extraction_presence(espece, rue)
		liste_obs = [[0 for i in range(len(liste_pa_interet))] for j in range(len(liste_an))]
		file_data = open(data, 'rt')
		reader = csv.reader(file_data, delimiter = ',')
		for row in reader :
			if row[4] == espece and row[1] == rue:
				liste_obs[liste_an.index(row[2])][liste_pa_interet.index(row[3])] = 1
		file_data.close()
		for j in range(len(liste_an)) :
			for elem in liste_obs[j] :
				liste_obs_fusion[j].append(elem)
		for pa in liste_pa_interet :
			liste_pa_interet_total.append(pa)

	#A la fin de cette etape : on a la liste des observations
	#Nombre de pieds d'arbre
	nbr_pa = len(liste_obs_fusion[0])
	print(nbr_pa)
	print(len(liste_pa_interet_total))

	nbr_tests = 1000
	liste_sbce_est = []
	liste_g_est = []
	liste_c_est = []
	liste_d_est = []
	liste_pi_est = []
		
	for nbr in range(nbr_tests):
		if nbr % 10 == 1:
			print('Etape '+str(nbr))
			str_rue = ''
			for rue in liste_rue :
				str_rue = str_rue + rue
			print('Espece '+espece+' et rue '+str_rue)
			print(str(sum(liste_sbce_est)/len(liste_sbce_est)))
		#Si l'espece est presente en 2013
		generation_bootstrap(espece, liste_rue, liste_pa_interet_total)
		str_rue = ''
		for rue in liste_rue :
			str_rue = str_rue + rue
		data_bootstrap = lire_colonne_csv(lire_csv('temp_bs_'+espece+str_rue))
		mod_avec_BGS = ModPRM(Decimal(rd.uniform(0,1)), 1, Decimal(rd.uniform(0,1)), Decimal(rd.uniform(0,1)), Decimal(rd.uniform(0,1))) #Tirage des CI
		if espece in liste_2013 :
			try :
				for i in range(200): 
					resultat = etape_EM_PRM_BGS(data_bootstrap,mod_avec_BGS)
					mod_avec_BGS = resultat[0]
			
				val1 = 1 - (1-resultat[0].d)*(1-resultat[0].c)*(1-resultat[0].g)

				if val1 > 0:
					val2 = resultat[0].g*(1-resultat[0].d)*(1-resultat[0].c)*(1-resultat[0].g)/val1
			   
				else :
					val2 = 0

				liste_sbce_est.append(val2)
				liste_g_est.append(resultat[0].g)
				liste_c_est.append(resultat[0].c)
				liste_d_est.append(resultat[0].d)
				liste_pi_est.append(resultat[0].pi)
			except :
				print('Estimation could not be carried out')

		#Sinon
		else :
			try :
				for i in range(200): 
					liste_annees = [2009, 2010, 2011, 2012, 2014, 2015, 2016, 2017, 2018]
					resultat = etape_EM_PRM_BGS_na(data_bootstrap,mod_avec_BGS, 4)
					mod_avec_BGS = resultat[0]
				
					val1 = 1 - (1-resultat[0].d)*(1-resultat[0].c)*(1-resultat[0].g)

					if val1 > 0:
						val2 = resultat[0].g*(1-resultat[0].d)*(1-resultat[0].c)*(1-resultat[0].g)/val1
				   
					else :
						val2 = 0

				liste_sbce_est.append(val2)
				liste_g_est.append(resultat[0].g)
				liste_c_est.append(resultat[0].c)
				liste_d_est.append(resultat[0].d)
				liste_pi_est.append(resultat[0].pi)
			except :
				print('Estimation could not be carried out')

	str_rue = ''
	for rue in liste_rue :
		str_rue = str_rue + rue
	file_res = open('bootstrap_'+espece+str_rue+'.csv', 'wt')
	writer = csv.writer(file_res, delimiter = ';')
	writer.writerow(['SBCE', 'g', 'c', 'd', 'pi'])
	for i in range(len(liste_sbce_est)):
		writer.writerow([liste_sbce_est[i], liste_g_est[i], liste_c_est[i], liste_d_est[i], liste_pi_est[i]])
	file_res.close()




