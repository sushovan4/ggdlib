#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from graph import Graph, distance

def GMD(g1: Graph, g2: Graph, C_V, C_E, multiplier, sort = False):
    if sort:
        if g1.n < g2.n:
            g1, g2 = g2, g1
        g2.sortN(g1.vertices)
    
    # todo: check if the graphs live in the same ambient
    n1, n2 = g1.n, g2.n
    p = min(n1, n2)
    m1, m2 = g1.PDD(), g2.PDD()
    #m1, m2 = g1.adjacency1(), g2.adjacency1() 
    
    G = nx.DiGraph()

    for u in g1.vertices:
        G.add_node(u.label, demand = -1 * multiplier)

    G.add_node("eps1", demand = -n2 * multiplier)

    for v in g2.vertices:
        G.add_node(v.label, demand = 1 * multiplier)
    
    G.add_node("eps2", demand = n1 * multiplier)

    for i in range(n1):
        for j in range(n2):
            weight = C_V * distance( g1.vertices[i], g2.vertices[j] )
            weight += C_E * 0.5 * np.linalg.norm( m1[i, :] @ np.eye(n1-1, p) - m2[j, :] @ np.eye(n2-1, p), ord = 1)

            G.add_edge(g1.vertices[i].label, g2.vertices[j].label, weight = round( weight * multiplier) )

    for j in range(n2):
        weight =  C_E * np.linalg.norm( m2[j, :], ord = 1 )
        G.add_edge("eps1", g2.vertices[j].label, weight = round( weight * multiplier))

    for i in range(n1):
        weight = C_E * np.linalg.norm( m1[i, :], ord = 1 )
        G.add_edge(g1.vertices[i].label, "eps2", weight = round( weight * multiplier))
    
    G.add_edge("eps1", "eps2", weight = 0)

    cost, flow = nx.network_simplex(G)
    cost  = cost / (multiplier * multiplier)

    return cost, flow, G