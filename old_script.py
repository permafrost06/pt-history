# this file is just for testing purposes and reference
# main script has moved to object based parsing
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

def dayToDate(day_int):
    bin = pack(">H", day_int)
    hexstr = bin.hex()
    binarystr = format(int(hexstr, 16), "16b")
    datestr = f"{int(binarystr[-5:], 2)}/{int(binarystr[-9:-5], 2)}/20{int(binarystr[0:-9], 2)}"
    return datestr

# x = open("data/exported_view all 20220427", "rb")   # all data till 27/04/2022
# x = open("data/exported_view 20210804", "rb")   # data from 04/08/2021
# x = open("data/exported_view 20220430", "rb")   # data from 30/04/2022
x = open("data/exported_view 20220101", "rb")   # data from 01/01/2022
# x = open("data/exported_view 20210514", "rb") # data from 14/5/2021

# struct DATABASE {
# 	int version (== 13, as of June 9 2019, format may be different if other version)
# 	int magic (== 'PTFF' on x86)
# 	int numtags
# (version, magic, numtags) = unpack("iii", x.read(12))
version = readBytes("i")
magic = pack("i", readBytes(">i")[0])
numtags = readBytes("i")
print(version, magic, numtags)

# 	struct { char name[32]; int color; } tags[numtags]
for i in range(numtags):
    (name, color) = unpack("<32si", x.read(36))
    print(name, color)

# 	int minfilter
# 	int foldlevel
(minfilter, foldlevel) = unpack("ii", x.read(8))
print(minfilter, foldlevel)

# 	int prefs[10] (see advanced prefs window, also see "prefs" in procrastitracker.cpp)
perfs = unpack("10i", x.read(40))
print(perfs)

# 	NODE root
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
    print(tagindex, ishidden, numberofdays)

    for i in range(numberofdays):    # 	DAY days[numberofdays]

        # timestruct DAY {
        (day,   # 	unsigned short day
                #   (lower 5 bits = day, next 4 bits = month, rest = year counted from 2000)
        firstminuteused,    # 	unsigned short firstminuteused (counted from midnight)
        # 	int activeseconds, semiidleseconds, key, lmb, rmb, scrollwheel
        activeseconds, semiidleseconds, key, lmb, rmb, scrollwheel
        ) = readBytes("HHiiiiii")
        print(day, firstminuteused, activeseconds, semiidleseconds, key, lmb, rmb, scrollwheel)
        print(dayToDate(day))
        print(getHHMMSS(activeseconds))
        # }

    numchildren = readBytes("i")    # 	int numchildren
    for i in range(numchildren):    # 	NODE children[numchildren]
        getNode()
    # }
# }

getNode()