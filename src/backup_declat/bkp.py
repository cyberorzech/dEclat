d = {frozenset({"a", "b", "d"}): [6, {1,5,6,7}, "d"], frozenset({"a", "c"}): [2, {1,4}, "t"], frozenset({"a"}): [5, {1,4,5,6,7}, "t"], frozenset({"a", "c", "e"}): [4, {1,4}, "d"] }


dt = {k:v for (k,v) in d.items() if v[2] == 't'}

dts = sorted(dt.keys(), key= lambda X: (len(X[0]),X[0]))