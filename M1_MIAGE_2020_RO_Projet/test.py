# -*- coding=utf-8 -*-
"""Le programme de test `test.py`."""
from pathlib import Path
# Importer le programme principal qui se trouve dans le dossier du projet
import projet_RO_NOM1_PRENOM1_NOM2_PRENOM2.solve_truck_problem as solve_truck_problem
# La magie de pathlib...
THIS_FILE_DIR = Path(__file__).parent.resolve()
DATA_DIR = THIS_FILE_DIR / 'data'
if __name__ == '__main__':
# ...
# instancier `file_path`
instance_path = DATA_DIR / 'quelquechose.data'
optval, roads_qty, ... = solve_truck_problem(instance_path)
# ...
