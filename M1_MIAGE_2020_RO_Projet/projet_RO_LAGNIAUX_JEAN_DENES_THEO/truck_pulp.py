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
from Reader import extract_graph
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
    for i,j in list_route:
        dicts_route[i,j] = {'cap' : graph.edges[i,j]['capacity'], 'gas' : graph.edges[i,j]['Gas'], 'tax' : graph.edges[i,j]['Tax']}
    use_road = pl.LpVariable.dicts("Use_road", list_route, 0, 1, cat=pl.LpBinary)

    truck_stock_onRoad = pl.LpVariable.dicts('stock_on_road', list_route, cat=pl.LpInteger)

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #

    prob += pl.lpSum(1000 * use_customer[c] * customer_need[c] for c in list_customer) - pl.lpSum((use_road[(i, j)] * dicts_route[(i,j)]['gas'] + (use_road[(i, j)] * dicts_route[(i,j)]['tax'] * truck_stock_onRoad[(i,j)]) for (i,j) in list_route))

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #

    #le nombre de client que l'on va fournir doit etre inférieur ou égal a la contraintes sur le nombre de client livrable
    for c in list_customer:
        prob += use_customer[c] <= int(entete[2])

    #le nombre de depot dans lesquel on va s'aprovisionner doit etre inférieur ou égal a la contraintes sur le nombre de depot utilissable
    for d in list_depot:
        prob += use_depot[d] <= int(entete[3])

    #la capacité du camion sur toute les route doit etre inferieur a la capacite total du camion
    for (i,j) in list_route:
        prob += truck_stock_onRoad[(i,j)] <= entete[0]

    # stock du camion inferieur ou egale à la capacité de la route
    for (i,j) in list_route:
        prob += truck_stock_onRoad[(i,j)] <= dicts_route[(u,v)]['capacity']

    # contrainte
    for d in list_depot:
        prob += depot_stk[d] <= 0

    # contrainte
    for c in list_customer:
        prob += customer_need[c] >= 0

    # si on a servi un client alors il la ete dans la totalite
    for c in use_customer:
        prob += use_customer[c] * customer_need[c] == 0

    # une route ne peut etre utiliser plusieur fois
    for (i,j) in list_route:
        prob += pl.lpSum(use_road[(u,v)]) <= 1

    return prob, truck_stock_onRoad

# ============================================================================ #
#                               SOLVE WITH DATA                                #
# ============================================================================ #

def solve_truck_problem(file_path):
    graph, entete = extract_graph(file_path)
    prob, truck_stock_onRoad = def_truck_problem(graph, entete)
    prob.solve(pl.PULP_CBC_CMD(logPath='./CBC_max_flow.log'))
    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print()
    print('solvre truck problem')
    print()
    print(f'Status:\n{pl.LpStatus[prob.status]}')
    print()
    obj = prob.objective
    print('le résultat de la fonction objectif est : ', obj)
    print('-' * 40)
    dicts_var = {}
    for v in prob.variables():
        print(v.name, '=', v.varValue)
        dicts_var[v.name] = v.varValue
    print()
    print('le dictionnaire du nombre de GPU transporter sur chaque route est : ', truck_stock_onRoad)
    return obj, dicts_var, truck_stock_onRoad
