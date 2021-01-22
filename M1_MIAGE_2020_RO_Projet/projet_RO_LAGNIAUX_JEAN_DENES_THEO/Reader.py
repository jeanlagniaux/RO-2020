#! /bin/env python3.8
# -*- coding=utf-8 -*-

"""TP5"""

import pulp as pl
import networkx as nx
SOURCE = 'S'
TARGET = 'T'
file_path = 'truck_instance_base.data'


def extract_adm_cells(file_path):
    graph = nx.DiGraph()
    graph.add_node(SOURCE)
    graph.add_node(TARGET)

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
                print(line)
                line_split = line.split()
                if block == '':
                    block = line_split[0]
                elif line_split[0] == '}':
                    block = ''
                elif block == 'ENTITIES':
                    print('IN ENTITES BLOCK')
                elif block =='ROADS':
                    print('IN ROADS BLOCK')
                else:
                    exit(f'ERROR: line = {line}')
    return graph


graph = extract_adm_cells(file_path)
#print(graph.nodes())
