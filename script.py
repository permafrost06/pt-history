from struct import *
from math import floor

def readBytes(formatstr):
    unpacked_tuple = unpack(formatstr, x.read(calcsize(formatstr)))
    if len(formatstr) == 1:
        return unpacked_tuple[0]
    else:
        return unpacked_tuple

def getHHMMSS(seconds):
    timestr = ""
    HH = floor(seconds/(60*60))
    if HH > 0:
        timestr += f"{HH:02d}:"
    else:
        timestr += "00:"
    MM = floor(seconds/60)%60
    if MM > 0:
        timestr += f"{MM:02d}:"
    else:
        timestr += "00:"
    SS = seconds%60
    if SS:
        timestr += f"{SS:02d}"
    else:
        timestr += "00"

    return timestr

x = open("data/exported_view 20220427", "rb")
(version, magic, numtags) = unpack("iii", x.read(12))
print(version, magic, numtags)

for i in range(numtags):
    (name, color) = unpack("<32si", x.read(36))
    print(name, color)

(minfilter, foldlevel) = unpack("ii", x.read(8))
print(minfilter, foldlevel)

perfs = unpack("10i", x.read(40))
print(perfs)

def getNode():

# timestruct NODE {
    name = b''    # 	char *name (null terminated bytes
    lastchar = x.read(1)
    name += lastchar
    while lastchar != b'\x00':
        lastchar = x.read(1)
        name += lastchar
    print(name)
    tagindex = readBytes("i")    # 	int tagindex
    ishidden = readBytes("c")    # 	char ishidden
    numberofdays = readBytes("i")    # 	int numberofdays
    # print(tagindex, ishidden, numberofdays)

    for i in range(numberofdays):    # 	DAY days[numberofdays]

    # timestruct DAY {
        (day,   # 	unsigned short day
                #   (lower 5 bits = day, next 4 bits = month, rest = year counted from 2000)
        firstminuteused,    # 	unsigned short firstminuteused (counted from midnight)
        # 	int activeseconds, semiidleseconds, key, lmb, rmb, scrollwheel
        activeseconds, semiidleseconds, key, lmb, rmb, scrollwheel
        ) = readBytes("HHiiiiii")
        # print(day, firstminuteused, activeseconds, semiidleseconds, key, lmb, rmb, scrollwheel)
        print(getHHMMSS(activeseconds))
    # }

    numchildren = readBytes("i")    # 	int numchildren
    for i in range(numchildren):    # 	NODE children[numchildren]
        getNode()
# }

getNode()
