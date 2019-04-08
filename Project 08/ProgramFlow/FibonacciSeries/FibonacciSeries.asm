//D:\Users\muril\OneDrive\Documentos\UFU\6_semestre\ESC\projetos\Project 8\ProgramFlow\FibonacciSeries\FibonacciSeries.asm
//PUSH argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
//POP pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//POP that 0
@0
D=A
@THAT
D=D+M
@tempVariable
M=D
@SP
M=M-1
A=M
D=M
@tempVariable
A=M
M=D
@tempVariable
M=0
//PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//POP that 1
@1
D=A
@THAT
D=D+M
@tempVariable
M=D
@SP
M=M-1
A=M
D=M
@tempVariable
A=M
M=D
@tempVariable
M=0
//PUSH argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
//PUSH constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M=M-1
A=M-1
D=M
@SP
A=M
D=D-M
@SP
A=M-1
M=D
//POP argument 0
@0
D=A
@ARG
D=D+M
@tempVariable
M=D
@SP
M=M-1
A=M
D=M
@tempVariable
A=M
M=D
@tempVariable
M=0
//LABEL MAIN_LOOP_START
(MAIN_LOOP_START)
//PUSH argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
//IF-GOTO COMPUTE_ELEMENT
@SP
AM=M-1
D=M
@COMPUTE_ELEMENT
D; JNE
//GOTO END_PROGRAM
@END_PROGRAM
0; JMP
//LABEL COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
//PUSH that 0
@0
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
//PUSH that 1
@1
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
//add
@SP
M=M-1
A=M-1
D=M
@SP
A=M
D=D+M
@SP
A=M-1
M=D
//POP that 2
@2
D=A
@THAT
D=D+M
@tempVariable
M=D
@SP
M=M-1
A=M
D=M
@tempVariable
A=M
M=D
@tempVariable
M=0
//PUSH pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//add
@SP
M=M-1
A=M-1
D=M
@SP
A=M
D=D+M
@SP
A=M-1
M=D
//POP pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D
//PUSH argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
//PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//sub
@SP
M=M-1
A=M-1
D=M
@SP
A=M
D=D-M
@SP
A=M-1
M=D
//POP argument 0
@0
D=A
@ARG
D=D+M
@tempVariable
M=D
@SP
M=M-1
A=M
D=M
@tempVariable
A=M
M=D
@tempVariable
M=0
//GOTO MAIN_LOOP_START
@MAIN_LOOP_START
0; JMP
//LABEL END_PROGRAM
(END_PROGRAM)
