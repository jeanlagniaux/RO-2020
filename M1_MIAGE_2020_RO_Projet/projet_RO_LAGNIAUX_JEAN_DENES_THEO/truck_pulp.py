# -*- coding=utf-8 -*-
"""Module `truck_pulp.py`.
Attention à l'importation de module, explication :
quand vous lancerez votre test, vous vous trouverez
un étage précédent dans l'arborescence des fichiers
par rapport au dossier contenant vos programmes.
Par conséquent, dans chacun des programmes dans le dossier
vous devez indiquer un chemin relatif par rapport à votre
fichier `test.py`
"""
# Pour charger un module dans le dossier du projet
import projet_RO_LAGNIAUX_JEAN_DENES_THEO.module as mod
# ...
def solve_truck_problem(file_path):
# Faire quelque chose ici avec l'argument `file_path`
# qui est un chemin de fichier
# ...
# La fonction retournera :

#       - la valeur de la fonction objectif égale aux bénéfices
#           de l'entreprise si le problème est resolvable,
#           sinon `None`. Le type de retour sera un "float" ;
#       - un dictionnaire,
#           où les clefs sont les routes et les valeurs associées
#           sont les quantités de marchandises qui les traversent ;
#       - ce que vous voulez en plus si besoin.
    return optval, roads_qty #, ...
