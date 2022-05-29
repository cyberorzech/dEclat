import sys

sys.path.append("../")

from src.declat import *


filename = "../fixtures/result.csv"

data = pd.read_csv(filename, sep=';')

# print(data)

def save_tids_json_test():
    dEclat.dEclat(0, data)
    dEclat.convert_to_tids()
    dEclat.save_tids_json()

save_tids_json_test()