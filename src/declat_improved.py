# for testing memory and time measurement
from memory_profiler import profile

import numbers
import pandas as pd
import numpy as np
import json

    

class dEclatImpr:

    # diftidsets[key=wordset] = list([support, diflist])
    diftidsets = dict()
    minSup = 0

    tids = dict()

    @profile
    def dEclatImpr(relMinSup: int, data: pd.DataFrame = None, filename: str = None):

        if data is None and filename is not None:
            try:
                data = pd.read_csv(filename, sep=',', dtype=str, index_col=0)
            except:
                print("Wrong file")
        
        dEclatImpr.minSup = relMinSup if relMinSup else dEclatImpr.minSup

        if data is None:
            return

        dEclatImpr.n = data.shape[0]

        dEclatImpr.minSup = relMinSup * dEclatImpr.n

        # print(data.head)

        dEclatImpr.diftidsets, start_items_list  = dEclatImpr.get_items(data)

        print(f"one element freqsets: {len(dEclatImpr.diftidsets)}")

        # print(dEclatImpr.diftidsets)

        dEclatImpr.dEclatImpr_running(start_items_list)

    def get_items(data: pd.DataFrame):
        
        # n = range(data.shape[1]) # liczba transakcji
        T = set(range(dEclatImpr.n))
        one_length_items_d = dict() # dict[itemset] = [support, transaction_list(tid/dif), tid_or_dif_flag] 
        one_length_items_l = list() 
        for i in range(data.shape[0]):
            for j in range(0, data.shape[1]):
                cell_ij = data.iloc[i, j]
                if isinstance(cell_ij, numbers.Number):
                    continue

                if frozenset({cell_ij}) not in one_length_items_d:
                    one_length_items_d[frozenset({cell_ij})] = [1, {i}, 't']
                    one_length_items_l.append(frozenset({cell_ij}))
                else:
                    one_length_items_d[frozenset({cell_ij})][0] += 1
                    one_length_items_d[frozenset({cell_ij})][1] = one_length_items_d[frozenset({cell_ij})][1].union({i})

            

        for item in one_length_items_l:
            if one_length_items_d[item][0] <= dEclatImpr.minSup:                
                del one_length_items_d[item]
            else:
                if one_length_items_d[item][0] > dEclatImpr.n/2: # convert to diflist
                    one_length_items_d[item][1] = T - one_length_items_d[item][1]
                    one_length_items_d[item][2] = 'd'

        one_length_items_l = dEclatImpr.sort_sets(one_length_items_d)
       
        return one_length_items_d, one_length_items_l

    def sort_sets(items: dict):
        pass
        items_t = {k:v for (k,v) in items.items() if v[2] == 't'}
        items_t_sorted = (sorted(items_t.keys(), key= lambda X: (len(X),X)))
        items_d = {k:v for (k,v) in items.items() if v[2] == 'd'}
        items_d_sorted = (sorted(items_d.keys(), key= lambda X: (-len(X),X)))
        
        items_list = items_t_sorted+items_d_sorted

        return items_list

    def dEclatImpr_running(P: list):

        for i in range(0, len(P)):
            Ti = {}
            Xi = P[i]
            for j in range(i+1, len(P)):
                Xj = P[j]
                R = Xi.union(Xj)
                tdR, tdR_flag = dEclatImpr.calculate_tiddif(Xi, Xj)
                supR = dEclatImpr.calculate_support(Xi, tdR, tdR_flag)
                
                if supR > dEclatImpr.minSup:
                    dEclatImpr.diftidsets[frozenset(R)] = [supR, tdR, tdR_flag]
                    Ti[frozenset(R)] = dEclatImpr.diftidsets[frozenset(R)]

            if Ti:
                Ti = dEclatImpr.sort_sets(Ti)
                dEclatImpr.dEclatImpr_running(Ti)

    def calculate_support(Xi: set, tdR: set, td_flag):
        return len(tdR) if td_flag == "t" else dEclatImpr.diftidsets[frozenset(Xi)][0] - len(tdR)

    def calculate_tiddif(Xi: set, Xj: set):
        Xi_t = dEclatImpr.diftidsets[frozenset(Xi)][2] # dif or tid (flag)
        Xj_t = dEclatImpr.diftidsets[frozenset(Xj)][2] # dif or tid (flag)
        tdXi = dEclatImpr.diftidsets[frozenset(Xi)][1]
        tdXj = dEclatImpr.diftidsets[frozenset(Xj)][1]

        tdR = set()
        td_flag = "d"
        if (Xi_t, Xj_t) == ("t", "t"):
            tdR = tdXi.intersection(tdXj)
            td_flag = "t"
        elif (Xi_t, Xj_t) == ("t", "d"):
            tdR = tdXi.intersection(tdXj)
        elif (Xi_t, Xj_t) == ("d", "d"):
            tdR = tdXj-tdXi

        return tdR, td_flag

    def get_items_and_supp():
        d = {"itemset": list(dEclatImpr.diftidsets.keys()), "support": [e[1][0] for e in dEclatImpr.diftidsets.items()]}
        df = pd.DataFrame(d)
        return df

    def save_to_file(df: pd.DataFrame, filename):
        df.to_csv(filename , sep=";")

        
    def get_value(s: set):
        return dEclatImpr.tids(frozenset({s}))

if __name__ == "__main__":
    file = f"../fixtures/datasets/dataset2_case4"

    data = pd.read_csv(file, sep=',', dtype=str, index_col=0)

    dEclatImpr.dEclatImpr(0.1, data=data)

    # df = dEclatImpr.get_items_and_supp()
    # dEclatImpr.save_to_file(df, "../tests/data/declimpr.csv")

    print("* * * * * * * * * * * * * * * *")
    # print(dEclat.difsets.keys())
    # print("* * * * * * * * * * * * * * * *")
    
    print(f"number of frequent sets: {len(dEclatImpr.diftidsets)}")
