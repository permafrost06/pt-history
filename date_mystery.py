from struct import *
import sys

d = int(sys.argv[1])
m = int(sys.argv[2])
y = int(sys.argv[3])

print(d,m,y)

# the function used to convert date in procrastitracker c++ code day.h
def dayordering(day, month, year):
    monthfactor = 32
    yfactor = 512
    ybase = 2000

    return day + (month * monthfactor) + ((year - ybase) * yfactor)

date_int = dayordering(d, m, y)

# this seems to work
datebin = format(int(pack(">H", date_int).hex(), 16), "16b")
print(f"{int(datebin[-5:], 2)}/{int(datebin[-9:-5], 2)}/20{int(datebin[0:-9], 2)}")

# converted the one-liner (two?) into a function
def dayToDate(day_int):
    bin = pack(">H", day_int)
    hexstr = bin.hex()
    binarystr = format(int(hexstr, 16), "16b")
    datestr = f"{int(binarystr[-5:], 2)}/{int(binarystr[-9:-5], 2)}/20{int(binarystr[0:-9], 2)}"
    return datestr

print(dayToDate(date_int))

# this is an older function that didn't work, I'm still not sure what exactly is wrong
def binaryToDate(day_int):
    bin = pack("H", day_int)
    hexstr = bin.hex()
    binarystr = format(int(hexstr, 16), "16b")
    datestr = f"{int(binarystr[0:5][::-1], 2)}/{int(binarystr[5:9][::-1], 2)}/20{int(binarystr[9:-1], 2)}"
    return datestr

print(binaryToDate(date_int))