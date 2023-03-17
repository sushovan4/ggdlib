#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from networkx.classes import Graph

def ggd(g1: Graph, g2: Graph, C_V, C_E):
    '''
    pi encodes a matching; it's a map from V(g1) to V(g2). A non-negative entry
    (e.g. pi[i] = j) indicates that the ith vertex of g1 is mapped to the jth
    vertex of g2. If j = -1, then the vertex of g1 is deleted.
    '''
    if g1.order() > g2.order():
        g1, g2 = g2, g1
    
    n1, n2 = g1.order(), g2.order()     
    # m1, m2 = g1.adjacency(), g2.adjacency()
    pi = np.zeros(n1, dtype = np.int32)

    # Define the cost of a matching pi
    def compute_cost(pi):
        cost = 0
        for i, j in enumerate(pi):
            # Vertex translation
            if j != -1:
                u, v = list(g1.nodes)[i], list(g2.nodes)[j] 
                cost += C_V * np.linalg.norm(np.array(g1.nodes[u]["coords"])- np.array(g2.nodes[v]["coords"])) 

        for i in range(n1):
            for j in range(n1):
                u1, u2 = list(g1.nodes)[i], list(g1.nodes)[j]
                
                if g1.has_edge(u1, u2):
                    if pi[i] != -1 and pi[j] != -1:
                        v1, v2 = list(g2.nodes)[pi[i]], list(g2.nodes)[pi[j]]
                        if g2.has_edge(v1, v2):
                            # Edge translation
                            cost += C_E * abs(
                                np.linalg.norm(np.array(g1.nodes[u1]["coords"]) - np.array(g1.nodes[u2]["coords"])) - 
                                np.linalg.norm(np.array(g2.nodes[v1]["coords"]) - np.array(g2.nodes[v2]["coords"]))
                            )
                        else: 
                            # Edge deletion from g1
                            cost += C_E * np.linalg.norm(np.array(g1.nodes[u1]["coords"]) - np.array(g1.nodes[u2]["coords"]))
                    else:
                        # Edge deletion from g1
                        cost += C_E * np.linalg.norm(np.array(g1.nodes[u1]["coords"]) - np.array(g1.nodes[u2]["coords"]))

        for i in range(n2):
            for j in range(n2):
                v1, v2 = list(g2.nodes)[i], list(g2.nodes)[j]
                if g2.has_edge(v1, v2):    
                    if i not in pi or j not in pi:
                        # Edge deletion from g2
                        cost += C_E * np.linalg.norm(np.array(g2.nodes[v1]["coords"]) - np.array(g2.nodes[v2]["coords"]))
                    else:
                        i1, j1 = np.where(pi == i)[0][0], np.where(pi == j)[0][0]
                        u1, u2 = list(g1.nodes)[i1], list(g1.nodes)[j1]
                        if not g1.has_edge(u1, u2):
                            # Edge deletion from g2
                            cost += C_E * np.linalg.norm(np.array(g2.nodes[v1]["coords"]) - np.array(g2.nodes[v2]["coords"]))
        return cost
 
    # Define the recursion
    def recurse(k, pi):
        if k == n1 - 1:
            return ( compute_cost(pi), np.copy(pi) )

        k += 1
        pi[k] = -1
        res, pi_opt = recurse(k, pi)

        for m in range(n2):
            # if k > 0 and m == pi[k - 1]:
            #    continue
            pi[k] = m
            res1, pi1 = recurse(k, pi)
        
            if res1 < res:
                res = res1
                pi_opt = pi1
        return (res, pi_opt)

    cost_opt, pi_opt = recurse(-1, pi)

    flow_opt = []
    for i in range(n1):
        if pi_opt[i] != -1:
            u, v = list(g1.nodes)[i], list(g2.nodes)[pi_opt[i]]
            flow_opt.append( (u, v) )

    return (cost_opt, flow_opt)