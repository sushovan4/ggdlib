#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import cmp_to_key
import graphlib
import numpy as np
import networkx as nx

class Graph:
    """class defining a geometric graph"""
    def __init__(self, vertices, edges):
        ''' Graph with vertices associated to points in d-dimensional space.
        Edges are represented simply as pairs of vertices.
        e.g:
            graph = Graph(...)
        Args:
            vertices: list of Point objects
            edges: list of [Point, Point] lists
        '''
        self.vertices = vertices
        self.edges = edges

    @property
    def d(self):
        ''' Dimension of embedding space. '''
        return self.vertices[0].d

    @property
    def n(self):
        ''' Number of vertices. '''
        return len(self.vertices)

    @property
    def m(self):
        ''' Number of edges. '''
        return len(self.edges)

    @property
    def k(self):
        ''' Number of connected components.'''
        return len(self.components)

    @property
    def components(self):
        ''' Returns the connected components as a dictionary:
            {i: [Points of component i]}
        '''
        cmpts = []
        visited = []
        for v in self.vertices:
            if not v in visited:
                comp_of_v = self.component(v)
                # add vertices from component to visited
                for u in comp_of_v:
                    visited.append(u)
                cmpts.append(comp_of_v)

        return dict(zip(range(len(cmpts)), cmpts))

    def vertex_positions(self):
        return [np.array(u.coords) for u in self.vertices]

    def neighbors(self, v):
        ''' Neighbors of vertex v. '''
        nbrs = []
        for edge in self.edges:
            u1, u2 = edge
            if u1.equals(v):
                nbrs.append(u2)
            elif u2.equals(v):
                nbrs.append(u1)
        return nbrs
        
    def component(self, v):
        ''' Connected component of v. '''
        def cmpt(v, T):
            nhbs = list(set(self.neighbors(v)) - set(T))
            if nhbs == []:
                return [v]
            else:
                T += nhbs # expand the tree
                for nhb in nhbs:
                    T += cmpt(nhb, T) # expand the tree in BFS way
            return list(set(T))
        return cmpt(v, [v]) # start with T = [v]
    
    def adjacency(self):
        mat = np.zeros((self.n, self.n))
        for edge in self.edges:
            u1, u2 = edge
            i = self.indexOf(u1)
            j = self.indexOf(u2)
            
            mat[i, j] = 1
            mat[j, i] = 1
        return mat

    def indexOf(self, v):
        for index, vertex in enumerate(self.vertices):
            if v.equals(vertex):
                return index
        return -1

    def sort(self):
        self.vertices.sort(key = cmp_to_key(compare))

    def toNX(self):
        G = nx.Graph()
        G.add_nodes_from([(u.label, { "coords": u.coords }) for u in self.vertices])
        G.add_edges_from([[e[0].label, e[1].label] for e in self.edges])

        return G

    def sortN(self, points):
        if len(points) < self.n:
            raise Exception("Not enough sites.")
        vertices = [None] * len(points)
        points = np.copy(points)

        for u in self.vertices:
            v, id = nearestNeighbor(u, points)
            vertices[id] = u
            points[id] = None
        self.vertices = [u for u in vertices if u is not None]

class Point:
    ''' Supporting class for storing coordinates and labels of points.
    e.g:
        point = Point(...)
    Args:
        coords::tuple(float)
            The coordinates of a point. Should be a tuple of floats.
        label::str
            Should be: 'E' for edge point and 'V' for vertex point.
    '''
    def __init__(self, coords = (), label = 'P'):
        self.coords = coords
        self.label = label

    def __str__(self):
        return self.label + str(self.coords)

    @property
    def d(self):
        ''' Dimension of embedding space. '''
        return len(self.coords)

    def equals(self, p, eps=1e-4):
        ''' Returns true if point is close to p. '''
        if self.d != p.d:
            return False
        return distance(self, p) < eps
    
def distance(p1, p2):
    p1 = np.array(p1.coords)
    p2 = np.array(p2.coords)
    return np.linalg.norm(p1 - p2)

def compare(u: Point, v: Point):
    if u.coords[0] < v.coords[0]:
        return -1
    elif u.coords[0] > v.coords[0]:
        return 1
    else:
        if u.coords[1] < v.coords[1]:
            return -1
        elif u.coords[1] > v.coords[1]:
            return 1        
    return 0

def nearestNeighbor(p, points):
    neighbor = None
    idx = None
    dist = np.inf
    for i, v in enumerate(points):
        if v == None:
            continue
        d = distance(p, v)
        if d < dist:
            neighbor = v
            dist = d
            idx = i
    return (neighbor, idx)
