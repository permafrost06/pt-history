from struct import *
from math import floor
from typing import BinaryIO
from datetime import date, timedelta

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

class Day:
    def __init__(self, fp: BinaryIO):
        (self.day, self.firstminuteused,
        self.activeseconds, self.semiidleseconds,
        self.key, self.lmb, self.rmb, self.scrollwheel
        ) = readBytes("HHiiiiii", fp)

        self.date = self.__dayToDate(self.day)
        self.activetime = self.__secondsToTimeDelta(self.activeseconds)

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

    def __secondsToTimeDelta(self, seconds: int):
        return timedelta(seconds=seconds)

class Node:
    def __init__(self):
        self.name: str = ""
        self.tagindex: int = 0
        self.ishidden: str = ""
        self.numberofdays: int = 0

        self.days: list[Day] = []

        self.numchildren: int = 0

        self.children: list['Node'] = []

    def __repr__(self) -> str:
        return f"<Node object '{self.name}'>"

    def __readName(self, fp: BinaryIO) -> str:
            name = b''    # 	char *name (null terminated bytes
            # do
            lastchar = fp.read(1)
            name += lastchar
            while lastchar != b'\x00':
                lastchar = fp.read(1)
                name += lastchar
            
            return name

    def createRoot(self, fp: BinaryIO):
        self.name = self.__readName(fp)
        (self.tagindex,) = readBytes("i", fp)
        (self.ishidden,) = readBytes("c", fp)
        (self.numberofdays,) = readBytes("i", fp)

        for i in range(self.numberofdays):
            self.days.append(Day(fp))
        
        (self.numchildren,) = readBytes("i", fp)

        for i in range(self.numchildren):
            childNode = Node()
            childNode.getChild(fp)
            self.children.append(childNode)

    def getChild(self, fp: BinaryIO):
        name = self.__readName(fp)
        name = name.rstrip(b'\0')
        name = name.decode()
        self.name = name

        (self.tagindex,) = readBytes("i", fp)
        (self.ishidden,) = readBytes("c", fp)
        (self.numberofdays,) = readBytes("i", fp)

        for i in range(self.numberofdays):
            self.days.append(Day(fp))
        
        (self.numchildren,) = readBytes("i", fp)

        for i in range(self.numchildren):
            childNode = Node()
            childNode.getChild(fp)
            self.children.append(childNode)

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

        self.root.createRoot(fp)
