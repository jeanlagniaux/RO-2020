#! /bin/env python3.8
# -*- coding=utf-8 -*-

"""TP5"""

import pulp as pl
import networkx as nx
SOURCE = 'S'
TARGET = 'T'

def extract_adm_cells(file_path):
    graph = nx.DiGraph()
    graph.add_node(SOURCE)
    graph.add_node(TARGET)

    with open (file_path, 'r') as f_in:
        # Read one line by one line without store all the lines (streaming)
        header = f_in.readline()
        splitHead = header.split()

        #nrow = int(splitHead[0])
        #ncol = int(splitHead[1])

        n_row, n_col = (int(str_num) for str_num in header.split())
        block = ''
        for line in f_in:
            line_split = line.split()
            if block == '':
                block = line_split[0]
            elif line_split[0] == '}':
                block = ''
            elif block == 'ADMISSIBLE':
                i,j = line_split
                add_admissible(graph, i, j)
            elif block =='ROW_LIMIT':
                i = line_split[0]
                ri = int(line_split[1])
                add_ri(graph, i, ri)
            elif block =='COLUMN_LIMIT':
                j = line_split[0]
                cj = int(line_split[1])
                add_cj(graph, j, cj)
            else:
                exit(f'ERROR: line = {line}')
    return graph

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

graph = extract_adm_cells('admissible_cells.info')
#print(graph.nodes())
