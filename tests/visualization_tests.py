from ast import keyword
import sys

sys.path.append("../")

import matplotlib.pyplot as plt
from src.declat import *

plt.style.use('ggplot')

minSup = 5
n = 8
keywords = {"poland"}
title = f"Keywords: {str(keywords)}"

dEclat.dEclat(minSup)

difsorted = sorted(dEclat.difsets.items(), key=lambda x: x[1][0], reverse=True)

i = 0

x = list()
y = list()

for item in difsorted:
    s = str(item[0])
    s = s[11:len(s)-2]
    
    if any(el in {"rt"}.union(keywords) for el in item[0]):
        continue

    x.append(s)
    y.append(item[1][0])

    i+=1
    if i >= n:
        break

print(f"i = {i}")

x_pos = range(0, n)

plt.bar(x_pos, y, color='green')
plt.xlabel("Itemsets")
plt.ylabel("Support of Itemset")
plt.title(title)
plt.xticks(x_pos, x)

plt.show()