// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Inicia o loop
(LOOP)

// Armazena o endereço do início do mapa da tela no local ADDR da memória
@SCREEN
D=A

@ADDR
M=D

// Armazena o valor 8192 no contador i
@8192
D=A

@i
M=D

// Verifica se alguma tecla está sendo pressionada
@KBD
D=M

// Caso esteja, pula para o preenchimento com branco
@WHITE
D; JEQ

// Caso não, pula para o preenchimento com preto
@BLACK
0; JMP

(WHITE)

// Preenche com 0 o conteudo do local apontado pelo ADDR
@ADDR
A=M
D=M
M=0

// Se o local já estiver preenchido com 0, retorna ao início do programa
@LOOP
D; JEQ

// Incrementa a posição atual
@ADDR
M=M+1

// Decrementa o contador
@i
M=M-1
D=M

// Se o contador alcançou o 0, retorna ao início do programa
@LOOP
D; JEQ

// Se não alcançou, passa para o preenchimento da próxima posição apontada pelo ADDR
@WHITE
0; JMP

(BLACK)

// Preenche com 1 o conteudo do local apontado pelo ADDR
@ADDR
A=M
D=M
M=-1

// Se o local já estiver preenchido com 1, retorna ao início do programa
@LOOP
D; JLT

// Incrementa a posição atual
@ADDR
M=M+1

// Decrementa o contador
@i
M=M-1
D=M

// Se o contador alcançou o 0, retorna ao início do programa
@LOOP
D; JEQ

// Se não alcançou, passa para o preenchimento da próxima posição apontada pelo ADDR
@BLACK
0; JMP