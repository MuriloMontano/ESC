import os
from os import listdir

commandDict = {
    "add" : "C_ARITHMETIC",
    "sub" : "C_ARITHMETIC",
    "neg" : "C_ARITHMETIC",
    "eq" : "C_ARITHMETIC",
    "gt" : "C_ARITHMETIC",
    "lt" : "C_ARITHMETIC",
    "and" : "C_ARITHMETIC",
    "or" : "C_ARITHMETIC",
    "not" : "C_ARITHMETIC",
    "push" : "C_PUSH",
    "pop" : "C_POP",
    "label" : "C_LABEL",
    "goto" : "C_GOTO",
    "if-goto" : "C_IF",
    "function" : "C_FUNCTION",
    "call" : "C_CALL",
    "return" : "C_RETURN"
}

segmentPointers = {
    "constant" : "SP",
    "local" : "LCL",
    "argument" : "ARG",
    "this" : "THIS",
    "that" : "THAT",
    "temp" : "5",
    "pointer" : "SP"
}

jumpDict = {
    "TRUE" : 0,
    "CONTINUE" : 0
}

functionDict = {
    "RETURN" : '',
    "CALL" : ''
}


def main():

    path = input("Informe o local e o nome do arquivo ou da pasta: ")

    if os.path.exists(path):

        path = path.replace(".VM", ".vm")

        if os.path.isfile(path) and ".vm" in path:

            output_path = path.replace(".vm", ".asm")
        
            output_name = output_path.split("\\")
            output_name = output_name[len(output_name) - 1]
            segmentPointers["static"] = output_name.replace(".asm", '') + "."

            try:

                file = open(output_path, 'w')
                
                if output_name.replace(".asm", '') == "Sys":
                    
                    if codeWriter(output_path, ["C_INIT"]) == -1:

                        file.close()
                        return -1
                
                file.close()

            except IOError:
        
                print("Não foi possível criar o arquivo de saída!")
                return -1
        
            if codeReader(path, output_path) == -1:

                return -1

        else:

            if path[len(path) - 1] == "\\":

                    path = path[0:len(path) - 1]

            output_name = path.split("\\")
            output_name = output_name[len(output_name) - 1]
            
            output_path = path + "\\" + output_name + ".asm"

            segmentPointers["static"] = output_name + "."

            lista_arqs = [arq for arq in listdir(path)]

            try:

                file = open(output_path, 'w')

                if "Sys.vm" in lista_arqs:
                    
                    if codeWriter(output_path, ["C_INIT"]) == -1:

                        file.close()
                        return -1
                
                file.close()

            except IOError:
        
                print("Não foi possível criar o arquivo de saída!")
                return -1

            for arquivo in lista_arqs:

                if ".vm" in arquivo:

                    if codeReader(path + "\\" + arquivo, output_path) == -1:

                        return -1

        print("Tradução realizada com sucesso!")
                    
    else:

        print ("O arquivo informado não existe!")

def codeReader(path, output_path):

    try:
            
        file = open(path, 'r')
        lines = file.readlines()
        file.close()

        file = open(output_path, 'a')
        file.writelines("//" + output_path + "\n")      
        file.close()

        functionDict["CALL"] = path.split("\\")[len(path.split("\\")) - 1].replace(".vm", '') + "$ret."
        functionDict[functionDict["CALL"]] = 1
        
        for line in lines:
            
            result = parse(line)

            if result == -1:
                
                print("O arquivo não pode ser traduzido! " +
                      "Por favor, verifique se não existem erros de sintaxe.")
                return -1


            elif result != 0:

                writed = codeWriter(output_path, result)

                if  writed == -1:

                    return -1

    except IOError:
        
        print("Não foi possível acessar o arquivo!")

def parse(line):

    print(line)

    if line.find("//") != -1:

        line = line.split("//")[0]

    elements = line.replace("\n", "").split(' ')
        
    print(elements)

    if elements[0] != '': #and elements[0] != "\n":

        if elements[0] in commandDict:
            
            commandType = commandDict[elements[0]]
            result = [commandType]

        else:

            return -1
                
        if commandType != "C_RETURN":

            if commandType == "C_ARITHMETIC":

                arg1 = elements[0]

            else:

                arg1 = elements[1]

            result.append(arg1)
            arg2CallList = ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]

            if commandType in arg2CallList:

                arg2 = elements[2]
                result.append(arg2)

        return result
    
    else:

        return 0

def codeWriter(output_file, arguments):

    if arguments[0] == "C_INIT":

        output = writeInit()

    elif arguments[0] == "C_RETURN":

        output = writeReturn()
    
    elif arguments[0] == "C_ARITHMETIC":

        output = writeArithmetic(arguments[1])

    elif arguments[0] ==  "C_LABEL":

        output = writeLabel(arguments[1])

    elif arguments[0] ==  "C_GOTO":

        output = writeGoto(arguments[1])

    elif arguments[0] ==  "C_IF":

        output = writeIf(arguments[1])

    elif arguments[0] ==  "C_FUNCTION":

        output = writeFunction(arguments[1], arguments[2])

    elif arguments[0] ==  "C_CALL":

        output = writeCall(arguments[1], arguments[2])

    elif arguments[0] ==  "C_PUSH" or arguments[0] ==  "C_POP":

        output = writePushPop(arguments[0], arguments[1], arguments[2])

    if output == -1:

        return -1

    try:
        
        file = open(output_file, 'a')

        for line in output:

            file.writelines(line)

        file.close()

        return 0
    
    except IOError:
        
        print ("Ocorreu um erro! Não foi possível traduzir o arquivo")
        return -1

