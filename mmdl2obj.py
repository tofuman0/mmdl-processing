import mmdl
import sys
import traceback

modelfile = ''
objfile = ''

def main(argv):
    global modelfile
    global objfile  
    unique = False
    try:
        for i in range(len(argv)):
            if (argv[i] == "-m"):
                i += 1
                modelfile = argv[i]
            elif (argv[i] == "-o"):
                i += 1
                objfile = argv[i]
            elif (argv[i] == "-u"):
                unique = True
        if (modelfile != '' and objfile != ''):
            try:
                initializeobj()
                mmdl2obj(modelfile, objfile, unique)
            except Exception as err:
                print(f"Error: {err}")
                sys.exit(110)
        else:
            raise
    except:
        print("Syntax Error!\r\n Usage: mmdl2obj.py -m model.mmdl -o model.obj [-u]")
        print("    -u    Make object names unique.")
        sys.exit(1)

def mmdl2obj(modelfilename, objfilename, unique):
    try:
        mmdlFile = mmdl.MMDL()
        mmdlFile.ReadMMDL(modelfilename)
        objbuf = ''
        objbuf += "# mmdl2obj.py - https://github.com/tofuman0/mmdl-processing\n"
        objbuf += f"# OBJ Model converted from {mmdlFile.fileName}\n\n"
        # TODO: Create Objects and Groups based on Object table
        objbuf += f"# Vertices {mmdlFile.verticesCount}\n"
        for vertice in mmdlFile.verticesTable:
            colour = mmdlFile.GetFloatColour(vertice.Colour)
            objbuf += f"v  {vertice.X} {vertice.Y} {vertice.Z}\n"# {colour[1]} {colour[2]} {colour[3]}\n"
            #objbuf += f"vt {vertice.U} {vertice.V}\n"
            #if (mmdlFile.verticesEntrySize == 36):
            #    objbuf += f"vn {vertice.NX} {vertice.NY} {vertice.NZ}\n"
        objbuf += f"\n# Faces {int(mmdlFile.faceCount / 3)}\n"
        for Object1 in mmdlFile.objectEntries.Entries:
            for Object2 in Object1.Entries:
                if(unique == True):
                    shortName = mmdlFile.fileName.replace(".mmdl", "")
                    objbuf += f"\no {shortName}-{Object2.Name}\n"
                else:
                    objbuf += f"\no {Object2.Name}\n"
                for Object3 in Object2.Entries:
                    #objbuf += f"s {Object3.ID}\n"
                    objbuf += f"s off\n"
                    objbuf += f"usemtl {Object3.MaterialName}\n"
                    objbuf += f"usemap {Object3.TextureName}\n"
                    for i in range(Object3.FaceCount):
                        face1 = mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 0] + 1
                        face2 = mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 1] + 1
                        face3 = mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 2] + 1
                        objbuf += f"f  {face1} {face2} {face3}\n"
                        #if (mmdlFile.verticesEntrySize == 24):
                        #    objbuf += f"f  {face1}//{face1} {face2}//{face2} {face3}//{face3}\n"
                        #else:
                        #    objbuf += f"f  {face1}/{face1}/{face1} {face2}/{face2}/{face2} {face3}/{face3}/{face3}\n"
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