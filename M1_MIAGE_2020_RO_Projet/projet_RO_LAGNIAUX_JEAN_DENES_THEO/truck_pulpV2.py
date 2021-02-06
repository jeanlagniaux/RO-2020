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
#import projet_RO_LAGNIAUX_JEAN_DENES_THEO.module as mod
import pulp as pl
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from reader import extract_graph
# ---------------------------------------------------------------------------------------------------#
#                             ===== TEMPLATE PROJET ====                                             #
# ---------------------------------------------------------------------------------------------------#
def def_truck_problem(graph, entete):
    # ------------------------------------------------------------------------ #
    # Linear problem with minimization or maximization
    # ------------------------------------------------------------------------ #
    prob = pl.LpProblem(name='benefice', sense=pl.LpMaximize)
    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #

    list_depot = []
    list_customer = []
    for val in graph.nodes():
        if val[0] == 'D':
            list_depot.append(val)
        else:
            list_customer.append(val)

    depot_stk = {}
    for i in list_depot:
        depot_stk[i] = graph.nodes[i]['stock']
    nbDepotLivrable = len(list_depot) - int(entete[3])

    use_depot = pl.LpVariable.dicts("Use_depot", list_depot, 0, 1, cat=pl.LpBinary)

    customer_need = {}
    for i in list_customer:
        customer_need[i] = graph.nodes[i]['stock']

    use_customer = pl.LpVariable.dicts("Served_cust", list_customer, 0, 1, cat=pl.LpBinary)

    list_route = [val for val in graph.edges()]
    dicts_route = {}
    for i, j in list_route:
        dicts_route[i,j] = {'cap' : graph.edges[i,j]['capacity'], 'gas' : graph.edges[i,j]['Gas'], 'tax' : graph.edges[i,j]['Tax']}
    use_road = pl.LpVariable.dicts("Use_road", list_route, 0, 1, cat=pl.LpBinary)

    truck_stock_onRoad = pl.LpVariable.dicts('raod', list_route, cat=pl.LpInteger)

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #

    #erruer vient peut etre du fait qu'on déclare plusieur fois i , j 

    prob += pl.lpSum(1000 * use_customer[c] * customer_need[c] for c in list_customer) - pl.lpSum( (use_road[(i, j)] * dicts_route[use_road[(i,j)]]['gas'] for (i, j) in list_route) + ( use_road[(i, j)] * dicts_route[use_road[[(i, j)]]['tax'] * truck_stock_onRoad[(i, j)] for (i, j) in list_route))

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #

    #si on supprime un ou plusieur stock/depot alors le nombre de stock/depot utilisée doit etre inférieur ou égale au nombre max de stock/depot
    for c in list_customer:
        prob += (use_customer[c] <= int(entete[2])
    for d in list_depot:
        prob += use_depot[d] <= int(entete[3])

    for (i, j) in list_route:
        prob += truck_stock_onRoad[(i,j)] <= entete[0]

    # stk du camion inf à la capacité de la route
    for (i, j) in list_route:
        prob += truck_stock_onRoad[(i,j)] <= dicts_route[(u,v)]['capacity']

    for d in list_depot:
        prob += depot_stk[d] <= 0

    for c in list_customer:
        prob += customer_need[c] >= 0

    for c in use_customer:
        prob += use_customer[c] * customer_need[c] = 0

    for (i, j) in list_route:
        prob += pl.lpSum(use_road[(u,v)]) <= 1

    return prob
    return optval, roads_qty #, ...

# ============================================================================ #
#                               SOLVE WITH DATA                                #
# ============================================================================ #

def solve_truck_problem(file_path):
    # La fonction retournera :
    #       - la valeur de la fonction objectif égale aux bénéfices
    #           de l'entreprise si le problème est resolvable,
    #           sinon `None`. Le type de retour sera un "float" ;
    #       - un dictionnaire,
    #           où les clefs sont les routes et les valeurs associées
    #           sont les quantités de marchandises qui les traversent ;
    #       - ce que vous voulez en plus si besoin.

    graph, entete = extract_graph(file_path)
    prob, d_edge_flow = def_truck_problem(graph, entete)
    prob.solve(pl.PULP_CBC_CMD(logPath='./CBC_max_flow.log'))
    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print()
    print('solve_max_flow')
    print()
    print(f'Status:\n{pl.LpStatus[prob.status]}')
    print()
    print('-')
    print()
    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        print(v.name, '=', v.varValue)
    print()
if __name__ == '__main__':
    path = Path(__file__)
    print(path)
    newpath = path.parent.parent.resolve()
    dataDir = newpath / 'data'
    InstancePath = dataDir / 'truck_instance_base.data'
    filePath = InstancePath
    solve_truck_problem(filePath)
