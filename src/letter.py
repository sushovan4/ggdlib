import math
import os
import json

from graph import Graph, Point

def letter(distortion, C_V, C_E):
    PROTOTYPE = []
    out = []
    prototype_path = 'data/PROTOTYPE/'
    source_path = 'data/Letter/json/Test/'
    
    for file in os.listdir(prototype_path):
        data = open(prototype_path + file)
        gxl = json.load(data)
        PROTOTYPE.append((file[0], gxl2Graph(gxl)))

    for file in os.listdir(source_path):
        data = open(source_path + file)
        gxl = json.load(data)
        # todo: filter only json files
        dist = math.inf
        closest = None
        g = gxl2Graph(gxl)

        for proto in PROTOTYPE:
            d = GGMD(g, proto[1])[0]
            print(d)
            if( d < dist ):
                closest = proto[0]
                dist = d
        print(file, closest)
    return

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
    
    for e in gxl["gxl"]["graph"][0]["edge"]:
        fr = next( filter(lambda p: p.label == e["$"]["from"], vertices) )
        to = next( filter(lambda p: p.label == e["$"]["to"], vertices) )
        edges.append([fr, to])

    return Graph(vertices, edges)

 #letter('LOW', 1, 1)
