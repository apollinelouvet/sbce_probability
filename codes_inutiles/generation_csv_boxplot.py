# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:04:01 2020

@author: apolline.louvet
"""

import csv

#Liste des rues
file_liste_tests = open('liste_bootstrap.csv', 'rb')
reader = csv.reader(file_liste_tests, delimiter = ',')
liste_rue = []

compt = 0
for row in reader :
    if compt != 0:
        if row[1] != 'NA' and row[1] not in liste_rue :
            liste_rue.append(row[1])
    else :
        compt = 1
        
file_liste_tests.close()

#Pour chaque rue, liste des especes
for rue in liste_rue:
    print(rue)
    liste_espece = []
    file_liste_tests = open('liste_bootstrap.csv', 'rb')
    reader = csv.reader(file_liste_tests, delimiter = ',')
    
    compt = 0
    for row in reader :
        if compt != 0:
            if row[1] == rue :
                liste_espece.append(row[0])
        else :
            compt = 1
    
    file_liste_tests.close()
    
    #Generation du csv
    file_concat = open('liste_'+rue+'.csv', 'wb')
    writer = csv.writer(file_concat, delimiter = ',')
    
    writer.writerow(['espece', 'SBCE'])
    
    for espece in liste_espece :
        file_bootstrap = open('bootstrap_'+espece+rue+'.csv', 'rb')
        reader = csv.reader(file_bootstrap, delimiter = ';')
        
        compt = 0
        for row in reader :
            if compt != 0:
                writer.writerow([espece, row[0]])
            else :
                compt = 1
        file_bootstrap.close()
    
    file_concat.close()
    
        

