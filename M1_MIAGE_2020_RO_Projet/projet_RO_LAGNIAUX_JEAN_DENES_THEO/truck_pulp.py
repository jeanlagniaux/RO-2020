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
from projet_RO_LAGNIAUX_JEAN_DENES_THEO.reader import extract_graph

# ...

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

    roads = graph.edges()
    roads = LpVariable("Road", cat=pl.LpBinary)
    roads_cap = graph.edges()
    roads_cap = LpVariable("Road capacity", lowBound=0, cat=pl.LInteger)

    list_depot = []
    list_customer = []
    nodes = graph.nodes()
    for val in nodes:
        if val[0] == 'D':
            list_depot.append(val)
        else:
            list_customer.append(val)

    # get le stock d'un depot    
    print(graph.nodes[list_depot[list_depot.index("D1")]]["stock"])

    #pas besoins car on a les information de la route sur la variable route
    #road_ap[(u, v)] = pl.LpVariable('road capacity', lowBound=0, cat=pl.LpInteger)
    #road_cap_i = pl.LpVariable('road capacity', lowBound=0, cat=pl.LpInteger)
    #customer_req = pl.LpVariable('customer request', lowBound=0, cat=pl.LpInteger)

    truck_cap = pl.LpVariable('truck capacity', lowBound=0, cat=pl.LpInteger)
    truck_stk = pl.LpVariable('truck stock on road', lowBound=0, cat=pl.LpInteger)

    nbDeDepot = pl.LpVariable('Nb de dépot total dans le systeme', lowBound=0, cat=pl.LpInteger)
    nbDepotLivrable = pl.LpVariable('nb de depot que lon va pouvoir livrer', lowBound=0, cat=pl.LpInteger)

    nbDeClient = pl.LpVariable('Nb de client total dans le systeme', lowBound=0, cat=pl.LpInteger)
    nbClientLivrable = pl.LpVariable('nb de client que lon va pouvoir livrer', lowBound=0, cat=pl.LpInteger)

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #
    prob += pl.LpMaximize(pl.lpSum(1000*customer_req[node]*customer[node])-pl.lpSum(road*road_cap[edge]))

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #

    # stk du camion inf à la capacité de la route
    prob += truck_stk <= road_cap
    # route pas encore emprunté
    prob += pl.lpSum(road_i) < 1
    #stk camion <= capacité du camion
    prob += truck_stk <= entete[0]

    #   on divise la contrainte en 2 contraintes relativement similaire.
    #charger
    prob += pl.lpSum(deposit_stk) <= 0
    #dechager
    prob += pl.lpSum(customer_req) >= 0

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

    path = Path(__file__)
    print(path)
    newpath = path.parent.parent.resolve()
    dataDir = newpath / 'data'
    InstancePath = dataDir / 'truck_instance_base.data'
    filePath = InstancePath

    graph, entete = extract_graph(filePath)
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
    solve_truck_problem()











# ---------------------------------------------------------------------------------------------------#
#                             ===== TEMPLATE TP5 ====                                                #
# ---------------------------------------------------------------------------------------------------#

def set_max_flow_model(graph):

    prob = pl.LpProblem(name='max_flow', sense=pl.LpMaximize)
    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #
    #total FLOW = phi0
    flow = pl.LpVariable('flow', lowBound=0, cat=pl.LpInteger)
    # the flow on each edge
    d_edge_flow = pl.LpVariable.dicts('flow', graph.edges(),
                                      lowBound=0, cat=pl.LpInteger)

    # ------------------------------------------------------------------------ #
    # The objective function
    # ------------------------------------------------------------------------ #
    prob += flow, 'maximize_the_flow'

    for v in graph.nodes():
        prob += calcul_D_mu
        t_PHI_0(v, flow) \
        + calcul_A_mult_PHI(graph, v, d_edge_flow) == 0,\
         F'flow_conservation_{v}'

    #Phi < Capa
    for e in graph.edges():
        prob += d_edge_flow[e] <= graph.edges()[e]['capacity']

    return prob, d_edge_flow

#int flow
# D = -1 si v=SROUCE; 1 si v=TARGET et 0 sinon
def calcul_D_mult_PHI_0(v, flow):
    eq = 0
    if v == SOURCE:
        eq -= flow
    elif v == TARGET:
        eq += flow
    return eq

# A[v,e] = 1 si v = e-; -1 si v = e+; 0 sinon
def calcul_A_mult_PHI(graph, v, d_edge_flow):
    eq = 0
    for u in graph.predecessors(v):
        eq -= d_edge_flow[u,v]
    for w in graph.successors(v):
        eq += d_edge_flow[v,w]
    return eq


# ============================================================================ #
#                               SOLVE WITH DATA                                #
# ============================================================================ #



def solve_max_flow():

    path = Path(__file__)
    print(path)
    newpath = path.parent.parent.resolve()
    dataDir = newpath / 'data'
    InstancePath = dataDir / 'truck_instance_base.data'
    filePath = InstancePath

    graph, entete = extract_adm_cells(filePath)
    prob, d_edge_flow = set_max_flow_model(graph)

    prob.solve(pl.PULP_CBC_CMD(logPath='./CBC_max_flow.log'))
    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print()
    print('solve_max_flow')
    print()
    print(f'Status:\n{pl.LpStatus[prob.status]}')

    print()
    print('-' * 40)
    print()

    # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        print(v.name, '=', v.varValue)

    print()

if __name__ == '__main__':
    solve_max_flow()

def solve_min_cut():
    graph = extract_adm_cells('admissible_cells.info')
    prob, d_edge_flow = set_min_cut_model(graph)

    nx.write_graphml(graph, 'graph_file0.graphml')
    graph2 = nx.Graph()
    for edge, variable in d_edge_flow.items():
        edge_flow = variable.varValue
        graph2.add_edge(edge[0], edge[1], flow=edge_flow)
    nx.write_graphml(graph, 'graph_file.graphml')
    plt.show()

    prob.solve(pl.PULP_CBC_CMD(logPath='./CBC_max_flow.log'))
        # ------------------------------------------------------------------------ #
        # Print the solver output
        # ------------------------------------------------------------------------ #
    print()
    print('solve_min_cut')
    print()
    print(f'Status:\n{pl.LpStatus[prob.status]}')

    print()
    print('=' * 40)
    print()

        # Each of the variables is printed with it's resolved optimum value
    for v in prob.variables():
        print(v.name, '=', v.varValue)

    print('Obj : ', prob.objective.value())

if __name__ == '__main__':
    solve_min_cut()
