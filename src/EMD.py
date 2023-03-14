#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx


from graph import Graph, Point
from letter import gxl2Graph

def GGMD(g1: Graph, g2: Graph, C_V = 1, C_E = 1):
    if(g1.n < g2.n):
        g1, g2 = g2, g1
    # todo: check if the graphs live in the same ambient
    print(g1.n, g2.n)

    G = nx.DiGraph()
    sig1, sig2 = signature(g1), signature(g2, g1.n - g2.n)

    for i in range(g1.n):
        G.add_node(i, demand = -1)

    G.add_node(g1.n, demand = -g2.n)

    for i in range(g1.n + 1, g1.n + g2.n + 1):
        G.add_node(i, demand = 1)
    
    G.add_node(g1.n + g2.n + 1, demand = g1.n)


    for i in range(g1.n):
        u = g1.vertices[i]
        for j in range(g2.n):
            weight = C_V * np.linalg.norm( sig1[i][0] - sig2[j][0] )
            weight += 0.5 * C_E * np.linalg.norm( sig1[i][1] - sig2[j][1], ord = 1 )
            G.add_edge(i , j + g1.n + 1, weight = weight)
        weight = 0.5 * C_E * np.linalg.norm( sig1[i][1], ord = 1 )
        G.add_edge(i, g1.n + g2.n + 1, weight = weight)

    for j in range(g2.n):
        weight = 0.5 * C_E * np.linalg.norm( sig1[j][1], ord = 1 ) 
        G.add_edge(g1.n, j + g1.n + 1, weight = weight)

    G.add_edge(g1.n, g1.n + g2.n + 1, weight = 0)
    
    print(G)
    return nx.network_simplex(G)

def signature(g: Graph, offset = 0):
    m = g.adjacency()
    sig = []
    for i in range(g.n):
        u =  g.vertices[i]
        for j in range(g.n):
            if m[i, j] == 0:
                v = g.vertices[j]
                m[i, i] = np.linalg.norm(np.array(u.coords) - np.array(v.coords))
        sig.append( (np.array(u.coords), np.pad(m[i, :], (0, offset), 'constant', constant_values = 0)) )

    return sig

import json 

gxl = json.load( open('data/Letter/json/Test/AP1_0034.json') )
G = gxl2Graph(gxl)
gxl = json.load( open('data/PROTOTYPE/A_prototype.json') )
A = gxl2Graph(gxl)

GGMD(G, A)

# p1 = Point((0, 0))
# p2 = Point((1, 0))
# p3 = Point((2, 1))
# p4 = Point((0, 1))
# g1 = Graph([p1, p2, p3, p4], [
#     [p1, p2],
#     [p2, p4],
#     [p4, p3]
# ])
# g2 = Graph([p1, p2, p3, p4], [
#     [p1, p2],
#     [p2, p3]
# ])
