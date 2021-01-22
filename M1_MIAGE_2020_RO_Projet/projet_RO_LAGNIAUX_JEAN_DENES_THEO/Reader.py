#! /bin/env python3.8
# -*- coding=utf-8 -*-

"""TP5"""

import pulp as pl
import networkx as nx
import matplotlib.pyplot as plt
file_path = 'truck_instance_base.data'


def extract_adm_cells(file_path):
    graph = nx.DiGraph()

    with open (file_path, 'r') as f_in:
        print('')
        print('!! IN FILE READ LOOP !!')
        print('')
        # Read one line by one line without store all the lines (streaming)
        header = f_in.readline()
        splitHead = header.split()

        LimCam = splitHead[0]
        start = splitHead[1]
        n_clientsuppr = splitHead[2]
        n_depsuppr = splitHead[3]

        print('LimCam =', LimCam, ' start =',start, ' n_clientsuppr = ', n_clientsuppr, ' n_depsuppr =',n_depsuppr )
        print('')
        block = ''
        for line in f_in:
                line_split = line.split()
                if block == '':
                    block = line_split[0]
                elif line_split[0] == '}':
                    block = ''
                elif block == 'ENTITIES':
                    print('IN ENTITES BLOCK')
                elif block =='ROADS':
                    print('IN ROADS BLOCK')
                    print(line_split)
                    s, e, cap, gas, tax = line_split
                    addRoad(graph, s, e)
                else:
                    exit(f'ERROR: line = {line}')
    return graph

def addRoad(graph, s, e):
    start = f'{s}'
    end = f'{e}'
    graph.add_edge(start, end)


def add_admissible(graph, i, j):
    i_id = f'R{i}'
    j_id = f'C{j}'
    graph.add_edge(i_id, j_id)

def add_ri(graph, i, ri):
    i_id = f'R{i}'
    graph.add_edge(SOURCE, i_id, capacity = ri)
    for j_id in graph.successors(i_id):
        graph[i_id][j_id]['capacity'] = ri

def add_cj(graph, j, cj):
    j_id = f'C{j}'
    graph.add_edge(j_id, TARGET, capacity = cj)


graph = extract_adm_cells(file_path)
print('')
print(graph.nodes())
nx.draw(graph)
plt.show()
