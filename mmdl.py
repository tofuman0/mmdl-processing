import sys
import struct
from dataclasses import dataclass, field
import re

class MMDL:
    def __init__(self):
        self.fileName = str()
        self.objectTableSize = int()
        self.verticesTableSize = int()
        self.verticesEntrySize = int()
        self.verticesCount = int()
        self.faceTableSize = int()
        self.faceEntrySize = int()
        self.faceCount = int()
        self.unknownValue1 = int()
        self.objectEntries = self.ObjectBase()
        self.verticesTable = []
        self.faceTable = []
        self.verticesEntryStructures = [
                [
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Unknown Value 4", float],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float],
                    ["Colour", int, 4],
                    ["Unknown Value 7", float],
                    ["Unknown Value 8", float]
                ],
                [
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Colour", int, 4],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float]
                ]
            ]
        
    @dataclass
    class ObjectBase:
        UnknownValue1: float = 0.0
        UnknownValue2: float = 0.0
        UnknownValue3: float = 0.0
        UnknownValue4: float = 0.0
        UnknownValue5: float = 0.0
        UnknownValue6: float = 0.0
        UnknownValue7: float = 0.0
        UnknownValue8: int = 0
        UnknownValue9: int = 0
        UnknownValue10: int = 0
        UnknownValue11: int = 0
        SubEntryCount: int = 0
        ID: int = 0
        Entries: list = field(default_factory=list)

    @dataclass 
    class Object1:
        UnknownValue1: float = 0.0
        UnknownValue2: float = 0.0
        UnknownValue3: float = 0.0
        UnknownValue4: float = 0.0
        UnknownValue5: float = 0.0
        UnknownValue6: float = 0.0
        UnknownValue7: float = 0.0
        UnknownValue8: float = 0.0
        SubEntryCount: int = 0
        ID: int = 0
        Entries: list = field(default_factory=list)

    @dataclass
    class Object2:
        UnknownValue1: float = 0.0
        Name: str = str()
        UnknownValue2: float = 0.0
        UnknownValue3: float = 0.0
        UnknownValue4: float = 0.0
        UnknownValue5: float = 0.0
        UnknownValue6: float = 0.0
        UnknownValue7: float = 0.0
        UnknownValue8: float = 0.0
        UnknownValue9: float = 0.0
        UnknownValue10: float = 0.0
        UnknownValue11: float = 0.0
        UnknownValue12: float = 0.0
        UnknownValue13: float = 0.0
        UnknownValue14: float = 0.0
        UnknownValue15: float = 0.0
        UnknownValue16: float = 0.0
        UnknownValue17: float = 0.0
        UnknownValue18: float = 0.0
        UnknownValue19: float = 0.0
        UnknownValue20: float = 0.0
        UnknownValue21: float = 0.0
        UnknownValue22: float = 0.0
        UnknownValue23: float = 0.0
        UnknownValue24: float = 0.0
        UnknownValue25: float = 0.0
        SubEntryCount: int = 0
        ID: int = 0
        Entries: list = field(default_factory=list)
    
    @dataclass
    class Object3:
        UnknownValue1: int = 0
        VerticeOffset: int = 0
        VerticeCount: int = 0
        FaceOffset: int = 0
        FaceCount: int = 0
        UnknownValue2: float = 0.0
        UnknownValue3: float = 0.0
        UnknownValue4: float = 0.0
        UnknownValue5: float = 0.0
        UnknownValue6: float = 0.0
        UnknownValue7: float = 0.0
        UnknownValue8: float = 0.0
        UnknownValue9: float = 0.0
        UnknownValue10: float = 0.0
        UnknownValue11: float = 0.0
        UnknownValue12: float = 0.0
        UnknownValue13: float = 0.0
        UnknownValue14: float = 0.0
        UnknownValue15: float = 0.0
        UnknownValue16: float = 0.0
        UnknownValue17: float = 0.0
        UnknownValue18: float = 0.0
        MaterialName: str = str()
        UnknownValue19: float = 0.0
        TextureName: str = str()
        ID: int = 0

    @dataclass
    class Vertice1:
        X: float = 0.0
        Y: float = 0.0
        Z: float = 0.0
        Colour :int = 0
        U: float = 0.0
        V: float = 0.0

    @dataclass
    class Vertice2:
        X: float = 0.0
        Y: float = 0.0
        Z: float = 0.0
        Colour :int = 0
        U: float = 0.0
        V: float = 0.0
        NX: float = 0.0
        NY: float = 0.0
        NZ: float = 0.0

    def ReadMMDL(self, filename):
        file = open(filename, "rb")
        self.fileType = file.read(4)
        if (self.fileType != b"LDMM"):
            raise Exception(f'Not An MMDL File: {filename}')
        fileNameOnly = re.split(r"\\|/", filename)
        self.fileName = fileNameOnly.pop()
        
        # File header
        self.objectTableSize = self.toInt(file.read(4))
        self.verticesTableSize = self.toInt(file.read(4))
        self.faceTableSize = self.toInt(file.read(4))
        self.unknownValue1 = self.toInt(file.read(4))
        self.verticesEntrySize = self.toInt(file.read(4))
        self.verticesCount = self.toInt(file.read(4))
        self.faceEntrySize = self.toInt(file.read(4))
        self.faceCount = self.toInt(file.read(4))
        
        # Object Table
        # Read Initial Entry (Structure 0)
        self.objectEntries.UnknownValue1 = self.toFloat(file.read(4))
        self.objectEntries.UnknownValue2 = self.toFloat(file.read(4))
        self.objectEntries.UnknownValue3 = self.toFloat(file.read(4))
        self.objectEntries.UnknownValue4 = self.toFloat(file.read(4))
        self.objectEntries.UnknownValue5 = self.toFloat(file.read(4))
        self.objectEntries.UnknownValue6 = self.toFloat(file.read(4))
        self.objectEntries.UnknownValue7 = self.toFloat(file.read(4))
        self.objectEntries.UnknownValue8 = self.toInt(file.read(4))
        self.objectEntries.UnknownValue9 = self.toInt(file.read(4))
        self.objectEntries.UnknownValue10 = self.toInt(file.read(4))
        self.objectEntries.UnknownValue11 = self.toInt(file.read(4))
        self.objectEntries.SubEntryCount = self.toInt(file.read(4))
        self.objectEntries.ID = self.toInt(file.read(4))

        # Read Object 1 (Structure 1)
        for i in range(self.objectEntries.SubEntryCount):
            __object1 = self.Object1()
            __object1.UnknownValue1 = self.toFloat(file.read(4))
            __object1.UnknownValue2 = self.toFloat(file.read(4))
            __object1.UnknownValue3 = self.toFloat(file.read(4))
            __object1.UnknownValue4 = self.toFloat(file.read(4))
            __object1.UnknownValue5 = self.toFloat(file.read(4))
            __object1.UnknownValue6 = self.toFloat(file.read(4))
            __object1.UnknownValue7 = self.toFloat(file.read(4))
            __object1.UnknownValue8 = self.toFloat(file.read(4))
            __object1.SubEntryCount = self.toInt(file.read(4))
            __object1.ID = self.toInt(file.read(4))
            self.objectEntries.Entries.append(__object1)

        # Read Object 2 (Structure 2)
        for entry in self.objectEntries.Entries:
            for i in range(entry.SubEntryCount):
                __object2 = self.Object2()
                __object2.UnknownValue1 = self.toFloat(file.read(4))
                __object2.Name = self.toStr(file.read(32))
                __object2.UnknownValue2 = self.toFloat(file.read(4))
                __object2.UnknownValue3 = self.toFloat(file.read(4))
                __object2.UnknownValue4 = self.toFloat(file.read(4))
                __object2.UnknownValue5 = self.toFloat(file.read(4))
                __object2.UnknownValue6 = self.toFloat(file.read(4))
                __object2.UnknownValue7 = self.toFloat(file.read(4))
                __object2.UnknownValue8 = self.toFloat(file.read(4))
                __object2.UnknownValue9 = self.toFloat(file.read(4))
                __object2.UnknownValue10 = self.toFloat(file.read(4))
                __object2.UnknownValue11 = self.toFloat(file.read(4))
                __object2.UnknownValue12 = self.toFloat(file.read(4))
                __object2.UnknownValue13 = self.toFloat(file.read(4))
                __object2.UnknownValue14 = self.toFloat(file.read(4))
                __object2.UnknownValue15 = self.toFloat(file.read(4))
                __object2.UnknownValue16 = self.toFloat(file.read(4))
                __object2.UnknownValue17 = self.toFloat(file.read(4))
                __object2.UnknownValue18 = self.toFloat(file.read(4))
                __object2.UnknownValue19 = self.toFloat(file.read(4))
                __object2.UnknownValue20 = self.toFloat(file.read(4))
                __object2.UnknownValue21 = self.toFloat(file.read(4))
                __object2.UnknownValue22 = self.toFloat(file.read(4))
                __object2.UnknownValue24 = self.toFloat(file.read(4))
                __object2.UnknownValue25 = self.toFloat(file.read(4))
                __object2.SubEntryCount = self.toInt(file.read(4))
                __object2.ID = self.toInt(file.read(4))
                entry.Entries.append(__object2)
            
        # Read Object 3 (Structure 3)
            for subentry in entry.Entries:
                for i in range(subentry.SubEntryCount):
                    __object3 = self.Object3()
                    __object3.UnknownValue1 = self.toInt(file.read(4))
                    __object3.VerticeOffset = self.toInt(file.read(4))
                    __object3.VerticeCount = self.toInt(file.read(4))
                    __object3.FaceOffset = self.toInt(file.read(4))
                    __object3.FaceCount = self.toInt(file.read(4))
                    __object3.UnknownValue2 = self.toFloat(file.read(4))
                    __object3.UnknownValue3 = self.toFloat(file.read(4))
                    __object3.UnknownValue4 = self.toFloat(file.read(4))
                    __object3.UnknownValue5 = self.toFloat(file.read(4))
                    __object3.UnknownValue6 = self.toFloat(file.read(4))
                    __object3.UnknownValue7 = self.toFloat(file.read(4))
                    __object3.UnknownValue8 = self.toFloat(file.read(4))
                    __object3.UnknownValue9 = self.toFloat(file.read(4))
                    __object3.UnknownValue10 = self.toFloat(file.read(4))
                    __object3.UnknownValue11 = self.toFloat(file.read(4))
                    __object3.UnknownValue12 = self.toFloat(file.read(4))
                    __object3.UnknownValue13 = self.toFloat(file.read(4))
                    __object3.UnknownValue14 = self.toFloat(file.read(4))
                    __object3.UnknownValue15 = self.toFloat(file.read(4))
                    __object3.UnknownValue16 = self.toFloat(file.read(4))
                    __object3.UnknownValue17 = self.toFloat(file.read(4))
                    __object3.UnknownValue18 = self.toFloat(file.read(4))
                    __object3.MaterialName = self.toStr(file.read(32))
                    __object3.UnknownValue19 = self.toFloat(file.read(4))
                    __object3.TextureName = self.toStr(file.read(32))
                    __object3.ID = self.toInt(file.read(4))
                    subentry.Entries.append(__object3)

        
        # Vertices Table
        file.seek(16 + self.objectTableSize)
        for i in range(self.verticesCount):
            if (self.verticesEntrySize == 24):
                vertice = self.Vertice1()
                vertice.X = self.toFloat(file.read(4))
                vertice.Y = self.toFloat(file.read(4))
                vertice.Z = self.toFloat(file.read(4))
                vertice.Colour = self.toInt(file.read(4))
                vertice.U = self.toFloat(file.read(4))
                vertice.V = self.toFloat(file.read(4))
                self.verticesTable.append(vertice)
            elif (self.verticesEntrySize == 36):
                vertice = self.Vertice2()
                vertice.X = self.toFloat(file.read(4))
                vertice.Y = self.toFloat(file.read(4))
                vertice.Z = self.toFloat(file.read(4))
                vertice.Colour = self.toInt(file.read(4))
                vertice.U = self.toFloat(file.read(4))
                vertice.V = self.toFloat(file.read(4))
                vertice.NX = self.toFloat(file.read(4))
                vertice.NY = self.toFloat(file.read(4))
                vertice.NZ = self.toFloat(file.read(4))
                self.verticesTable.append(vertice)
            else:
                raise Exception(f'Unsupported Vertices Size: {self.vertSize}')

        # Face Table
        file.seek(16 + self.objectTableSize + self.verticesTableSize)
        for i in range(self.faceCount):
            self.faceTable.append(self.toInt(file.read(self.faceEntrySize)))
        file.close()

    def WriteMMDL(self, filename):
        # TODO: Write MMDL
        return
        file = open(filename, "wb")

        # Write Header
        file.write(b"LDMM")
        file.write(self.toBytes(self.GetObjectTableSize(), 4))
        file.write(self.toBytes(self.GetVerticesTableSize(), 4))
        file.write(self.toBytes(self.GetFaceTableSize(), 4))
        file.write(self.toBytes(self.unknownValue1, 4))
        file.write(self.toBytes(self.verticesEntrySize, 4))
        file.write(self.toBytes(self.GetVerticesCount(), 4))
        file.write(self.toBytes(self.faceEntrySize, 4))
        file.write(self.toBytes(self.GetFaceCount(), 4))

        # Write Object Table
        #for object in self.objectTable:
        #    for value in object[1:]:
        #        if (type(value) is str):
        #            if(value == '[NO NAME]'):
        #                file.write(self.toBytes(int(0), 4))
        #            else:
        #                file.write(self.toBytes(value, len(value)))
        #                strRemainder = 32 - len(value)
        #                for i in range(strRemainder):
        #                    file.write(b'\0')
        #        else:
        #            file.write(self.toBytes(value, 4))

        # Write Vertices Table
        for vertice in self.verticesTable:
            for value in vertice:
                file.write(self.toBytes(value, 4))

        # Write Faces Table
        for value in self.faceTable:
            file.write(self.toBytes(value, self.faceEntrySize))

        file.close()

    def InitializeMMDL(self, unknownValue = 0x142, verticeSize = 24, faceSize = 2):
        self.unknownValue1 = unknownValue
        self.verticesEntrySize = verticeSize
        self.faceEntrySize = faceSize
        self.objectEntries = self.ObjectBase()
        self.objectTableSize = 0
        self.verticesTable = []
        self.verticesCount = 0
        self.verticesTableSize = 0
        self.faceTable = []
        self.faceCount = 0
        self.faceTableSize = 0

    # TODO: Add Object Methods

    #def AddObject(self, object):
    #    if (self.__checkObjectEntry(object) == True):
    #        self.objectTable.append(object)
    #        self.__calculateObjectTableSize()
    #    else:
    #        raise Exception("Object entry invalid")

    def AddVertice(self, vertice):
        if (self.verticesEntrySize == 0 and (len(vertice) * 4 == 24 or len(vertice) * 4 == 36)):
            self.verticesEntrySize = len(vertice) * 4
        elif (self.verticesEntrySize != len(vertice) * 4):
            raise Exception("Vertice size invalid")

        self.verticesTable.append(vertice)
        self.__calculateVerticeTableSize()

    def AddFace(self, face):
        self.faceTable.append(face)
        self.__calculateFaceTableSize()

    def __checkObjectEntry(self, object):
        if (object[0] > 4 or object[0] < 0):
            return False

        structure = self.objectEntryStructures[object[0]]
        i = 0
        for value in object[1:]:
            if (type(value) is not structure[i][1]):
                return False
            i += 1

        return True
    
    def __calculateObjectTableSize(self):
        size = int(0)
        for object in self.objectTable:
            for value in object[1:]:
                if (type(value) is str):
                    if(value == '[NO NAME]'):
                        size += 4
                    else:
                        size += 32
                else:
                    size += 4
        size += 20 # For the header information
        self.objectTableSize = size
        return size

    def GetObjectTableSize(self):
        return self.__calculateObjectTableSize()

    def __calculateVerticeTableSize(self):
        size = int(0)
        for vertice in self.verticesTable:
            size += int(len(vertice) * 4)
        self.verticesTableSize = size
        self.verticesCount = len(self.verticesTable)
        return size

    def GetVerticesTableSize(self):
        return self.__calculateVerticeTableSize()

    def GetVerticesCount(self):
        count = int(len(self.verticesTable))
        self.verticesCount = count
        return count

    def __calculateFaceTableSize(self):
        size = int(len(self.faceTable) * self.faceEntrySize)
        self.faceTableSize = size
        self.faceCount = len(self.faceTable)
        return size

    def GetFaceTableSize(self):
        return self.__calculateFaceTableSize()

    def GetFaceCount(self):
        count = int(len(self.faceTable))
        self.faceCount = count
        return count

    def GetFloatColour(self, value):
        alpha = float(((value >> 24) & 0xFF) * 0.003921568627451)
        red = float(((value >> 16) & 0xFF) * 0.003921568627451)
        green = float(((value >> 8) & 0xFF) * 0.003921568627451)
        blue = float(((value) & 0xFF) * 0.003921568627451)
        return [alpha, red, green, blue]

    def toInt(self, bytes):
        return int.from_bytes(bytes, byteorder = "little")

    def toFloat(self, bytes):
        return struct.unpack("f", bytes)[0]

    def toStr(self, bytes):
        retstr = str()
        for byte in bytes:
            if (byte == 0):
                break
            retstr += f"{chr(byte)}"
        return retstr

    def toBytes(self, value, count):
        if(type(value) is float):
            return bytearray(struct.pack('f', value))
        elif(type(value) is str):
            return bytearray(value, 'utf-8')
        else:
            return value.to_bytes(count, byteorder = 'little')