#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from graph import Graph

def ggd(g1: Graph, g2: Graph, C_V, C_E):
    '''
    pi encodes a matching; it's a map from V(g1) to V(g2). A non-negative entry
    (e.g. pi[i] = j) indicates that the ith vertex of g1 is mapped to the jth
    vertex of g2. If j = -1, then the vertex of g1 is deleted.
    '''
    
    if(g1.n > g2.n):
        g1, g2 = g2, g1
    
    m1, m2 = g1.adjacency(), g2.adjacency()
    pi = np.zeros(g1.n, dtype = np.int32)

    # Define the cost of a matching pi
    def compute_cost(pi):
        cost = 0
        for i, j in enumerate(pi):
            # Vertex translation
            if j != -1:
                cost += C_V * np.linalg.norm(np.array(g1.vertices[i].coords)- np.array(g2.vertices[j].coords)) 

        for i in range(g1.n):
            for j in range(g1.n):
                if m1[i, j] == 1:
                    if (pi[i] == -1) or (pi[j] == -1) or (m2[pi[i], pi[j]] == 0):
                        # Edge deletion from g1
                        cost += C_E * np.linalg.norm(np.array(g1.vertices[i].coords) - np.array(g1.vertices[j].coords))
                    else: 
                        # Edge translation
                        cost += C_E * abs(
                            np.linalg.norm(np.array(g1.vertices[i].coords) - np.array(g1.vertices[j].coords)) - 
                            np.linalg.norm(np.array(g2.vertices[pi[i]].coords) - np.array(g2.vertices[pi[j]].coords))
                        )

        for i in range(g2.n):
            for j in range(g2.n):
                if (m2[i, j] == 1) and (i not in pi or j not in pi or m1[np.where(pi == i)[0][0], np.where(pi == j)[0][0]] == 0):
                    # Edge deletion from g2
                    cost += C_E * np.linalg.norm(np.array(g2.vertices[i].coords) - np.array(g2.vertices[j].coords))
        return cost
 
    # Define the recursion
    def recurse(k, pi):
        if k == g1.n - 1:
            return ( compute_cost(pi), np.copy(pi) )

        k += 1
        pi[k] = -1
        res, pi_opt = recurse(k, pi)

        for m in range(g2.n):
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
    for i in range(g1.n):
        if pi_opt[i] != -1:
            flow_opt.append( (g1.vertices[i], g2.vertices[pi_opt[i]]) )

    return (cost_opt, flow_opt)