import mmdl
import sys
import traceback

modelfile = ''
objfile = ''

def main(argv):
    global modelfile
    global objfile  
    try:
        for i in range(len(argv)):
            if (argv[i] == "-m"):
                i += 1
                modelfile = argv[i]
            elif (argv[i] == "-o"):
                i += 1
                objfile = argv[i]
        if (modelfile != '' and objfile != ''):
            try:
                initializeobj()
                mmdl2obj(modelfile, objfile)
            except Exception as err:
                print(f"Error: {err}")
                sys.exit(110)
        else:
            raise
    except:
        print("Syntax Error!\r\n Usage: mmdl2obj.py -m model.mmdl -o model.obj")
        sys.exit(1)

def mmdl2obj(modelfilename, objfilename):
    try:
        mmdlFile = mmdl.MMDL()
        mmdlFile.ReadMMDL(modelfilename)
        objbuf = ''
        objbuf += "# mmdl2obj.py - https://github.com/tofuman0/mmdl-processing\n"
        objbuf += f"# OBJ Model converted from {mmdlFile.fileName}\n\n"
        # TODO: Create Objects and Groups based on Object table
        objbuf += f"# Vertices {mmdlFile.verticesCount}\n"
        for vertice in mmdlFile.verticesTable:
            objbuf += f"v  {vertice[0]} {vertice[1]} {vertice[2]}\n"
        objbuf += f"\n# Faces {int(mmdlFile.faceCount / 3)}\n"
        for Object1 in mmdlFile.objectEntries.Entries:
            for Object2 in Object1.Entries:
                objbuf += f"\ng {Object2.Name}\n"
                for Object3 in Object2.Entries:
                    objbuf += f"s {Object3.ID}\n"
                    objbuf += f"o {Object3.MaterialName}\n"
                    objbuf += f"usemtl {Object3.MaterialName}\n"
                    objbuf += f"usemap {Object3.TextureName}\n"
                    for i in range(Object3.FaceCount):
                        objbuf += f"f  {mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 0] + 1} {mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 1] + 1} {mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 2] + 1}\n"
        objoutput(objbuf)
        print(f"{objfilename} created successfully.")
    except Exception as err:
        print(f"Error: {err}")
        print(traceback.format_exc())

def objoutput(objdata):
    global objfile
    if (objfile == ''):
        raise Exception("OBJ file not specified")
    try:
        file = open(objfile, "a")
        file.write(f"{objdata}\n")
        file.close
    except Exception as err:
        print(f"Error writing to OBJ file: {err}")
        sys.exit(110)

def initializeobj():
    global objfile
    if (objfile == ''):
        raise Exception("OBJ file not specified")
    try:
        file = open(objfile, "w")
        file.write("")
        file.close
    except Exception as err:
        print(f"Error writing to OBJ file: {err}")
        sys.exit(110)

if (__name__ == "__main__"):
    main(sys.argv[1:])