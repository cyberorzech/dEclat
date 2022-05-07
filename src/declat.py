import pandas as pd
import numpy as np

class dEclat:

    result = dict()

    def dEclat():
        pass

    def dEclat(minSup: int, data: pd.DataFrame = None, filename: str = None):
        
        data = pd.read_csv("../fixtures/result.csv", sep=";")

        if data is None and filename is not None:
            try:
                data = pd.read_csv(filename, sep=';')
            except:
                print("Wrong file")
        
        if data is None:
            return

        start_dict, start_items_list  = dEclat.get_items(data)
        result = start_dict
        dEclat.dEclat_running(start_items_list, minSup)

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

                one_length_items_l.append({cell_ij})
                if cell_ij not in one_length_items_d:
                    one_length_items_d[str({cell_ij})] = [1, T-{i}]
                else:
                    one_length_items_d[cell_ij][0] += 1
                    one_length_items_d[cell_ij][1] -= {i}
        
        return one_length_items_d, one_length_items_l

    def dEclat_running(P: list, minSup: int):
        for i in range(0, len(P)-1):
            print(f"i = {i}")
            Ti = []
            Xi = P[i]
            for j in range(i+1, len(P)-1):
                Xj = P[j]
                R = Xi.union(Xj)
                dR = dEclat.result[str(Xj)][1] - dEclat.result[str(Xi)][1]
                supR = dEclat.result[str(Xi)][0] - len(dEclat.result[str(Xj)][1])
                if supR > minSup:
                    Ti.append(R)
                    dEclat.result[str(R)] = [supR, dR]
            if not Ti:
                dEclat.dEclat_running(Ti, minSup)

if __name__ == "__main__":
    dEclat.dEclat(4)