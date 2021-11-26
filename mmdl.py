import sys
import struct

# Material Entry Types:
#   The material types that are specified by this class are used to identify the entries they are not part of the file structure itself
#   0: Initial material Entry (first and only entry of this type). Has no material name 1, 2 or 3 nor Float value at the beginning of the structure
#   1: Entry with no material name 1, 2, or 3 that doesn't have faces assigned to it
#   2: Entry with no name that does have faces assigned to it but does have material names 2 and 3.
#   3: Initial material Entry that has a material name 1. Unlikely to exist but just incase it is handled
#   4: Entry that has a material name 1 but not material name 2 or 3.

class MMDL:
    def __init__(self):
        self.fileName = str()
        self.materialTableSize = int()
        self.verticesTableSize = int()
        self.verticesEntrySize = int()
        self.verticesCount = int()
        self.faceTableSize = int()
        self.faceEntrySize = int()
        self.faceCount = int()
        self.unknownValue1 = int()
        self.materialTable = []
        self.verticesTable = []
        self.faceTable = []
        self.materialEntryStructures = [
                [
                    ["Material Name 1", str],
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Unknown Value 4", float],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float],
                    ["Unknown Value 7", int],
                    ["Unknown Value 8", int],
                    ["Unknown Value 9", int],
                    ["Unknown Value 10", int],
                    ["Material Type", int],
                    ["Material ID", int]
                ],
                [
                    ["Material Opacity", float],
                    ["Material Name 1", str],
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Unknown Value 4", float],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float],
                    ["Material Type", int],
                    ["Material ID", int]
                ],
                [
                    ["Material Name 1", str],
                    ["Vertice Offset", int],
                    ["Vertice Count", int],
                    ["Face Offset", int],
                    ["Face Count", int],
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Unknown Value 4", float],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float],
                    ["Unknown Value 7", float],
                    ["Unknown Value 8", float],
                    ["Unknown Value 9", float],
                    ["Unknown Value 10", float],
                    ["Unknown Value 11", float],
                    ["Unknown Value 12", float],
                    ["Unknown Value 13", float],
                    ["Unknown Value 14", float],
                    ["Unknown Value 15", float],
                    ["Unknown Value 16", float],
                    ["Unknown Value 17", float],
                    ["Material Name 2", str],
                    ["Unknown Value 18", float],
                    ["Material Name 3", str],
                    ["Material ID", int]
                ],
                [
                    ["Material Name 1", str],
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Unknown Value 4", float],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float],
                    ["Unknown Value 7", float],
                    ["Unknown Value 8", float],
                    ["Unknown Value 9", float],
                    ["Unknown Value 10", float],
                    ["Unknown Value 11", float],
                    ["Unknown Value 12", float],
                    ["Unknown Value 13", float],
                    ["Unknown Value 14", float],
                    ["Unknown Value 15", float],
                    ["Unknown Value 16", float],
                    ["Unknown Value 17", float],
                    ["Unknown Value 18", float],
                    ["Unknown Value 19", float],
                    ["Unknown Value 20", float],
                    ["Unknown Value 21", float],
                    ["Unknown Value 22", float],
                    ["Unknown Value 23", float],
                    ["Material Type", int],
                    ["Material ID", int]
                ],
                [
                    ["Material Opacity", float],
                    ["Material Name 1", str],
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Unknown Value 4", float],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float],
                    ["Unknown Value 7", float],
                    ["Unknown Value 8", float],
                    ["Unknown Value 9", float],
                    ["Unknown Value 10", float],
                    ["Unknown Value 11", float],
                    ["Unknown Value 12", float],
                    ["Unknown Value 13", float],
                    ["Unknown Value 14", float],
                    ["Unknown Value 15", float],
                    ["Unknown Value 16", float],
                    ["Unknown Value 17", float],
                    ["Unknown Value 18", float],
                    ["Unknown Value 19", float],
                    ["Unknown Value 20", float],
                    ["Unknown Value 21", float],
                    ["Unknown Value 22", float],
                    ["Unknown Value 23", float],
                    ["Material Type", int],
                    ["Material ID", int]
                ]
            ]
        self.verticesEntryStructures = [
                [
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Unknown Value 4", float],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float],
                    ["Colour", int],
                    ["Unknown Value 7", float],
                    ["Unknown Value 8", float]
                ],
                [
                    ["Unknown Value 1", float],
                    ["Unknown Value 2", float],
                    ["Unknown Value 3", float],
                    ["Colour", int],
                    ["Unknown Value 5", float],
                    ["Unknown Value 6", float]
                ]
            ]
    
    def ReadMMDL(self, filename):
        file = open(filename, "rb")
        self.fileType = file.read(4)
        if (self.fileType != b"LDMM"):
            raise Exception('Not An MMDL File.')
        self.fileName = filename
        
        # File header
        self.materialTableSize = self.toInt(file.read(4))
        self.verticesTableSize = self.toInt(file.read(4))
        self.faceTableSize = self.toInt(file.read(4))
        self.unknownValue1 = self.toInt(file.read(4))
        self.verticesEntrySize = self.toInt(file.read(4))
        self.verticesCount = self.toInt(file.read(4))
        self.faceEntrySize = self.toInt(file.read(4))
        self.faceCount = self.toInt(file.read(4))
        
        # Material Table
        matCount = 0
        while (file.tell() < (16 + self.materialTableSize)):
            matCount += 1
            currOffset = file.tell()
            matOpacity = 0.0
            if(matCount > 1): # First Entry doesn't have Opacity
                matOpacity = self.toFloat(file.read(4))
            if ((matCount == 1) or not (self.toInt(file.read(4)) & 0xFF000000)): # No Name
                matName1 = "[NO NAME]"
                if (matCount == 1):
                    currOffset += 4
                    file.seek(currOffset)
                matUnknown1 = self.toFloat(file.read(4))
                if (self.toInt(bytearray(struct.pack('f', matUnknown1))) & 0xFFFF0000): # lame check for if float value
                    matUnknown2 = self.toFloat(file.read(4))
                    matUnknown3 = self.toFloat(file.read(4))
                    matUnknown4 = self.toFloat(file.read(4))
                    matUnknown5 = self.toFloat(file.read(4))
                    matUnknown6 = self.toFloat(file.read(4))
                    if(matCount == 1): # First Entry has more data
                        matUnknown7 = self.toInt(file.read(4))
                        matUnknown8 = self.toInt(file.read(4))
                        matUnknown9 = self.toInt(file.read(4))
                        matUnknown10 = self.toInt(file.read(4))
                    matType = self.toInt(file.read(4))
                    matId = self.toInt(file.read(4))

                    if(matCount == 1): # First Entry has more data  
                        self.materialTable.append([0, matName1, matUnknown1, matUnknown2, matUnknown3, matUnknown4, matUnknown5, matUnknown6, matUnknown7, matUnknown8, matUnknown9, matUnknown10, matType, matId])
                    else:
                        self.materialTable.append([1, matOpacity, matName1, matUnknown1, matUnknown2, matUnknown3, matUnknown4, matUnknown5, matUnknown6, matType, matId])
                else: # Is material assigned to object
                    file.seek(currOffset + 4)
                    matUnknown1 = self.toInt(file.read(4))
                    matUnknown2 = self.toInt(file.read(4))
                    matUnknown3 = self.toInt(file.read(4))
                    matUnknown4 = self.toInt(file.read(4))
                    matUnknown5 = self.toFloat(file.read(4))
                    matUnknown6 = self.toFloat(file.read(4))
                    matUnknown7 = self.toFloat(file.read(4))
                    matUnknown8 = self.toFloat(file.read(4))
                    matUnknown9 = self.toFloat(file.read(4))
                    matUnknown10 = self.toFloat(file.read(4))
                    matUnknown11 = self.toFloat(file.read(4))
                    matUnknown12 = self.toFloat(file.read(4))
                    matUnknown13 = self.toFloat(file.read(4))
                    matUnknown14 = self.toFloat(file.read(4))
                    matUnknown15 = self.toFloat(file.read(4))
                    matUnknown16 = self.toFloat(file.read(4))
                    matUnknown17 = self.toFloat(file.read(4))
                    matUnknown18 = self.toFloat(file.read(4))
                    matUnknown19 = self.toFloat(file.read(4))
                    matUnknown20 = self.toFloat(file.read(4))
                    matUnknown21 = self.toFloat(file.read(4))
                    matName2 = self.toStr(file.read(32))
                    matUnknown22 = self.toFloat(file.read(4))
                    matName3 = self.toStr(file.read(32))
                    matId = self.toInt(file.read(4))
                    self.materialTable.append([2, matName1, matUnknown1, matUnknown2, matUnknown3, matUnknown4, matUnknown5, matUnknown6, matUnknown7, matUnknown8, matUnknown9, matUnknown10, matUnknown11, matUnknown12, matUnknown13, matUnknown14, matUnknown15, matUnknown16, matUnknown17, matUnknown18, matUnknown19, matUnknown20, matUnknown21, matName2, matUnknown22, matName3, matId])
            else: # Has Name
                file.seek(currOffset + 4)
                matName = self.toStr(file.read(32))
                matUnknown1 = self.toFloat(file.read(4))
                matUnknown2 = self.toFloat(file.read(4))
                matUnknown3 = self.toFloat(file.read(4))
                matUnknown4 = self.toFloat(file.read(4))
                matUnknown5 = self.toFloat(file.read(4))
                matUnknown6 = self.toFloat(file.read(4))
                matUnknown7 = self.toFloat(file.read(4))
                matUnknown8 = self.toFloat(file.read(4))
                matUnknown9 = self.toFloat(file.read(4))
                matUnknown10 = self.toFloat(file.read(4))
                matUnknown11 = self.toFloat(file.read(4))
                matUnknown12 = self.toFloat(file.read(4))
                matUnknown13 = self.toFloat(file.read(4))
                matUnknown14 = self.toFloat(file.read(4))
                matUnknown15 = self.toFloat(file.read(4))
                matUnknown16 = self.toFloat(file.read(4))
                matUnknown17 = self.toFloat(file.read(4))
                matUnknown18 = self.toFloat(file.read(4))
                matUnknown19 = self.toFloat(file.read(4))
                matUnknown20 = self.toFloat(file.read(4))
                matUnknown21 = self.toFloat(file.read(4))
                matUnknown22 = self.toFloat(file.read(4))
                matUnknown23 = self.toFloat(file.read(4))
                matType = self.toInt(file.read(4))
                matId = self.toInt(file.read(4))
                if(matCount == 1): # First Entry doesn't have Opacity 
                    self.materialTable.append([3, matName, matUnknown1, matUnknown2, matUnknown3, matUnknown4, matUnknown5, matUnknown6, matUnknown7, matUnknown8, matUnknown9, matUnknown10, matUnknown11, matUnknown12, matUnknown13, matUnknown14, matUnknown15, matUnknown16, matUnknown17, matUnknown18, matUnknown19, matUnknown20, matUnknown21, matUnknown22, matUnknown23, matType, matId])
                else:
                    self.materialTable.append([4, matOpacity, matName, matUnknown1, matUnknown2, matUnknown3, matUnknown4, matUnknown5, matUnknown6, matUnknown7, matUnknown8, matUnknown9, matUnknown10, matUnknown11, matUnknown12, matUnknown13, matUnknown14, matUnknown15, matUnknown16, matUnknown17, matUnknown18, matUnknown19, matUnknown20, matUnknown21, matUnknown22, matUnknown23, matType, matId])
        # Vertices Table
        file.seek(16 + self.materialTableSize)
        for i in range(self.verticesCount):
            if (self.verticesEntrySize == 36):
                self.verticesTable.append([self.toFloat(file.read(4)), self.toFloat(file.read(4)), self.toFloat(file.read(4)), self.toFloat(file.read(4)), self.toFloat(file.read(4)), self.toFloat(file.read(4)), self.toInt(file.read(4)), self.toFloat(file.read(4)), self.toFloat(file.read(4))])
            elif (self.verticesEntrySize == 24):
                self.verticesTable.append([self.toFloat(file.read(4)), self.toFloat(file.read(4)), self.toFloat(file.read(4)), self.toInt(file.read(4)), self.toFloat(file.read(4)), self.toFloat(file.read(4))])
            else:
                raise Exception(f'Unsupported Vertices Size: {self.vertSize}')

        # Face Table
        file.seek(16 + self.materialTableSize + self.verticesTableSize)
        for i in range(self.faceCount):
            self.faceTable.append(self.toInt(file.read(self.faceEntrySize)))
        file.close()

    def WriteMMDL(self, filename):
        # TODO: Write MMDL
        file = open(filename, "wb")

        # Write Header
        file.write(b"LDMM")
        file.write(self.toBytes(self.GetMaterialTableSize(), 4))
        file.write(self.toBytes(self.GetVerticesTableSize(), 4))
        file.write(self.toBytes(self.GetFaceTableSize(), 4))
        file.write(self.toBytes(self.unknownValue1, 4))
        file.write(self.toBytes(self.verticesEntrySize, 4))
        file.write(self.toBytes(self.GetVerticesCount(), 4))
        file.write(self.toBytes(self.faceEntrySize, 4))
        file.write(self.toBytes(self.GetFaceCount(), 4))

        # Write Material Table
        for material in self.materialTable:
            for value in material[1:]:
                if (type(value) is str):
                    if(value == '[NO NAME]'):
                        file.write(self.toBytes(int(0), 4))
                    else:
                        file.write(self.toBytes(value, len(value)))
                        strRemainder = 32 - len(value)
                        for i in range(strRemainder):
                            file.write(b'\0')
                else:
                    file.write(self.toBytes(value, 4))

        # Write Vertices Table
        for vertice in self.verticesTable:
            for value in vertice:
                file.write(self.toBytes(value, 4))

        # Write Faces Table
        for value in self.faceTable:
            file.write(self.toBytes(value, self.faceEntrySize))

        file.close()
    
    def GetMaterialTableSize(self):
        size = int(0)
        for material in self.materialTable:
            for value in material[1:]:
                if (type(value) is str):
                    if(value == '[NO NAME]'):
                        size += 4
                    else:
                        size += 32
                else:
                    size += 4
        size += 20 # For the header information
        self.materialTableSize = size
        return size

    def GetVerticesTableSize(self):
        size = int(0)
        for vertice in self.verticesTable:
            size += int(len(vertice) * 4)
        self.verticesTableSize = size
        return size

    def GetVerticesCount(self):
        count = int(len(self.verticesTable))
        self.verticesCount = count
        return count

    def GetFaceTableSize(self):
        size = int(len(self.faceTable) * self.faceEntrySize)
        self.faceTableSize = size
        return size

    def GetFaceCount(self):
        count = int(len(self.faceTable))
        self.faceCount = count
        return count

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