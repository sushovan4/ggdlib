#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from networkx.classes import Graph

def GGMD(g1: Graph, g2: Graph, C_V, C_E, multiplier):
    if g1.order() < g2.order():
        g1, g2 = g2, g1
    # todo: check if the graphs live in the same ambient
    n1, n2 = g1.order(), g2.order()

    G = nx.DiGraph()
    sig1, sig2 = signature(g1), signature(g2, n1 - n2)

    for i in range(n1):
        G.add_node(sig1[i][2], demand = -1 * multiplier)

    G.add_node("eps1", demand = -n2 * multiplier)

    for i in range(n2):
        G.add_node(sig2[i][2], demand = 1 * multiplier)
    
    G.add_node("eps2", demand = n1 * multiplier)

    for i in range(n1):
        for j in range(n2):
            weight = C_V * np.linalg.norm( sig1[i][0] - sig2[j][0] )
            weight += 0.5 * C_E * np.linalg.norm(sig1[i][1] - sig2[j][1], ord = np.inf)
            G.add_edge(sig1[i][2] , sig2[j][2], weight = round( weight * multiplier) )
        weight = 0.5 * C_E * np.sum( sig1[i][1] )
        G.add_edge(sig1[i][2], "eps2", weight = round( weight * multiplier))
    
    for j in range(n2):
        weight = 0.5 * C_E * np.sum( sig2[j][1] ) 
        G.add_edge("eps1", sig2[j][2], weight = round( weight * multiplier))
    
    G.add_edge("eps1", "eps2", weight = 0)

    cost, flow = nx.network_simplex(G)
    cost  = cost / (multiplier * multiplier)

    return cost, flow, G

def signature(g: Graph, offset = 0):
    sig = []
    for i in range(g.order()):
        A = np.zeros(g.order() + offset)
        u =  list(g.nodes)[i]
        for j in range(g.order()):
            v =  list(g.nodes)[j]
            if g.has_edge(u, v):
                A[j] = np.linalg.norm(np.array(g.nodes[u]["coords"]) - np.array(g.nodes[v]["coords"]))
        sig.append( (np.array(g.nodes[u]["coords"]), A,  u) )

    return sig