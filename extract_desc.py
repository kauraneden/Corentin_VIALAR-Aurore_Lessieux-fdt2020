'''
 © Corentin VIALAR, 2020
Ce programme se lance en ligne de commande ainsi:
$ python3 extract-desc.py FICHIER
où FICHIER est le fichier d'URLs à traiter, nommé selon le format suivant:
CATEGORIEsite, avec CATEGORIE la classe où le stocker (ex: 1400, ou bureautique),
et site la première lettre du site: L majuscule pour LDLC, m minuscule materiel.net

Au préalable, il faut que:
- le dossier correspondant à la catégorie soit présent dans le même répertoire que le fichier (ex: 1400)
- un dossier 'temp' se situe dans ce même répertoire

À chaque URl correspondra un fichier html dans 'temp', et un fichier .html.txt contenant uniquement le tableau formaté, dans le dossier de la classe voulue
'''
import lxml.html as html
from lxml import etree
import sys, os, subprocess
import pandas as pd

def wifi(fi, site):
	if site == "L":
		#print(os.getcwd())
		fo = fi.replace("https://www.ldlc.com/fiche/","./pages/temp/")
	elif site == "m":
		fo = fi.replace("https://www.materiel.net/produit/","./pages/temp/")

	commande = "wget " + fi
	subprocess.call(commande, shell=True, cwd=(str(os.getcwd())+"/pages/temp/"))

	return(fo)

def selfi(rubrique): #fonction qui devait servir à l'origine mais qui a été supplanté par une autre avec un changement de système de stockage des urls
	listefic = []
	global n
	for r, d, f in os.walk(sys.argv[1]): #parcours de l'arborescence sous un répertoire donné
		for file in f: #sélection des fichiers correspondant à la rubrique
			n = n + 1
			listefic.append(os.path.join(r, file))
	print(n," fichiers à traiter")
	return(listefic)
	

def exfi(fi, out, site):
	tree = html.parse(fi)

	labels, vals = [], []

	if site == "L":
		for case in tree.xpath('//table[@id="product-parameters"]'):
			#print("############")
			#etree.dump(case)
			#récupération des éléments intéressants dans une catégorie à part créée à la fin de la section
			body = case.xpath(".//tbody")[0] #récupération du tbody dans lequel on mettra les labels et valeurs
			for cl in body.xpath('.//td[@class="label"]'):
				labtext = cl.xpath('.//text()')[0]
				item = etree.SubElement(body, "item")
				el = etree.Element("labs")
				el.text = labtext
				item.append(el)
				#repérage des suivants
				suivant = cl.getparent().getnext()
				#print("****\nactuel: ", cl.xpath('.//text()')[0])

				#récupération des valeurs
				vali, liste = [], False
				for mmcase in cl.xpath('..//td[@class="checkbox"]|..//td[@class="no-checkbox"]'):
					val = mmcase.xpath('string()')
					clean = " " + val.replace("\n","").replace("  ","").rstrip()
					#print("même case: ", clean)
					vali.append(clean)

				if suivant is not None:
					n = 1
					#print("value du suivant[0]: ", suivant.getchildren()[0].values())
					#print("texte du suivant[0]: ", suivant.getchildren()[0].xpath('.//text()'))
				else:
					n = 0
					#print('pas de suivant')
				#etree.dump(case)

				while (suivant is not None) and ("checkbox" in suivant.getchildren()[0].values()):
					liste = True
					#print("suivant.getchildren()[0].values()")
					#print(suivant.getchildren()[0].values())

					val = suivant.getchildren()[0].xpath('string()')
					clean = " " + val.replace("\n","").replace("  ","").rstrip()
					vali.append(clean)
					suivant = suivant.getnext()
					#print(suivant)

				el = etree.Element("vals")
				if liste == True:
					el.text = ", ".join(vali)
				else:
					el.text = ", ".join(vali)
				item.append(el)

			#récupération des textes dans des listes
			for scase in case.xpath('./tbody'):
				#print("------")
				#etree.dump(scase)
				vali = []
				for lab in scase.xpath('.//labs/text()'):
					labels.append(lab)
				for val in scase.xpath('.//vals/text()'):
					if val:
						vals.append(val)

	elif site == "m":
		for case in tree.xpath('//table[@class="table c-specs__table"]'):
			#print("############")
			#etree.dump(case)
			#récupération des éléments intéressants dans une catégorie à part créée à la fin de la section
			body = etree.SubElement(case, "tbody")#création du tbody dans lequel on mettra les labels et valeurs
			for cl in case.xpath('.//td[@class="label"]'):
				labtext = cl.xpath('.//text()')[0]
				item = etree.SubElement(body, "item")
				el = etree.Element("labs")
				el.text = labtext
				item.append(el)
				#repérage des suivants
				suivant = cl.getparent().getnext()
				#print("actuel: ", cl.xpath('.//text()')[0])
				if suivant is not None:
					n = 1
					#print("value du suivant[0]: ", suivant.getchildren()[0].values())
					#print("texte du suivant[0]: ", suivant.getchildren()[0].xpath('.//text()'))
				else:
					n = 0
					#print('pas de suivant')
				#etree.dump(case)

				#récupération des valeurs
				vali, liste = [], False
				for mmcase in cl.xpath('..//td[@class="value"]'):
					val = mmcase.xpath('string()')
					clean = " " + val.replace("\n","").replace("  ","").rstrip()
					vali.append(clean)
				while (suivant is not None) and ("value" in suivant.getchildren()[0].values()):
					liste = True
					#print("suivant.getchildren()[0].values()")
					#print(suivant.getchildren()[0].values())

					val = suivant.getchildren()[0].xpath('string()')
					clean = " " + val.replace("\n","").replace("  ","").rstrip()
					vali.append(clean)
					suivant = suivant.getnext()
					#print(suivant)

				el = etree.Element("vals")
				if liste == True:
					el.text = ", ".join(vali[:-1])
				else:
					el.text = ", ".join(vali)
				body.append(el)

			#récupération des textes dans des listes
			for scase in case.xpath('./tbody'):
				#print("------")
				#etree.dump(scase)
				vali = []
				for lab in scase.xpath('.//labs/text()'):
					labels.append(lab)
				for val in scase.xpath('.//vals/text()'):
					if val:
						vals.append(val)


	dico = dict(zip(labels, vals))
	print(dico)

	tab = pd.DataFrame.from_dict(dico, orient='index')
	tab.to_csv(out)

def lifi(fi):
	with open(fi, 'r') as f:
		return(f.read().split('\n'))

########################################
#nettoyage de temp
filelist = [f for f in os.listdir('./pages/temp')]
for f in filelist:
	os.remove(os.path.join('./pages/temp', f))

a = sys.argv[1]
site = a[-1]
cat = a[:-1] + "/"
for i in lifi(sys.argv[1]):
	fo = wifi(i, site)
	ecris = cat + fo.replace("./pages/temp/","") + ".txt"
	exfi(fo, ecris, site)


