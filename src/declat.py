from unittest import result
import pandas as pd
import numpy as np

class dEclat:

    difsets = dict()
    minSup = 0

    one_el_tids = dict()

    
    def dEclat(minSup: int, data: pd.DataFrame = None, filename: str = None):
        
        data = pd.read_csv("../fixtures/result.csv", sep=";")

        if data is None and filename is not None:
            try:
                data = pd.read_csv(filename, sep=';')
            except:
                print("Wrong file")
        
        dEclat.minSup = minSup if minSup else dEclat.minSup

        if data is None:
            return

        dEclat.n = data.shape[1]

        dEclat.difsets, start_items_list  = dEclat.get_items(data)

        dEclat.dEclat_running(start_items_list)

    def get_items(data: pd.DataFrame):
        """
        
        """
        T = set(range(data.shape[1]))
        one_length_items_d = dict()
        one_length_items_l = list()
        for i in range(data.shape[1]):
            for j in range(0, data.shape[0]):
                cell_ij = data.iat[j, i]
                if cell_ij is np.nan:
                    break

                if frozenset({cell_ij}) not in one_length_items_d:
                    one_length_items_d[frozenset({cell_ij})] = [1, T-{i}]
                    one_length_items_l.append(frozenset({cell_ij}))
                else:
                    one_length_items_d[frozenset({cell_ij})][0] += 1
                    one_length_items_d[frozenset({cell_ij})][1] -= {i}

        for item in one_length_items_l:
            if one_length_items_d[item][0] <= dEclat.minSup:                
                del one_length_items_d[item]

        one_length_items_l = list(sorted(one_length_items_d.keys(), key=lambda X: next(iter(X))))

        return one_length_items_d, one_length_items_l

    def dEclat_running(P: list):

        for i in range(0, len(P)):
            Ti = []
            Xi = P[i]
            for j in range(i+1, len(P)):
                Xj = P[j]
                R = Xi.union(Xj)
                dR = dEclat.difsets[frozenset(Xj)][1] - dEclat.difsets[frozenset(Xi)][1]
                supR = dEclat.difsets[frozenset(Xi)][0] - len(dR)
                if supR > dEclat.minSup:
                    Ti.append(R)
                    dEclat.difsets[frozenset(R)] = [supR, dR]
            if not Ti:
                dEclat.dEclat_running(Ti)

    def convert_to_tids():
        T = set(range(dEclat.n))
        for dif in dEclat.difsets.items():
            if len(dif[0]) == 1:
                dEclat.one_el_tids[dif[0]] = T - dif[1][1]
        
    def get_tidlist(elems: frozenset):
        tid = {}
        it = 0 
        for el in elems:
            if it == 0:
                tid = dEclat.one_el_tids[frozenset({el})]
                it = 1
            else:
                print(type(tid))
                tid = tid.intersection(dEclat.one_el_tids[frozenset({el})])
        return tid

if __name__ == "__main__":
    dEclat.dEclat(4)