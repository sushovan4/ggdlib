import os
import json
from EMD import GGMD
import networkx as nx



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

            match[proto[0]] = d
        match = sorted(match.items(), key=lambda x: x[1])
        n_checks += 1
        if(file[0] == match[0][0]):
            n_successes += 1
            # print("S", file, match)
        else:
            print("F", file, match)

        for k, v in flow.items():
            if k != "eps1" and k != "eps2":
                if len(v) != 0:
                    for v1 in v.values():
                        if v1 != 0 and v1 != multiplier:
                            print(flow)

    return n_successes / n_checks * 100

def gxl2Graph(gxl, prefix = ''):
    vertices = []
    edges = []
    for n in gxl["gxl"]["graph"][0]["node"]:
        out = {}  
        out["id"] = prefix + n["$"]["id"]
        for v in n["attr"]:
            out[v["$"]["name"]] = float(v["float"][0])

        vertices.append( (out["id"], { "coords": (out["x"], out["y"]) }) )
    
    if "edge" in gxl["gxl"]["graph"][0]:        
        for e in gxl["gxl"]["graph"][0]["edge"]:
            fr = next( filter(lambda p: p[0] == prefix + e["$"]["from"], vertices) )[0]
            to = next( filter(lambda p: p[0] == prefix + e["$"]["to"], vertices) )[0]
            edges.append((fr, to))

    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    return G


def main():
    C_V = 2
    C_E = 1
    print( letter('MED', C_V, C_E, 1000) )

#for i in range(100):
#    for j in range(100):
#        C_V = i / 100.0 * 5
#        C_E = j / 100.0 * 5
#        print( C_V, C_E, letter('LOW', C_V, C_E) )

if __name__ == "__main__":
    main()