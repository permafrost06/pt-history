from struct import *
from typing import BinaryIO
from datetime import date

def secondsToTimestring(seconds: int):
    mm, ss = divmod(seconds, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

def readBytes(formatstr: str, fp: BinaryIO):
    return unpack(formatstr, fp.read(calcsize(formatstr)))

class Tag:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self) -> str:
        return f"<Tag object '{self.name}'>"

    def __str__(self) -> str:
        return f"Tag: {self.name} - {self.color}"

    def __iter__(self):
        yield self.name, self.color

class Day:
    def __init__(self, fp: BinaryIO):
        (self.day, self.firstminuteused,
        self.activeseconds, self.semiidleseconds,
        self.key, self.lmb, self.rmb, self.scrollwheel
        ) = readBytes("HHiiiiii", fp)

        self.date = self.__dayToDate(self.day)
        self.activetime = secondsToTimestring(self.activeseconds)

    def __repr__(self) -> str:
        return f"<Day object {self.day}>"
    
    def __dayToDate(self, day_int: int):
        bin = pack(">H", day_int)
        hexstr = bin.hex()
        binarystr = format(int(hexstr, 16), "16b")
        day = int(binarystr[-5:], 2)
        month = int(binarystr[-9:-5], 2)
        year = 2000 + int(binarystr[0:-9], 2)
        return date(year, month, day)

    def __iter__(self):
        yield "day", self.day
        yield "date", str(self.date)
        yield "firstminuteused", self.firstminuteused
        yield "activeseconds", self.activeseconds
        yield "activetime", self.activetime
        yield "semiidleseconds", self.semiidleseconds
        yield "key", self.key
        yield "lmb", self.lmb
        yield "rmb", self.rmb
        yield "scrollwheel", self.scrollwheel

class Node:
    def __init__(self):
        self.name: str = ""
        self.tagindex: int = 0
        self.ishidden: str = ""
        self.numberofdays: int = 0

        self.days: list[Day] = []

        self.numchildren: int = 0

        self.children: list['Node'] = []

        self.totalseconds: int = 0

    def __repr__(self) -> str:
        return f"<Node object '{self.name}'>"

    def __readName(self, fp: BinaryIO) -> str:
            name = b''    # 	char *name (null terminated bytes
            # do:
            lastchar = fp.read(1)
            name += lastchar
            while lastchar != b'\x00':
                lastchar = fp.read(1)
                name += lastchar
            
            return name.rstrip(b'\0').decode()

    def parseNode(self, fp: BinaryIO):
        self.name = self.__readName(fp)
        (self.tagindex,) = readBytes("i", fp)
        (self.ishidden,) = readBytes("c", fp)
        self.ishidden = self.ishidden.decode()
        (self.numberofdays,) = readBytes("i", fp)

        for i in range(self.numberofdays):
            day = Day(fp)
            self.totalseconds += day.activeseconds
            self.days.append(day)

        (self.numchildren,) = readBytes("i", fp)

        for i in range(self.numchildren):
            childNode = Node()
            childNode.parseNode(fp)
            self.totalseconds += childNode.totalseconds
            self.children.append(childNode)

    def __iter__(self):
        yield "name", self.name
        yield "tagindex", self.tagindex
        yield "ishidden", self.ishidden
        yield "numberofdays", self.numberofdays
        yield "days", [dict(day) for day in self.days]
        yield "totalseconds", self.totalseconds
        yield "totaltime", secondsToTimestring(self.totalseconds)
        yield "numchildren", self.numchildren
        yield "children", [dict(child) for child in sorted(self.children, key=lambda x: x.totalseconds, reverse=True)]


class PTHistory:
    def __init__(self):
        self.version: int = 0
        self.magic: int = 0
        self.numtags: int = 0

        self.tags: list[Tag] = []
    
        self.minfilter: int = 0
        self.foldlevel: int = 0

        self.perfs: list[int] = []

        self.root: Node = Node()

    def parseHistory(self, fp: BinaryIO):
        (self.version,) = readBytes("i", fp)
        if not self.version == 13:
            raise ValueError("File version is not supported")

        self.magic = pack("i", readBytes(">i", fp)[0])
        if not self.magic == b'PTFF':
            raise ValueError("File is not ProcrastiTracker database file")

        (self.numtags,) = readBytes("i", fp)

        for i in range(self.numtags):
            (name, color) = readBytes("<32si", fp)
            name = name.rstrip(b'\0')
            name = name.decode()
            self.tags.append(Tag(name, color))
        
        (self.minfilter, self.foldlevel) = readBytes("ii", fp)

        self.perfs = list(readBytes("10i", fp))

        self.root.parseNode(fp)

    def __iter__(self):
        yield "version", self.version
        yield "magic", self.magic.decode()
        yield "numtags", self.numtags
        yield "tags", [dict(tag) for tag in self.tags]
        yield "minfilter", self.minfilter
        yield "foldlevel", self.foldlevel
        yield "perfs", self.perfs
        yield "root", dict(self.root)