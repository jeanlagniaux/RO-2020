# -*- coding=utf-8 -*-
"""Le programme de test `test.py`."""
from pathlib import Path
# Importer le programme principal qui se trouve dans le dossier du projet
import projet_RO_LAGNIAUX_JEAN_DENES_THEO.truck_pulp as solve_truck_problem

# La magie de pathlib...
THIS_FILE_DIR = Path(__file__).parent.resolve()
DATA_DIR = THIS_FILE_DIR / 'data'
if __name__ == '__main__':
    instance_path = DATA_DIR / 'truck_instance_base.data'
    print(instance_path)
    obj, dicts_var, truck_stock_onRoad  = solve_truck_problem(instance_path)