def writeArithmetic(command):

    output = ["//" + command + "\n"]

    if command == "neg" or command == "not":

        output.append("@SP\n")
        output.append("A=M-1\n")

        if command == "neg":
            
            output.append("M=-M\n")

        else:

            output.append("M=!M\n")

        return output

    else:

        output.append("@SP\n")
        output.append("M=M-1\n")
        #output.append("@SP\n")
        output.append("A=M-1\n")
        output.append("D=M\n")
        output.append("@SP\n")
        output.append("A=M\n")

        if command == "add":

            output.append("D=D+M\n")

        elif command == "sub":

            output.append("D=D-M\n")

        elif command == "and":

            output.append("D=D&M\n")

        elif command == "or":

            output.append("D=D|M\n")

        else:
            
            if command == "eq":

                output.append("D=D-M\n")
                output.append("@TRUE_" + str(jumpDict["TRUE"]) + "\n")
                output.append("D; JEQ\n")
            
            elif command == "gt":

                output.append("D=D-M\n")
                output.append("@TRUE_" + str(jumpDict["TRUE"]) + "\n")
                output.append("D; JGT\n")

            elif command == "lt":

                output.append("D=D-M\n")
                output.append("@TRUE_" + str(jumpDict["TRUE"]) + "\n")
                output.append("D; JLT\n")

            else:

                return -1

            output.append("D=0\n")
            output.append("@CONTINUE_" + str(jumpDict["CONTINUE"]) + "\n") 
            output.append("0; JMP\n")
            output.append("(TRUE_" + str(jumpDict["TRUE"]) + ")\n")
            output.append("D=-1\n")
            output.append("(CONTINUE_" + str(jumpDict["CONTINUE"]) + ")\n")

            jumpDict["TRUE"] = jumpDict["TRUE"] + 1
            jumpDict["CONTINUE"] = jumpDict["CONTINUE"] + 1
        
        output.append("@SP\n")
        output.append("A=M-1\n")
        output.append("M=D\n")

        return output
    
def writePushPop(command, segment, index):

    output = ["//" + command.replace("C_", '') + " " + segment + " " + index + "\n"]

    if command == "C_PUSH":
                
        if segment == "constant" or segment == "pointer":

            if segment == "pointer":

                if index == '0':

                    output.append("@THIS\n")

                elif index == '1':

                    output.append("@THAT\n")

                else:

                    print("Erro de sintaxe! Por favor, verifique os valores passados em um parametro POINTER.")
                    return -1
                
                output.append("D=M\n")

            else:
                
                output.append("@" + str(index) + "\n")
                output.append("D=A\n")


        else:

            if segment == "temp":

                output.append("@" + str(int(segmentPointers[segment]) + int(index)) + "\n")
                output.append("D=M\n")

            elif segment == "static":
            
                output.append("@" + segmentPointers[segment] + str(index) + "\n")
                output.append("D=M\n")
                
            else:

                output.append("@" + str(index) + "\n")
                output.append("D=A\n")
                output.append("@" + segmentPointers[segment] + "\n")
                output.append("A=D+M\n")
                output.append("D=M\n")


            
        output.append("@SP\n")
        output.append("M=M+1\n")
        output.append("A=M-1\n")
        output.append("M=D\n")

        return output

    else:

        if segment == "static":

            output.append("@SP\n")
            output.append("AM=M-1\n")
            output.append("D=M\n")
            output.append("@" + segmentPointers[segment] + str(index) + "\n")
            output.append("M=D\n")

            return output

        elif segment == "pointer":

            if index == '0':

                i = "THIS"

            elif index == '1':

                i = "THAT"

            else:

                print("Erro de sintaxe! Por favor, verifique os valores passados em um parametro POINTER")
                return -1

            output.append("@SP\n")
            output.append("AM=M-1\n")
            output.append("D=M\n")
            output.append("@" + i + "\n")
            output.append("M=D\n")

            return output
        
        elif segment == "temp":

            output.append("@" + str(int(segmentPointers[segment]) + int(index)) + "\n")
            output.append("D=A\n")
            output.append("@tempVariable\n")
            output.append("M=D\n")
            output.append("@SP\n")
            output.append("AM=M-1\n")
            output.append("D=M\n")      
            output.append("@tempVariable\n")
            output.append("A=M\n")
            output.append("M=D\n")
            output.append("@tempVariable\n")
            output.append("M=0\n")

            return output

        else:
            
            output.append("@" + str(index) + "\n")
            output.append("D=A\n")
            output.append("@" + segmentPointers[segment] + "\n")
            output.append("D=D+M\n")
            output.append("@tempVariable\n")
            output.append("M=D\n")
            output.append("@SP\n")
            output.append("AM=M-1\n")
            output.append("D=M\n")      
            output.append("@tempVariable\n")
            output.append("A=M\n")
            output.append("M=D\n")
            output.append("@tempVariable\n")
            output.append("M=0\n")

            return output

