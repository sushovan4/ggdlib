import json
from GMD import GMD
from graph import Point, Graph
from functools import cmp_to_key
import os
from globals import ROOT_DIR

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

proto_path = os.path.join(ROOT_DIR, 'data', 'Letter', 'PROTOTYPE')
models = [(f[0], gxl2Graph(json.load(open(os.path.join(proto_path, f))), f[0])) for f in os.listdir(proto_path)]

class Letter:

    def __init__(self, C_V = 1.0, C_E = 1.0, multiplier = 10000, sort = False):
        self.C_V = C_V
        self.C_E = C_E
        self.multiplier = multiplier
        self.sort = sort            

    def classify(self, graph):
        return self.findModels(graph)[0][0]
    
    def findModels(self, graph):    
        match =  [ (m[0], GMD(graph, m[1], self.C_V, self.C_E, self.multiplier, self.sort)[0]) for m in models]
        
        return sorted(match, key = lambda x: x[1])

    def test(self, distortion = 'LOW', k = 1):
        n, s = 0, 0
        
        for file in os.listdir('data/Letter/json/' + distortion + '/'):
            if file.split('.')[1] != 'json' or file.split('.')[0] in ['test', 'train', 'validation']:
                continue
            
            data = open('data/Letter/json/' + distortion + '/' + file)
            gxl = json.load(data)
            g = gxl2Graph(gxl)
            matches = self.findModels(g)
            n += 1

            if file[0] in [ m[0] for m in matches[0:k]]:
                s += 1
                # print("S", file, match)
            else:
                pass
                #print("F", file, match)
            print(s / n * 100.0)
        return
    
    def train(self, distortion = 'LOW'):
        train_source = os.path.join(ROOT_DIR, 'data', 'Letter', 'json', distortion, 'train.json')
        files = json.load(open(train_source))["GraphCollection"]["fingerprints"]["print"]

        def compare(file1, file2):
            data = open('data/Letter/json/LOW/' + file1["_file"].split('.')[0] + '.json' )            
            g1 = gxl2Graph(json.load(data), 'u')

            data = open('data/Letter/json/LOW/' + file2["_file"].split('.')[0] + '.json' )            
            g2 = gxl2Graph(json.load(data), 'v')

            d1 = GMD(g1, g, C_V = self.C_V, C_E = self.C_E, multiplier = self.multiplier, sort = self.sort)[0]
            d2 = GMD(g2, g, C_V = self.C_V, C_E = self.C_E, multiplier = self.multiplier, sort = self.sort)[0]
        
            if d1 < d2:
                return -1
            elif d1 > d2:
                return 1
            else:
                return 0
                
        for file in files:
            data = open('data/Letter/json/LOW/' + file["_file"].split('.')[0] + '.json' )
            g = gxl2Graph(json.load(data))

            nn = sorted(files, key = cmp_to_key(compare))

            file["_classes"] = [ file["_class"] for file in nn ] 


            with open("nn_output.json", "w") as outfile:
                outfile.write(json.dumps(files))

def main():
    # for i in range(2,10):
    #    for j in range(2,10):
    #        if i <= j:
    #            continue
    #        C_V = i / 10.0 * 5
    #        C_E = j / 10.0 * 5
    #        l = Letter(C_V, C_E, sort = True)
    #        l.test('LOW', k = 3)
    
    l = Letter(4, 1, sort = False)
    l.test('LOW', k = 3)
    #l.train()

if __name__ == "__main__":
    main()