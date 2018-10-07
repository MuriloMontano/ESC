import sys
import os
import re
from pathlib import Path, PureWindowsPath

compDict = {
  "0": "0101010",
  "1": "0111111",
  "-1": "0111010",
  "D": "0001100",
  "A": "0110000",
  "M": "1110000",
  "!D": "0001101",
  "!A": "0110001",
  "!M": "1110001",
  "-D": "0001111",
  "-A": "0110011",
  "-M": "1110011",
  "D+1": "0011111",
  "A+1": "0110111",
  "M+1": "1110111",
  "D-1": "0001110",
  "A-1": "0110010",
  "M-1": "1110010",
  "D+A": "0000010",
  "D+M": "1000010",
  "D-A": "0010011",
  "D-M": "1010011",
  "A-D": "0000111",
  "M-D": "1000111",
  "D&A": "0000000",
  "D&M": "1000000",
  "D|A": "0010101",
  "D|M": "1010101"
}

jumpDict = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

symbolsDict = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4"
}

labelDict = {
}

def main():
    while True:
        file_name = input("Informe o caminho do arquivo: ")
        if(os.path.exists(file_name)):
            try:
              file = open(file_name, "r")
              lines = file.readlines()
              file.close()

              parse(reduce(lines), file_name)
            except IOError:
              print ("Não foi possível abrir o arquivo")
              return 0
            
        else:
            print ("O arquivo informado não existe!")

def reduce(lines):
    instructions = []

    for line in lines:

        line = line.replace(" ", "")
        line = line.replace("\n", "")
        
        if line.find("//") != -1:
            line = line.split("//")[0]
              
        if line.find("(") != -1 and line.find(")") != -1:
            label = line.replace("(", "")
            label = label.replace(")", "")

            if label not in labelDict:
                labelDict[label] = str(len(instructions))

        elif line != "":
            instructions.append(line)
            
    return instructions

def parse(instructions, file_name):

    input_file = os.path.split(file_name)[1]
    
    if os.path.split(file_name)[0] != "":
        output_file = os.path.split(file_name)[0] + "\\"
        
    else:
        output_file = ""

    for letter in input_file:
        if letter != ".":
            output_file += letter
            
        else:
            break

    output_file += ".hack"

    try:
        file = open(output_file, 'w+')
        
        output_instruction = ""

        symbIndex = 16
        
        for instruction in instructions:        
            if instruction.find("@") != -1:                
                number = instruction.replace("@", "")

                if number.isdigit():
                    output_instruction = "0" + "{0:015b}".format(int(number)) + "\n"
                    
                else:
                    if number in symbolsDict:
                        output_instruction = "0" + "{0:015b}".format(int(symbolsDict[number])) + "\n"

                    elif number in labelDict:
                        output_instruction = "0" + "{0:015b}".format(int(labelDict[number])) + "\n"

                    elif symbIndex < 16384:
                        symbolsDict[number] = str(symbIndex)                            
                        symbIndex += 1
                        output_instruction = "0" + "{0:015b}".format(int(symbolsDict[number])) + "\n"
                    
                file.writelines(output_instruction)
                
            else:                
                output_instruction = "111"
                
                c_intruction = re.split('=|;', instruction)
                
                dest = ""

                i = 0

                if instruction.find("=") != -1:
                    if c_intruction[i].find("A") != -1:
                        dest += "1"
                    else:
                        dest += "0"

                    if c_intruction[i].find("D") != -1:
                        dest += "1"
                    else:
                        dest += "0"

                    if c_intruction[i].find("M") != -1:
                        dest += "1"
                    else:
                        dest += "0"

                    i += 1
                else:
                    dest = "000"
                    
                comp = compDict[c_intruction[i]]

                i += 1

                if instruction.find(";") != -1:
                    jump = jumpDict[c_intruction[i]]
                else:
                    jump = "000"

                
                output_instruction += comp + dest + jump + "\n"

                file.writelines(output_instruction)

        file.close()
        
    except IOError:
        print ("Não foi possível salvar o resultado")
        return 0
                        
main()



