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
    m1, m2 = g1.adjacency(), g2.adjacency()

    G = nx.DiGraph()

    for u in g1.vertices:
        G.add_node(u.label, demand = -1 * multiplier)

    G.add_node("eps1", demand = -n2 * multiplier)

    for v in g2.vertices:
        G.add_node(v.label, demand = 1 * multiplier)
    
    G.add_node("eps2", demand = n1 * multiplier)

    for i in range(n1):
        u = g1.vertices[i]
        for j in range(n2):
            v = g2.vertices[j]
            # Compute ground cost
            weight = C_V * np.linalg.norm( np.array(u.coords) - np.array(v.coords))
            l = 0

            for k in range(min(n1, n2)):                
                if k >= n1:
                    if m2[j, k] ==  1:
                        x = g2.vertices[k]
                        #l += np.linalg.norm( np.array(v.coords) - np.array(x.coords))
                    continue

                if k >= n2:
                    if m1[i, k] ==  1:
                        w = g1.vertices[k]
                        #l += np.linalg.norm( np.array(u.coords) - np.array(w.coords))
                    continue
                
                w, x = g1.vertices[k], g2.vertices[k]
                if m1[i, k] == 1 and m2[j, k] == 1:
                    l += abs(
                        np.linalg.norm( np.array(u.coords) - np.array(w.coords)) -
                        np.linalg.norm( np.array(v.coords) - np.array(x.coords))
                    )
                elif m1[i, k] == 0 and m2[j, k] == 1:
                    l += np.linalg.norm( np.array(v.coords) - np.array(x.coords))
                elif m1[i, k] == 1 and m2[j, k] == 0:
                    l += np.linalg.norm( np.array(u.coords) - np.array(w.coords))
            
            weight += 0.5 * C_E * l
            G.add_edge(u.label, v.label, weight = round( weight * multiplier) )
    
    for j in range(n2):
        l = 0
        u = g2.vertices[j]
        for k in range(n2):
            if m2[j, k] == 1:
                v =  g2.vertices[k]
                l += np.linalg.norm( np.array(u.coords) - np.array(v.coords) )
        weight = 0.5 * C_E * l
        G.add_edge("eps1", u.label, weight = round( weight * multiplier))

    for i in range(n1):
        l = 0
        u = g1.vertices[i]
        for k in range(n1):
            if m1[i, k] == 1:
                v =  g1.vertices[k]
                l += np.linalg.norm( np.array(u.coords) - np.array(v.coords) )
        weight = 0.5 * C_E * l
        G.add_edge(u.label, "eps2", weight = round( weight * multiplier))
    
    G.add_edge("eps1", "eps2", weight = 0)

    cost, flow = nx.network_simplex(G)
    cost  = cost / (multiplier * multiplier)

    return cost, flow, G

# def signature(g: Graph, offset = 0):
#     sig = []
#     for i in range(g.order()):
#         A = np.zeros(g.order() + offset)
#         u =  list(g.nodes)[i]
#         for j in range(g.order()):
#             v =  list(g.nodes)[j]
#             if g.has_edge(u, v):
#                 A[j] = np.linalg.norm(np.array(g.nodes[u]["coords"]) - np.array(g.nodes[v]["coords"]))
#         sig.append( (np.array(g.nodes[u]["coords"]), A,  u) )

#     return sig