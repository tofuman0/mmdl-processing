import mmdl
import sys
import traceback

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
                readmmdl(modelfile)
            except Exception as err:
                print(f"Error: {err}")
                sys.exit(110)
        else:
            raise
    except:
        print("Syntax Error!\r\n Usage: readmodel.py -m model.mmdl [-l logfile.txt]")
        sys.exit(1)

def readmmdl(modelfilename):
    try:
        mmdlFile = mmdl.MMDL()
        mmdlFile.ReadMMDL(modelfilename)
        logoutput(f"File: {mmdlFile.fileName}")
        logoutput(f"Material table size: {mmdlFile.materialTableSize}")
        logoutput(f"Vertices table size: {mmdlFile.verticesTableSize}")
        logoutput(f"Face table size: {mmdlFile.faceTableSize}")
        logoutput(f"Unknown Value 1: {mmdlFile.unknownValue1}")
        logoutput(f"Vertice size: {mmdlFile.verticesEntrySize}")
        logoutput(f"Vertice count: {mmdlFile.verticesCount}")
        logoutput(f"Face size: {mmdlFile.faceEntrySize}")
        logoutput(f"Face count: {mmdlFile.faceCount}")

        # Material
        logbuf = '\n'
        i = 0
        for materials in mmdlFile.materialTable:
            structure = mmdlFile.materialEntryStructures[materials[0]]
            i += 1
            j = 0
            logbuf += f"Current Material: {i}\n"
            for value in materials[1:]:
                if (type(value) is structure[j][1]):
                    logbuf += f"{structure[j][0]}: {value}\n"
                else:
                    logbuf += f"{structure[j][0]}: {value} - Structure mismatch!\n"
                j += 1
            logbuf += "\n"
        logoutput(logbuf)

        # Vertices
        logbuf = ''
        i = 0
        for vertices in mmdlFile.verticesTable:
            i += 1
            logbuf += f"Vertice {i}:"
            first = True
            for vertice in vertices:
                if first == True:
                    first = False
                    logbuf += f" {vertice}"
                else:
                    logbuf += f", {vertice}"
            logbuf += "\n"
        logoutput(logbuf)

        # Faces
        logbuf = ''
        i = 0
        for face in mmdlFile.faceTable:
            i += 1
            logbuf += f"Face {i}: {face}\n"
        logoutput(logbuf)

    except Exception as err:
        print(f"Error: {err}")
        print(traceback.format_exc())

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