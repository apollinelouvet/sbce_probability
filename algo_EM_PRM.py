#!/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 11:34:23 2018

@author: apolline l
"""

import generation_simulation as gs
import representation_simulation as rs
import random as rd
#import numpy as np
#from numpy import *
from decimal import *

#############################################################
#Reading the dataset, and introducing potential errors in it#
#############################################################

#Potentially useful function (not used much in the code though)
def lecture_data(nom_du_csv):
	"""Reads the csv file and returns presence/absence data only."""
	return rs.lire_csv(nom_du_csv)[0]

#Function to use along with lire_csv in order to get the presence/absence data in a suitable format
def lire_colonne_csv(lecture_csv):
	"""Takes as argument a reading of a csv file performed by lire_csv. Reorganizes the content per tree base instead of per year."""
	data = lecture_csv[0]
	nbr_pa = len(data[0])
	liste_pa = []
	for i in range(nbr_pa):
		pa = []
		for j in range(len(data)):
			if data[j][i] == 'na':
				pa.append(data[j][i])
			else:
				pa.append(int(data[j][i]))
		liste_pa.append(ListePlante(pa[:]))
	return liste_pa

###Functions used in tests###

#Function used to introduce false negatives
#def lire_colonne_csv_erreur(lecture_csv, proba_erreur): 
#	"""Same as lire_colonne_csv but introducing extra false negatives."""
#	data = lecture_csv[0]
#	nbr_pa = len(data[0])
#	liste_pa = []
#	for i in range(nbr_pa):
#		pa = []
#		for j in range(len(data)):
#			if data[j][i] == 'na':
#				pa.append(data[j][i])
#			else:
#				val_pres = int(data[j][i])
#				if val_pres == 0 :
#					pa.append(val_pres)
#		elif rd.uniform(0, 1) <= proba_erreur :
#		    print('Faux negatif')
#		    pa.append(0)
#		else :
#		    pa.append(val_pres)
#       liste_pa.append(ListePlante(pa[:]))
#    return liste_pa

#Function used to introduce false positives
#def lire_colonne_csv_erreur_positif(lecture_csv, proba_erreur): 
#    """Same as lire_colonne_csv but introducing extra false positives."""
#    data = lecture_csv[0]
#    nbr_pa = len(data[0])
#    liste_pa = []
#    for i in range(nbr_pa):
#        pa = []
#        for j in range(len(data)):
#            if data[j][i] == 'na':
#                pa.append(data[j][i])
#            else:
#		val_pres = int(data[j][i])
#                if val_pres == 1 :
#		    pa.append(val_pres)
#		elif rd.uniform(0, 1) <= proba_erreur :
#		    print('Faux positif')
#		    pa.append(1)
#		else :
#		    pa.append(val_pres)
#        liste_pa.append(ListePlante(pa[:]))
#    return liste_pa

#Format de stockage des informations du fichier
class ListePlante(object):
    """Associated to a given tree base. Encodes the list of observations for each year."""
    
    def __init__(self, liste):
        """Takes as argument the list of observations."""
        self.plante = liste
        self.tps = len(liste)
        try :
            for value in liste: #Check that the observations are at the required format
                assert value in [1, 0, 'na', '1', '0', '1.0', '0.0'] #'na' stands for missing data
        except AssertionError:
            print('Warning : some observations were not at the required format. They were recorded as missing data.')
        finally :
            for i in range(self.tps): #Ensure consistency of representation of presence and absence data inside the list 
                value = liste[i]
                if value in ['1', '1.0']: #Presence
                    liste[i] = 1
                if value in ['0', '0.0']: #Absence
                    liste[i] = 0
                if value not in [1, 0, 'na', '1', '0', '1.0', '0.0']: #Missing
                    liste[i] = 'na'
    
    #Methods to access and modify the list of observations
    def __getitem__(self, index):
        return self.plante[index]
    
    def __setitem__(self, index, value):
        try:
            assert value in [1, 0, 'na']
        except AssertionError :
            print("Warning : observation data is not formatted properly")
        else:
            self.plante[index] = value
    
    def __len__(self):
        return self.tps
    
    def complete(self, index, value):
        """Changes one observation"""
        self[index] = value
    
    def affiche(self):
        """Print the list of observations."""
        return self.plante

###############################
#Estimation pour le modele PRM#
###############################

#Forward-backward algorithm
#Uses a rescaling to prevent rounding-related issues
#Remark : will be applied patch by patch

def algo_fb_prm_rescale(patch, modprm):
    """Forward-backward algorithm.
    Caution : requires a complete observation set. """
    try : #Check that there is no missing data
        assert 'na' not in patch.plante
    except AssertionError:
        print("Error : missing data.")
    #Step 1 : sets containing values for alpha and beta are created
    alpha = [0 for i in range(patch.tps)] #Forward probas
    beta = [0 for i in range(patch.tps)] #Backward probas
    coef = [Decimal('1.0') for i in range(patch.tps)] #For rescaling
    mat = modprm.matrice_transition_prm() #Transition matrix
    
    #Etape 2 : initialisations
    #Pour alpha
    if patch[0] == 0: #If no seed germinated
        alpha[0] = [1 - modprm.pi, modprm.pi*(1-modprm.g), Decimal('0.0')] #Either there were no seeds, either it didn't germinate
    else :
        alpha[0] = [Decimal('0.0'), Decimal('0.0'), modprm.pi*modprm.g] #There were seeds, and they germinated
    
    #Etape 3 : completion par recurrence
    #Pour alpha
    for i in range(1, patch.tps):
	#Write the probabilities of all possible transitions
        alpha_0 = alpha[i-1][0]*mat[0][0] + alpha[i-1][1]*mat[1][0] + alpha[i-1][2]*mat[2][0] 
        alpha_1 = alpha[i-1][0]*mat[0][1] + alpha[i-1][1]*mat[1][1] + alpha[i-1][2]*mat[2][1]
        alpha_2 = alpha[i-1][0]*mat[0][2] + alpha[i-1][1]*mat[1][2] + alpha[i-1][2]*mat[2][2]
        alpha_0 *= (1-patch[i]) #Can't happen if there is standing vegetation
        alpha_1 *= (1-patch[i])
        alpha_2 *= patch[i] #Can't happen if there is no standing vegetation
        somme = alpha_0 + alpha_1 + alpha_2 #Used for rescaling
        alpha_0 /= somme
        alpha_1 /= somme
        alpha_2 /= somme
        alpha[i] = [alpha_0, alpha_1, alpha_2]
        coef[i] = somme #Rescaling coefficient is kept
    #Pour beta
    #Etape 2
    beta[-1] = [Decimal('1.0')/coef[-1], Decimal('1.0')/coef[-1], Decimal('1.0')/coef[-1]] #Initialization
    for i in range(patch.tps-2, -1, -1):
	#Probabilities of all possible transitions, taking into account some transitions were not possible
        beta_0 = mat[0][0]*beta[i+1][0]*(1-patch[i+1]) + mat[0][1]*beta[i+1][1]*(1-patch[i+1]) + mat[0][2]*beta[i+1][2]*patch[i+1]
        beta_1 = mat[1][0]*beta[i+1][0]*(1-patch[i+1]) + mat[1][1]*beta[i+1][1]*(1-patch[i+1]) + mat[1][2]*beta[i+1][2]*patch[i+1]
        beta_2 = mat[2][0]*beta[i+1][0]*(1-patch[i+1]) + mat[2][1]*beta[i+1][1]*(1-patch[i+1]) + mat[2][2]*beta[i+1][2]*patch[i+1]
	#Rescaling
        beta_0 /= coef[i]
        beta_1 /= coef[i]
        beta_2 /= coef[i]
        beta[i] = [beta_0, beta_1, beta_2]
    return alpha, beta, coef

#Probabilité des différents états initiaux et transitions

def obs_bg_simple(alpha, beta, coef, tps, modprm):
    """For each possible state, computes the probability of the seed bank and standing vegetation of a given patch to be in that state at time tps, given observations.
    Takes as arguments what was computed with fb algorithm."""
    cst = Decimal('1.0')/sum(alpha[-1])
    liste = [0 for i in range(tps)]
    
    for i in range(tps):
        liste[i] = [cst*alpha[i][0]*beta[i][0]*coef[i], cst*alpha[i][1]*beta[i][1]*coef[i], cst*alpha[i][2]*beta[i][2]*coef[i]]
    return liste

def obs_bg_trans(alpha, beta, tps, modprm, obs_cond):
    """For each possible transition, computes the probability of it happening for a given patch at time tps, given observations. """
    cst = Decimal('1.0')/sum(alpha[-1])
    mat = modprm.matrice_transition_prm() 
    
    liste = [ [[0, 0, 0], [0, 0, 0], [0, 0, 0]] for i in range(tps-1)]
    
    for i in range(tps-1):
        liste[i][0] = [alpha[i][0]*mat[0][0]*beta[i+1][0]*(1-obs_cond[i+1])*cst, alpha[i][0]*mat[0][1]*beta[i+1][1]*(1-obs_cond[i+1])*cst, alpha[i][0]*mat[0][2]*beta[i+1][2]*(obs_cond[i+1])*cst]
        liste[i][1] = [alpha[i][1]*mat[1][0]*beta[i+1][0]*(1-obs_cond[i+1])*cst, alpha[i][1]*mat[1][1]*beta[i+1][1]*(1-obs_cond[i+1])*cst, alpha[i][1]*mat[1][2]*beta[i+1][2]*(obs_cond[i+1])*cst]
        liste[i][2] = [alpha[i][2]*mat[2][0]*beta[i+1][0]*(1-obs_cond[i+1])*cst, alpha[i][2]*mat[2][1]*beta[i+1][1]*(1-obs_cond[i+1])*cst, alpha[i][2]*mat[2][2]*beta[i+1][2]*(obs_cond[i+1])*cst]
        
    return liste

def condit_log(param):
    """Corrige les parametres de facon que le logarithme puisse etre calcule."""
    a = param
    if a <= 0.000000000000000000000000000000000000000000000000000000000000000001:
        a = Decimal('0.000000000000000000000000000000000000000000000000000000000000000001')
    if a >= 0.9999999 :
        a = Decimal('0.999999999999999999999999999999999999999999999999999999999999999999')
    return(a)

###PRM BGS###

def etape_EM_PRM_BGS(liste_obs, modprm):
    try:
        assert modprm.p == 1
    except AssertionError:
        print("Error : the model entered is not a SB+ model")
        return(modprm)
        
    api = Decimal('0.0')
    bpi = Decimal('0.0')
    ag = Decimal('0.0')
    bg = Decimal('0.0')
    ac = Decimal('0.0')
    bc = Decimal('0.0')
    ac2 = Decimal('0.0')
    bc2 = Decimal('0.0')
    vrais2 = Decimal('0.0')
    #Each tree base is treated one by one
    for obs in liste_obs:
	#Forward-backward algorithm
	#Rescaling is used to prevent rounding errors 
        algo_fb = algo_fb_prm_rescale(obs, modprm)

        alpha = algo_fb[0]
        beta = algo_fb[1]
        coef = algo_fb[2]
        
        tps = obs.tps #Time duration
        
        #vrais2 += coef[-1].ln()
        for value in coef:
            vrais2 += value.ln()
        
        proba_s = obs_bg_simple(alpha, beta, coef, tps, modprm)
        proba_t = obs_bg_trans(alpha, beta, tps, modprm, obs)
        
	#Integration of probabilities in coefficients
	#Initial conditions
        bpi += proba_s[0][0]
        api += (proba_s[0][1] + proba_s[0][2])
        
        ag += proba_s[0][2]
        bg += (proba_s[0][1])
        
	#Transitions
        for j in range(len(obs)-1):
            ag += (proba_t[j][0][2] + proba_t[j][1][2] + proba_t[j][2][2])
            bg += (proba_t[j][0][1] + proba_t[j][1][1] + proba_t[j][2][1])
            
            ac += (proba_t[j][0][1] + proba_t[j][0][2])
            bc += proba_t[j][0][0]
            
            bc2 += (proba_t[j][1][0])
            ac2 += (proba_t[j][1][1] + proba_t[j][1][2])

    #Optimisation
    npi = api/(api+bpi)
    ng = ag/(ag+bg)

    nc = ac/(ac+bc)
    nc2 = ac2/(ac2+bc2)

    if nc2 < nc:
        nc = (ac + ac2)/(ac + ac2 + bc + bc2)
        nc2 = nc        

    nd = (1-nc2)/(1-nc)    

    np = Decimal('1.0')
    
    try :
        newmod = gs.ModPRM(nc, np, ng, nd, npi) #Check if there is no error (e.g too high/low probas)
    except :
        return(modprm, 0, 10000)
    return (newmod, 0, 8 - 2*vrais2) #The 0 is a remnant from a former version of the code

#Version dealing with one year of missing data
def etape_EM_PRM_BGS_na(liste_obs, modprm, year):
    try:
        assert modprm.p == 1
    except AssertionError:
        print("Error : the model entered is not a SB+ model")
        return(modprm)
        
    api = Decimal('0.0')
    bpi = Decimal('0.0')
    ag = Decimal('0.0')
    bg = Decimal('0.0')
    ac = Decimal('0.0')
    bc = Decimal('0.0')
    ac2 = Decimal('0.0')
    bc2 = Decimal('0.0')
    vrais2 = Decimal('0.0')
    #Each tree base is treated one by one
    for obs in liste_obs:
	    #Writing the two possible completed observations
        obs_temp = obs.affiche()
        obs1 = ListePlante(obs_temp[:])
        obs0 = ListePlante(obs_temp[:])
        obs1[year] = 1
        obs0[year] = 0

	#Forward-backward algorithm
	#Rescaling is used to prevent rounding errors 
	#1 - On obs1
        algo_fb_1 = algo_fb_prm_rescale(obs1, modprm)

        alpha_1 = algo_fb_1[0]
        beta_1 = algo_fb_1[1]
        coef_1 = algo_fb_1[2]
        
        tps = obs.tps #Time duration
          
        proba_s_1 = obs_bg_simple(alpha_1, beta_1, coef_1, tps, modprm)
        proba_t_1 = obs_bg_trans(alpha_1, beta_1, tps, modprm, obs1)

	#2 - On obs0

        algo_fb_0 = algo_fb_prm_rescale(obs0, modprm)

        alpha_0 = algo_fb_0[0]
        beta_0 = algo_fb_0[1]
        coef_0 = algo_fb_0[2]
        
        tps = obs.tps #Time duration
        
        proba_s_0 = obs_bg_simple(alpha_0, beta_0, coef_0, tps, modprm)
        proba_t_0 = obs_bg_trans(alpha_0, beta_0, tps, modprm, obs0)

        #Computation of coefficients
        proba0 = sum(alpha_0[-1])
        for coef in coef_0 :
            proba0 *= coef
	
        proba1 = sum(alpha_1[-1])
        for coef in coef_1 :
            proba1 *= coef

        cond0 = proba0/(proba0+proba1)
        cond1 = proba1/(proba0+proba1)
        
	#Integration of probabilities in coefficients
	#Initial conditions
	#For obs0
        bpi += proba_s_0[0][0]*cond0
        api += (proba_s_0[0][1] + proba_s_0[0][2])*cond0
        
        ag += proba_s_0[0][2]*cond0
        bg += (proba_s_0[0][1])*cond0

	#For obs1
        bpi += proba_s_1[0][0]*cond1
        api += (proba_s_1[0][1] + proba_s_1[0][2])*cond1
        
        ag += proba_s_1[0][2]*cond1
        bg += (proba_s_1[0][1])*cond1
        
	#Transitions
        for j in range(len(obs)-1):
	    #For obs0
            ag += (proba_t_0[j][0][2] + proba_t_0[j][1][2] + proba_t_0[j][2][2])*cond0
            bg += (proba_t_0[j][0][1] + proba_t_0[j][1][1] + proba_t_0[j][2][1])*cond0
            
            ac += (proba_t_0[j][0][1] + proba_t_0[j][0][2])*cond0
            bc += proba_t_0[j][0][0]*cond0
            
            bc2 += (proba_t_0[j][1][0])*cond0
            ac2 += (proba_t_0[j][1][1] + proba_t_0[j][1][2])*cond0

	    #For obs1
            ag += (proba_t_1[j][0][2] + proba_t_1[j][1][2] + proba_t_1[j][2][2])*cond1
            bg += (proba_t_1[j][0][1] + proba_t_1[j][1][1] + proba_t_1[j][2][1])*cond1
            
            ac += (proba_t_1[j][0][1] + proba_t_1[j][0][2])*cond1
            bc += proba_t_1[j][0][0]*cond1
            
            bc2 += (proba_t_1[j][1][0])*cond1
            ac2 += (proba_t_1[j][1][1] + proba_t_1[j][1][2])*cond1

    #Optimisation
    npi = api/(api+bpi)
    if npi > Decimal('0.999999') :
        npi = Decimal('0.999999')
    if npi < Decimal('0.000001'):
        npi = Decimal('0.000001')

    ng = ag/(ag+bg)
    if ng > Decimal('0.999999') :
        ng = Decimal('0.999999')
    if ng < Decimal('0.000001'):
        ng = Decimal('0.000001')

    nc = ac/(ac+bc)
    if nc > Decimal('0.999999') :
        nc = Decimal('0.999999')
    if nc < Decimal('0.000001'):
        nc = Decimal('0.000001')

    nc2 = ac2/(ac2+bc2)
    if nc2 > Decimal('0.999999') :
        nc2 = Decimal('0.999999')
    if nc2 < Decimal('0.000001'):
        nc2 = Decimal('0.000001')

    if nc2 < nc:
        nc = (ac + ac2)/(ac + ac2 + bc + bc2)

        nc2 = nc        

    nd = (1-nc2)/(1-nc)    

    np = Decimal('1.0')

    vrais_c = api*npi.ln() + bpi*((1-npi).ln()) + ag*ng.ln() + bg*((1-ng).ln())
    vrais_c += ac*nc.ln() + bc*((1-nc).ln()) + ac2*nc2.ln() + bc2*((1-nc2).ln())
    
    try :
        newmod = gs.ModPRM(nc, np, ng, nd, npi) #Check if there is no error (e.g too high/low probas)
    except :
        return(modprm, 0, 10000)
    return (newmod, 0, 8-2*vrais_c) #The 0 is a remnant from a former version of the code


########################################
#Test du fonctionnement des estimateurs#
########################################

if __name__ == '__main__':
    #En Levins, on peut descendre à 19 d'AIC avec ce jeu
    abscisse = [0.45, 0.52]
    ordonnee = [0.1, 0.2]
    a = Decimal('0.2')
    y = Decimal('0.6')
    an = [2013, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023]
    patch_ex = ListePlante([0, 1, 1, 1, 0, 1, 0, 1, 0]) 
    patch_ex2 = ListePlante([1, 1, 1, 0, 1, 0, 1, 1, 0])
    #levins_ex = gs.ModLevins(a, y, Decimal('1'), Decimal('0.5'), Decimal('0.5'), Decimal('0.5'))
    prm_ex = gs.ModPRM(Decimal('0.6'), Decimal('0.4'), Decimal('0.5'), Decimal('0.4'), Decimal('0.5'))
    for i in range(100):
        res = etape_EM_PRM_BGS_na([patch_ex, patch_ex2], prm_ex, an)
        print(res)
        print(res[0])
        prm_ex = res[0]
        #res = etape_EM_PRM_BGS_pen([patch_ex, patch_ex2], prm_ex, Decimal('20'), Decimal('0.4'))
        print(res[2])
    print(res[0].c, res[0].g, res[0].d, res[0].pi)
    matrice = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    print(puis_matrice_33(matrice))



      
    
