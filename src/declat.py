# for testing memory and time measurement
from memory_profiler import profile

import numbers
import math
from operator import index

import pandas as pd
import numpy as np
import json

class dEclat:

    # difsets[key=wordset] = list([support, diflist])
    difsets = dict()
    minSup = 0
    n = 0
    tids = dict()

    # @profile
    def dEclat(relMinSup: int, data: pd.DataFrame = None, filename: str = None):
        """
        data - tweets with words, each row is a representation of tweet
        """
        if data is None and filename is not None:
            try:
                data = pd.read_csv(filename, sep=',', dtype=str, index_col=0)
            except:
                print("Wrong file")
        
        dEclat.minSup = relMinSup if relMinSup else dEclat.minSup

        if data is None:
            return

        
        dEclat.n = data.shape[0]

        # dEclat.n = data.shape[1]
        dEclat.minSup = relMinSup * dEclat.n

        # print(data.head)
        # print(data.iloc[0,0])

        dEclat.difsets, start_items_list  = dEclat.get_items(data)

        # print(dEclat.difsets.keys())
        print(f"number of frequent one elemented sets: {len(dEclat.difsets)}")

        dEclat.dEclat_running(start_items_list)

    # @profile
    def get_items(data: pd.DataFrame):
        
        T = set(range(data.shape[0])) # tidlist for empty set (all tweets)
        one_length_items_d = dict()
        one_length_items_l = list()

        for i in range(data.shape[0]):
            for j in range(0, data.shape[1]):
                cell_ij = data.iloc[i, j]

                if isinstance(cell_ij, numbers.Number) and np.isnan(cell_ij):
                    continue

                if frozenset({cell_ij}) not in one_length_items_d:
                    one_length_items_d[frozenset({cell_ij})] = [1, T-{i}]# 0 = 
                    one_length_items_l.append(frozenset({cell_ij}))
                else:
                    one_length_items_d[frozenset({cell_ij})][0] += 1
                    one_length_items_d[frozenset({cell_ij})][1] -= {i}

        for item in one_length_items_l:
            if one_length_items_d[item][0] <= dEclat.minSup:                
                del one_length_items_d[item]

        one_length_items_l = list(sorted(one_length_items_d.keys(), key=lambda X: X))

        return one_length_items_d, one_length_items_l

    def encode_words():

        word_code = {"word": [], "code": []}
        words = list(dEclat.difsets.keys())
        i = 0
        for word in words:
            word_code["word"].append(word)
            word_code["code"].append(i)
            i+=1

        df = pd.DataFrame(word_code)
        # save encoded words to file

    def save_to_file(df: pd.DataFrame, filename):
        df.to_csv(filename, sep=",")

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
            if Ti: # ? not Ti != []
                dEclat.dEclat_running(Ti)

    def get_items_and_supp():
        d = {"itemset": list(dEclat.difsets.keys()), "support": [e[1][0] for e in dEclat.difsets.items()]}
        df = pd.DataFrame(d)
        return df

    def save_to_file(df: pd.DataFrame, filename):
        df.to_csv(filename , sep=";")


    def convert_to_tids():
        T = set(range(dEclat.n))
        for dif in dEclat.difsets.items():
            T = set(range(dEclat.n))
            elems = sorted([x for x in dif[0]])
            for i in range(len(elems)):
                T = T - dEclat.difsets[frozenset(elems)][1]
                elems.pop()
            dEclat.tids[dif[0]] = {'sup': dif[1][0], 'tidlist': [e for e in T]}

    def save_tids_json(outfilename: str = "tids.json"):
        jsontids = {str(e[0]): e[1] for e in dEclat.tids.items()}
        with open(outfilename, 'w') as fp:
            json.dump(jsontids, fp)
        
    def get_value(s: set):
        return dEclat.tids(frozenset({s}))

if __name__ == "__main__":
    file = f"../fixtures/datasets/dataset2_case4"

    data = pd.read_csv(file, sep=',', dtype=str, index_col=0)
#
    dEclat.dEclat(0.1, data=data)#, filename=file)
#

    print("* * * * * * * * * * * * * * * *")
    # print(dEclat.difsets.keys())
    # print("* * * * * * * * * * * * * * * *")
    
    print(f"number of frequent sets: {len(dEclat.difsets)}")

    # dEclat.convert_to_tids()
    # print(dEclat.tids)

    # df = dEclat.get_items_and_supp()

    # file_to_write = "../tests/data/dataset1_case0.csv"
    # dEclat.save_to_file(df, file_to_write)