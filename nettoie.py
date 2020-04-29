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
		e = 0
		for li in lignes:
			efface = False
			for t in ['gamer', 'gaming', 'streaming', 'bureautique', 'Bureautique', 'streamer', 'Gamer', 'Gaming', 'Streamer', 'Streaming', 'Bureautique', 'bureau', 'Bureau']:
				if t in li:
					efface = True
			if efface == False:
				f.write(li)
			else:
				e = e + 1
	print(e, " ligne(s) effacée(s)")

#################
fichiers = selfi()
for fi in fichiers:
	net(fi)