import os
import json
from EMD import GGMD
from ggd import ggd
from graph import Point, Graph

def letter(distortion, C_V, C_E, multiplier):
    PROTOTYPE = []
    n_checks = 0
    n_successes = 0 
    
    prototype_path = 'data/PROTOTYPE/'
    source_path = 'data/Letter/json/' + distortion + '/'
    
    for file in os.listdir(prototype_path):
        data = open(prototype_path + file)
        gxl = json.load(data)
        PROTOTYPE.append((file[0], gxl2Graph(gxl, file[0])))

    for file in os.listdir(source_path):
        # todo: filter only json files
        if file.split('.')[1] != 'json':
            continue
        data = open(source_path + file)
        gxl = json.load(data)
        g = gxl2Graph(gxl)
        match = {}
        for proto in PROTOTYPE:
            d, flow, A = GGMD(g, proto[1], C_V, C_E, multiplier)  
            # d, flow = ggd(g, proto[1], C_V, C_E)  
            
            match[proto[0]] = d
        match = sorted(match.items(), key=lambda x: x[1])
        n_checks += 1
        if(file[0] == match[0][0]):
            n_successes += 1
            # print("S", file, match)
        else:
            pass
            #print("F", file, match)


        for k, v in flow.items():
            if k != "eps1" and k != "eps2":
                if len(v) != 0:
                    for v1 in v.values():
                        if v1 != 0 and v1 != multiplier:
                            print(flow)
    print(C_V, C_E, n_successes / n_checks * 100)
    return n_successes / n_checks * 100

def gxl2Graph(gxl, prefix = ''):
    vertices = []
    edges = []
    for n in gxl["gxl"]["graph"][0]["node"]:
        out = {}  
        out["id"] = prefix + n["$"]["id"]
        for v in n["attr"]:
            out[v["$"]["name"]] = float(v["float"][0])

        vertices.append( Point((out["x"], out["y"]), out["id"]) )
    
    if "edge" in gxl["gxl"]["graph"][0]:        
        for e in gxl["gxl"]["graph"][0]["edge"]:
            fr = next( filter(lambda p: p.label == prefix + e["$"]["from"], vertices) )
            to = next( filter(lambda p: p.label == prefix + e["$"]["to"], vertices) )
            edges.append((fr, to))

    return Graph(vertices, edges)


def main():
    for i in range(10):
        for j in range(10):
            C_V = i / 10.0 * 5
            C_E = j / 10.0 * 5
            print(C_V, C_E, letter('LOW', C_V, C_E, 10000))
    #C_V, C_E = 2, 1
    #letter('LOW', C_V, C_E, 10000)

if __name__ == "__main__":
    main()