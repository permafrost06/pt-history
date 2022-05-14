from datetime import timedelta
from PTHistory import Node, PTHistory
import gzip
import json

x = PTHistory()

with gzip.open("data/exported_view all 20220502.PT", "rb") as fp:   # data from 01/01/2022

    x.parseHistory(fp)

    # for child in x.root.children:
    #     print(child)

# obj = x.toDict()
obj = dict(x)

with open("data/dump.json", "w") as fp:
    json.dump(obj, fp)

# print(dict(x))

# def getNodeSeconds(node: Node):
#     seconds = sum(day.activeseconds for day in node.days)
#     for child in node.children:
#         seconds += getNodeSeconds(child)
#     return seconds

# totalseconds = getNodeSeconds(x.root)
# print(timedelta(seconds=totalseconds))

# print(sorted(x.root.children, key=lambda x: x.totalseconds, reverse=True))