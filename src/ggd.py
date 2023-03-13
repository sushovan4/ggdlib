#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from graph import Graph

def ggd(g1: Graph, g2: Graph, C_V = 1, C_E = 1):

    m1, m2 = g1.adjacency(), g2.adjacency()
    
    '''
    pi encodes a matching; it's a map from V(g1) to V(g2). A non-negative entry
    (e.g. pi[i] = j) indicates that the ith vertex of g1 is mapped to the jth
    vertex of g2. If j = -1, then the vertex of g1 is deleted.
    '''
    pi = np.zeros(g1.n, dtype = np.int32)

    # Define the recursion
    def recurse(k, l, pi):
        if k == g1.n:
            # Compute the cost
            cost = 0
            for i, j in enumerate(pi):
                # Vertex translation
                if j != -1:
                    cost += C_V * np.linalg.norm(np.array(g1.vertices[i].coords)- np.array(g2.vertices[j].coords)) # type: ignore

            for i in range(g1.n):
                for j in range(g1.n):
                    if m1[i, j] == 1:
                        if (pi[i] == -1) or (pi[j] == -1) or (m2[pi[i], pi[j]] == 0):
                            # Edge deletion from g1
                            cost += C_E * np.linalg.norm( np.array(g1.vertices[i].coords) - np.array(g1.vertices[j].coords) )
                        else: 
                            # Edge translation
                            cost += C_E * abs(
                                np.linalg.norm( np.array(g1.vertices[i].coords) - np.array(g1.vertices[j].coords) ) - 
                                np.linalg.norm( np.array(g2.vertices[pi[i]].coords) - np.array(g2.vertices[pi[j]].coords) ) # type: ignore
                            )
            
            for i in range(g2.n):
                for j in range(g2.n):
                    if (m2[i, j] == 1) and (i not in pi or j not in pi or m1[np.where(pi == i)[0][0], np.where(pi == j)[0][0]] == 0):
                        # Edge deletion from g2
                        cost += C_E * np.linalg.norm( np.array(g2.vertices[i].coords) - np.array(g2.vertices[j].coords) )
            return cost

        pi[k] = -1
        res = recurse(k + 1, l, pi)
        for m in range(g2.n):
            if m == l:
                continue
            pi[k] = m
            res1 = recurse(k + 1, m, pi)
        
            if res1 < res:
                res = res1
        return res

    return recurse(0, -1, pi)