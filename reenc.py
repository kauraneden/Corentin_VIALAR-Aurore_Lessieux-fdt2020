import chardet, os, sys

def selfi():
	listefic, listeenc, n = [], [], 0
	for r, d, f in os.walk(sys.argv[1]): #parcours de l'arborescence sous un répertoire donné
		for file in f:
			with open(os.path.join(r, file), 'rb') as fic:
				enc = chardet.detect(fic.read())['encoding']
				#print(enc)
			if 'UTF' not in enc: #sélection des fichiers correspondant à la rubrique
				n = n + 1
				listefic.append(os.path.join(r, file))
				listeenc.append(enc)
	print(n," fichiers à traiter")

	dico = dict(zip(listefic, listeenc))
	for i in dico.keys():
		a = 2
		#print(i, dico[i])

	return(dico)

def reenc(fi, enc):
	fo = fi.replace(".html.txt","u8.html.txt")
	with open(fi, 'r') as fuck:
		if "Ã©" in fuck.read():
			re = True
		else:
			re = False
	if re == True:
		with open(fi, 'r', encoding="utf-8") as e, open(fo, 'w', encoding="ISO 8859-1") as o:
			o.write(e.read())
		'''with open(fo, 'r', encoding="ISO 8859-1") as fiso, open(fi, 'w', encoding="utf-8") as fu8:
			fu8.write(fiso.read())'''
		os.remove(fi)
#######
a = selfi()
if len(a)>0:
	for fi in a.keys():
		enc = a[fi]
		reenc(fi, enc)
print("fait")