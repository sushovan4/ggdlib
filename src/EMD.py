#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx


from graph import Graph

def GGMD(g1: Graph, g2: Graph, C_V, C_E, multiplier):
    if(g1.n < g2.n):
        g1, g2 = g2, g1
    # todo: check if the graphs live in the same ambient

    G = nx.DiGraph()
    sig1, sig2 = signature(g1), signature(g2, g1.n - g2.n)

    for i in range(g1.n):
        G.add_node(sig1[i][2], demand = -1 * multiplier)

    G.add_node("eps1", demand = -g2.n * multiplier)

    for i in range(g2.n):
        G.add_node(sig2[i][2], demand = 1 * multiplier)
    
    G.add_node("eps2", demand = g1.n * multiplier)

    for i in range(g1.n):
        for j in range(g2.n):
            weight = C_V * np.linalg.norm( sig1[i][0] - sig2[j][0] )
            weight += 0.5 * C_E * np.linalg.norm(sig1[i][1] - sig2[j][1], ord = 1)
            G.add_edge(sig1[i][2] , sig2[j][2], weight = round( weight * multiplier) )
        weight = 0.5 * C_E * np.sum( sig1[i][1] )
        G.add_edge(sig1[i][2], "eps2", weight = round( weight * multiplier))
    
    for j in range(g2.n):
        weight = 0.5 * C_E * np.sum( sig2[j][1] ) 
        G.add_edge("eps1", sig2[j][2], weight = round( weight * multiplier))
    
    G.add_edge("eps1", "eps2", weight = 0)


    # print( [(str(n), nbrdict) for n, nbrdict in G.adjacency()][1] )

    cost, flow = nx.network_simplex(G)
    cost  = cost / (multiplier * multiplier)

    return cost, flow

def signature(g: Graph, offset = 0):
    m = g.adjacency()
    sig = []
    for i in range(g.n):
        u =  g.vertices[i]
        for j in range(g.n):
            if m[i, j] == 0:
                v = g.vertices[j]
                m[i, i] = np.linalg.norm(np.array(u.coords) - np.array(v.coords))
        sig.append( (np.array(u.coords), np.pad(m[i, :], (0, offset), 'constant', constant_values = 0), u) )

    return sig