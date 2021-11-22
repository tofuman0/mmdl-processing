import sys
import struct

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
    filetype = file.read(4)
    if (filetype != b"LDMM"):
        raise Exception('Not An MMDL File.')
    logoutput(f"File: {modelfile}")
    mattablesize = toInt(file.read(4))
    logoutput(f"Material table size: {mattablesize}")
    verttablesize = toInt(file.read(4))
    logoutput(f"Vertices table size: {verttablesize}")
    facetablesize = toInt(file.read(4))
    logoutput(f"Face table size: {facetablesize}")
    unknown1 = toInt(file.read(4))
    logoutput(f"Unknown value 1: {hex(unknown1)}")
    vertsize = toInt(file.read(4))
    logoutput(f"Vertice size: {vertsize}")
    vertcount = toInt(file.read(4))
    logoutput(f"Vertice count: {vertcount}")
    facesize = toInt(file.read(4))
    logoutput(f"Face size: {facesize}")
    facecount = toInt(file.read(4))
    logoutput(f"Face count: {facecount}")
    # Material Table
    # TODO: Process material table header
    file.seek(80)
    matcount = 0
    logbuf = ''
    while (file.tell() < (16 + mattablesize)):
        matcount += 1
        curroffset = file.tell()
        matid = toInt(file.read(4))
        matflag = toInt(file.read(4))
        matopacity = toFloat(file.read(4))
        logbuf += f"Current Offset: {curroffset}\n"
        logbuf += f"\nCurrent Material: {matcount}\n"
        logbuf += f"Mat ID: {matid}\n"
        logbuf += f"Mat Flag: {hex(matflag)}\n"
        if(matflag == 0):
            # Is Mat type
            matname = toStr(file.read(32))
            unknownmat1 = toInt(file.read(4))
            matname2 = toStr(file.read(32))
            logbuf += f"Mat Name: {matname}\n"
            logbuf += f"Mat Name 2: {matname2}\n"
            logbuf += f"{toInt(file.read(4))}, {toInt(file.read(4))}\n"
            curroffset = file.tell()
            if (toInt(file.read(2)) == 12336):
                # If has '00' then is string and structure different
                file.seek(curroffset)
                matname3 = toStr(file.read(32))
                logbuf += f"Mat Name 3: {matname3}\n"
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toInt(file.read(4))}, {toInt(file.read(4))}, {toInt(file.read(4))}, {toInt(file.read(4))}, "
                logbuf += f"{toInt(file.read(4))}, {toInt(file.read(4))}, {toInt(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
            else:
                file.seek(curroffset)
                logbuf += f"{toInt(file.read(4))}, {toInt(file.read(4))}, {toInt(file.read(4))}, {toInt(file.read(4))}\n"
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
        else:
            # Is regular type
            matname = toStr(file.read(24))
            if(matname == ''):
                file.seek(curroffset + 18)
                unknownvalue = toInt(file.read(2))
                file.seek(curroffset + 16)
                logbuf += "Mat Name: [NO NAME]\n"
                if (unknownvalue != 0):
                    logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
                else:
                    # Is entry before mat type
                    logbuf += f"{toInt(file.read(4))}, {toInt(file.read(4))}, {toInt(file.read(4))}, "
                    logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                    logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                    logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                    logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
            else:
                logbuf += f"Mat Name: {matname}\n"
                logbuf += f"{toInt(file.read(4))}\n"
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}, "
                logbuf += f"{toFloat(file.read(4))}\n"
                logbuf += f"{toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
    logbuf += f"-------------------------\nTotal Materials: {matcount}\n-------------------------\n"
    logoutput(logbuf)
    # Vertice Table
    file.seek(16 + mattablesize)
    logbuf = ''
    for i in range(vertcount):
        if (vertsize == 36):
            logbuf += f"Vertice {i + 1}: {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {hex(toInt(file.read(4)))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
        elif (vertsize == 24):
            logbuf += f"Vertice {i + 1}: {toFloat(file.read(4))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}, {hex(toInt(file.read(4)))}, {toFloat(file.read(4))}, {toFloat(file.read(4))}\n"
    logoutput(logbuf)
    # Face Table 
    file.seek(16 + mattablesize + verttablesize)
    logbuf = ''
    for i in range(int(facecount / 3)):
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