#! /bin/env python3.8
# -*- coding=utf-8 -*-

"""Projet"""

import pulp as pl
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from termcolor import colored

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

graph, entete = extract_graph(file_path)
nx.draw(graph)
# decomenter la ligne ci dessous pour afficher le graph avec matplotlib
#plt.show()
nx.write_graphml(graph, 'projet_RO_LAGNIAUX_JEAN_DENES_THEO\output_files\graphDenesLagniaux.graphml')
print()
print(colored('le graph a été créer et on peut le trouve dans le fichier => output_files', 'red'))
print()
