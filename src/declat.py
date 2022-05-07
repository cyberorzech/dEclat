from unittest import result
import pandas as pd
import numpy as np

class dEclat:

    result = dict()
    minSup = 0

    temp0 = list()

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

        dEclat.result, start_items_list  = dEclat.get_items(data)
        # dEclat.result = start_dict

        # dEclat.temp0 = start_items_list
        dEclat.dEclat_running(start_items_list)
        # dEclat.convert_to_tids(data.shape[1])

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

                if str({cell_ij}) not in one_length_items_d:
                    one_length_items_d[str({cell_ij})] = [1, T-{i}]
                    one_length_items_l.append({cell_ij})
                else:
                    one_length_items_d[str({cell_ij})][0] += 1
                    one_length_items_d[str({cell_ij})][1] -= {i}
        
        one_length_items_clear = list()

        for i in one_length_items_l:

            if one_length_items_d[str(i)][0] <= dEclat.minSup:
                del one_length_items_d[str(i)]
            else:
                one_length_items_clear.append(i)
                
        return one_length_items_d, one_length_items_clear

    def dEclat_running(P: list):

        for i in range(0, len(P)):
            Ti = []
            Xi = P[i]
            for j in range(i+1, len(P)):
                Xj = P[j]
                R = Xi.union(Xj)
                dR = dEclat.result[str(Xj)][1] - dEclat.result[str(Xi)][1]
                supR = dEclat.result[str(Xi)][0] - len(dR)
                if supR > dEclat.minSup:
                    Ti.append(R)
                    dEclat.result[str(R)] = [supR, dR]
            if not Ti:
                dEclat.dEclat_running(Ti)

    def convert_to_tids(n: int):
        T = set(range(n))

        for key in dEclat.result.keys():
            parent_key = dEclat.get_parent_key(key)
            dEclat.result[key][1] = dEclat.result[parent_key][1] - dEclat.result[key][1] if parent_key else T - dEclat.result[key][1]

    def get_parent_key(key: str):
        return key[0:key.rfind(',')] + '}' if ',' in key else ""

if __name__ == "__main__":
    dEclat.dEclat(4)