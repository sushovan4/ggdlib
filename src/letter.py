import math
import os
import json
from EMD import GGMD

from graph import Graph, Point

def letter(distortion, C_V, C_E):
    PROTOTYPE = []
    n_checks = 0
    n_successes = 0 
    
    prototype_path = 'data/PROTOTYPE/'
    source_path = 'data/Letter/json/' + distortion + '/'
    
    for file in os.listdir(prototype_path):
        data = open(prototype_path + file)
        gxl = json.load(data)
        PROTOTYPE.append((file[0], gxl2Graph(gxl)))

    for file in os.listdir(source_path):
        # todo: filter only json files
        if file.split('.')[1] != 'json':
            continue
        data = open(source_path + file)
        gxl = json.load(data)
        dist = math.inf
        closest = None
        g = gxl2Graph(gxl)

        for proto in PROTOTYPE:
            d = GGMD(g, proto[1], C_V, C_E, 100)[0]
    
            if( d < dist ):
                closest = proto[0]
                dist = d
        n_checks += 1
        if(file[0] == closest):
            n_successes += 1

    return n_successes / n_checks * 100

def gxl2Graph(gxl):
    vertices = []
    edges = []
    for n in gxl["gxl"]["graph"][0]["node"]:
        out = {}  
        out["id"] = n["$"]["id"]
        for v in n["attr"]:
            out[v["$"]["name"]] = float(v["float"][0])
        p = Point((out["x"], out["y"]), out["id"])
        vertices.append(p)
    
    if "edge" in gxl["gxl"]["graph"][0]:        
        for e in gxl["gxl"]["graph"][0]["edge"]:
            fr = next( filter(lambda p: p.label == e["$"]["from"], vertices) )
            to = next( filter(lambda p: p.label == e["$"]["to"], vertices) )
            edges.append([fr, to])

    return Graph(vertices, edges)

C_V = 2
C_E = 0.3
print( C_V, C_E, letter('LOW', C_V, C_E) )
