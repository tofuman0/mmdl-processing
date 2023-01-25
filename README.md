# MMDL model file format
This is a collection of python scripts that can process the model format used in SBOL

## readmmdl.py
Returns the data from an MMDL file and can also log to file
```Commandline
Usage: python readmmdl.py -m modelfile.mmdl [-l modelfile.log]
```

## mmdl2obj.py
Converts MMDL to OBJ file
```Commandline
Usage: python mmdl2obj.py -m modelfile.mmdl -o modelfile.obj [-mtl materialfile.mtl] [-u]
  -mtl:  Generates a material file for the obj using the specified filename after the mtl switch
  -u:    Makes Object names unique by prefixing the filename
```