def writeInit():

    output = ["//Bootstrap code\n"]
    output.append("@256\n")
    output.append("D=A\n")
    output.append("@SP\n")
    output.append("M=D\n")
    output.append("@Sys.init\n")
    output.append("0; JMP\n")

    return output

def writeLabel(label):

    output = ["//LABEL " + label + "\n"]
    output.append("(" + label + ")\n")

    return output

def writeGoto(label):

    output = ["//GOTO " + label + "\n"]
    output.append("@" + label + "\n")
    output.append("0; JMP\n")

    return output

def writeIf(label):

    output = ["//IF-GOTO " + label + "\n"]
    output.append("@SP\n")
    output.append("AM=M-1\n")
    output.append("D=M\n")
    output.append("@" + label + "\n")
    output.append("D; JNE\n")

    return output

def writeFunction(functionName, numVars):

    functionDict["RETURN"] = functionName + ".END"

    output = ["//FUNCTION " + functionName + " " + numVars + "\n"]
    #output.append("@" + functionDict["RETURN"] + "\n")
    #output.append("0; JMP\n")
    output.append("(" + functionName + ")\n")

    count = int(numVars)

    while count > 0:

        output.append("@SP\n")
        output.append("M=M+1\n")
        output.append("A=M-1\n")
        output.append("M=0\n")

        count -= 1

    return output

def writeCall(functionName, numArgs):

    output = ["//CALL " + functionName + " " + numArgs + "\n"]
    output.append("@" + functionDict["CALL"]
                  + str(functionDict[functionDict["CALL"]]) + "\n")
    output.append("D=A\n")
    output.append("@SP\n")
    output.append("M=M+1\n")
    output.append("A=M-1\n")
    output.append("M=D\n")

    output.append("@LCL\n")
    output.append("D=M\n")
    output.append("@SP\n")
    output.append("M=M+1\n")
    output.append("A=M-1\n")
    output.append("M=D\n")
    
    output.append("@ARG\n")
    output.append("D=M\n")
    output.append("@SP\n")
    output.append("M=M+1\n")
    output.append("A=M-1\n")
    output.append("M=D\n")

    output.append("@THIS\n")
    output.append("D=M\n")
    output.append("@SP\n")
    output.append("M=M+1\n")
    output.append("A=M-1\n")
    output.append("M=D\n")

    output.append("@THAT\n")
    output.append("D=M\n")
    output.append("@SP\n")
    output.append("M=M+1\n")
    output.append("A=M-1\n")
    output.append("M=D\n")

    output.append("@5\n")
    output.append("D=A\n")
    output.append("@" + numArgs + "\n")
    output.append("D=D-A\n")
    output.append("@SP\n")
    output.append("D=M-D\n")
    output.append("@ARG\n")
    output.append("M=D\n")

    output.append("@SP\n")
    output.append("D=M\n")
    output.append("@LCL\n")
    output.append("M=D\n")

    output.append("@" + functionName + "\n")
    output.append("0; JMP\n")

    output.append("(" + functionDict["CALL"]
                  + str(functionDict[functionDict["CALL"]]) + ")\n")

    functionDict[functionDict["CALL"]] += 1

    return output

def writeReturn():

    output = ["//RETURN\n"]
    output.append("@LCL\n")
    output.append("D=M\n")
    output.append("@endFrame\n")
    output.append("M=D\n")
    
    output.append("@5\n")
    output.append("A=D-A\n")
    output.append("D=M\n")
    output.append("@retAddr\n")
    output.append("M=D\n")

    output.append("@SP\n")
    output.append("A=M\n")
    output.append("D=M\n")
    output.append("@ARG\n")
    output.append("A=M\n")
    output.append("M=D\n")

    output.append("@ARG\n")
    output.append("D=M+1\n")
    output.append("@SP\n")
    output.append("M=D\n")

    output.append("@endFrame\n")
    output.append("A=M-1\n")
    output.append("D=M\n")
    output.append("@THAT\n")
    output.append("M=D\n")

    output.append("@2\n")
    output.append("D=A\n")
    output.append("@endFrame\n")
    output.append("A=M-D\n")
    output.append("D=M\n")
    output.append("@THIS\n")
    output.append("M=D\n")

    output.append("@3\n")
    output.append("D=A\n")
    output.append("@endFrame\n")
    output.append("A=M-D\n")
    output.append("D=M\n")
    output.append("@ARG\n")
    output.append("M=D\n")

    output.append("@4\n")
    output.append("D=A\n")
    output.append("@endFrame\n")
    output.append("A=M-D\n")
    output.append("D=M\n")
    output.append("@LCL\n")
    output.append("M=D\n")
    
    output.append("@retAddr\n")
    output.append("A=M\n")
    output.append("0; JMP\n")

    #output.append("(" + functionDict["RETURN"] + ")\n")

    return output

while True:
    main()
