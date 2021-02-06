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

    prob += pl.lpSum(use_customer[i] for i in list_customer) <= int(entete[2])
    prob += pl.lpSum(use_depot[i] for i in list_depot) <= int(entete[3])

    list_route = [val for val in graph.edges()]
    dicts_route = {}
    for i, j in graph.edges():
        dicts_route[i,j] = {'cap' : graph.edges[i,j]['capacity'], 'cost' : graph.edges[i,j]['Gas'] + graph.edges[i,j]['Tax']}
    use_road = pl.LpVariable.dicts("Use_road", list_route, 0, 1, cat=pl.LpBinary)

    truck_cap = entete[0]

    #truck_stk = [pl.LpVariable(f'route_{u}_{v}', lowBound=0, cat=pl.LpInteger) for (u, v) in roads]
    truck_stk_road_ = pl.LpVariable.dicts('i', graph.edges(), cat=pl.LpInteger)

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #
    prob += pl.lpSum(1000*([graph.nodes[list_customer[list_customer.index(cust)]]["stock"] for cust in list_customer]) * ([customer_is_served[i] for i in list_customer])) - pl.lpSum( ([road_is_used[i] for i in roads]) * ([graph.edges[u, v]['capacity'] for (u, v) in roads]))
    #prob += pl.LpMaximize(pl.lpSum(1000*customer_req*customer[utilisé])-pl.lpSum(road*road_cap[edge]))
    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #
    # stk du camion inf à la capacité de la route
    for (u, v) in graph.edges():
        prob += truck_stk_road_[(u,v)] <= road_is_used[(u,v)]['capacity']

    # for (u, v) in graph.edges():
        #prob += truck_cap <= truck_stk_road_[(u,v)]

    for (u, v) in graph.edges():
        prob += pl.lpSum(road_is_used[(u,v)]) < 1

    #   on divise la contrainte en 2 contraintes relativement similaire.
    #charger
    prob += deposit_stk <= 0
    #dechager
    prob += customer_req >= 0
    # un client doit etre servi en totalité


    prob += nbDepotLivrable <= nbDeDepot
    prob += nbClientLivrable <= nbDeClient
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
