# Corentin_VIALAR-Aurore_Lessieux-fdt2020-GIT
 
Mode d'emploi de l'archive de ce proket de Fouille de Textes:


1) CV-AL_fdt2020.pdf est le compte-rendu rédigé par nos soins

2) extract-desc.py est le script python principal de notre collecte de données

3) les fichiers utilisés pour nettoyer et affiner le formatage sont nettoie.py (qui efface les lignes contenant les noms des classes ou trop explicites), reenc.py (qui résout des problèmes d'encodage en ISO 8859-1 présents dans certaines pages), et teste.py (qui normalise les couples nombres-unités de mesure).
Ils se lancent tous ainsi: $ python3 SCRIPT DIR, où SCRIPT est le script, et DIR le répertoire à parcourir.

4) le dossier capt/ contient les captures d'écran de tous les résultats des classifieurs présentés dans notre compte-rendu (mesures et matrices de confusion), si les tableaux et matrices présentés au long du document ne satisfont pas la curiosité du lecteur.

5) enfin, le dossier CORPUS/ contient l'ensemble des pages extraites et normalisée, rangées par classes, ainsi que le dossier temp/ et les fichiers d'URLS à extraire, comme requis par le script extract-desc.py (voir sa notice d'utilisation dans le script même).

Bonne lecture!
