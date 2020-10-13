# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:17:24 2020

@author: apolline l
"""

import csv

file_liste_tests = open('liste_bootstrap.csv', 'rb')
reader = csv.reader(file_liste_tests, delimiter = ',')
liste_tests = []

compt = 0
for row in reader :
    if compt != 0:
        if row[1] != 'NA' :
            liste_tests.append([row[0], row[1]])
    else :
        compt = 1
        
file_liste_tests.close()
        
liste_icmin = []
liste_icmax = []
liste_nbr_inf = []

for test in liste_tests :
    print(test)
    espece = test[0]
    rue = test[1]
    
    liste_g = []
    
    file_test = open('bootstrap_'+espece+rue+'.csv', 'rb')
    reader = csv.reader(file_test, delimiter = ';')
    
    count = 0    
    
    for row in reader :
        if count != 0 :
            liste_g.append(float(row[1]))
        else :
            count = 1
    
    liste_g.sort()
    liste_icmin.append(liste_g[24])
    liste_icmax.append(liste_g[974])
    
    file_test.close()

file_res = open('resultat_analyse_bootstrap_g.csv', 'wb')
writer = csv.writer(file_res, delimiter = ',')

for i in range(len(liste_tests)) :
    writer.writerow([liste_tests[i][0], liste_tests[i][1], liste_icmin[i], liste_icmax[i]])

file_res.close()


    
    
            
    
