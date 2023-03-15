#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx


from graph import Graph, Point

def GGMD(g1: Graph, g2: Graph, C_V = 1, C_E = 1, multiplier = 100):
    if(g1.n < g2.n):
        g1, g2 = g2, g1
    # todo: check if the graphs live in the same ambient

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
            G.add_edge(i , j + g1.n + 1, weight = round( weight * multiplier) )
        weight = 0.5 * C_E * np.linalg.norm( sig1[i][1], ord = 1 )
        G.add_edge(i, g1.n + g2.n + 1, weight = round( weight * multiplier))
    
    for j in range(g2.n):
        weight = 0.5 * C_E * np.linalg.norm( sig1[j][1], ord = 1 ) 
        G.add_edge(g1.n, j + g1.n + 1, weight = round( weight * multiplier))
    
    G.add_edge(g1.n, g1.n + g2.n + 1, weight = 0)

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