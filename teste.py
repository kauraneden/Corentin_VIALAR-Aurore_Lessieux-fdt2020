# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:33:50 2020

@author: auror
"""
import re
import os, sys

def selfi():
	listefic, n = [], 0
	for r, d, f in os.walk(sys.argv[1]): #parcours de l'arborescence sous un répertoire donné
		for file in f:
			n = n + 1
			listefic.append(os.path.join(r, file))
	print(n," fichiers à traiter")

	return(listefic)

def net(fi):
	with open(fi, 'r') as f:
		lignes = f.readlines()
	with open(fi, 'w') as f:
		for ligne in lignes:
			ligne = re.sub(r"(?<=[0-9])\s(?=[a-z]|[A-Z])", "", ligne)
			ligne = re.sub(r"(?<=([A-Z]))\s(?=[0-9])", "-", ligne)
			ligne = re.sub(r"(x|X)\s(?=[A-Z]|[0-9])", "x", ligne)
			f.write(ligne)

#################
fichiers = selfi()
for fi in fichiers:
	net(fi)
print('fait')