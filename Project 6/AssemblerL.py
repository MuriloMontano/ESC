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

def main():
    while True:
        file_name = input("Informe o caminho do arquivo: ")
        if(os.path.exists(file_name)):
            try:
              file = open(file_name, "r")
              lines = file.readlines()
              file.close()

              parse(lines, file_name)
            except IOError:
              print ("Não foi possível abrir o arquivo")
              return 0
            
        else:
            print ("O arquivo informado não existe!")

def parse(lines, file_name):

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
        
        for line in lines:
            instruction = line.replace(" ", "")        
    
            if instruction.find("//") == -1 and instruction != "\n":
                if instruction.find("@") != -1:
                    number = line.replace("@", "")

                    #if number.isdigit():
                    output_instruction = "0" + "{0:015b}".format(int(number)) + "\n"
                        
                    file.writelines(output_instruction)
                    
                else:
                    output_instruction = "111"
                    
                    c_intruction = re.split('=|;|\n', instruction)
                    
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
        print ("Não foi possível abrir o arquivo")
        return 0
                        
main()



