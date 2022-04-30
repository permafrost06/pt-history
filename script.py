from PTHistory import PTHistory
import gzip

x = PTHistory()

fp = gzip.open("data/exported_view 20220101.PT", "rb")   # data from 01/01/2022

x.parseHistory(fp)
print(x.version)
print(x.magic)
print(x.numtags)
print(x.tags)
print(x.root.children[-11].children)