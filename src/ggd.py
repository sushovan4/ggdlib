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
    if g1.n > g2.n:
        g1, g2 = g2, g1
    
    n1, n2 = g1.n, g2.n
    v1 = [np.array(u.coords) for u in g1.vertices]
    v2 = [np.array(v.coords) for v in g2.vertices]
    m1, m2 = g1.adjacency(), g2.adjacency()
    
    pi = np.zeros(n1, dtype = np.int32)

    # Define the cost of a matching pi
    def compute_cost(pi):
        cost = 0
        for i, j in enumerate(pi):
            # Vertex translation
            if j != -1:
                cost += C_V * np.linalg.norm(v1[i]- v2[j])

        for i in range(n1):
            for j in range(i + 1, n1):                
                if m1[i, j] == 1:
                    if pi[i] == -1 or pi[j] == -1 or m2[pi[i], pi[j]] == 0:
                        # Edge deletion from g1
                        cost += C_E * np.linalg.norm(v1[i] - v1[j])
                    else:
                        # Edge translation
                        cost += C_E * abs(
                            np.linalg.norm(v1[i] - v1[j]) - 
                            np.linalg.norm(v2[pi[i]] - v2[pi[j]])
                        )

        for i in range(n2):
            for j in range(i + 1, n2):
                if m2[i, j] == 1:    
                    if i not in pi or j not in pi or m1[np.where(pi == i)[0][0], np.where(pi == j)[0][0]] == 0:
                        # Edge deletion from g2
                        cost += C_E * np.linalg.norm(v2[i] - v2[j])
        #print(cost, pi)
        return cost
 
    # Define the recursion
    def recurse(k, pi):
        if k == n1 - 1:
            return ( compute_cost(pi), pi )

        k += 1
        pi[k] = -1
        res, pi_opt = recurse(k, np.copy(pi))

        for m in range(n2):
            if k > 0 and m in pi[0:k - 1]:
                continue
            pi[k] = m
            res1, pi1 = recurse(k, np.copy(pi))
        
            if res1 < res:
                res = res1
                pi_opt = pi1
        return (res, pi_opt)

    cost_opt, pi_opt = recurse(-1, pi)

    flow_opt = []
    for i in range(n1):
        if pi_opt[i] != -1:
            u, v = g1.vertices[i], g2.vertices[pi_opt[i]]
            flow_opt.append( (u.label, v.label) )

    return (cost_opt, flow_opt)