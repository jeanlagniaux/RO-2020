#! /bin/env python3.8
# -*- coding=utf-8 -*-

"""Projet"""

import pulp as pl
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def extract_graph(file_path):
    graph = nx.DiGraph()

    with open (file_path, 'r') as f_in:
        header = f_in.readline()
        splitHead = header.split()
        LimCam = splitHead[0]
        start = splitHead[1]
        n_clientsuppr = splitHead[2]
        n_depsuppr = splitHead[3]
        valHead = (LimCam, start,  n_clientsuppr , n_depsuppr)
        block = ''
        for line in f_in:
                line_split = line.split()
                if block == '':
                    block = line_split[0]
                elif line_split[0] == '}':
                    block = ''
                elif block == 'ENTITIES':
                    s, type, stock = line_split
                    stock = int(stock)
                    addEntity(graph, s, type, stock)
                elif block =='ROADS':
                    s, e, cap, gas, tax = line_split
                    cap = int(cap)
                    gas = int(gas)
                    tax = int(tax)
                    addRoad(graph, s, e, cap, gas, tax)
                else:
                    exit(f'ERROR: line = {line}')
    return graph, valHead

def addEntity(graph, s, type, stock):
    typeEntity = F'{type}'
    stockEntity =  stock
    graph.add_node(s, type = typeEntity, stock = stockEntity)

def addRoad(graph, s, e, cap, gas, tax):
    start = f'{s}'
    end = f'{e}'
    RoadCap = cap
    RoadGas = gas
    RoadTax = tax
    graph.add_edge(start, end, capacity = RoadCap, Gas = RoadGas, Tax = RoadTax)

#############################  MAIN RUNNING TEST READER  #############################

path = Path(__file__)
newpath = path.parent.parent.resolve()
dataDir = newpath / 'data'
InstancePath = dataDir / 'truck_instance_less_customers.data'

file_path = InstancePath

#print(file_path)

graph, entete = extract_graph(file_path)
#print('')
#print('LimCam, start, n_clientsuppr, n_depsuppr', val)
#print('')
#print('=== les noeuds dans notre graph ===')
#print('')
#node = {}
#for value in graph.nodes():
#    node = graph.nodes[value]
    #print(value, node)
#    if graph.nodes[value]['type'] == 'customer':
        #print('OK')
#print('')
#print('=== la liste des arc dans notre graphe ===')
#print('')

#roads = {}
#road = {}
#for value in graph.edges():
    #print(value, graph.edges[value[0], value[1]])


#roads = graph.edges()


#nx.draw(graph)
#plt.show()
#nx.write_graphml(graph, 'projet_RO_LAGNIAUX_JEAN_DENES_THEO\output_files\graphe_init.graphml')
#print('le graph a été créer et on peut le trouve dans le fichier => output_files')



#list_depot = []
#list_customer = []
#nodes = graph.nodes()
#for val in nodes:
#    if val[0] == 'D':
#        list_depot.append(val)
#    else:
#        list_customer.append(val)

# get le stock d'un depot
#print(graph.nodes[list_depot[list_depot.index("D1")]]["stock"])

#print([graph.edges[u, v] for (u, v) in roads])

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
customer_need = {}
for i in list_customer:
    customer_need[i] = graph.nodes[i]['stock']

dicts_route = {}
for i, j in graph.edges():
    dicts_route[i,j] = {'cap' : graph.edges[i,j]['capacity'], 'cost' : graph.edges[i,j]['Gas'] + graph.edges[i,j]['Tax']}
list_route = [val for val in graph.edges()]

customer_need = {}
for i in list_customer:
    customer_need[i] = graph.nodes[i]['stock']
