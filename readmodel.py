import sys
import struct
import array

modelfile = ''
logfile = ''

def main(argv):
    global modelfile
    global logfile  
    try:
        for i in range(len(argv)):
            if (argv[i] == "-m"):
                i += 1
                modelfile = argv[i]
            elif (argv[i] == "-l"):
                i += 1
                logfile = argv[i]
        if (modelfile != ''):
            try:
                if (logfile != ''):
                    initializelog()
                readmmdl()
            except Exception as err:
                print(f"Error: {err}")
                sys.exit(110)
        else:
            raise
    except:
        print("Syntax Error!\r\n Usage: readmodel.py -m model.mmdl [-l logfile.txt]")
        sys.exit(1)

def readmmdl():
    file = open(modelfile, "rb")
    fileType = file.read(4)
    if (fileType != b"LDMM"):
        raise Exception('Not An MMDL File.')
    logoutput(f"File: {modelfile}")
    matTableSize = toInt(file.read(4))
    logoutput(f"Material table size: {matTableSize}")
    vertTableSize = toInt(file.read(4))
    logoutput(f"Vertices table size: {vertTableSize}")
    faceTableSize = toInt(file.read(4))
    logoutput(f"Face table size: {faceTableSize}")
    modelType = toInt(file.read(4))
    logoutput(f"Unknown value 1: {hex(modelType)}")
    vertSize = toInt(file.read(4))
    logoutput(f"Vertice size: {vertSize}")
    vertCount = toInt(file.read(4))
    logoutput(f"Vertice count: {vertCount}")
    faceSize = toInt(file.read(4))
    logoutput(f"Face size: {faceSize}")
    faceCount = toInt(file.read(4))
    logoutput(f"Face count: {faceCount}")
    # Material Table
    matCount = 0
    logbuf = ''

    while (file.tell() < (16 + matTableSize)):
        matCount += 1
        currOffset = file.tell()
        matOpacity = 0.0
        if(matCount > 1): # First Entry doesn't have Opacity
            matOpacity = toFloat(file.read(4))
        if ((matCount == 1) or not (toInt(file.read(4)) & 0xFF000000)): # No Name
            matName = "[NO NAME]"
            logbuf += f"\nCurrent Offset: {currOffset}\n"
            logbuf += f"Current Material: {matCount}\n"
            logbuf += f"Mat Name 1: {matName}\n"
            if (matCount == 1):
                currOffset += 4
                file.seek(currOffset)
            matUnknown1 = toFloat(file.read(4))
            if (toInt(bytearray(struct.pack('f', matUnknown1))) & 0xFFFF0000): # lame check for if float value
                matUnknown2 = toFloat(file.read(4))
                matUnknown3 = toFloat(file.read(4))
                matUnknown4 = toFloat(file.read(4))
                matUnknown5 = toFloat(file.read(4))
                matUnknown6 = toFloat(file.read(4))
                if(matCount == 1): # First Entry has more data
                    matUnknown7 = toInt(file.read(4))
                    matUnknown8 = toInt(file.read(4))
                    matUnknown9 = toInt(file.read(4))
                    matUnknown10 = toInt(file.read(4))

                matType = toInt(file.read(4))
                matId = toInt(file.read(4))
                logbuf += f"Mat Type: {matType}\n"
                logbuf += f"Mat ID: {hex(matId)}\n"
                if(matCount > 1): # First Entry doesn't have Opacity            
                    logbuf += f"Mat Opacity: {matOpacity}\n" 

                if(matCount == 1): # First Entry has more data   
                    logbuf += f"{matUnknown1}, {matUnknown2}, {matUnknown3}, {matUnknown4}, "
                    logbuf += f"{matUnknown5}, {matUnknown6}, {matUnknown7}, {matUnknown8}, "
                    logbuf += f"{matUnknown9}, {matUnknown10}\n"
                else:
                    logbuf += f"{matUnknown1}, {matUnknown2}, {matUnknown3}, {matUnknown4}, "
                    logbuf += f"{matUnknown5}, {matUnknown6}\n"
                
            else: # Is material assigned to object
                file.seek(currOffset + 4)
                matUnknown1 = toInt(file.read(4))
                matUnknown2 = toInt(file.read(4))
                matUnknown3 = toInt(file.read(4))
                matUnknown4 = toInt(file.read(4))
                matUnknown5 = toFloat(file.read(4))
                matUnknown6 = toFloat(file.read(4))
                matUnknown7 = toFloat(file.read(4))
                matUnknown8 = toFloat(file.read(4))
                matUnknown9 = toFloat(file.read(4))
                matUnknown10 = toFloat(file.read(4))
                matUnknown11 = toFloat(file.read(4))
                matUnknown12 = toFloat(file.read(4))
                matUnknown13 = toFloat(file.read(4))
                matUnknown14 = toFloat(file.read(4))
                matUnknown15 = toFloat(file.read(4))
                matUnknown16 = toFloat(file.read(4))
                matUnknown17 = toFloat(file.read(4))
                matUnknown18 = toFloat(file.read(4))
                matUnknown19 = toFloat(file.read(4))
                matUnknown20 = toFloat(file.read(4))
                matUnknown21 = toFloat(file.read(4))
                matName2 = toStr(file.read(32))
                matUnknown22 = toFloat(file.read(4))
                matName3 = toStr(file.read(32))
                matId = toInt(file.read(4))
                logbuf += f"Mat Name 2: {matName2}\n"
                logbuf += f"Mat Name 3: {matName3}\n"
                logbuf += f"Mat ID: {hex(matId)}\n"  
                logbuf += f"{matUnknown1}, {matUnknown2}, {matUnknown3}, {matUnknown4}, "
                logbuf += f"{matUnknown5}, {matUnknown6}, {matUnknown7}, {matUnknown8}, "
                logbuf += f"{matUnknown9}, {matUnknown10}, {matUnknown11}, {matUnknown12}, "
                logbuf += f"{matUnknown13}, {matUnknown14}, {matUnknown15}, {matUnknown16}, "
                logbuf += f"{matUnknown17}, {matUnknown18}, {matUnknown19}, {matUnknown20}, "
                logbuf += f"{matUnknown21}\n"      
        else: # Has Name
            file.seek(currOffset + 4)
            matName = toStr(file.read(32))
            logbuf += f"\nCurrent Offset: {currOffset}\n"
            logbuf += f"Current Material: {matCount}\n"
            logbuf += f"Mat Name 1: {matName}\n"
            matUnknown1 = toFloat(file.read(4))
            matUnknown2 = toFloat(file.read(4))
            matUnknown3 = toFloat(file.read(4))
            matUnknown4 = toFloat(file.read(4))
            matUnknown5 = toFloat(file.read(4))
            matUnknown6 = toFloat(file.read(4))
            matUnknown7 = toFloat(file.read(4))
            matUnknown8 = toFloat(file.read(4))
            matUnknown9 = toFloat(file.read(4))
            matUnknown10 = toFloat(file.read(4))
            matUnknown11 = toFloat(file.read(4))
            matUnknown12 = toFloat(file.read(4))
            matUnknown13 = toFloat(file.read(4))
            matUnknown14 = toFloat(file.read(4))
            matUnknown15 = toFloat(file.read(4))
            matUnknown16 = toFloat(file.read(4))
            matUnknown17 = toFloat(file.read(4))
            matUnknown18 = toFloat(file.read(4))
            matUnknown19 = toFloat(file.read(4))
            matUnknown20 = toFloat(file.read(4))
            matUnknown21 = toFloat(file.read(4))
            matUnknown22 = toFloat(file.read(4))
            matUnknown23 = toFloat(file.read(4))
            matType = toInt(file.read(4))
            matId = toInt(file.read(4))
            logbuf += f"Mat Type: {matType}\n"
            logbuf += f"Mat ID: {hex(matId)}\n"
            if(matCount > 1): # First Entry doesn't have Opacity            
                logbuf += f"Mat Opacity: {matOpacity}\n" 
            logbuf += f"{matUnknown4}, {matUnknown5}, {matUnknown6}, {matUnknown7}, "
            logbuf += f"{matUnknown8}, {matUnknown9}, {matUnknown10}, {matUnknown11}, "
            logbuf += f"{matUnknown12}, {matUnknown13}, {matUnknown14}, {matUnknown15}, "
            logbuf += f"{matUnknown16}, {matUnknown17}, {matUnknown18}, {matUnknown19}, "
            logbuf += f"{matUnknown20}, {matUnknown21}, {matUnknown22}, {matUnknown23}\n"
    logbuf += f"\n-------------------------\nTotal Materials: {matCount}\n-------------------------\n"
    logoutput(logbuf)
    
    # Vertice Table
    file.seek(16 + matTableSize)
    logbuf = ''
    for i in range(vertCount):
        if (vertSize == 36):
            logbuf += f"Vertice {i + 1}: {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {hex(toInt(file.read(4)))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
        elif (vertSize == 24):
            logbuf += f"Vertice {i + 1}: {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {hex(toInt(file.read(4)))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
    logoutput(logbuf)
    
    # Face Table 
    file.seek(16 + matTableSize + vertTableSize)
    logbuf = ''
    for i in range(int(faceCount / 3)):
        logbuf += f"Face {i + 1}: {toInt(file.read(2))}, {toInt(file.read(2))}, {toInt(file.read(2))}\n"
    logoutput(logbuf)
    file.close

def toInt(bytes):
    return int.from_bytes(bytes, byteorder = "little")

def toFloat(bytes):
    return struct.unpack("f", bytes)[0]

def toStr(bytes):
    retstr = ''
    for byte in bytes:
        if (byte == 0):
            return retstr
        retstr += f"{chr(byte)}"
    return retstr

def logoutput(logstr):
    global logfile
    print(logstr)
    if (logfile == ''):
        return
    try:
        file = open(logfile, "a")
        file.write(f"{logstr}\n")
        file.close
    except Exception as err:
        print(f"Error writing to log file: {err}")
        sys.exit(110)

def initializelog():
    global logfile
    if (logfile == ''):
        return
    try:
        file = open(logfile, "w")
        file.write("")
        file.close
    except Exception as err:
        print(f"Error writing to log file: {err}")
        sys.exit(110)

if (__name__ == "__main__"):
    main(sys.argv[1:])