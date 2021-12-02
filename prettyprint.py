def print(str, indent = 4):
    retStr = ''
    indentCount = 0
    lastWasNewLine = False
    for char in str:
        newLine = False
        
        if lastWasNewLine == True and char == ' ':
            continue
        elif lastWasNewLine == True and char == ',':
            lastWasNewLine = False
        elif lastWasNewLine == True:
            retStr += "\n"
            for i in range(indent * indentCount):
                retStr += " "
            lastWasNewLine = False
        
        if char == '(' or char == '[' or char == '{':
            indentCount += 1
            newLine = True
        elif char == ')' or char == ']' or char == '}':
            indentCount -= 1
            retStr += "\n"
            for i in range(indent * indentCount):
                retStr += " "
        elif char == ',':
            newLine = True
        
        if indentCount < 0:
            indentCount = 0
        
        retStr += char

        if newLine:
            lastWasNewLine = True
            
    return retStr