import json
from EMD import GGMD
from graph import Point, Graph
from functools import cmp_to_key
import os

class Letter:
    
    def __init__(self, C_V = 1.0, C_E = 1.0, multiplier = 10000, sort = False):
        self.C_V = C_V
        self.C_E = C_E
        self.multiplier = multiplier
        self.sort = sort            

    def findModels(self, graph):
        models = [(f[0], gxl2Graph(json.load(open('data/Letter/PROTOTYPE/' + f)), f[0])) for f in os.listdir('data/Letter/PROTOTYPE/')]
        match =  [ (m[0], GGMD(graph, m[1], self.C_V, self.C_E, self.multiplier, self.sort)[0]) for m in models]
        
        return sorted(match, key = lambda x: x[1])

    def test(self, distortion = 'LOW'):
        n, s = 0, 0
        models = [(f[0], gxl2Graph(json.load(open('data/Letter/PROTOTYPE/' + f)), f[0])) for f in os.listdir('data/Letter/PROTOTYPE/')]
        
        for file in os.listdir('data/Letter/json/' + distortion + '/'):
            if file.split('.')[1] != 'json' or file.split('.')[0] in ['test', 'train', 'validation']:
                continue
            
            data = open('data/Letter/json/' + distortion + '/' + file)
            gxl = json.load(data)
            g = gxl2Graph(gxl)
            match =  [ (m[0], GGMD(g, m[1], self.C_V, self.C_E, self.multiplier, self.sort)[0]) for m in models]
            match.sort(key = lambda x: x[1])
            n += 1

            if(file[0] == match[0][0]):
                s += 1
                # print("S", file, match)
            else:
                pass
                #print("F", file, match)
            print(s / n * 100.0)
        return s / n * 100.0
    
def letter(C_V, C_E, multiplier, sort = True):
    def compare(file1, file2):
        data = open('data/Letter/json/LOW/' + file1["_file"].split('.')[0] + '.json' )            
        g1 = gxl2Graph(json.load(data), 'u')

        data = open('data/Letter/json/LOW/' + file2["_file"].split('.')[0] + '.json' )            
        g2 = gxl2Graph(json.load(data), 'v')

        d1, d2 = GGMD(g1, g, C_V, C_E, multiplier, sort)[0], GGMD(g2, g, C_V, C_E, multiplier, sort)[0]
        
        if d1 < d2:
            return -1
        elif d1 > d2:
            return 1
        else:
            return 0
        
    source_file = 'data/Letter/json/LOW/train.json'
    data = open(source_file)
    files = json.load(data)["GraphCollection"]["fingerprints"]["print"]
        
    for file in files:
        data = open('data/Letter/json/LOW/' + file["_file"].split('.')[0] + '.json' )
        g = gxl2Graph(json.load(data))

        nn = sorted(files, key = cmp_to_key(compare))

        file["_classes"] = [ file["_class"] for file in nn ] 


        with open("nn_output.json", "w") as outfile:
            outfile.write(json.dumps(files))


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
    #for i in range(2,10):
    #    for j in range(2,10):
    #        C_V = i / 10.0 * 5
    #        C_E = j / 10.0 * 5
    #        print(C_V, C_E, letter('LOW', C_V, C_E, 10000, True))
    
    l = Letter(C_V = 1, C_E = 1, sort = True)
    l.test('LOW')

if __name__ == "__main__":
    main()