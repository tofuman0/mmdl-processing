import mmdl
import sys
import traceback
import re

modelfile = ''
objfile = ''
mtlfile = ''

def main(argv):
    global modelfile
    global objfile
    global mtlfile

    unique = False
    try:
        for i in range(len(argv)):
            if (argv[i] == "-m"):
                i += 1
                modelfile = argv[i]
            elif (argv[i] == "-o"):
                i += 1
                objfile = argv[i]
            elif (argv[i] == "-mtl"):
                i += 1
                mtlfile = argv[i]
            elif (argv[i] == "-u"):
                unique = True
        if (modelfile != '' and objfile != ''):
            try:
                initializefiles()
                mmdl2obj(modelfile, objfile, mtlfile, unique)
            except Exception as err:
                print(f"Error: {err}")
                sys.exit(110)
        else:
            raise
    except:
        print("Syntax Error!\r\n Usage: mmdl2obj.py -m model.mmdl -o model.obj [-u]")
        print("    -u    Make object names unique.")
        sys.exit(1)

def mmdl2obj(modelfilename, objfilename, mtlfilename, unique):
    try:
        mmdlFile = mmdl.MMDL()
        mmdlFile.ReadMMDL(modelfilename)
        objbuf = ''
        objbuf2 = ''
        objbuf3 = ''
        objbuf += "# mmdl2obj.py - https://github.com/tofuman0/mmdl-processing\n"
        objbuf += f"# OBJ Model converted from {mmdlFile.fileName}\n"
        if (mtlfile != ''):
            fileNameOnly = re.split(r"\\|/", mtlfile)
            mtlfileOnly = fileNameOnly.pop()
            objbuf += f"mtllib {mtlfileOnly}\n\n"
        else:
            objbuf += "\n"
        objbuf += f"# Vertices {mmdlFile.verticesCount}\n"
        for vertice in mmdlFile.verticesTable:
            colour = mmdlFile.GetFloatColour(vertice.Colour)
            objbuf += f"v  {(vertice.X * -1.0)} {vertice.Y} {vertice.Z} {colour[1]} {colour[2]} {colour[3]}\n"
            objbuf2 += f"vt  {vertice.U} {(vertice.V * -1.0)}\n"
            if (mmdlFile.verticesEntrySize == 36):
                objbuf3 += f"vn  {vertice.NX} {vertice.NY} {vertice.NZ}\n"
        objoutput(objbuf) # Vertices
        objoutput(objbuf2) # Textures
        objoutput(objbuf3) # Normals
        mtlbuf = "# mmdl2obj.py - https://github.com/tofuman0/mmdl-processing\n"
        mtlbuf += f"# MTL Generated from - {mmdlFile.fileName}\n\n"
        objbuf = ''
        objbuf2 = ''
        objbuf3 = ''
        objbuf += f"\n# Faces {int(mmdlFile.faceCount / 3)}\n"
        for Object1 in mmdlFile.objectEntries.Entries:
            for Object2 in Object1.Entries:
                if(unique == True):
                    shortName = mmdlFile.fileName.replace(".mmdl", "")
                    objbuf += f"\no {shortName}-{Object2.Name}\n"
                else:
                    objbuf += f"\no {Object2.Name}\n"
                for Object3 in Object2.Entries:
                    objbuf += f"s off\n"
                    objbuf += f"g {Object3.MaterialName}\n"
                    objbuf += f"usemtl {Object3.MaterialName}\n"
                    objbuf += f"usemap {Object3.TextureName}\n"
                    mtlbuf += f"newmtl {Object3.MaterialName}\n"
                    mtlbuf += f"Ka {Object3.Ka_r} {Object3.Ka_g} {Object3.Ka_b}\n"
                    mtlbuf += f"Kd {Object3.Kd_r} {Object3.Kd_g} {Object3.Kd_b}\n"
                    mtlbuf += f"Ks {Object3.Ks_r} {Object3.Ks_g} {Object3.Ks_b}\n"
                    mtlbuf += f"Ns {Object3.Ns}\n"
                    mtlbuf += f"Ni {Object3.Ni}\n"
                    mtlbuf += f"d {(Object3.d)}\n"
                    mtlbuf += f"Tr {(Object3.d)}\n"
                    mtlbuf += f"illum 0\n"
                    if (Object3.TextureName != ''):
                        mtlbuf += f"map_Kd \\textures\\{Object3.TextureName}.png\n\n"
                    else:
                        mtlbuf += "\n"
                    for i in range(Object3.FaceCount):
                        face1 = mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 0] + 1
                        face2 = mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 1] + 1
                        face3 = mmdlFile.faceTable[int(i * 3) + int(Object3.FaceOffset) + 2] + 1
                        if (mmdlFile.verticesEntrySize == 24):
                            objbuf += f"f  {face1}//{face1} {face2}//{face2} {face3}//{face3}\n"
                        else:
                            objbuf += f"f  {face1}/{face1}/{face1} {face2}/{face2}/{face2} {face3}/{face3}/{face3}\n"
        objoutput(objbuf)
        mtloutput(mtlbuf)
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

def mtloutput(mtldata):
    global mtlfile
    try:
        if (mtlfile != ''):
            file = open(mtlfile, "a")
            file.write(f"{mtldata}\n")
            file.close
    except Exception as err:
        print(f"Error writing to MTL file: {err}")
        sys.exit(110)

def initializefiles():
    global objfile
    global mtlfile
    try:
        if (objfile != ''):
            file = open(objfile, "w")
            file.write("")
            file.close
        if (mtlfile != ''):
            file = open(mtlfile, "w")
            file.write("")
            file.close
    except Exception as err:
        print(f"Error initialising file: {err}")
        sys.exit(110)

if (__name__ == "__main__"):
    main(sys.argv[1:])