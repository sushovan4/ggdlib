#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from graph import Graph

def GGMD(g1: Graph, g2: Graph, C_V, C_E, multiplier, sort = False):
    if sort:
        if g1.n < g2.n:
            g1, g2 = g2, g1
        g2.sortN(g1.vertices)
    
    # todo: check if the graphs live in the same ambient
    n1, n2 = g1.n, g2.n
    p = min(n1, n2)
    m1, m2 = g1.adjacency(), g2.adjacency()

    S1 = [ (np.array(g1.vertices[i].coords), np.array([ m1[i,j] * np.linalg.norm( np.array(g1.vertices[i].coords) - np.array(g1.vertices[j].coords)) for j in range(n1) ])) for i in range(n1) ]
    S2 = [ (np.array(g2.vertices[i].coords), np.array([ m2[i,j] * np.linalg.norm( np.array(g2.vertices[i].coords) - np.array(g2.vertices[j].coords)) for j in range(n2) ])) for i in range(n2) ]

    G = nx.DiGraph()

    for u in g1.vertices:
        G.add_node(u.label, demand = -1 * multiplier)

    G.add_node("eps1", demand = -n2 * multiplier)

    for v in g2.vertices:
        G.add_node(v.label, demand = 1 * multiplier)
    
    G.add_node("eps2", demand = n1 * multiplier)

    for i in range(n1):
        for j in range(n2):
            # Compute ground cost
            weight = C_V * np.linalg.norm( S1[i][0] - S2[j][0] )
            weight += 0.5 * C_E * np.linalg.norm( np.dot(S1[i][1], np.eye(n1, p)) - np.dot(S2[j][1], np.eye(n2, p)), ord = 1)
            G.add_edge(g1.vertices[i].label, g2.vertices[j].label, weight = round( weight * multiplier) )

    for j in range(n2):
        weight = C_E * np.linalg.norm(S2[j][1], ord = 1)
        G.add_edge("eps1", g2.vertices[j].label, weight = round( weight * multiplier))

    for i in range(n1):
        weight = C_E * np.linalg.norm(S1[i][1], ord = 1)
        G.add_edge(g1.vertices[i].label, "eps2", weight = round( weight * multiplier))
    
    G.add_edge("eps1", "eps2", weight = 0)

    cost, flow = nx.network_simplex(G)
    cost  = cost / (multiplier * multiplier)

    return cost, flow, G